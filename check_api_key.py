from google import genai

# Initialize client (best practice: load GEMINI_API_KEY from environment)
client = genai.Client(api_key="AQ.Ab8RN6JpZxauAZAGZm6gPu7NEACPLU12Wk05zZL7Skb6p-asbA")

response = client.models.generate_content(
    model="gemini-3.5-flash",
    contents="hi"
)

print(response.text)