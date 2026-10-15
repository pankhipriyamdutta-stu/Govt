import fitz
from pathlib import Path

docs_dir = Path("source_documents")
for pdf_file in docs_dir.glob("*.pdf"):
    doc = fitz.open(pdf_file)
    print(f"\n==========================================")
    print(f"FILE: {pdf_file.name} | Pages: {len(doc)}")
    has_text = False
    for pno in range(min(5, len(doc))):
        txt = doc[pno].get_text()
        if txt.strip():
            has_text = True
            print(f"--- Page {pno+1} Text snippet (len {len(txt)}): ---")
            print(txt[:300].strip())
            print("...")
            break
    if not has_text:
        print(">>> NO EMBEDDED TEXT FOUND ON FIRST 5 PAGES (SCANNED/IMAGE-ONLY)")
        # Check image xrefs on page 0
        img_list = doc[0].get_images()
        print(f">>> Page 1 has {len(img_list)} images")
