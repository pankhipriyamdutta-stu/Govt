import numpy as np
from PIL import Image

for p in [2, 8]:
    img = Image.open(f"vc_page_{p}.png").convert("L")
    arr = np.array(img)
    print(f"Page {p}: min={arr.min()}, max={arr.max()}, mean={arr.mean():.2f}, std={arr.std():.2f}")
