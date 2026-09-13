# Google Search Console — setup and ongoing workflow

**Prerequisite: ✅ met as of 2026-09-13.** The domain is live and HTTPS is enforced, so
everything on this page is ready to do. No need to touch
[DOMAIN_AND_HOSTING_FIX.md](DOMAIN_AND_HOSTING_FIX.md) first.

**Verification status: NOT VERIFIED.** Verification requires signing into a Google
account and either editing DNS or uploading a token — it cannot be done for you, and
nothing here pretends it has been done.

---

## What's already in place on the site

| Item | Status | Where |
|---|---|---|
| `robots.txt` | Live, allows all crawlers | `/robots.txt` |
| Sitemap referenced from robots.txt | Yes | last line of `/robots.txt` |
| `sitemap.xml` | Live, 7 canonical URLs | `/sitemap.xml` |
| Canonical tags | On all 8 pages | each page `<head>` |
| `noindex` on the 404 page | Yes (correctly excluded from sitemap) | `/404.html` |

Current `robots.txt`:

```
User-agent: *
Allow: /

Disallow: /docs/
Disallow: /tools/

Sitemap: https://precisionwashlandscape.com/sitemap.xml
```

Current sitemap contents:

```
https://precisionwashlandscape.com/
https://precisionwashlandscape.com/pressure-washing/
https://precisionwashlandscape.com/landscaping/
https://precisionwashlandscape.com/junk-removal/
https://precisionwashlandscape.com/window-washing/
https://precisionwashlandscape.com/service-area/
https://precisionwashlandscape.com/contact/
```

---

## Step 1 — Create and verify the property (Britton must do this)

Go to <https://search.google.com/search-console> and sign in with the Google account
you want to own this long-term. **Use the same Google account you use for the Google
Business Profile** — it makes linking them later trivial.

You'll be offered two property types. **Choose "Domain".**

| | Domain property (recommended) | URL prefix property |
|---|---|---|
| Covers | every subdomain, both http and https | only the exact prefix typed |
| Verified by | one DNS TXT record | file upload, meta tag, or DNS |
| Downside | DNS access required | you'd need separate properties for www and non-www |

A Domain property means you never have to think about `www` vs non-`www` again.

### Verifying by DNS TXT record

1. In Search Console, pick **Domain**, type `precisionwashlandscape.com`, click
   **Continue**.
2. Google shows a TXT record value that looks like
   `google-site-verification=XXXXXXXXXXXXXXXXXXXXXXXXX`. **Copy it.**
3. In a second tab, go to Namecheap → **Domain List → precisionwashlandscape.com →
   Manage → Advanced DNS**.
4. **Add New Record:**
   - Type: `TXT Record`
   - Host: `@`
   - Value: paste the whole `google-site-verification=...` string
   - TTL: Automatic
5. Save.
6. Back in Search Console, click **Verify**. If it fails, wait 15–30 minutes for DNS to
   propagate and click Verify again. It can occasionally take a few hours.

**Leave the TXT record in place forever.** Deleting it un-verifies the property.

> If you're already doing Step 2 of DOMAIN_AND_HOSTING_FIX.md, add this TXT record at
> the same time as the A records — one trip to Advanced DNS instead of two.

---

## Step 2 — Submit the sitemap

Once verified:

1. Left sidebar → **Sitemaps**.
2. In "Add a new sitemap", type just: `sitemap.xml`
3. **Submit.**

Expect *"Couldn't fetch"* for the first few minutes — that's normal. Refresh after an
hour. You want **Status: Success** and **Discovered URLs: 7**.

If it still says "Couldn't fetch" after a day, open
`https://precisionwashlandscape.com/sitemap.xml` in a browser yourself. If that loads
fine, the problem is almost always that the domain/HTTPS work in
DOMAIN_AND_HOSTING_FIX.md isn't finished.

---

## Step 3 — Inspect the homepage

1. Paste `https://precisionwashlandscape.com/` into the search box at the very top of
   Search Console (the one labelled "Inspect any URL...").
2. Press Enter and read the result.

| What it says | What it means | What to do |
|---|---|---|
| "URL is on Google" | Already indexed | Nothing |
| "URL is not on Google" | Not indexed yet | Click **Request Indexing** |
| "URL is available to Google" | Crawlable, not yet indexed | Click **Request Indexing** |
| "Excluded by 'noindex' tag" | Something's wrong | Tell me — shouldn't happen |
| "Blocked by robots.txt" | Something's wrong | Tell me — shouldn't happen |

Also click **Test Live URL** on the homepage once. It should report the page as
mobile-friendly with no issues. This is also where you can see the page as Googlebot
renders it — a useful sanity check that the site isn't broken for crawlers.

---

## Step 4 — Inspect the service pages

Repeat Step 3 for each of these, in this order (most valuable first):

1. `https://precisionwashlandscape.com/pressure-washing/`
2. `https://precisionwashlandscape.com/contact/`
3. `https://precisionwashlandscape.com/landscaping/`
4. `https://precisionwashlandscape.com/service-area/`
5. `https://precisionwashlandscape.com/junk-removal/`
6. `https://precisionwashlandscape.com/window-washing/`

Request indexing for any that aren't indexed yet.

### Rules about Request Indexing

- **Once per URL.** Requesting the same URL repeatedly does nothing good and the
  quota is shared across your whole property.
