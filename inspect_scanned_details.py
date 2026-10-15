import fitz
import asyncio
import winocr
from PIL import Image

doc_vc = fitz.open("source_documents/Vacancy circular for employment news-1m1R62.pdf")
print("Vacancy Circular pages:", len(doc_vc))
for p in [1, 7]: # 0-indexed page 2 and 8
    page = doc_vc[p]
    pix = page.get_pixmap(dpi=150)
    pix.save(f"vc_page_{p+1}.png")
    print(f"Page {p+1} saved to vc_page_{p+1}.png")

# Also check dms22_assam_public_procurement_rules_2020.pdf first 5 pages and table of contents
doc_proc = fitz.open("source_documents/dms22_assam_public_procurement_rules_2020.pdf")
print("\nProcurement Rules pages:", len(doc_proc))
for p in range(min(5, len(doc_proc))):
    page = doc_proc[p]
    pix = page.get_pixmap(dpi=150)
    pix.save(f"proc_page_{p+1}.png")
