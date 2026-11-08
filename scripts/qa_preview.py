"""Measure resvg previews and compose the requested two-card plus activity layout."""
import json
from pathlib import Path
import sys
from PIL import Image

folder = Path(sys.argv[1])
report = []
for theme, background in [('light', '#ffffff'), ('dark', '#16121c')]:
    images = {}
    for name in ['stats', 'languages', 'activity']:
        file = max(folder.glob(f'{name}-*-{theme}.png'), key=lambda p: p.stat().st_mtime)
        image = Image.open(file).convert('RGBA')
        w, h = image.size
        # Rounded card borders are inset, so all four outer edges must be transparent.
        edge = [image.getpixel((x, y))[3] for x, y in
                [(x, 0) for x in range(w)] + [(x, h-1) for x in range(w)] +
                [(0, y) for y in range(h)] + [(w-1, y) for y in range(h)]]
        assert max(edge) == 0, f'{file}: clipped content on outer edge'
        images[name] = image
        report.append({'card': name, 'theme': theme, 'size': [w, h], 'edge_ink': sum(edge)})
    canvas = Image.new('RGBA', (2200, 1160), background)
    canvas.alpha_composite(images['stats'], (0, 0))
    canvas.alpha_composite(images['languages'], (1140, 0))
    canvas.alpha_composite(images['activity'], (0, 600))
    canvas.convert('RGB').save(folder/f'profile-composite-{theme}.png')


def luminance(color):
    values = [int(color[i:i+2], 16)/255 for i in (1, 3, 5)]
    values = [v/12.92 if v <= .04045 else ((v+.055)/1.055)**2.4 for v in values]
    return sum(v*w for v, w in zip(values, [.2126, .7152, .0722]))


for background, foreground in [('#ffffff', '#584b62'), ('#ffffff', '#80546e'),
                               ('#16121c', '#cbbfd5'), ('#16121c', '#f0afbe')]:
    a, b = sorted([luminance(background), luminance(foreground)])
    contrast = (b+.05)/(a+.05)
    assert contrast >= 4.5
    report.append({'background': background, 'foreground': foreground, 'contrast': round(contrast, 2)})
(folder/'qa.json').write_text(json.dumps(report, indent=2))
print(json.dumps(report, indent=2))
