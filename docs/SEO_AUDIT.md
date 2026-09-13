# SEO audit — Precision Wash & Landscape

**Audited and rebuilt:** 2026-09-12
**Site:** https://precisionwashlandscape.com (GitHub Pages, static HTML)
**Repo:** brittonleggett/precision-wash-landscape

> ### Status update — 2026-09-13
> **The domain suspension is fixed and the site is live over HTTP.** Britton verified
> the WHOIS registrant contact on 2026-09-13; nameservers returned to normal, DNS now
> points at GitHub Pages, and all 7 pages plus robots.txt, sitemap.xml, CSS and images
> were re-verified serving 200 from the real domain, byte-identical to the local build.
>
> **One hosting task remains: HTTPS.** `https://` still serves a `*.github.io`
> certificate because GitHub never queued one (its DNS check last ran while the domain
> was dead). Fix is a 30-second remove/re-add of the custom domain in GitHub Pages
> settings → [DOMAIN_AND_HOSTING_FIX.md](DOMAIN_AND_HOSTING_FIX.md).
> **Do not start Search Console until HTTPS works** — Google's first crawl should find
> the `https://` version.
>
> *Original finding, for the record: the domain was suspended by Namecheap on 2026-08-29
> for unverified WHOIS registrant details, leaving no working URL for the site for 15
> days.*

---

## Technical SEO

| Check | Status | Detail |
|---|---|---|
| **HTTP status** | ✅ Verified live | All 7 pages 200 over HTTP on the real domain, byte-identical to local. Unknown paths return a real 404 with the branded page. `/docs/`, `/tools/`, `/README.md` correctly 404 (excluded from the build). |
| **HTTPS** | ❌ **Outstanding** | Serves a `*.github.io` cert — mismatch, so browsers warn. GitHub has no certificate object for this domain yet. Needs a custom-domain remove/re-add in Pages settings, then tick Enforce HTTPS. **The last blocking item.** |
| **Canonical domain** | ✅ Correct, ⚠️ not yet enforced | Apex (`precisionwashlandscape.com`, no `www`) in `CNAME` and every canonical tag. DNS for apex + `www` both verified correct. `http`→`https` collapse waits on Enforce HTTPS. |
| **Robots** | ✅ Verified live | `/robots.txt` allows all crawlers, disallows only `/docs/` and `/tools/` (repo housekeeping, unlinked), and references the sitemap on the last line. |
| **Sitemap** | ✅ Verified live | 7 canonical, indexable, 200-status URLs with `lastmod`. No redirects, no 404s, no noindex pages, no dev routes. Verified programmatically against the canonical tag of every page — zero drift in either direction. |
| **Noindex issues** | ✅ Correct | Exactly one page is `noindex, follow` — `/404.html` — and it's correctly excluded from the sitemap. No accidental noindex anywhere. |
| **Structured data** | ✅ Good | 19 JSON-LD blocks across 8 pages, **all parse-validated**. See breakdown below. |
| **Mobile** | ✅ Fixed | Was badly broken: **247px of horizontal overflow at 375px wide**, caused by the nav bar. Measured before/after in-browser; now 0px overflow at 320 / 375 / 390 / 480 / 600 / 700 / 860px. |
| **Performance** | ✅ Excellent | DOMContentLoaded 66ms, **CLS 0.000**, **1 subresource request** on first load (the 25KB stylesheet). Zero web fonts, zero third-party scripts, zero trackers. All 13 homepage images lazy-load — none fetched above the fold. |

### Structured data detail

| Page | Schema types |
|---|---|
| `/` | `HomeAndConstructionBusiness` (LocalBusiness subtype), `WebSite`, `FAQPage` |
| `/pressure-washing/` | `Service`, `BreadcrumbList`, `FAQPage` |
| `/landscaping/` | `Service`, `BreadcrumbList`, `FAQPage` |
| `/junk-removal/` | `Service`, `BreadcrumbList`, `FAQPage` |
| `/window-washing/` | `Service`, `BreadcrumbList`, `FAQPage` |
| `/service-area/` | `BreadcrumbList`, `FAQPage` |
| `/contact/` | `ContactPage`, `BreadcrumbList` |

The business entity is declared once with `@id: .../#business`; every `Service` block
references it by `@id` rather than restating it, so Google resolves them to one entity.

**Deliberately omitted, because it can't be verified:**

- **No `aggregateRating` and no `review` markup.** There is one real Facebook comment
  from Cindy Young, quoted honestly on-page as a testimonial. Fake rating markup is a
  manual-action risk and is not present.
