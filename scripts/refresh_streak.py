"""Cache the official Streak Stats endpoint; preserve the last card on failure."""
from pathlib import Path
import os
import urllib.parse
import urllib.request
import xml.etree.ElementTree as ET

params = {
    'user': os.environ.get('GITHUB_REPOSITORY_OWNER', 'DevXingMC'),
    'theme': 'github-dark-blue', 'background': '0D1424', 'border': '26354C',
    'ring': '70D8EF', 'fire': '70D8EF', 'currStreakLabel': '70D8EF',
    'sideLabels': 'BFCCDE', 'dates': '8B9FB9', 'border_radius': 16,
    'disable_animations': 'true', 'card_width': 460, 'stroke': '26354C',
    'sideNums': '70D8EF', 'currStreakNum': 'E6EDF3', 'timezone': 'Asia/Shanghai',
}
url = 'https://streak-stats.demolab.com?' + urllib.parse.urlencode(params)
destination = Path(__file__).resolve().parents[1] / 'assets/streak-stats.svg'
try:
    request = urllib.request.Request(url, headers={'User-Agent': 'DevXingMC-profile'})
    with urllib.request.urlopen(request, timeout=30) as response:
        data = response.read()
    tree = ET.fromstring(data)
    text = ' '.join(tree.itertext())
    if tree.tag != '{http://www.w3.org/2000/svg}svg' or not all(
        label in text for label in ['Total Contributions', 'Current Streak', 'Longest Streak']
    ):
        raise ValueError('Endpoint did not return a valid streak card')
    destination.write_bytes(data)
    print('Updated the official Streak Stats card.')
except Exception as error:
    if not destination.exists():
        raise
    print(f'::warning::Streak service unavailable ({type(error).__name__}); retaining the previous card.')
