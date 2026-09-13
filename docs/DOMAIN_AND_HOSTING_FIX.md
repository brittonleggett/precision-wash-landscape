# READ THIS FIRST — the website is currently offline

**Status as of 2026-09-12: `precisionwashlandscape.com` does not load for anyone.**

Everything else in this folder is ready to go. None of it can work until this is fixed,
because Google cannot index a site it cannot reach. **This is the #1 priority and only
Britton can do it** — it requires logging into Namecheap.

---

## What is wrong

The domain's nameservers have been switched by Namecheap to these:

```
FAILED-WHOIS-VERIFICATION.NAMECHEAP.COM
VERIFY-CONTACT-DETAILS.NAMECHEAP.COM
```

That is Namecheap's automated penalty for an unverified registrant email address.

ICANN requires every new domain registration to have its contact email verified within
15 days. Namecheap sent a verification email when the domain was registered on
**2026-08-14**. It was never clicked. On **2026-08-29** Namecheap suspended the domain
by pointing it at those placeholder nameservers.

### What that means in practice

| What you'd expect | What actually happens |
|---|---|
| `https://precisionwashlandscape.com` | Connection fails — no HTTPS at all |
| `http://precisionwashlandscape.com` | Namecheap "verify your WHOIS contact information" holding page |
| `https://brittonleggett.github.io/precision-wash-landscape/` | Redirects (301) to the dead domain, so it fails too |

The GitHub Pages `CNAME` file tells GitHub to redirect the `github.io` address to the
custom domain — so while the domain is suspended, **there is no working address for the
site at all.** The site itself is fine; it's the front door that's locked.

### How this was confirmed

Registry (RDAP) lookup on 2026-09-12:

```
STATUS:      ['client transfer prohibited']
registration 2026-08-14
last changed 2026-08-29      <- the day it was suspended
NS:          FAILED-WHOIS-VERIFICATION.NAMECHEAP.COM,
             VERIFY-CONTACT-DETAILS.NAMECHEAP.COM
REGISTRAR:   NameCheap, Inc.
```

---

## Fix it — Britton's steps

### Step 1 — Verify the registrant email (5 minutes)

1. Search your email (**including spam/junk**) for a message from Namecheap with a
   subject close to *"Verify your email address"* or *"IMPORTANT: Verify your WHOIS
   contact information"*, sent around **2026-08-14**.
2. Click the verification link in it.
3. **If you can't find it or the link has expired** — it does expire — log in at
   <https://www.namecheap.com> and go to **Domain List → precisionwashlandscape.com →
   Manage**. There will be a red banner about contact verification with a
   **"Resend verification email"** or similar button. Click it, then click the link in
   the new email.
4. If neither works, open a Namecheap support chat and tell them: *"My domain is on
   FAILED-WHOIS-VERIFICATION nameservers and I need to complete registrant contact
   verification."* They resolve this routinely.

Verification usually restores the domain within an hour or two.

### Step 2 — Point DNS at GitHub Pages

Once the suspension is lifted, the nameservers go back to Namecheap's normal ones
(`dns1.registrar-servers.com` / `dns2.registrar-servers.com`). Then set the DNS records.

In Namecheap: **Domain List → precisionwashlandscape.com → Manage → Advanced DNS**.

Delete any existing parking/redirect records (Namecheap usually leaves a `CNAME` for
`www` pointing at `parkingpage.namecheap.com`, and an `URL Redirect Record`). Then add:

| Type | Host | Value | TTL |
|---|---|---|---|
| A Record | `@` | `185.199.108.153` | Automatic |
| A Record | `@` | `185.199.109.153` | Automatic |
| A Record | `@` | `185.199.110.153` | Automatic |
| A Record | `@` | `185.199.111.153` | Automatic |
| CNAME Record | `www` | `brittonleggett.github.io.` | Automatic |

*(Those four IPs were verified on 2026-09-12 to resolve to `cdn-*.github.com`, and
`brittonleggett.github.io` itself resolves to exactly that set. They are GitHub's
standard, long-stable Pages addresses. If you want to double-check, GitHub's current
list is at
<https://docs.github.com/pages/configuring-a-custom-domain-for-your-github-pages-site/managing-a-custom-domain-for-your-github-pages-site>.)*

Optionally also add the IPv6 records (nice to have, not required):

| Type | Host | Value |
|---|---|---|
| AAAA | `@` | `2606:50c0:8000::153` |
| AAAA | `@` | `2606:50c0:8001::153` |
| AAAA | `@` | `2606:50c0:8002::153` |
| AAAA | `@` | `2606:50c0:8003::153` |

DNS changes take anywhere from a few minutes to a few hours to spread.

### Step 3 — Re-save the custom domain on GitHub and turn on HTTPS

1. Go to <https://github.com/brittonleggett/precision-wash-landscape/settings/pages>.
2. Under **Custom domain**, if `precisionwashlandscape.com` is already there, clear it,
   click Save, re-type it, and Save again. This forces GitHub to re-run its DNS check
   and request a fresh TLS certificate.
3. Wait for the green *"DNS check successful"*.
4. Certificate issuing takes up to ~30 minutes. When the **Enforce HTTPS** checkbox
   stops being greyed out, **tick it.**

**Do not skip Enforce HTTPS.** Google treats `http://` and `https://` as different
sites, and an unencrypted site is both a ranking negative and a trust problem for
customers. This checkbox is what makes `http://` permanently 301-redirect to `https://`
and collapses them into one site.

### Step 4 — Confirm it worked

Visit all of these. Every one should land on the live site over `https://` with a padlock:

- `https://precisionwashlandscape.com`
- `https://www.precisionwashlandscape.com`
- `http://precisionwashlandscape.com` (should auto-redirect to https)
- `https://precisionwashlandscape.com/pressure-washing/`
- `https://precisionwashlandscape.com/robots.txt`
- `https://precisionwashlandscape.com/sitemap.xml`

**Only after all six work** should you start
[docs/GOOGLE_SEARCH_CONSOLE_SETUP.md](GOOGLE_SEARCH_CONSOLE_SETUP.md). Verifying a
domain in Search Console while it's suspended will just fail.

---

## Stop this happening again

- **Renewal.** The domain expires **2027-08-14**. Turn on auto-renew in Namecheap and
  make sure the card on file doesn't expire before then. A lapsed domain loses all
  accumulated SEO value, and recovering one after expiry can be expensive.
- **Registrant email.** Keep the WHOIS contact email an address you actually read.
  Namecheap re-sends verification any time you change it.
- **Set a calendar reminder** for July 2027 to confirm the renewal went through.

---

## Optional: get the site visible again *today*, before DNS is fixed

If you want something to show people while you wait on Namecheap, you can temporarily
un-hook the custom domain so the `github.io` address serves the site directly:

1. Delete the `CNAME` file from the repository root.
2. On <https://github.com/brittonleggett/precision-wash-landscape/settings/pages>,
   clear the **Custom domain** field and Save.
3. The site becomes live at
   `https://brittonleggett.github.io/precision-wash-landscape/`.

**Two warnings before you do this.** First, every internal link and the canonical tags
on the site are absolute paths (`/pressure-washing/`), which break under the
`/precision-wash-landscape/` subpath — the pages would load but navigation between them
would 404. Second, if Google indexes the `github.io` URLs you create a duplicate-content
problem you'd have to clean up later.

**Recommendation: don't.** Fixing the WHOIS verification takes five minutes and solves
it properly. This is listed only so you know the option exists.
