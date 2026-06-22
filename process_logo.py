# Make ONLY the outer background (connected to corners) transparent.
# Keep the badge exactly as drawn (black lines, white interior, any shading).
from PIL import Image
import numpy as np
from collections import deque

src = r"C:\Users\ASUS\Downloads\Logo Website personal.png"
out = r"D:\C. BUSINESS\NO NAME\PRODUCTS\david-site\img\logo.png"

im = Image.open(src).convert("RGB")
im.thumbnail((420, 420))
a = np.asarray(im)
h, w = a.shape[:2]
L = a.mean(axis=2)
white = L > 222

mask = np.zeros((h, w), bool)
dq = deque()
for c in [(0, 0), (0, w - 1), (h - 1, 0), (h - 1, w - 1)]:
    if white[c]:
        mask[c] = True
        dq.append(c)
while dq:
    y, x = dq.popleft()
    for dy, dx in ((-1, 0), (1, 0), (0, -1), (0, 1)):
        ny, nx = y + dy, x + dx
        if 0 <= ny < h and 0 <= nx < w and not mask[ny, nx] and white[ny, nx]:
            mask[ny, nx] = True
            dq.append((ny, nx))

alpha = np.where(mask, 0, 255).astype("uint8")
rgba = np.dstack([a.astype("uint8"), alpha])
Image.fromarray(rgba, "RGBA").save(out)
print("done", (w, h), "transparent px:", int(mask.sum()))
