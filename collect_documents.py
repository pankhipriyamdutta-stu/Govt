import shutil
import hashlib
from pathlib import Path
import json

source_dir = Path("C:/Users/pankh/Downloads")
dest_dir = Path("c:/Users/pankh/OneDrive/Desktop/Govt/source_documents")
dest_dir.mkdir(parents=True, exist_ok=True)

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

inventory = []

for filename in target_files:
    src_file = source_dir / filename
    dst_file = dest_dir / filename
    
    if not src_file.exists():
        print(f"File not found: {filename}")
        continue
        
    shutil.copy2(src_file, dst_file)
    
    with open(dst_file, "rb") as f:
        data = f.read()
        sha256 = hashlib.sha256(data).hexdigest()
        md5 = hashlib.md5(data).hexdigest()
        
    inventory.append({
        "filename": filename,
        "size_bytes": len(data),
        "sha256": sha256,
        "md5": md5,
        "copied_path": str(dst_file)
    })
    print(f"Copied & Hashed: {filename} -> {sha256[:12]}...")

with open("source_documents_inventory.json", "w", encoding="utf-8") as f:
    json.dump(inventory, f, indent=2)

print("\nAll 10 target documents copied and hashed successfully!")
