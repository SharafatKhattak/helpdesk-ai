"""
Qt-based GUI chatbot for SoftStore Support Assistant.

Usage:
    python gui_chatbot.py
"""
import sys
from datetime import datetime
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QTextEdit, QLineEdit, QPushButton, QLabel, QSplitter, QMessageBox
)
from PyQt6.QtCore import Qt, QThread, pyqtSignal
from PyQt6.QtGui import QFont, QTextCursor

from embedding.embedder import embed_query
from llm.gemini_client import generate_answer
from retrieval.vector_store import search
from config import GEMINI_API_KEY


class QueryThread(QThread):
    """Background thread for processing queries to keep UI responsive."""
    finished = pyqtSignal(dict)
    error = pyqtSignal(str)

    def __init__(self, query):
        super().__init__()
        self.query = query

    def run(self):
        try:
            # Embed query
            query_embedding = embed_query(self.query)

            # Search vector database - retrieve more chunks for better coverage
            results = search(query_embedding, top_k=10)

            # Prepare context chunks
            context_chunks = []
            docs = results.get("documents", [[]])[0]
            metas = results.get("metadatas", [[]])[0]

            for doc, meta in zip(docs, metas):
                context_chunks.append({
                    "text": doc,
                    "doc_title": meta.get("doc_title", ""),
                    "section_heading": meta.get("section_heading", ""),
                    "doc_type": meta.get("doc_type", ""),
                })

            # Generate answer with Gemini
            result = generate_answer(
                query=self.query,
                context_chunks=context_chunks,
            )

            self.finished.emit(result)

        except Exception as e:
            self.error.emit(str(e))


