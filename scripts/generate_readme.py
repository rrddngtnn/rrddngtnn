"""Validate standard upstream SVGs, then publish the authored README unchanged."""
from pathlib import Path
import xml.etree.ElementTree as ET


def validate_card(path, expected):
    root = ET.fromstring(path.read_text())
    if root.tag != '{http://www.w3.org/2000/svg}svg':
        raise ValueError(f'{path}: not an SVG')
    text = ' '.join(root.itertext())
    if any(error in text.lower() for error in ['something went wrong', 'rate limit', 'bad credentials', 'deployment_paused', 'deployment_disabled', 'error fetching', 'failed to fetch']):
        raise ValueError(f'{path}: upstream error card')
    if expected not in text or not root.get('width') or not root.get('height'):
        raise ValueError(f'{path}: missing standard card content')


def publish(root=Path('.')):
    assets = root/'.github/assets'
    validate_card(assets/'stats.svg', 'Total Stars')
    validate_card(assets/'top-langs.svg', 'Most Used Languages')
    validate_card(assets/'streak.svg', 'Current Streak')
    validate_card(assets/'trophies.svg', 'Stars')
    (root/'README.md').write_text((root/'README.source.md').read_text())
    for path in assets.glob('*.svg'):
        if path.name not in {'stats.svg', 'top-langs.svg', 'streak.svg', 'trophies.svg'}:
            path.unlink()
    print('Validated official stats, languages, streak and trophy cards; published README source.')


if __name__ == '__main__':
    publish()
