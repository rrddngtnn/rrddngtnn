"""Generate only from authenticated GitHub data; CI is the output writer."""
import argparse
import hashlib
import os
from pathlib import Path
import profile_stats


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--output-dir', type=Path, default=Path('.'))
    args = parser.parse_args()
    if not os.environ.get('GITHUB_TOKEN'):
        raise SystemExit('GITHUB_TOKEN is required; refusing mock-data generation')
    source = Path('README.source.md').read_text()
    marker = '<!-- github-stats -->'
    if source.count(marker) != 1:
        raise ValueError('Source must contain exactly one statistics marker')
    # Finish every API read and validation before writing anything.
    data = profile_stats.fetch()
    cards = profile_stats.render(data)
    paths = {name: f'.github/assets/{name}-{hashlib.sha256(svg.encode()).hexdigest()[:12]}.svg'
             for name, svg in cards.items()}
    markup = ('<p align="center">\n'
              f'<img src="./{paths["stats"]}" width="48%" alt="GitHub Stats: personal contributions in the displayed calendar window" />\n'
              f'<img src="./{paths["languages"]}" width="48%" alt="Top Languages by code bytes in owned public non-fork repositories" />\n'
              '</p>\n<p align="center">\n'
              f'<img src="./{paths["activity"]}" width="100%" alt="Contribution Activity: daily GitHub contribution calendar" />\n'
              '</p>')
    output = args.output_dir
    assets = output/'.github/assets'
    assets.mkdir(parents=True, exist_ok=True)
    for name, svg in cards.items():
        (output/paths[name]).write_text(svg)
    (output/'README.md').write_text(source.replace(marker, markup))
    for asset in assets.glob('*.svg'):
        if str(asset.relative_to(output)) not in paths.values():
            asset.unlink()
    print('Validated and generated 3 cards from live GitHub GraphQL data.')


if __name__ == '__main__':
    main()
