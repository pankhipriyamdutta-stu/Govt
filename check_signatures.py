import fitz
import json
from pathlib import Path

docs_dir = Path("source_documents")

sig_results = {}

for pdf_file in sorted(docs_dir.glob("*.pdf")):
    doc = fitz.open(pdf_file)
    has_sig = False
    sig_details = []
    
    # Check for signature fields / /ByteRange / /Contents
    try:
        for page in doc:
            for field in page.widgets():
                if field.field_type == fitz.PDF_WIDGET_TYPE_SIGNATURE:
                    has_sig = True
                    sig_details.append({
                        "name": field.field_name,
                        "value": str(field.field_value)
                    })
    except Exception as e:
        sig_details.append({"error": str(e)})
        
    # Check raw trailer and object types
    raw_sig_present = False
    try:
        for i in range(1, doc.xref_length()):
            obj_str = doc.xref_object(i)
            if "/Type /Sig" in obj_str or "/Type/Sig" in obj_str:
                raw_sig_present = True
                break
    except Exception as e:
        pass
        
    sig_results[pdf_file.name] = {
        "widget_sig_present": has_sig,
        "sig_widgets": sig_details,
        "raw_sig_dict_present": raw_sig_present,
        "is_encrypted": doc.is_encrypted,
        "page_count": len(doc)
    }

print(json.dumps(sig_results, indent=2))
