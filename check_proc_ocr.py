import asyncio
import winocr
from PIL import Image

async def check():
    for p in [1, 2, 3, 4, 5]:
        res = await winocr.recognize_pil(Image.open(f"proc_page_{p}.png"), lang='en')
        print(f"--- Procurement Rules Page {p} ({len(res.text)} chars) ---")
        print(res.text[:400].strip())
        print("...")

asyncio.run(check())
