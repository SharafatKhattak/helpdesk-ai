# Enterprise AI Customer Support Assistant Architecture Design Prompt You are a Senior AI Architect, Machine Learning Engineer, NLP Engineer, Software Architect, and Backend Engineer. Design a production-ready AI-powered Customer Support Assistant for a large online marketplace similar to Amaz

pasted

this is my current thinking of the project 
ask me qustions if you have any
we will follow phasewise development 
this is for real company


Architected file classification strategy with deduplication and exclusion criteria
Architected file classification strategy with deduplication and exclusion criteria
Before we talk automation — look at this list carefully. Not everything here should go into data/raw/ at all, and getting that wrong isn't just messy organization, it's a real risk: anything you put in the knowledge base is retrievable and can end up quoted to a customer. Several of these are clearly internal-only documents.

My classification, file by file:

File	Recommendation	Reasoning
00_Cross_Verification_Report	Exclude	Sounds like internal QA/audit output, not customer-facing content
01_Terms_and_Conditions	policy	General platform ToC, applies to both buyer and seller
02_Privacy_Policy (1), (2), plain	policy — pick ONE, delete the other two	Three copies of the same doc; indexing all three triples-up retrieval noise for zero benefit
03_Seller_Terms_and_Conditions	seller_policy	Seller-specific terms
04_Seller_Policies (1), plain	seller_policy — pick ONE, delete the duplicate	Same dedup issue
05_Commission_and_Fee_Schedule	seller_policy — but check against FBA_FEE_SCHEDULE_DRAFT below	Fees are seller-facing
06_Terms_of_Reference (1), plain	Needs your input	"Terms of Reference" usually means an internal project-scope document, not customer content — but I can't tell from the filename alone. What's actually in it?
ABOUT_SOFTSTORE	policy	General company info, reasonable shared content
DEPLOY_NAMECHEAP_CPANEL	Exclude	This is a server-deployment/infra doc. This should never be anywhere near a customer-facing retrieval corpus
FBA_FEE_SCHEDULE_DRAFT	Needs your input — conflict	You have two fee-schedule files (this one and 05_Commission_and_Fee_Schedule). Which is current/authoritative? Don't index both — conflicting fee numbers retrieved together is exactly the kind of error the whole citation-validation design was built to prevent, and two different fee docs will produce exactly that
FBA_SELLER_GUIDE	seller_policy	
FINAL_RUN_PROMPT	Exclude	This looks like an internal prompt-engineering artifact (possibly literally a prompt you wrote for building this bot) — must not enter the KB
PLATFORM_CHARGES	Needs your input	Buyer-facing (shipping fees) or seller-facing (platform cut)? Ambiguous from the name alone
PLATFORM_READINESS	Exclude	Sounds like an internal launch-readiness report
QA_Reports_2026-08-04	Exclude	Internal QA output
SoftStore-Executive-Deck (1)	Exclude	Executive/internal deck, not customer support content
What-You-Can-Sell-on-SoftStore	seller_policy	Product-eligibility guidance for sellers
WHO_IS_WORKING_ON_WHAT	Exclude	Internal team/staffing doc
So: of ~20 files, roughly half look genuinely customer-facing, half look internal — and I can't verify that from filenames alone, only flag the pattern. This is exactly why I wouldn't hand this whole classification job to Copilot unsupervised. A filename-based heuristic (which is all an IDE autocomplete-style tool can realistically do without you pasting full file contents in) will happily "classify" DEPLOY_NAMECHEAP_CPANEL or FINAL_RUN_PROMPT into some folder because it pattern-matches on surrounding filenames, not because it understood the content is inappropriate for a customer bot. The include/exclude decision needs a human actually skimming each file — that part shouldn't be automated.

What Copilot genuinely is useful for, once you've made the classification calls above: the mechanical part — moving/renaming files into the right folders per a mapping you give it. That's a safe thing to automate because there's no judgment call left, just execution.

Renaming convention I'd suggest (matches what documents_config.py's _guess_title() expects — clean snake_case, no version suffixes, no numeric prefixes since folder location now encodes the category):

policy/terms_and_conditions.md (or .pdf)
policy/privacy_policy.pdf
policy/about_softstore.md
seller_policy/seller_terms_and_conditions.pdf
seller_policy/seller_policies.pdf
seller_policy/commission_and_fee_schedule.pdf
seller_policy/seller_guide.md
seller_policy/what_you_can_sell.md
Practical next step: answer the three flagged unknowns (06_Terms_of_Reference content, which fee schedule is authoritative, PLATFORM_CHARGES buyer-vs-seller), then I'll give you the exact move/rename list to hand Copilot as a mechanical batch operation — at that point it's just file operations, safe to automate.

