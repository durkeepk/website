from pathlib import Path
import sys
from PIL import Image, ImageOps, ImageDraw

for folder_name in sys.argv[1:]:
    folder = Path(folder_name)
    pages = sorted(folder.glob("page-*.png"), key=lambda p: int(p.stem.split("-")[-1]))
    if not pages:
        continue
    thumbs = []
    for i, page in enumerate(pages, 1):
        im = Image.open(page).convert("RGB")
        im.thumbnail((420, 560))
        canvas = Image.new("RGB", (440, 600), "white")
        canvas.paste(im, ((440-im.width)//2, 25))
        ImageDraw.Draw(canvas).text((10, 5), f"Page {i}", fill="black")
        thumbs.append(canvas)
    cols = 3
    rows = (len(thumbs) + cols - 1) // cols
    sheet = Image.new("RGB", (cols*440, rows*600), "#cccccc")
    for i, im in enumerate(thumbs):
        sheet.paste(im, ((i%cols)*440, (i//cols)*600))
    sheet.save(folder / "contact-sheet.jpg", quality=92)
