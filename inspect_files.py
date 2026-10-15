import fitz # PyMuPDF
from pathlib import Path
import json

downloads_dir = Path("C:/Users/pankh/Downloads")

gov_files_in_screenshot = [
    "Citizen Charter.pdf",
    "untitled_23.pdf",
    "ias_fixation_of_cadre_strength_second_amendment_regulations_2025.pdf",
    "ARTPS RULES_0.pdf",
    "ARTPS ACT.pdf",
    "dms22_assam_public_procurement_rules_2020.pdf",
    "MaintenanceofRecordstSZEC.pdf",
    "Vacancy circular for employment news-1m1R62.pdf",
    "Manual_for_Procurement_of_Consultancy_&_Other_Services_Updated June, 2022_1.pdf",
    "c9fe9c9b6840524844316f74bb1c556c.pdf",
    # Also check nearby files:
    "Identity Card.pdf",
    "Doc5.docx",
    "Doc8.docx",
    "19,20,23,24.docx"
]

results = []
for name in gov_files_in_screenshot:
    p = downloads_dir / name
    if not p.exists():
        results.append({"name": name, "exists": False})
        continue
    info = {
        "name": name,
        "exists": True,
        "size": p.stat().st_size,
        "ext": p.suffix
    }
    if p.suffix.lower() == ".pdf":
        try:
            doc = fitz.open(p)
            info["pages"] = len(doc)
            info["metadata"] = doc.metadata
            first_page_text = doc[0].get_text() if len(doc) > 0 else ""
            info["preview"] = first_page_text[:400].strip()
            # check if scanned (low text)
            total_chars = sum(len(page.get_text()) for page in doc)
            info["total_chars"] = total_chars
            info["is_likely_scanned"] = (total_chars / max(1, len(doc))) < 50
        except Exception as e:
            info["error"] = str(e)
    results.append(info)

print(json.dumps(results, indent=2))
