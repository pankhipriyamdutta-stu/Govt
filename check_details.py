import fitz
import sys

sys.stdout.reconfigure(encoding='utf-8')

# Check Citizen Charter.pdf
doc = fitz.open("source_documents/Citizen Charter.pdf")
print("Citizen Charter pages:", len(doc))
for i in range(min(5, len(doc))):
    print(f"--- CC Page {i+1} ---")
    print(doc[i].get_text()[:400].strip())

# Check untitled_23.pdf
doc23 = fitz.open("source_documents/untitled_23.pdf")
print("\nuntitled_23 pages:", len(doc23))
for i in range(len(doc23)):
    print(f"--- untitled_23 Page {i+1} ---")
    print(doc23[i].get_text().strip())
