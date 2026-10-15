import zipfile
import xml.etree.ElementTree as ET
from pathlib import Path

downloads_dir = Path("C:/Users/pankh/Downloads")

for doc_name in ["Identity Card.pdf", "Doc5.docx", "Doc8.docx", "19,20,23,24.docx"]:
    p = downloads_dir / doc_name
    print(f"=== {doc_name} ===")
    if doc_name.endswith(".docx"):
        try:
            with zipfile.ZipFile(p) as z:
                xml_content = z.read("word/document.xml")
                tree = ET.fromstring(xml_content)
                text = "".join(node.text for node in tree.iter() if node.text)
                print(f"Text preview ({len(text)} chars): {text[:300]}...")
        except Exception as e:
            print(f"Error reading docx: {e}")
    elif doc_name.endswith(".pdf"):
        import fitz
        doc = fitz.open(p)
        print(f"PDF pages: {len(doc)}")
        for i, page in enumerate(doc):
            pix = page.get_pixmap()
            print(f"Page {i+1} dimensions: {pix.width}x{pix.height}, text length: {len(page.get_text())}")
