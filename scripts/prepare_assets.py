"""Validate upstream component output without drawing custom image assets."""
from pathlib import Path
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parents[1]
ASSETS = ROOT / 'assets'
SVG = 'http://www.w3.org/2000/svg'


def read_svg(name):
    raw = (ASSETS / name).read_text(encoding='utf-8')
    root = ET.fromstring(raw)
    if root.tag != f'{{{SVG}}}svg':
        raise ValueError(f'{name} is not an SVG')
    if any(node.tag.rsplit('}', 1)[-1] in {'script', 'foreignObject'} for node in root.iter()):
        raise ValueError(f'{name} contains unexpected active content')
    return root, raw


def main():
    stats, _ = read_svg('github-stats.svg')
    required = {'stars', 'commits', 'prs', 'issues', 'contribs'}
    if not required.issubset({node.get('data-testid') for node in stats.iter()}):
        raise ValueError('Stats card is missing metrics; refusing to publish an error image')

    for name in ['github-snake.svg', 'github-snake-dark.svg']:
        root, raw = read_svg(name)
        cells = [node for node in root if 'c' in node.get('class', '').split()]
        if len(cells) < 350:
            raise ValueError(f'{name} is missing its contribution grid')
        # Keep the component's own artwork and initial state for reduced motion.
        if 'id="reduced-motion"' not in raw:
            style = '<style id="reduced-motion">@media (prefers-reduced-motion:reduce){svg *{animation:none!important}}</style>'
            (ASSETS / name).write_text(raw.replace('</svg>', style + '</svg>'), encoding='utf-8')

    streak, _ = read_svg('streak-stats.svg')
    labels = ' '.join(streak.itertext())
    if not all(label in labels for label in ['Total Contributions', 'Current Streak', 'Longest Streak']):
        raise ValueError('Streak card is missing metrics')

    for path in ASSETS.glob('*.svg'):
        read_svg(path.name)
        content = path.read_text(encoding='utf-8')
        path.write_text('\n'.join(line.rstrip() for line in content.splitlines()).strip() + '\n', encoding='utf-8')
    print('All upstream component SVGs are valid.')


if __name__ == '__main__':
    main()
