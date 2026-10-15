import fitz
import sys

sys.stdout.reconfigure(encoding='utf-8')
doc = fitz.open("source_documents/untitled_23.pdf")
print("=== PAGE 1 ===")
print(doc[0].get_text())
print("=== PAGE 2 ===")
print(doc[1].get_text())
