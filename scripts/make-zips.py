"""Build data/co_zips.json: each Colorado ZIP code and the counties it falls in.

Source: the HUD USPS ZIP-to-county crosswalk, as bundled in the
zipcodes-nrviens npm package (resources/zip_fips_county_code_and_state.csv).

Usage (from the repo root):
    python3 scripts/make-zips.py path/to/zip_fips_county_code_and_state.csv
"""
import csv, json, os, sys

root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
counties = {c['n'] for c in json.load(open(os.path.join(root, 'data/co_counties.json')))}

zips = {}
for row in csv.DictReader(open(sys.argv[1], encoding='utf-8')):
    if row['state'] != 'CO':
        continue
    name = row['county'].strip()
    if name not in counties:
        sys.exit(f'Unknown county name: {name!r}')
    zips.setdefault(row['zip'].zfill(5), set()).add(name)

out = {z: sorted(c) for z, c in sorted(zips.items())}
with open(os.path.join(root, 'data/co_zips.json'), 'w', encoding='utf-8') as f:
    json.dump(out, f, separators=(',', ':'))
print(f'Wrote {len(out)} ZIP codes')
