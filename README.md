# lumiwire-site

The website for Lumiwire (PLAN.md "Website track W1" in the app repo), published by GitHub Pages from `docs/` on `main`:
https://sriramgoparaju.github.io/lumiwire-site/

Static HTML made by `build.py` (the Inkbloom site generator, retargeted). Edit the sources, rebuild, commit both:

```
python tools/import_images.py   # only when the app's look changes: screenshots from ../lumiwire/docs/emulator
python build.py                 # writes docs/
python build.py preview --preview   # browsable from disk (index.html links), not committed
bash tools/check.sh             # every page answers 200 over HTTPS (after the push has deployed)
```

| File | What it holds |
| --- | --- |
| `build.py` | Layout, styles (the app's Paper and Graphite tokens), `SITE_ORIGIN`, `BASE_PATH`, `LIVE_STORES` |
| `content.py` | Home features, rules, obstacles, stars, modes, chapters, FAQ, support address, `SHOP_LIVE` |
| `legal/*.html` | Privacy policy, terms of use, delete-account page (body only; `{{EMAIL}}` etc. are filled in by the build) |
| `images/` | Source pictures (app icon, emulator screenshots); the build writes resized WebP files to `docs/assets/` |

Switches:

- `SHOP_LIVE` (content.py): `False` while testers have a build without ads and purchases; the legal pages carry a note and the FAQ leaves out ads, hints and purchases. Flip to `True` when the Phase 10 build reaches the Alpha track.
- `LIVE_STORES` (build.py): `True` on launch day, with `APP_STORE_URL` set in content.py.
- Domain move (W1 step 4): `SITE_ORIGIN = "https://<domain>"`, `BASE_PATH = ""`, add `docs/CNAME` and `docs/app-ads.txt` (`google.com, pub-8395918704114267, DIRECT, f08c47fec0942fa0`) to the build, then update the store URL fields and the app's Remote Config links (`links_privacy`, `links_terms`, `links_support`, `links_delete_account`).
