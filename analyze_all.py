import asyncio
import sys
import fitz
import winocr
from PIL import Image
from pathlib import Path
import json

sys.stdout.reconfigure(encoding='utf-8')

target_files = [
    "Citizen Charter.pdf",
    "untitled_23.pdf",
    "ias_fixation_of_cadre_strength_second_amendment_regulations_2025.pdf",
    "ARTPS RULES_0.pdf",
    "ARTPS ACT.pdf",
    "dms22_assam_public_procurement_rules_2020.pdf",
    "MaintenanceofRecordstSZEC.pdf",
    "Vacancy circular for employment news-1m1R62.pdf",
    "Manual_for_Procurement_of_Consultancy_&_Other_Services_Updated June, 2022_1.pdf",
    "c9fe9c9b6840524844316f74bb1c556c.pdf"
]

async def analyze_document(filename):
    p = Path("source_documents") / filename
    doc = fitz.open(p)
    info = {
        "filename": filename,
        "page_count": len(doc),
        "file_size": p.stat().st_size,
        "pdf_metadata": doc.metadata,
        "has_digital_text": False,
        "pages_summary": []
    }
    
    # Check digital text
    total_digital_chars = sum(len(page.get_text()) for page in doc)
    info["total_digital_chars"] = total_digital_chars
    
    if total_digital_chars > 100:
        info["has_digital_text"] = True
        # Grab first 2 pages digital text
        sample_pages = []
        for i in range(min(3, len(doc))):
            sample_pages.append({
                "page_no": i + 1,
                "text": doc[i].get_text()[:1500]
            })
        info["sample_pages"] = sample_pages
    else:
        info["has_digital_text"] = False
        # Do OCR on first 2-3 pages
        sample_pages = []
        for i in range(min(3, len(doc))):
            page = doc[i]
            pix = page.get_pixmap(dpi=150)
            tmp_img = f"tmp_page_{i}.png"
            pix.save(tmp_img)
            img = Image.open(tmp_img)
            res = await winocr.recognize_pil(img, lang='en')
            sample_pages.append({
                "page_no": i + 1,
                "text": res.text[:1500]
            })
        info["sample_pages"] = sample_pages
        
    return info

async def main():
    results = {}
    for filename in target_files:
        print(f"Analyzing {filename}...")
        results[filename] = await analyze_document(filename)
        
    with open("document_deep_analysis.json", "w", encoding="utf-8") as f:
        json.dump(results, f, ensure_ascii=False, indent=2)
    print("Deep analysis finished and saved to document_deep_analysis.json")

asyncio.run(main())
