"""Validate generated SVGs and derive an accessible static contribution map."""
from copy import deepcopy
from pathlib import Path
import re
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parents[1]
ASSETS = ROOT / 'assets'
SVG = 'http://www.w3.org/2000/svg'
ET.register_namespace('', SVG)


def read_svg(name):
    raw = (ASSETS / name).read_text(encoding='utf-8')
    root = ET.fromstring(raw)
    if root.tag != f'{{{SVG}}}svg':
        raise ValueError(f'{name} is not an SVG')
    if any(node.tag.rsplit('}', 1)[-1] in {'script', 'foreignObject'} for node in root.iter()):
        raise ValueError(f'{name} contains unexpected active content')
    return root, raw


def main():
    stats, raw = read_svg('github-stats.svg')
    required = {'stars', 'commits', 'prs', 'issues', 'contribs'}
    present = {node.get('data-testid') for node in stats.iter()}
    if not required.issubset(present):
        raise ValueError('Stats card is missing metrics; refusing to publish an error image')

    for name in ['github-snake.svg', 'github-snake-dark.svg']:
        root, raw = read_svg(name)
        cells = [node for node in root if 'c' in node.get('class', '').split()]
        if len(cells) < 350:
            raise ValueError(f'{name} is missing its contribution grid')

    source, raw = read_svg('github-snake-dark.svg')
    css = ''.join(node.text or '' for node in source.findall(f'{{{SVG}}}style'))
    colors = dict(re.findall(r'--([a-z0-9]+):([^;}]+)', css))
    classes = dict(re.findall(r'\.c\.(c\d+)\{fill:var\(--(c\d+)\)', css))
    cells = [node for node in source if 'c' in node.get('class', '').split()]
    if 'ce' not in colors:
        raise ValueError('Snake palette format changed')
    active_days = sum(any(c in classes for c in node.get('class', '').split()) for node in cells)
    static = ET.Element(f'{{{SVG}}}svg', {
        'viewBox': '0 0 880 174', 'width': '880', 'height': '174',
        'role': 'img', 'aria-labelledby': 'title description',
    })
    ET.SubElement(static, f'{{{SVG}}}title', {'id': 'title'}).text = 'GitHub contribution calendar'
    ET.SubElement(static, f'{{{SVG}}}desc', {'id': 'description'}).text = (
        f'{active_days} active days in the past year. Static version of the contribution snake.'
    )
    ET.SubElement(static, f'{{{SVG}}}rect', {
        'width': '880', 'height': '174', 'rx': '14', 'fill': '#0d1424',
    })
    ET.SubElement(static, f'{{{SVG}}}text', {
        'x': '20', 'y': '28', 'fill': '#bfccde', 'font-size': '14',
        'font-family': 'Segoe UI, sans-serif',
    }).text = f'Contribution map · {active_days} active days in the past year'
    group = ET.SubElement(static, f'{{{SVG}}}g', {'transform': 'translate(16 46)'})
    for node in cells:
        cell = deepcopy(node)
        names = cell.attrib.pop('class').split()
        key = next((classes[name] for name in names if name in classes), 'ce')
        cell.attrib.update({'width': '12', 'height': '12', 'fill': colors[key]})
        group.append(cell)
    (ASSETS / 'contributions.svg').write_text(ET.tostring(static, encoding='unicode'), encoding='utf-8')
    for path in ASSETS.glob('*.svg'):
        read_svg(path.name)
        content = path.read_text(encoding='utf-8')
        path.write_text('\n'.join(line.rstrip() for line in content.splitlines()).strip() + '\n', encoding='utf-8')
    print(f'Validated all SVG assets; static map contains {len(cells)} days, {active_days} active.')


if __name__ == '__main__':
    main()
