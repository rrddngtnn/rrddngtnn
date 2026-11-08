"""Measure resvg PNG previews, without adding a NumPy dependency."""
import json
from pathlib import Path
import sys
from PIL import Image

folder = Path(sys.argv[1])
report = []
images = []
for file in sorted(folder.glob('readme*.png')):
    image = Image.open(file).convert('RGB')
    images.append(image)
    w, h = image.size
    background = image.getpixel((0, 0))
    cols, rows, edge_ink = [0] * w, [0] * h, 0
    for y in range(h):
        for x in range(w):
            if max(abs(a-b) for a, b in zip(image.getpixel((x, y)), background)) > 20:
                cols[x] += 1
                rows[y] += 1
                edge_ink += int(x in (0, w-1) or y in (0, h-1))
    xs = [i for i, n in enumerate(cols) if n > 3]
    ys = [i for i, n in enumerate(rows) if n > 3]
    assert edge_ink == 0, file
    report.append(dict(card=file.name, left=min(xs)/2, right=(w-1-max(xs))/2,
                       top=min(ys)/2, bottom=(h-1-max(ys))/2, edge_ink=edge_ink))
assert len(images) == 4
assert max(r['left'] for r in report) - min(r['left'] for r in report) <= 2
assert all(abs(r['top'] - r['bottom']) <= 4 for r in report)
composite = Image.new('RGB', (1720, sum(im.height for im in images)+32*(len(images)-1)), '#ffffff')
y = 0
for image in images:
    composite.paste(image, (0, y))
    y += image.height+32
composite.save(folder/'profile-composite.png')
(folder/'qa.json').write_text(json.dumps(report, indent=2))
print(json.dumps(report, indent=2))