class ChatbotGUI(QMainWindow):
    def __init__(self):
        super().__init__()
        self.conversation_history = []
        self.init_ui()
        self.check_api_key()

    def check_api_key(self):
        """Check if API key is configured."""
        if not GEMINI_API_KEY or not GEMINI_API_KEY.startswith("AIza"):
            QMessageBox.warning(
                self,
                "API Key Issue",
                "Invalid or missing Gemini API key!\n\n"
                "Valid keys start with 'AIza' and are 39 characters long.\n\n"
                "To fix:\n"
                "1. Go to: https://aistudio.google.com/apikey\n"
                "2. Create a new API key\n"
                "3. Update the .env file with: GEMINI_API_KEY=AIzaXXXXXXXX\n"
                "4. Restart the application"
            )

    def init_ui(self):
        """Initialize the user interface."""
        self.setWindowTitle("SoftStore AI Support Assistant")
        self.setGeometry(100, 100, 1000, 700)

        # Central widget
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout(central_widget)

        # Header
        header = QLabel("🤖 SoftStore AI Support Assistant")
        header.setFont(QFont("Arial", 16, QFont.Weight.Bold))
        header.setAlignment(Qt.AlignmentFlag.AlignCenter)
        header.setStyleSheet("padding: 10px; background-color: #2c3e50; color: white;")
        main_layout.addWidget(header)

        # Splitter for chat and sources
        splitter = QSplitter(Qt.Orientation.Horizontal)

        # Chat area (left side)
        chat_widget = QWidget()
        chat_layout = QVBoxLayout(chat_widget)

        # Chat display
        self.chat_display = QTextEdit()
        self.chat_display.setReadOnly(True)
        self.chat_display.setFont(QFont("Segoe UI", 10))
        self.chat_display.setStyleSheet("""
            QTextEdit {
                background-color: #f5f5f5;
                border: 1px solid #ddd;
                border-radius: 5px;
                padding: 10px;
            }
        """)
        chat_layout.addWidget(self.chat_display)

        # Input area
        input_layout = QHBoxLayout()

        self.input_field = QLineEdit()
        self.input_field.setPlaceholderText("Ask a question... (e.g., 'What are the seller commission fees?')")
        self.input_field.setFont(QFont("Segoe UI", 10))
        self.input_field.setStyleSheet("""
            QLineEdit {
                padding: 10px;
                border: 2px solid #3498db;
                border-radius: 5px;
            }
        """)
        self.input_field.returnPressed.connect(self.send_message)
        input_layout.addWidget(self.input_field)

        self.send_button = QPushButton("Send")
        self.send_button.setFont(QFont("Segoe UI", 10, QFont.Weight.Bold))
        self.send_button.setStyleSheet("""
            QPushButton {
                background-color: #3498db;
                color: white;
                padding: 10px 20px;
                border-radius: 5px;
                border: none;
            }
            QPushButton:hover {
                background-color: #2980b9;
            }
            QPushButton:disabled {
                background-color: #bdc3c7;
            }
        """)
        self.send_button.clicked.connect(self.send_message)
        input_layout.addWidget(self.send_button)

        chat_layout.addLayout(input_layout)

        # Sources area (right side)
        sources_widget = QWidget()
        sources_layout = QVBoxLayout(sources_widget)

        sources_header = QLabel("📚 Sources")
        sources_header.setFont(QFont("Arial", 12, QFont.Weight.Bold))
        sources_header.setStyleSheet("padding: 5px; background-color: #34495e; color: white;")
        sources_layout.addWidget(sources_header)

        self.sources_display = QTextEdit()
        self.sources_display.setReadOnly(True)
        self.sources_display.setFont(QFont("Segoe UI", 9))
        self.sources_display.setStyleSheet("""
            QTextEdit {
                background-color: #ecf0f1;
                border: 1px solid #bdc3c7;
                border-radius: 5px;
                padding: 10px;
            }
        """)
        sources_layout.addWidget(self.sources_display)

        # Add widgets to splitter
        splitter.addWidget(chat_widget)
        splitter.addWidget(sources_widget)
        splitter.setStretchFactor(0, 3)  # Chat takes 75% width
        splitter.setStretchFactor(1, 1)  # Sources takes 25% width

        main_layout.addWidget(splitter)

        # Status bar
        self.status_label = QLabel("Ready to answer your questions!")
        self.status_label.setStyleSheet("padding: 5px; color: #7f8c8d;")
        main_layout.addWidget(self.status_label)

        # Welcome message
        self.add_system_message(
            "Welcome to SoftStore Support Assistant! 👋\n\n"
            "I can help you with:\n"
            "• Seller policies and commission fees\n"
            "• Platform terms and conditions\n"
            "• Product listing guidelines\n"
            "• FBA (Fulfilled by SoftStore) information\n\n"
            "Ask me anything!"
        )

    def add_system_message(self, message):
        """Add a system message to the chat."""
        self.chat_display.append(
            f'<div style="color: #7f8c8d; font-style: italic; margin: 10px 0;">'
            f'{message}</div>'
        )

    def add_user_message(self, message):
        """Add a user message to the chat."""
        timestamp = datetime.now().strftime("%H:%M")
        self.chat_display.append(
            f'<div style="margin: 10px 0;">'
            f'<span style="color: #2980b9; font-weight: bold;">You</span> '
            f'<span style="color: #95a5a6; font-size: 9pt;">({timestamp})</span><br>'
            f'<span style="background-color: #e3f2fd; padding: 8px; border-radius: 5px; '
            f'display: inline-block; margin-top: 5px;">{message}</span>'
            f'</div>'
        )
        self.scroll_to_bottom()

    def add_assistant_message(self, message):
        """Add an assistant message to the chat."""
        timestamp = datetime.now().strftime("%H:%M")
        self.chat_display.append(
            f'<div style="margin: 10px 0;">'
            f'<span style="color: #27ae60; font-weight: bold;">Assistant</span> '
            f'<span style="color: #95a5a6; font-size: 9pt;">({timestamp})</span><br>'
            f'<span style="background-color: #e8f5e9; padding: 8px; border-radius: 5px; '
            f'display: inline-block; margin-top: 5px;">{message}</span>'
            f'</div>'
        )
        self.scroll_to_bottom()

    def update_sources(self, sources):
        """Update the sources panel."""
        self.sources_display.clear()
        if not sources:
            self.sources_display.append("No sources available.")
            return

        html = '<div style="font-family: Segoe UI;">'
        for src in sources:
            section = f" > {src['section']}" if src.get('section') else ""
            html += (
                f'<div style="margin-bottom: 15px; padding: 10px; background-color: white; '
                f'border-left: 3px solid #3498db; border-radius: 3px;">'
                f'<span style="color: #3498db; font-weight: bold;">[{src["source_num"]}]</span> '
                f'<span style="color: #2c3e50; font-weight: bold;">{src["doc_title"]}</span>'
                f'<span style="color: #7f8c8d;">{section}</span><br>'
                f'<span style="color: #95a5a6; font-size: 8pt;">Type: {src["doc_type"]}</span>'
                f'</div>'
            )
        html += '</div>'
        self.sources_display.setHtml(html)

    def scroll_to_bottom(self):
        """Scroll chat to bottom."""
        cursor = self.chat_display.textCursor()
        cursor.movePosition(QTextCursor.MoveOperation.End)
        self.chat_display.setTextCursor(cursor)

    def send_message(self):
        """Handle sending a message."""
        query = self.input_field.text().strip()

        if not query:
            return

        # Add user message
        self.add_user_message(query)
        self.input_field.clear()

        # Disable input while processing
        self.input_field.setEnabled(False)
        self.send_button.setEnabled(False)
        self.status_label.setText("🔍 Searching knowledge base...")

        # Start background query thread
        self.query_thread = QueryThread(query)
        self.query_thread.finished.connect(self.on_query_finished)
        self.query_thread.error.connect(self.on_query_error)
        self.query_thread.start()

    def on_query_finished(self, result):
        """Handle successful query completion."""
        answer = result.get("answer", "No answer generated.")
        sources = result.get("sources", [])

        # Add assistant response
        self.add_assistant_message(answer)

        # Update sources panel
        self.update_sources(sources)

        # Track conversation
        self.conversation_history.append({"role": "user", "content": self.input_field.text()})
        self.conversation_history.append({"role": "assistant", "content": answer})

        # Keep only last 6 turns
        if len(self.conversation_history) > 6:
            self.conversation_history = self.conversation_history[-6:]

        # Re-enable input
        self.input_field.setEnabled(True)
        self.send_button.setEnabled(True)
        self.input_field.setFocus()
        self.status_label.setText(f"✓ Response generated using {len(sources)} sources")

    def on_query_error(self, error_message):
        """Handle query error."""
        self.add_system_message(f"❌ Error: {error_message}")

        # Show helpful message for API key errors
        if "API" in error_message or "404" in error_message or "NOT_FOUND" in error_message:
            self.add_system_message(
                "This looks like an API key issue.\n\n"
                "To fix:\n"
                "1. Go to: https://aistudio.google.com/apikey\n"
                "2. Create a new API key (starts with 'AIza')\n"
                "3. Update .env file: GEMINI_API_KEY=AIzaXXXXXXXX\n"
                "4. Restart the application"
            )

        # Re-enable input
        self.input_field.setEnabled(True)
        self.send_button.setEnabled(True)
        self.input_field.setFocus()
        self.status_label.setText("❌ Error occurred - see chat for details")


def main():
    app = QApplication(sys.argv)
    app.setStyle("Fusion")  # Modern look

    window = ChatbotGUI()
    window.show()

    sys.exit(app.exec())


if __name__ == "__main__":
    main()
