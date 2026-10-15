import fitz

doc = fitz.open("source_documents/untitled_23.pdf")
print("Page 1 images:", len(doc[0].get_images()))
print("Page 2 images:", len(doc[1].get_images()))
if len(doc[1].get_images()) > 0:
    for img in doc[1].get_images():
        print("Page 2 image xref:", img[0])
