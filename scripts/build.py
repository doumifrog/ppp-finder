"""Build index.html from template.html and the JSON files in data/, and the
Apps Script backend (apps-script/Code.gs) from apps-script/Code.template.gs.

Usage (from the repo root):
    python3 scripts/clean.py "Site Update 2025-26.xlsx" > data/sites.json
    python3 scripts/build.py

Code.gs needs apps-script/config.json (not committed, since it holds email
addresses). Copy apps-script/config.example.json to start one.
"""
import json, os

root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
read = lambda p: open(os.path.join(root, p), encoding='utf-8').read()

body = (read('template.html')
        .replace('__SITES__', read('data/sites.json'))
        .replace('__MAP__', read('data/co_counties.json'))
        .replace('__ZIPS__', read('data/co_zips.json'))
        .replace('__FORM_URL__', os.environ.get('FORM_URL', read('apps-script/form-url.txt').strip())))

page = ('<!doctype html>\n<html lang="en">\n<head>\n<meta charset="utf-8">\n'
        '<meta name="viewport" content="width=device-width, initial-scale=1">\n'
        '</head>\n<body>\n' + body + '\n</body>\n</html>\n')

with open(os.path.join(root, 'index.html'), 'w', encoding='utf-8') as f:
    f.write(page)
print('Wrote index.html')

# Apps Script backend: the server keeps its own site -> email list, so the form
# can only ever email the sites in data/sites.json.
cfg_path = os.path.join(root, 'apps-script/config.json')
if os.path.exists(cfg_path):
    cfg = json.load(open(cfg_path, encoding='utf-8'))
    sites = {str(s['id']): {'name': s['name'], 'program': s['program'], 'email': s['email']}
             for s in json.loads(read('data/sites.json'))}
    gs = (read('apps-script/Code.template.gs')
          .replace('__TEST_EMAIL__', cfg['test_email'])
          .replace('__INTAKE_EMAIL__', cfg['intake_email'])
          .replace('__SITES__', json.dumps(sites, indent=2, ensure_ascii=False)))
    with open(os.path.join(root, 'apps-script/Code.gs'), 'w', encoding='utf-8') as f:
        f.write(gs)
    print('Wrote apps-script/Code.gs')
else:
    print('Skipped apps-script/Code.gs (no apps-script/config.json)')