- There's a daily limit (roughly 10–12 URLs). Seven pages fits comfortably in one day.
- **Re-request only when a page's content meaningfully changes** — a rewritten service
  page, not a typo fix.
- Submitting the sitemap already tells Google these pages exist. URL Inspection just
  pushes them up the queue. Neither one guarantees or speeds up actual indexing.
- Indexing a brand-new site typically takes days to a few weeks. Don't panic at silence
  in week one.

---

## Step 5 — Monitor indexing (weekly at first, then monthly)

**Sidebar → Indexing → Pages.**

You want all 7 URLs under **"Indexed"**. Anything under "Not indexed" has a reason
listed — click through to see which URLs and why.

Reasons you may legitimately see, and what they mean:

| Reason | Serious? | Notes |
|---|---|---|
| "Crawled - currently not indexed" | Usually no | Google saw it and is deciding. Common on new sites. Give it weeks. |
| "Discovered - currently not indexed" | Usually no | Queued but not crawled yet. Same — wait. |
| "Excluded by 'noindex' tag" | Only for `/404.html` | Correct and intentional for that one URL |
| "Page with redirect" | No | Expected for `http://` → `https://` |
| "Duplicate without user-selected canonical" | **Yes** | Tell me — shouldn't happen, every page has a unique canonical |
| "Soft 404" | **Yes** | Tell me |
| "Server error (5xx)" | **Yes** | Tell me |

Don't chase "Crawled - currently not indexed" on a new site with no backlinks. The fix
is the Google Business Profile and real local links (see
[LOCAL_BACKLINK_PLAN.md](LOCAL_BACKLINK_PLAN.md)), not repeated indexing requests.

---

## Step 6 — Monitor queries and impressions (monthly)

**Sidebar → Performance → Search results.**

Set the date range to **Last 3 months** and turn on all four metric boxes at the top:
Clicks, Impressions, Average CTR, Average position.

Nothing will appear for the first couple of weeks. That's normal.

### The three tabs worth your time

**QUERIES** — the actual words people typed before seeing your site. This is the single
most valuable screen in Search Console, because it's real demand data rather than
guesswork. Look for:

- Queries where you get **impressions but no clicks** → people see you and scroll past.
  Usually a weak title or meta description. Fixable.
- Queries at **position 5–15** → you're on page one or just off it. A small content
  improvement often moves these into the top 3, which is where the clicks are.
- **Queries you didn't expect.** If "gutter cleaning Monroe LA" shows up and you've got
  no page for it, that's a real page worth building. This is how the content roadmap
  should get updated — from data, not from imagination.

**PAGES** — which URLs earn impressions. Tells you whether the service pages are
pulling their weight or whether everything rides on the homepage.

**Filter → Search type: Image** is worth a look occasionally too. Before/after photos
can pull traffic in image search.

### What good looks like over time

| Timeframe | Realistic expectation |
|---|---|
| Weeks 1–3 | Nothing. Possibly not even indexed yet. |
| Month 1–2 | A handful of impressions, mostly brand searches ("precision wash landscape monroe") |
| Month 3–6 | Impressions on real service queries; first clicks; positions 20–50 |
| Month 6–12 | Page-one positions on longer-tail queries like "flowerbed cleanup west monroe" |

Competitive head terms like "pressure washing monroe la" take longer and depend far more
on the **Google Business Profile and review count** than on the website. See
[GOOGLE_BUSINESS_PROFILE.md](GOOGLE_BUSINESS_PROFILE.md) — for a local service business,
that profile drives more calls than the website does.

---

## Step 7 — Link Search Console to the Business Profile

Once both exist, in Search Console go to **Settings → Associations** and link the Google
Business Profile. This surfaces some local performance data in one place.

---

## Bing Webmaster Tools (do this second, it takes 5 minutes)

Bing is maybe 3–6% of US search — small, but it also feeds DuckDuckGo and some AI
assistants, and it's nearly free to set up because **Bing can import everything from
Search Console.**

1. Go to <https://www.bing.com/webmasters> and sign in.
2. Choose **Import from Google Search Console** (offered right on the "add site" screen).
3. Authorise it with the same Google account.
4. Pick `precisionwashlandscape.com` from the imported list.

That copies the verification and the sitemap submission across. No DNS changes needed.

If the import route fails, add the site manually as
`https://precisionwashlandscape.com` and verify with the same DNS TXT method as above
(Bing gives you its own TXT value), then submit `sitemap.xml` under **Sitemaps**.

Worth doing once, then check it maybe twice a year. Bing's **IndexNow** feature can also
ping search engines when pages change — not worth setting up for a 7-page site that
changes rarely.

---

## Quick checklist for Britton

- [ ] Domain un-suspended and HTTPS working (DOMAIN_AND_HOSTING_FIX.md)
- [ ] Search Console **Domain** property created
- [ ] DNS TXT verification record added in Namecheap and verified
- [ ] `sitemap.xml` submitted, shows Success / 7 URLs
- [ ] Homepage inspected + indexing requested
- [ ] 6 service/contact pages inspected + indexing requested
- [ ] Bing Webmaster Tools imported from Search Console
- [ ] Search Console linked to Google Business Profile
- [ ] Calendar reminder: check Performance → Queries monthly
