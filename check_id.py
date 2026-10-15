import fitz
import io
from PIL import Image

doc = fitz.open("C:/Users/pankh/Downloads/Identity Card.pdf")
page = doc[0]
images = page.get_images()
print("Images count:", len(images))
for i, img in enumerate(images):
    xref = img[0]
    base_image = doc.extract_image(xref)
    print(f"Image {i}: format={base_image['ext']}, width={base_image['width']}, height={base_image['height']}")
