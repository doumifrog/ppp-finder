# Parent Possible Program Finder

A county-based finder for Parents as Teachers (PAT) and HIPPY home visiting programs in Colorado. Families or caseworkers pick their county, filter by program, child's age, and language, and send an "I'm interested" request to a site.

Built by Duke Global Research and Consulting for Parent Possible, fall 2026.

## What's here

| Path | What it is |
| --- | --- |
| `index.html` | The finder page. One self-contained file with no outside dependencies except Google Fonts. |
| `template.html` | The source for `index.html`, before the data is filled in. Edit this, not `index.html`. |
| `data/sites.json` | The 33 PAT and HIPPY sites, cleaned from the "Overall" tab of the Site Update spreadsheet. |
| `data/co_counties.json`, `data/co_adj.json` | Colorado county map shapes and which counties border each other. |
| `scripts/` | Scripts that rebuild the data and the page. |
| `wordpress-plugin/` | A small WordPress plugin that puts the finder on any page with `[program_finder]`. |

## Update the site list

When Parent Possible sends a new version of the spreadsheet:

```
python3 scripts/clean.py "Site Update 2025-26.xlsx" > data/sites.json
python3 scripts/build.py
```

Then commit and push. GitHub Pages republishes the page within a minute or two. The script needs `openpyxl` (`pip install openpyxl`).

## Put it on the WordPress site

1. In this repo on GitHub, go to Settings > Pages, set the source to "Deploy from a branch", branch `main`, folder `/ (root)`. The finder will be live at https://doumifrog.github.io/ppp-finder/.
2. Zip the `wordpress-plugin/pp-program-finder` folder (or use the ready-made `pp-program-finder.zip`), then in WordPress go to Plugins > Add New > Upload Plugin and activate it.
3. The plugin already points at https://doumifrog.github.io/ppp-finder/. If the page moves, update the link in Settings > Program Finder.
4. Add the shortcode `[program_finder]` to any page.

The iframe resizes itself to fit the finder, so there's no inner scroll bar.

If installing plugins isn't allowed on the site, paste this into a Custom HTML block instead (replace the link):

```html
<iframe id="pp-finder" src="https://doumifrog.github.io/ppp-finder/" title="Find a home visiting program" style="width:100%;border:0;height:1400px"></iframe>
<script>
window.addEventListener('message', function (e) {
  var f = document.getElementById('pp-finder');
  if (e.source === f.contentWindow && e.data && e.data.type === 'pp-finder-height') f.style.height = e.data.height + 'px';
});
</script>
```

## Still to do before launch

- The interest form is a mock. It shows the email it would send but doesn't send anything. Sending needs a form service (for example Formspree or a WordPress form plugin like Gravity Forms) and Parent Possible's intake email for the CC.
- Only 12 of 33 sites have an email on file (all 11 HIPPY sites and Roots Family Center PAT). Requests for the other sites go to Parent Possible to forward.
- Remove the "Prototype for review" banner at the top of `template.html`.
- The form must never ask about immigration or legal status.