- **No `openingHours`.** The Business Profile notes say hours are a *suggested default*,
  not confirmed. Inventing them would be a NAP inconsistency waiting to happen.
- **No street address.** Correct — this is a service-area business. Note this means the
  site won't earn a LocalBusiness rich result (Google wants a postal address for that);
  local visibility will come from the Business Profile instead, which is the right
  mechanism anyway.
- **`FAQPage` is included but won't produce rich results.** Since 2023 Google shows FAQ
  rich results only for government and health sites. It's valid, harmless, and still
  read by Bing and AI assistants — but don't expect star-style FAQ snippets.

---

## On-page SEO

| Check | Status | Detail |
|---|---|---|
| **Titles** | ✅ Good | 8 unique titles, 43–63 characters. Every one leads with service + city, ends with the brand. No "Home" / "Services" / "About Us". |
| **Descriptions** | ✅ Good | 8 unique meta descriptions, 132–165 characters. Each names the service, the towns, a benefit ("free estimates") and a call to action. No duplication. |
| **H1s** | ✅ Fixed | Exactly one H1 per page, all 8 verified programmatically. Heading hierarchy checked on every page — **no skipped levels anywhere** (no h3 following an h1, etc.). |
| **Internal links** | ✅ Good | 0 broken internal links. Every page links to all 6 others via nav + footer, plus contextual in-body links with descriptive anchors. |
| **Service pages** | ✅ Built | 4 dedicated pages, one per real service. |
| **Location relevance** | ✅ Good | Real, specific local content — not city-name padding. See *Local SEO* below. |

### Before → after

The site was **a single page** before this work. There were no other titles to compare
against, because there were no other pages.

| Page | Before title | After title | Primary search intent |
|---|---|---|---|
| `/` | Precision Wash & Landscape \| Pressure Washing & Junk Removal, Ouachita & Lincoln Parish LA *(97 chars — truncated in results)* | Pressure Washing & Yard Cleanup in Monroe, LA \| Precision Wash *(62)* | pressure washing Monroe LA |
| `/pressure-washing/` | *(did not exist)* | House & Driveway Pressure Washing, Monroe LA \| Precision Wash | pressure washing / house washing Monroe LA |
| `/landscaping/` | *(did not exist)* | Flowerbed Cleanup & Pine Straw in Monroe, LA \| Precision Wash | flower bed cleanup Monroe LA |
| `/junk-removal/` | *(did not exist)* | Junk Removal & Hauling in Monroe & Ruston, LA \| Precision Wash | junk removal Monroe LA |
| `/window-washing/` | *(did not exist)* | Window Cleaning in Monroe & West Monroe, LA \| Precision Wash | window cleaning Monroe LA |
| `/service-area/` | *(did not exist)* | Service Area: Monroe, West Monroe & Ruston, LA \| Precision Wash | pressure washing near me |
| `/contact/` | *(did not exist)* | Free Estimate — Call or Text \| Precision Wash & Landscape | pressure washing quote Monroe LA |
| `/404.html` | *(did not exist)* | Page Not Found \| Precision Wash & Landscape | n/a — `noindex` |

**H1 change on the homepage.** Before: `Precision Wash & Landscape` — brand only, which
tells a search engine nothing about the business. After: the brand wordmark *plus*
"Pressure washing and flowerbed care in Monroe, West Monroe & Ruston, Louisiana", inside
one H1. The giant brand lettering is still the visual centrepiece; the descriptive half
is a styled second line. No design was sacrificed for this.

### Also added

| Thing | Detail |
|---|---|
| **New pages** | 6 indexable + a custom 404 |
| **Redirects created** | **None — and none were needed.** The only pre-existing URL was `/`, and it still exists at the same address. No URL changed, so nothing needs a 301. |
| **Schema added** | 19 JSON-LD blocks (was: 1 `LocalBusiness` block on the homepage) |
| **Metadata added** | Per-page canonical, Open Graph (7 properties incl. a purpose-built 1200×630 image), Twitter card, `geo.region` / `geo.placename` |
| **Images** | 13 WebP conversions + 13 responsive 450w variants + 1 OG image; `<picture>` with `srcset`/`sizes`, explicit `width`/`height`, lazy loading below the fold |
| **Site chrome** | Persistent nav with `aria-current`, breadcrumbs on interior pages, footer nav, sticky mobile call/text bar |

---

## Local SEO

