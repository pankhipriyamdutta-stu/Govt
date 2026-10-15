import json
import sys

sys.stdout.reconfigure(encoding='utf-8')

with open("document_deep_analysis.json", "r", encoding="utf-8") as f:
    data = json.load(f)

for fname, d in data.items():
    print(f"\n=======================================================")
    print(f"FILE: {fname}")
    print(f"Pages: {d['page_count']} | Size: {d['file_size']} bytes | Digital Text: {d['has_digital_text']} ({d['total_digital_chars']} chars)")
    print(f"PDF Metadata: {d['pdf_metadata']}")
    print(f"--- SAMPLES (Page 1): ---")
    if d.get("sample_pages") and len(d["sample_pages"]) > 0:
        p1 = d["sample_pages"][0]["text"]
        print(p1[:500].strip())
