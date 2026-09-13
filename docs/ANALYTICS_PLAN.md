# Analytics plan

## Current state: no analytics exist

I checked every page. There is **no** Google Analytics, no Google Tag Manager, no Meta
Pixel, no Plausible, Fathom, Hotjar, or Clarity. Zero third-party scripts of any kind.

That's genuinely good for page speed — the homepage loads with exactly one subresource
request — but it means there is currently no way to answer "is the website producing
phone calls?"

**Nothing has been installed.** Installing analytics requires creating an account and
getting a real measurement ID, which needs Britton's Google login. No account IDs have
been invented.

---

## What's already wired and waiting

Every contact link on the site carries a `data-track` attribute, and each page includes
a small listener that fires a GA4 event **only if `gtag` exists**:

```js
document.addEventListener('click', function (e) {
  var a = e.target.closest && e.target.closest('[data-track]');
  if (!a || typeof window.gtag !== 'function') return;   // <- inert until GA is added
  ...
  window.gtag('event', 'contact_click', { method: ..., link_id: ..., page_path: ... });
});
```

Today that listener does nothing at all — no network requests, no cookies, no
performance cost. The moment a GA4 tag is added, conversion tracking starts working with
no further code changes.

Tracked elements:

| `data-track` value | What it is |
|---|---|
| `hero-call-jase` / `hero-call-garrett` | Homepage hero CTA buttons |
| `svc-call` | "Call or Text for a Free Estimate" on each service page |
| `call-jase` / `call-garrett` | Contact cards in the footer contact block |
| `sms-jase` / `sms-garrett` | Text-message links on `/contact/` |
| `contact-call-jase` / `contact-sms-jase` | `/contact/` hero buttons |
| `callbar-call` / `callbar-text` | Sticky mobile bottom bar |
| `facebook` | Facebook link |
| `404-call` | Call link on the 404 page |

---

## Recommendation: Google Analytics 4

For this business GA4 is the right pick, despite being heavier than the alternatives:

- Free, no volume limit at this scale
- Links directly to Search Console and the Google Business Profile, so organic search
  and local-pack traffic show up in one place
- Britton already has a Google account for the other two

A privacy-first alternative (Plausible, ~$9/mo) would be lighter and needs no cookie
banner, but it won't link to Search Console. **If you'd rather skip GA entirely**,
Search Console alone tells you impressions, clicks and queries — which for a 7-page
brochure site is honestly most of what matters. GA adds *what people did after they
arrived*.

---

## Setup — Britton's steps

### 1. Create the GA4 property

1. Go to <https://analytics.google.com> and sign in **with the same Google account
   used for Search Console and the Business Profile**.
2. **Admin** (bottom-left gear) → **Create** → **Property**.
3. Property name: `Precision Wash & Landscape`. Time zone: **United States → Central
   Time**. Currency: US Dollar.
4. Fill in the business details (industry: *Home & Garden* or *Business & Industrial
   Markets*; size: small).
5. Choose **Web** as the platform.
6. Website URL: `https://precisionwashlandscape.com`, stream name:
   `Precision Wash & Landscape`.
7. Leave **Enhanced measurement ON** — it automatically tracks scrolls, outbound clicks
   and file downloads with no extra work.
8. You'll land on a page showing a **Measurement ID** in the form `G-XXXXXXXXXX`.
   **Copy it and send it to me.**

### 2. Send me the ID

That's it for you. Give me the `G-XXXXXXXXXX` string and I'll add the tag to
`tools/build.py` so it lands on all 8 pages consistently, rebuild, and commit.

For reference, here's exactly what gets added to each page's `<head>`:

```html
<script async src="https://www.googletagmanager.com/gtag/js?id=G-XXXXXXXXXX"></script>
<script>
  window.dataLayer = window.dataLayer || [];
  function gtag(){dataLayer.push(arguments);}
  gtag('js', new Date());
  gtag('config', 'G-XXXXXXXXXX');
</script>
```

Note this adds a third-party script and will cost some page-speed score. That's the
trade — measurement isn't free. It's worth it.

### 3. Mark the conversions

Once data is flowing (give it 24–48 hours after the first real visit):

1. GA4 → **Admin → Events**. You should see `contact_click` appearing.
2. Toggle **"Mark as key event"** next to `contact_click`.

