import fitz
import asyncio
import winocr
from PIL import Image

async def ocr_u23():
    doc = fitz.open("source_documents/untitled_23.pdf")
    for i in range(len(doc)):
        pix = doc[i].get_pixmap(dpi=200)
        img_name = f"u23_p{i+1}.png"
        pix.save(img_name)
        res = await winocr.recognize_pil(Image.open(img_name), lang='en')
        print(f"=== UNTITLED_23 PAGE {i+1} OCR ===")
        print(res.text)

asyncio.run(ocr_u23())
