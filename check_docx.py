import zipfile
import xml.etree.ElementTree as ET
from pathlib import Path

downloads_dir = Path("C:/Users/pankh/Downloads")

for name in ["19,20,23,24.docx", "Doc5.docx", "Doc8.docx"]:
    p = downloads_dir / name
    print(f"\n=================== {name} ===================")
    try:
        with zipfile.ZipFile(p) as z:
            tree = ET.fromstring(z.read("word/document.xml"))
            texts = [node.text for node in tree.iter() if node.text]
            full_text = " ".join(texts)
            print("Full text length:", len(full_text))
            print("Full text:", full_text[:1000])
    except Exception as e:
        print("Error:", e)