Now GA4 counts every phone tap, text tap and Facebook click as a conversion, and you can
see which page produced it.

Also worth marking as key events, from enhanced measurement:
- `click` (outbound) — catches the Facebook link
- `scroll` — weak signal, but tells you if people read the service pages

### 4. Link GA4 to Search Console

GA4 → **Admin → Product links → Search Console links → Link**.

This puts organic query data inside GA4 so you can see *"people searching X landed on
page Y and then tapped the call button."* That's the full picture, and it's the single
most useful report for deciding what content to build next.

### 5. Link GA4 to the Business Profile

There's no direct GA4 ↔ Business Profile link, but Business Profile traffic shows up in
GA4 under **Acquisition → Traffic acquisition** as `google / organic` (or as a referral
from `business.google.com`). If you want it cleanly separated, use the UTM link
discussed in [GOOGLE_BUSINESS_PROFILE.md](GOOGLE_BUSINESS_PROFILE.md) — but read the
caveat there first.

---

## What to actually watch

Once a month, five minutes. Don't build dashboards nobody reads.

| Question | Where |
|---|---|
| **How many people tapped a phone number?** | Reports → Engagement → Events → `contact_click` |
| **Which page produced those taps?** | Same report, add `page_path` as a secondary dimension |
| **Where did visitors come from?** | Reports → Acquisition → Traffic acquisition |
| **What did they search first?** | Reports → Acquisition → **Search Console → Queries** *(needs the link from step 4)* |
| **Phone vs desktop?** | Reports → Tech → Tech details → Device category |
| **Which service page gets read most?** | Reports → Engagement → Pages and screens |

### The one number that matters

**Phone/text taps per month.** Everything else is context.

A realistic pattern for a new local site: near-zero for the first 2–3 months, then a
slow climb as the Business Profile gains reviews and the pages get indexed. If you're
getting 200 visitors a month and 2 phone taps, the problem is the page, not the traffic.
If you're getting 10 visitors and 2 taps, the pages are working fine and you need more
traffic. The ratio tells you which problem you actually have.

---

## Privacy & cookie banner

GA4 sets cookies, which brings GDPR/ePrivacy obligations for EU visitors. For a
pressure-washing business serving two Louisiana parishes, EU traffic is effectively
zero, and there is currently no US federal requirement (Louisiana has no state privacy
law of the kind California has) that forces a consent banner here.

**Recommendation: no cookie banner.** They hurt conversion and aren't required for this
audience. If the business ever starts collecting form submissions rather than just phone
calls, revisit — at that point a short privacy page becomes worthwhile.

If you'd rather avoid the question entirely, Plausible or Fathom are cookieless and need
no banner anywhere.

---

## What is NOT set up, and isn't recommended

| Thing | Why not |
|---|---|
| **Google Tag Manager** | Overkill. One tag on a static 7-page site doesn't need a tag manager. |
| **Call tracking numbers** | Services like CallRail swap the displayed phone number per visitor to attribute calls. Genuinely useful at higher volume, but a dynamic number **breaks NAP consistency**, which matters more than attribution for a business with zero reviews. Revisit at 20+ calls/month. |
| **Meta Pixel** | Only worth it if you start running paid Facebook ads. |
| **Heatmaps (Hotjar/Clarity)** | Microsoft Clarity is free and shows session recordings. Interesting, but there isn't enough traffic yet for the recordings to mean anything. Maybe at 500 visits/month. |
| **Conversion forms** | The site deliberately has no form — a static GitHub Pages site can't process one without a third-party service, and for this trade "call or text a photo" converts better anyway. If a form is ever wanted, Formspree's free tier is the path of least resistance. |

---

## Checklist

- [ ] GA4 property created *(Britton)*
- [ ] Measurement ID `G-XXXXXXXXXX` sent to me *(Britton)*
- [ ] Tag added to `tools/build.py`, site rebuilt and committed *(me)*
- [ ] Real-time report confirms a hit *(Britton — just load the site on your phone)*
- [ ] `contact_click` marked as a key event *(Britton, after 24–48h)*
- [ ] GA4 ↔ Search Console linked *(Britton)*
- [ ] Monthly reminder set to check phone taps *(Britton)*