| Check | Status | Detail |
|---|---|---|
| **Google Business Profile** | ❌ Not created | Prepared copy exists and is unused. **This is the single highest-value remaining action** — for a service-area business, the Profile drives more calls than the website. See [GOOGLE_BUSINESS_PROFILE.md](GOOGLE_BUSINESS_PROFILE.md). |
| **NAP consistency** | ✅ Consistent on-site | Name, service area and phone are identical on all 8 pages (generated from one source, so they can't drift). Off-site consistency is unverified — checklist in the GBP doc. |
| **Reviews** | ⚠️ One, unstructured | A single genuine Facebook comment from Cindy Young. Zero Google reviews. Review count is the biggest lever on local pack ranking. Ethical process documented in the GBP doc. |
| **Local schema** | ✅ Good | `areaServed` lists both parishes and all three cities, on the business entity and on every `Service`. |
| **Service areas** | ✅ Clear | Dedicated `/service-area/` page; parishes and cities named consistently. |

### On local relevance — what was avoided

The brief warned against manufacturing local trivia to insert city names. The local
content here is limited to things that are actually true about north Louisiana and
actually relevant to these services:

- Humid climate → mildew on shaded and north-facing siding
- *Gloeocapsa magma* algae streaking on asphalt shingles, worst on north-facing slopes
- Spring pine pollen film on glass and concrete
- Heavy tree cover keeping concrete damp → algae on driveways
- Pine straw as the regional norm over mulch, and why (cost, slope retention, fits the
  pines and azaleas already in local yards)
- Ruston's college-town rental-turnover market
- Storm limb debris and slow municipal pickup

No invented landmarks, no fake neighbourhood lists, no "proudly serving the historic
district of…" padding.

---

## Content

| Check | Detail |
|---|---|
| **Strong pages** | `/pressure-washing/` (1,255 words), `/landscaping/` (1,060), `/junk-removal/` (849), `/` (854) — all with specific, non-generic content |
| **Thin pages** | `/contact/` (422) and `/service-area/` (620) are short **by design** — a contact page shouldn't ramble. `/window-washing/` (645) is the weakest of the four service pages, matching the fact that it's the smallest service. |
| **Missing content** | No About page *(deliberate — see below)*. No pricing guidance. No city-level pages *(deliberate)*. No reviews to display. |
| **Duplicate content** | None. All 8 titles unique, all 8 descriptions unique, no shared body copy between service pages, every page a distinct canonical. |

### Generic AI filler that was removed or avoided

The original copy was largely fine — it already sounded like a real local business
("Call — we'll tell you straight"), and that voice was preserved. Across the new pages,
no instance of the following was used: *"your trusted partner"*, *"quality you can count
on"*, *"we pride ourselves on excellence"*, *"unparalleled service"*, *"attention to
detail"*, *"customer satisfaction is our top priority"*.

Where a trust claim is made it's attached to something concrete — "an outdoor spigot and
an outlet", "you don't have to move it to the curb", "a number before we come out, not
after the truck is in your driveway".

### Why there is no About page

E-E-A-T matters for local service businesses, and a real About page would help. But the
only verifiable facts available are: family-run, owner-operated, Jase Laborde and
Garrett Smith, Colossians 3:23. That's not a page — it's a paragraph, and it's already
on `/contact/` under "Who you're calling".

Writing a fuller About page would mean inventing a founding year, a backstory, or
experience claims. **That's not a trade worth making.** See *Priority actions* for what
Britton would need to supply to make it real.

### Unverified claims — deliberately absent

No licence number, no insurance claim, no "X years of experience", no employee count,
no "hundreds of satisfied customers". None of that is verifiable from available
material. **If the business is insured, saying so is a genuine conversion win** — see
Priority actions.

---

## Duplicate content / canonicalisation

| Risk | Status |
|---|---|
| Duplicate titles | ✅ None |
| Duplicate descriptions | ✅ None |
| Duplicate service copy | ✅ None |
| `www` vs non-`www` | ⚠️ Canonicals all point to apex; needs DNS + GitHub Pages to enforce |
| HTTP vs HTTPS | ❌ Must enable "Enforce HTTPS" once the cert issues |
| `github.io` duplicate | ✅ Handled — `CNAME` makes GitHub 301 it to the apex domain |
| Staging site | ✅ None exists |

---

## Broken links & assets

Crawled all 8 pages programmatically:

- **0** broken internal links
- **0** missing image files (all `src` and every `srcset` candidate resolves)
- **0** images without `alt`
- **0** images without explicit `width`/`height`
- Custom 404 page in place, links back to home, all four services, service area and
  contact — no dead end

One stale reference was found and fixed: `google_business_profile_setup.txt` listed five
photos to upload (`fence-before-after-2.jpg`, `fence-trees.jpg`,
`flowerbed-hydrangeas.jpg`, `porch-roof.jpg`) that **no longer exist** in `/images/` —
they were replaced in an earlier commit. The rewritten
[GOOGLE_BUSINESS_PROFILE.md](GOOGLE_BUSINESS_PROFILE.md) lists only files that are
actually present.

---

## Search Console

| Check | Status |
|---|---|
| **Verification** | ❌ Not verified. Requires Britton's Google login + a DNS TXT record. Not faked. |
| **Sitemap submitted** | ❌ Not submitted. |
| **Indexing status** | ❌ Almost certainly not indexed — the domain was unreachable for its first 15 days of life, so Google has had nothing to crawl. |

**Sequencing:** finish HTTPS first, then verify Search Console. Verifying while the site
only answers on `http://` risks Google settling on the wrong protocol as canonical.

Full click-by-click walkthrough: [GOOGLE_SEARCH_CONSOLE_SETUP.md](GOOGLE_SEARCH_CONSOLE_SETUP.md)

---

## Priority actions

### HIGH — do these first

1. ~~**Un-suspend the domain.**~~ ✅ **Done 2026-09-13.**
2. **Get HTTPS working.** DNS is already correct. Remove and re-add the custom domain in
   GitHub Pages settings to make GitHub issue the certificate, then tick Enforce HTTPS.
   *(Britton, 30 seconds + up to an hour of waiting)* →
   [DOMAIN_AND_HOSTING_FIX.md](DOMAIN_AND_HOSTING_FIX.md) — **this is now the blocker**
3. **Create the Google Business Profile.** For a service-area home-services business
   this outranks the website in importance for actual phone calls. *(Britton, ~30 min)* →
   [GOOGLE_BUSINESS_PROFILE.md](GOOGLE_BUSINESS_PROFILE.md)
4. **Verify Search Console + submit the sitemap.** *(Britton, ~20 min)*
5. **Ask 3–5 recent real customers for Google reviews.** Start with Cindy Young, who
   already commented positively. Zero → five reviews is the biggest single jump in local
   pack ranking you'll ever get. *(Britton, ongoing)*

### MEDIUM

6. **Turn on analytics.** No measurement exists today. → [ANALYTICS_PLAN.md](ANALYTICS_PLAN.md)
7. **Confirm business hours** so they can go on the Profile and into schema.
8. **Confirm insurance status.** If insured, say so on the site — it's a real
   differentiator in this trade and a genuine conversion lever. If not, say nothing.
9. **Photograph jobs by city.** Three Ruston jobs + one Ruston review unlocks a
   legitimate `/service-area/ruston/` page. Photos are the raw material for everything.
10. **Local citations** — Chamber of Commerce, Nextdoor, Apple Business Connect, Bing
    Places. → [LOCAL_BACKLINK_PLAN.md](LOCAL_BACKLINK_PLAN.md)

### LOW

11. First informational article, most likely the pressure-washing cost page. →
    [SEO_CONTENT_ROADMAP.md](SEO_CONTENT_ROADMAP.md)
12. A real About page, once there are facts to fill it — founding year, how Jase and
    Garrett started, equipment, anything concrete.
13. Bing Webmaster Tools (5 min, import from Search Console).
14. Re-crop the four portrait before/after photos. They're 585×1157 displayed in a 4:3
    box, so `object-fit: cover` crops them hard. Cosmetic, not an SEO issue.

---

## Definition of done — where things actually stand

| Goal | Status |
|---|---|
| **Crawlable** | ✅ **Verified live over HTTP** — ⚠️ HTTPS pending |
| **Indexable** | ✅ **Verified live over HTTP** — ⚠️ HTTPS pending |
| **Fast** | ✅ 66ms DCL, 1 request, CLS 0, no fonts, no third-party JS |
| **Mobile-friendly** | ✅ Fixed a real 247px overflow bug; verified 320–860px |
| **Locally relevant** | ✅ Genuine regional content, honest service area |
| **Structured correctly** | ✅ 19 validated JSON-LD blocks, no fabricated data |
| **Conversion-focused** | ✅ Click-to-call everywhere, sticky mobile call/text bar, SMS links, "text a photo" flow |
| **Clear path into Search Console** | ✅ Documented step by step — awaiting Britton's login |
