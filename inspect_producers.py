import fitz
from pathlib import Path
import json

docs = sorted(Path("source_documents").glob("*.pdf"))
report = {}
for d in docs:
    doc = fitz.open(d)
    report[d.name] = {
        "pages": len(doc),
        "metadata": doc.metadata,
        "is_encrypted": doc.is_encrypted
    }

print(json.dumps(report, indent=2))
