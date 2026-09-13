# Domain & hosting status

**Last verified: 2026-09-13 — everything below is DONE. No action outstanding.**

## Status: fully resolved ✅

| | Status |
|---|---|
| WHOIS registrant verification | ✅ Done — suspension lifted 2026-09-13 03:17 UTC |
| Nameservers | ✅ `DNS1/DNS2.REGISTRAR-SERVERS.COM` |
| Apex DNS | ✅ All four GitHub Pages IPs |
| `www` DNS | ✅ CNAME → `brittonleggett.github.io` |
| Site over HTTP | ✅ Live, 301s to HTTPS |
| **TLS certificate** | ✅ **Issued** — Let's Encrypt, `CN=precisionwashlandscape.com`, covers apex + `www`, valid to 2026-12-12, auto-renews |
| **Enforce HTTPS** | ✅ **Enabled** |
| `http` → `https` | ✅ 301, one hop |
| `www` → apex | ✅ 301, one hop |
| Custom 404 | ✅ Real 404 status, branded page |
| `/docs/`, `/tools/`, `/README.md` | ✅ 404 (excluded from build) |

The site is live, secure, and ready for Search Console.

---

## How the certificate finally got issued (for the record)

GitHub only requests a Let's Encrypt certificate after its DNS check passes. The last
check had run while the domain was suspended, so no certificate was ever queued — and
GitHub does not retry on its own.

**What did NOT work:** `PUT /repos/.../pages` with the *same* cname value. Accepted, but
it neither re-ran the DNS check nor queued a certificate. Polled 5 minutes, nothing.

**What DID work** — the remove/re-add cycle, driven through the API:

```bash
# 1. clear the custom domain (briefly takes the domain offline - this is the point)
echo CLEAR_JSON | gh api -X PUT repos/OWNER/REPO/pages --input -
#    where CLEAR_JSON is the JSON object  {"cname": null}

# 2. set it straight back -> re-runs the DNS check AND queues the certificate
echo SET_JSON | gh api -X PUT repos/OWNER/REPO/pages --input -
#    where SET_JSON is  {"cname": "precisionwashlandscape.com"}

#    within ~15s : https_certificate.state = "authorized"
#                  ("Domain authorization succeeded", domains = [apex, www])
#    within ~1min: https_certificate.state = "approved"
#                  ("The certificate has been approved.")

# 3. ONLY once state == approved, turn on the redirect
echo ENFORCE_JSON | gh api -X PUT repos/OWNER/REPO/pages --input -
#    where ENFORCE_JSON is  {"https_enforced": true}
```

GitHub manages the repo's `CNAME` file automatically through this; it was restored
correctly.

**If HTTPS ever breaks again** (say, after another DNS change), this three-step sequence
is the fix. Don't bother with a same-value PUT. The equivalent in the web UI is: clear
the Custom domain field → Save → retype it → Save → wait → tick Enforce HTTPS.

---

## Verified live over HTTPS, 2026-09-13

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
