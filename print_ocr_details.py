import json
import sys

sys.stdout.reconfigure(encoding='utf-8')

with open("scanned_docs_ocr.json", "r", encoding="utf-8") as f:
    data = json.load(f)

for doc_name, pages in data.items():
    print(f"\n=======================================================")
    print(f"DOC: {doc_name} (Total Pages: {len(pages)})")
    for p in pages:
        print(f"--- Page {p['page_num']} ({len(p['text'])} chars) ---")
        print(p['text'][:600].strip())
        print("...")
