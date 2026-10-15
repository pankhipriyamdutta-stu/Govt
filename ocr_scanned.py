import asyncio
import sys
import fitz
import winocr
from PIL import Image
from pathlib import Path
import json

sys.stdout.reconfigure(encoding='utf-8')

scanned_files = [
    "ias_fixation_of_cadre_strength_second_amendment_regulations_2025.pdf",
    "ARTPS RULES_0.pdf",
    "ARTPS ACT.pdf",
    "Vacancy circular for employment news-1m1R62.pdf"
]

async def ocr_full_document(filename):
    p = Path("source_documents") / filename
    doc = fitz.open(p)
    pages = []
    print(f"Starting OCR for {filename} ({len(doc)} pages)...")
    
    for i in range(len(doc)):
        page = doc[i]
        pix = page.get_pixmap(dpi=200)
        tmp_img = f"tmp_{filename[:10]}_{i}.png"
        pix.save(tmp_img)
        img = Image.open(tmp_img)
        res = await winocr.recognize_pil(img, lang='en')
        pages.append({
            "page_num": i + 1,
            "text": res.text
        })
        Path(tmp_img).unlink(missing_ok=True)
        print(f"  Page {i+1}/{len(doc)} done ({len(res.text)} chars)")
        
    return pages

async def main():
    all_ocr = {}
    for sf in scanned_files:
        all_ocr[sf] = await ocr_full_document(sf)
        
    with open("scanned_docs_ocr.json", "w", encoding="utf-8") as f:
        json.dump(all_ocr, f, ensure_ascii=False, indent=2)
    print("All scanned docs OCR complete and saved!")

asyncio.run(main())
