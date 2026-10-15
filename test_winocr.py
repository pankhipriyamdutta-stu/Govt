import asyncio
import sys
import fitz
import winocr
from PIL import Image

sys.stdout.reconfigure(encoding='utf-8')

async def test_ocr():
    doc = fitz.open("source_documents/ARTPS ACT.pdf")
    page = doc[0]
    pix = page.get_pixmap(dpi=200)
    img_path = "page_test.png"
    pix.save(img_path)
    
    img = Image.open(img_path)
    result = await winocr.recognize_pil(img, lang='en')
    print("OCR text recognized on ARTPS ACT.pdf Page 1:")
    print("Text length:", len(result.text))
    print("Lines count:", len(result.lines))
    print("--- SAMPLE TEXT ---")
    print(result.text[:600])

asyncio.run(test_ocr())