do you want me to paste it in zip and you can look inside each and give me the raw folder in zip with classified folder

Yes — that's a better approach than me guessing from filenames, especially for the three ambiguous ones (06_Terms_of_Reference, the fee schedule conflict, PLATFORM_CHARGES) and to confirm the exclude list is actually correct rather than inferred.

Go ahead and upload the zip. Once it's here, I'll:

Extract and actually read each file's content (not just the filename)
Confirm or correct the include/exclude classification from my last message based on what's actually inside
Dedupe the triplicated files (02_Privacy_Policy x3, 04_Seller_Policies x2, 06_Terms_of_Reference x2) — I'll pick the most complete/current version and flag it, but I'll show you which one I picked and why rather than silently discarding
Resolve the fee-schedule conflict by actually comparing 05_Commission_and_Fee_Schedule against FBA_FEE_SCHEDULE_DRAFT — if they genuinely disagree on numbers, I'll flag that explicitly rather than picking one silently, since that's a real discrepancy you need to know about regardless of what goes into the bot
Convert/rename into the data/raw/{buyer_policy,seller_policy,policy}/ structure
Give you back a zip with the classified folder structure, plus a short manifest explaining what went where and why, and a separate list of what I excluded and why — so you can sanity-check my judgment calls rather than just trusting them blind
One thing worth deciding now: several files are PDF, and my current parser doesn't handle PDF headings well (the earlier e-Commerce-policy test showed this). Do you want me to also convert the PDFs to clean Markdown as part of this pass — extracting the text and adding proper # heading structure — or keep them as PDF for now and treat the heading-detection fix as a separate task later?


policies or not.zip
zip

just the data/raw folder no need of the while project


Categorized documents, identified internal materials, resolved conflicting data sources
Categorized documents, identified internal materials, resolved conflicting data sources

Extract uploaded zip and list contents

Ensure pdf/pptx reading libraries available

Read all markdown files
Identified internal documentation structure.


Extract first pages of each PDF for classification
Categorized documents, identified internal materials, resolved conflicting data sources.


Check if duplicate-named PDFs are actually byte-identical content
bash

cd "/home/claude/extracted/policies or not" && python3 << 'EOF'
import pdfplumber, hashlib

def full_text(path):
    with pdfplumber.open(path) as pdf:
        return "\n".join((p.extract_text() or "") for p in pdf.pages)

groups = {
    "Privacy Policy": ["02_Privacy_Policy (1).pdf", "02_Privacy_Policy (2).pdf", "02_Privacy_Policy.pdf"],
    "Seller Policies": ["04_Seller_Policies (1).pdf", "04_Seller_Policies.pdf"],
    "Terms of Reference": ["06_Terms_of_Reference (1).pdf", "06_Terms_of_Reference.pdf"],
}

for name, files in groups.items():
    print(f"\n{name}:")
    for f in files:
        t = full_text(f)
        h = hashlib.md5(t.encode()).hexdigest()
        print(f"  {f}: {len(t)} chars, md5={h}")
EOF
Output


Privacy Policy:
  02_Privacy_Policy (1).pdf: 5013 chars, md5=14601480dd9ea4792261c79a7b74b6f3
  02_Privacy_Policy (2).pdf: 5013 chars, md5=14601480dd9ea4792261c79a7b74b6f3
  02_Privacy_Policy.pdf: 5013 chars, md5=14601480dd9ea4792261c79a7b74b6f3

Seller Policies:
  04_Seller_Policies (1).pdf: 4360 chars, md5=b2238a24987ba21cc5fb08b6a8a8083a
  04_Seller_Policies.pdf: 4360 chars, md5=b2238a24987ba21cc5fb08b6a8a8083a

Terms of Reference:
  06_Terms_of_Reference (1).pdf: 4719 chars, md5=73bcefcd2af464cf1c699ba18a89f472
  06_Terms_of_Reference.pdf: 4719 chars, md5=73bcefcd2af464cf1c699ba18a89f472

Peek at executive deck pptx content
bash

cd "/home/claude/extracted/policies or not" && python3 << 'EOF'
from pptx import Presentation

prs = Presentation("SoftStore-Executive-Deck (1).pptx")
print(f"Slides: {len(prs.slides)}\n")
for i, slide in enumerate(prs.slides[:6], 1):
    texts = []
    for shape in slide.shapes:
        if shape.has_text_frame:
            t = shape.text_frame.text.strip()
            if t:
                texts.append(t)
    print(f"--- Slide {i} ---")
    print(" | ".join(texts)[:300])
    print()
EOF
Output

Slides: 19

Done

You are out of free messages until 4:30 PM