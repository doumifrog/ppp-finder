"""Build index.html from template.html and the JSON files in data/.

Usage (from the repo root):
    python3 scripts/clean.py "Site Update 2025-26.xlsx" > data/sites.json
    python3 scripts/build.py
"""
import os

root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
read = lambda p: open(os.path.join(root, p), encoding='utf-8').read()

body = (read('template.html')
        .replace('__SITES__', read('data/sites.json'))
        .replace('__MAP__', read('data/co_counties.json')))

page = ('<!doctype html>\n<html lang="en">\n<head>\n<meta charset="utf-8">\n'
        '<meta name="viewport" content="width=device-width, initial-scale=1">\n'
        '</head>\n<body>\n' + body + '\n</body>\n</html>\n')

with open(os.path.join(root, 'index.html'), 'w', encoding='utf-8') as f:
    f.write(page)
print('Wrote index.html')
