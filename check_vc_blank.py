import fitz
from PIL import Image

for p in [2, 8]:
    img = Image.open(f"vc_page_{p}.png")
    print(f"Page {p} size: {img.size}, mode: {img.mode}")
