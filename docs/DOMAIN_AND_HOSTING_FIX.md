# Domain & hosting status

**Last verified: 2026-09-13**

## Where things stand

| | Status |
|---|---|
| WHOIS registrant verification | ✅ **Done** — suspension lifted 2026-09-13 03:17 UTC |
| Nameservers | ✅ Back to `DNS1/DNS2.REGISTRAR-SERVERS.COM` |
| Apex DNS (`precisionwashlandscape.com`) | ✅ Resolves to all four GitHub Pages IPs |
| `www` DNS | ✅ CNAME → `brittonleggett.github.io` |
| Site over HTTP | ✅ **Live.** All 7 pages, robots.txt, sitemap.xml, CSS and images serving 200 from `Server: GitHub.com` |
| Custom 404 | ✅ Returns a real 404 status with the branded page |
| **Site over HTTPS** | ❌ **Not working — one action left, see below** |

The site is live. The last remaining task is the TLS certificate.

---

## ⚠️ The one thing left: HTTPS

### What's wrong

`https://precisionwashlandscape.com` currently serves a certificate for `*.github.io`,
which doesn't match the domain — so browsers show a full-page security warning.

The GitHub Pages API confirms no certificate has been requested at all:

```
https_enforced   : False
https_certificate: (no cert object)
```

### Why

GitHub only requests a Let's Encrypt certificate after its DNS check passes. The last
time GitHub checked, the domain was still suspended and pointed at Namecheap's
placeholder nameservers — so it never queued one. DNS is correct now, but GitHub
doesn't automatically go back and retry.

Re-saving the custom domain through the API (`PUT /repos/.../pages` with the same
cname) was tried and **did not** trigger it. The removal/re-add cycle in the web UI is
what actually works.

### Fix it — 30 seconds, Britton only

1. Go to <https://github.com/brittonleggett/precision-wash-landscape/settings/pages>
2. Under **Custom domain**, you'll see `precisionwashlandscape.com`.
   **Clear the field completely** and click **Save**.
   *(The site briefly falls back to the `github.io` address. This is expected.)*
3. Type `precisionwashlandscape.com` back in and click **Save** again.
4. A **"DNS check in progress"** message appears, then a green
   **"DNS check successful"**. DNS is already correct, so this should pass immediately.
5. Below it, **"TLS certificate being provisioned"** appears. **Wait.** Usually 5–20
   minutes, occasionally up to an hour.
6. Refresh the page. When the **Enforce HTTPS** checkbox is no longer greyed out,
   **tick it.**

Tell me once you've ticked Enforce HTTPS and I'll re-verify every URL over `https://`.

### Why this matters and isn't optional

- Browsers show a scary interstitial on a cert mismatch. Most people will not click
  through it, so right now every `https://` visitor bounces.
- Google treats `http://` and `https://` as separate sites. Without Enforce HTTPS you
  risk both being indexed as duplicates.
- Every canonical tag on the site already says `https://`. Until the cert exists, those
  point at a URL that errors.
- HTTPS is a (light) ranking signal, and a hard trust requirement for a business asking
  strangers to let them onto their property.

**Don't start Search Console until this is done** — you want Google's first crawl to
find the `https://` version.

---

## Verified live (HTTP), 2026-09-13

```
/                        200  33823B   text/html
/pressure-washing/       200  27205B   text/html
/landscaping/            200  22947B   text/html
/junk-removal/           200  16404B   text/html
/window-washing/         200  14552B   text/html
/service-area/           200  13788B   text/html
/contact/                200  10781B   text/html
/robots.txt              200    310B   text/plain
/sitemap.xml             200   1364B   application/xml
/assets/site.css         200  24972B   text/css
/images/*.webp           200           image/webp
/this-does-not-exist/    404   6740B   (branded 404 page)
/docs/, /tools/, /README.md       404  (correctly excluded from the build)
```

All byte sizes match the local build exactly.

---

## Current DNS (correct — don't change)

| Type | Host | Value |
|---|---|---|
| A | `@` | `185.199.108.153` |
| A | `@` | `185.199.109.153` |
| A | `@` | `185.199.110.153` |
| A | `@` | `185.199.111.153` |
| CNAME | `www` | `brittonleggett.github.io.` |

Optional, not required — IPv6 support:

| Type | Host | Value |
|---|---|---|
| AAAA | `@` | `2606:50c0:8000::153` |
| AAAA | `@` | `2606:50c0:8001::153` |
| AAAA | `@` | `2606:50c0:8002::153` |
| AAAA | `@` | `2606:50c0:8003::153` |

**When you next open Advanced DNS**, add the Google Search Console TXT record at the
same time — see [GOOGLE_SEARCH_CONSOLE_SETUP.md](GOOGLE_SEARCH_CONSOLE_SETUP.md).

---

## Don't let this happen again

The domain was dark for **15 days** (2026-08-29 → 2026-09-13) because an ICANN
verification email went unclicked.

- ☐ **Turn on auto-renew** in Namecheap. The domain expires **2027-08-14**.
- ☐ Check the card on file doesn't expire before then.
- ☐ Keep the WHOIS registrant email one you actually read — changing it re-triggers
  verification, and the 15-day clock starts again.
- ☐ Set a calendar reminder for **July 2027** to confirm the renewal.

A lapsed domain forfeits every bit of SEO value built up in the meantime, and
recovering one after expiry can get expensive.
