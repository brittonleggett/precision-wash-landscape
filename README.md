# Precision Wash & Landscape — website

Static site for **precisionwashlandscape.com**, served by GitHub Pages from the root of
this repository.

> ## ✅ Live and secure
> <https://precisionwashlandscape.com> — HTTPS enforced, valid Let's Encrypt certificate,
> `http`→`https` and `www`→apex both 301. Verified 2026-09-13.
> Next step is Google Search Console:
> **[docs/GOOGLE_SEARCH_CONSOLE_SETUP.md](docs/GOOGLE_SEARCH_CONSOLE_SETUP.md)**

---

## ⚠️ Every `.html` file here is generated — don't hand-edit them

All eight pages share a header, nav, footer, metadata block and JSON-LD. Keeping those
identical by hand across eight files is how sites end up with three different phone
numbers and two different canonical tags.

So the HTML is generated from one script:

```
tools/build.py   →   index.html
                     pressure-washing/index.html
                     landscaping/index.html
                     junk-removal/index.html
                     window-washing/index.html
                     service-area/index.html
                     contact/index.html
                     404.html
                     robots.txt
                     sitemap.xml
```

### To change any page content

```bash
# 1. edit tools/build.py
# 2. regenerate
python tools/build.py
# 3. commit BOTH the script and the regenerated HTML
git add -A && git commit -m "..."
```

The generated files are committed to the repo (GitHub Pages serves them directly —
there's no build step on the server), so the commit must include both.

Every generated file carries this on line 2 as a reminder:

```html
<!-- GENERATED FILE - do not edit by hand. Edit tools/build.py and re-run it. -->
```

**The one exception is `assets/site.css`** — that's a normal file, edit it directly.

### Requirements

Python 3 with no third-party packages. `tools/build.py` uses only the standard library.

*(Pillow is needed only if you regenerate the WebP images — see below.)*

---

## Layout

```
├── index.html               generated
├── 404.html                 generated (noindex)
├── pressure-washing/        generated
├── landscaping/             generated
├── junk-removal/            generated
├── window-washing/          generated
├── service-area/            generated
├── contact/                 generated
├── robots.txt               generated
├── sitemap.xml              generated
├── CNAME                    custom domain for GitHub Pages — leave alone
├── _config.yml              keeps docs/ and tools/ out of the published site
├── assets/
│   └── site.css             hand-edited
├── images/
│   ├── *.jpg                originals + fallbacks
│   ├── *.webp               full-size WebP
│   ├── *-450.webp           450px-wide variants for phones
│   └── og-precision-wash-landscape.jpg   1200×630 social preview
├── tools/
│   └── build.py             the generator
└── docs/                    SEO notes — not part of the website
```

`docs/`, `tools/` and `README.md` are excluded from the published site by `_config.yml`,
disallowed in `robots.txt`, and unlinked from any page. Verified returning 404 on the
live domain.

---

## Local preview

```bash
python -m http.server 8777
# then open http://127.0.0.1:8777/
```

Use a server rather than opening the files directly — every internal link is an
absolute path (`/pressure-washing/`), which won't resolve over `file://`.

---

## Regenerating images

Only needed when new photos are added. Requires Pillow (`pip install Pillow`).

```python
from PIL import Image
import glob, os

for f in glob.glob('images/*.jpg'):
    if f.endswith(('-450.webp', 'og-precision-wash-landscape.jpg')):
        continue
    im = Image.open(f).convert('RGB')
    im.save(f[:-4] + '.webp', 'WEBP', quality=80, method=6)
    w, h = im.size
    if w > 450:
        im.resize((450, round(h * 450 / w)), Image.LANCZOS) \
          .save(f[:-4] + '-450.webp', 'WEBP', quality=78, method=6)
```

Then add the new photo to the `GALLERY_ITEMS` list in `tools/build.py` (with its real
pixel dimensions — they become the `width`/`height` attributes that keep CLS at zero)
and rebuild.

---

## SEO documentation

Start here:

| Doc | What it covers |
|---|---|
| [DOMAIN_AND_HOSTING_FIX.md](docs/DOMAIN_AND_HOSTING_FIX.md) | Hosting status (all resolved) + exactly how the cert was issued, if it ever breaks again |
| [SEO_AUDIT.md](docs/SEO_AUDIT.md) | Full audit, what changed, prioritised actions |
| [GOOGLE_SEARCH_CONSOLE_SETUP.md](docs/GOOGLE_SEARCH_CONSOLE_SETUP.md) | Verification, sitemap, indexing, monitoring, Bing |
| [GOOGLE_BUSINESS_PROFILE.md](docs/GOOGLE_BUSINESS_PROFILE.md) | Profile setup, NAP consistency, getting reviews ethically |
| [SEO_KEYWORD_MAP.md](docs/SEO_KEYWORD_MAP.md) | Which page targets which search, and why |
| [ANALYTICS_PLAN.md](docs/ANALYTICS_PLAN.md) | How to switch analytics on (nothing installed yet) |
| [LOCAL_BACKLINK_PLAN.md](docs/LOCAL_BACKLINK_PLAN.md) | Real local citations worth pursuing |
| [SEO_CONTENT_ROADMAP.md](docs/SEO_CONTENT_ROADMAP.md) | The short list of pages worth building later |

---

## Notes on how this site is built

A few decisions worth knowing before changing things:

- **No JavaScript framework, no build tooling, no npm.** Plain HTML and CSS.
- **No web fonts.** System font stack only — a real page-speed win.
- **No third-party scripts.** The homepage loads with exactly one subresource request
  (the stylesheet). Adding analytics will change that; see the analytics doc.
- **Images are lazy-loaded** below the fold and carry explicit `width`/`height`, which
  is why cumulative layout shift measures 0.000.
- **Business facts live in one place** — the `BIZ` dict at the top of `tools/build.py`.
  Change the phone number there and it updates on all 8 pages, in the schema, and in the
  `tel:`/`sms:` links simultaneously. This is what keeps NAP consistent.
- **No fabricated data anywhere.** No fake reviews, no invented `aggregateRating`, no
  guessed opening hours, no unverified licence or insurance claims. If a fact isn't
  confirmed, it isn't on the site. Several docs flag facts worth confirming so they
  *can* be added.
