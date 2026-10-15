import fitz
import sys

sys.stdout.reconfigure(encoding='utf-8')

# 1. MaintenanceofRecordstSZEC.pdf
doc_m = fitz.open("source_documents/MaintenanceofRecordstSZEC.pdf")
print("=== DOPT RTI INSTRUCTIONS FULL TEXT ===")
for p in range(len(doc_m)):
    print(f"--- Page {p+1} ---")
    print(doc_m[p].get_text())

# 2. Citizen Charter services overview
doc_cc = fitz.open("source_documents/Citizen Charter.pdf")
print("\n=== CITIZEN CHARTER SERVICES EXTRACT ===")
for p in range(min(5, len(doc_cc))):
    print(f"--- CC Page {p+1} ---")
    print(doc_cc[p].get_text()[:600])

# 3. MoF Procurement Manual table of contents
doc_mof = fitz.open("source_documents/Manual_for_Procurement_of_Consultancy_&_Other_Services_Updated June, 2022_1.pdf")
print("\n=== MOF PROCUREMENT MANUAL PREVIEW ===")
for p in range(min(15, len(doc_mof))):
    txt = doc_mof[p].get_text().strip()
    if "Chapter" in txt or "Table of Contents" in txt or "Contents" in txt:
        print(f"--- Page {p+1} ---")
        print(txt[:600])
