# Google Business Profile — setup, NAP consistency, and reviews

**Status: NOT CREATED.** This is the highest-value marketing action available to this
business, and it's higher-value than the website itself.

For a service-area home-services business, most customers never reach the website. They
search "pressure washing near me" on a phone, see the three-result **local pack** with a
map, and tap a phone number. If you're not in that pack, the website is a brochure
nobody finds.

**Only Britton (or whoever holds the phone) can do this** — Google verifies by calling
or texting the business number.

> This supersedes `google_business_profile_setup.txt` in the repo root, which was mostly
> correct but listed five photo filenames that no longer exist.

---

## Part 1 — Create the profile

Go to <https://business.google.com> → **Manage now**. Sign in with the Google account
you want to own this permanently — **the same one you'll use for Search Console.**

### Business name

```
Precision Wash & Landscape
```

Type it exactly. Do **not** add keywords — "Precision Wash & Landscape | Pressure
Washing Monroe LA" violates Google's naming guidelines and is a common cause of
suspension. The name field is not a ranking hack.

### Business type

Choose **Service area business** — *"I deliver goods and services to my customers"* —
not a storefront. You go to them.

This hides the home address publicly (Google still asks for one to confirm you're real;
it just isn't displayed) and shows your service area instead.

### Primary category

```
Pressure washing service
```

**The primary category is the single most important ranking field in the entire
profile.** Pressure washing is the biggest service and the most-searched term, so it
gets the primary slot.

### Additional categories

Add all that genuinely apply:

- `Landscaper`
- `Gutter cleaning service`
- `Window cleaning service`
- `Junk removal service`
- `Garden maintenance service`

Don't pad this list with categories you can't service — every category you add is a
category you can get calls for.

### Service area

Add these one at a time when prompted:

- Monroe, LA
- West Monroe, LA
- Ruston, LA
- Ouachita Parish, LA
- Lincoln Parish, LA

Google caps service areas at 20 and recommends keeping them within about a 2-hour drive.
Five is fine — resist the urge to add every town in north Louisiana. A tight, honest
area ranks better than a sprawling one.

### Phone

```
318-805-8288
```

Jase's number. Google takes one primary number, and **whoever owns this phone must be
the person doing the verification**, because the code arrives by call or text.

Garrett's number (318-614-8665) is on the website and can go in the description. Don't
put it in the secondary-phone field unless you want it ringing from Google searches too.

### Website

```
https://precisionwashlandscape.com
```

**Wait until the domain is actually working** before entering this — see
[DOMAIN_AND_HOSTING_FIX.md](DOMAIN_AND_HOSTING_FIX.md). A profile pointing at a dead
site is worse than one with no website link.

Optionally add UTM tracking so you can tell in analytics which visits came from the
Profile:

```
https://precisionwashlandscape.com/?utm_source=google&utm_medium=organic&utm_campaign=gbp
```

**Recommendation: use the plain URL.** UTM parameters on a Business Profile are a mixed
bag — they can create duplicate-looking URLs, and Google Analytics already reports
Business Profile traffic reasonably well without them. Only add UTMs if you've set up
analytics and actively want that split. If you do use one, use it on the main website
link only, not on the appointment link.

### Business description (750 character limit)

Ready to paste — 727 characters:

```
Precision Wash & Landscape is a family-run, owner-operated exterior cleaning and
flowerbed service covering Ouachita and Lincoln Parish, Louisiana, including Monroe,
West Monroe and Ruston. We soft wash house siding and roofs, pressure wash driveways,
patios, walkways, gutters and fences, and clean out flowerbeds with fresh pine straw
or mulch, weeding, trimming and planting. We also haul off tree limbs, storm debris,
old furniture and garage clutter, and hand-wash exterior windows, frames and sills.
Most jobs need nothing from you but an outdoor spigot and an outlet. Free estimates on
every job, with a price agreed before any work starts. Call or text Jase at
318-805-8288 or Garrett at 318-614-8665.
```

Note the description leads with what and where, not with adjectives. Google doesn't use
the description for ranking, but customers read it.

### Services

Google lets you list services individually with short descriptions. Add these four —
they mirror the website exactly, which is what you want:

**1. Soft & pressure washing**
> House siding, roofs, driveways, patios, sidewalks, gutters, fences and brick. Soft
> washing on delicate surfaces, higher pressure on concrete and stone.

**2. Flowerbed & landscape cleanup**
> Weeding and spraying, fresh pine straw or mulch, bush and shrub trimming, planting
> and plant removal. We haul off everything we pull.

**3. Junk removal & hauling**
> Tree limbs, storm debris, yard waste, old furniture and garage or shed cleanouts.
> We load it from wherever it sits — no need to drag it to the curb.

**4. Window washing**
> Hand-washed exterior glass, frames and sills. Screens pulled and rinsed on request.

### Hours

**Don't guess.** Confirm with Jase and Garrett what they actually answer the phone.

A common setting for this kind of business:

```
Monday–Friday   8:00 AM – 6:00 PM
Saturday        8:00 AM – 4:00 PM
Sunday          Closed
```

Hours matter mainly for call expectations, and Google shows "Open now" / "Closed" in the
local pack — wrong hours cost you calls. Once confirmed, tell me and I'll add matching
`openingHours` to the website's structured data. **Right now the site deliberately has
no hours in its schema, because inventing them would create an inconsistency.**

### Photos

Upload from `Precision_Wash_Landscape_Site/images/`. These files all exist and are
verified present:

| Role | File |
|---|---|
| **Cover / main photo** | `front-entry.jpg` — strongest single shot |
| Pressure washing | `siding-after.jpg`, `walkway-after.jpg`, `patio-after.jpg`, `stairway-after.jpg` |
| Flowerbed work | `flowerbed-pinestraw-after.jpg`, `flowerbed-roses-after.jpg` |
| Before/after pairs | upload the matching `*-before.jpg` too — Google shows them chronologically and the contrast sells the work |

Upload the `.jpg` files, not the `.webp` ones. Google's uploader prefers JPEG, and the
WebP versions exist purely for website speed.

**Photos matter more than almost anything else in the profile.** Profiles with regular
new photos get noticeably more calls. Have Jase or Garrett take a phone photo on every
single job — it costs nothing and it's the raw material for the profile, the website
gallery, and eventually city-specific pages.

---

## Part 2 — Verification

Google will offer one or more of: text message, phone call, email, video, or postcard.
Take the text or call if offered — it's instant. Video verification is increasingly
common for service-area businesses; if you get it, they'll ask you to film your
equipment, your vehicle and yourself. Have the pressure washer and truck handy.

**Until verified, the profile does not appear in search at all.**

---

## Part 3 — NAP consistency

**NAP** = Name, Address, Phone. Google cross-references these across the web to decide
whether you're a real, single, consistent business. Inconsistency dilutes local ranking.

### The canonical values — use these exactly, everywhere

| Field | Value |
|---|---|
| **Name** | `Precision Wash & Landscape` |
| **Address** | *(none published — service-area business)* |
| **Service area** | Ouachita Parish & Lincoln Parish, Louisiana — Monroe, West Monroe, Ruston |
| **Phone** | `318-805-8288` |
| **Website** | `https://precisionwashlandscape.com` |
| **Facebook** | `https://www.facebook.com/profile.php?id=61590393561873` |

Consistency rules:
- Always `Precision Wash & Landscape` — never "Precision Wash and Landscape",
  never "Precision Wash & Landscaping", never all-caps.
- Always `318-805-8288` with hyphens as the primary. Not `(318) 805-8288`, not
  `3188058288`.
- Always the `https://` version of the website, apex domain, no `www`.

**On-site status: ✅ consistent.** All 8 pages generate their name and phone from a
single source in `tools/build.py`, so they physically cannot drift.

### Checklist — audit these, don't change anything you don't own

| Platform | Name ✓ | Phone ✓ | Website ✓ | Done |
|---|---|---|---|---|
| Website | ✅ verified | ✅ verified | ✅ verified | ☑ |
| Google Business Profile | | | | ☐ |
| Facebook page | | | | ☐ |
| Instagram bio *(if one exists)* | | | | ☐ |
| Nextdoor business page | | | | ☐ |
| Bing Places | | | | ☐ |
| Apple Business Connect | | | | ☐ |
| Yelp *(claim it — a listing may already exist)* | | | | ☐ |
| Chamber of Commerce directory | | | | ☐ |
| Any truck/yard-sign/flyer phone number | | | | ☐ |

**Do not edit any account you don't control.** If you find an incorrect third-party
listing, use that platform's "suggest an edit" or "claim this business" flow.

Worth doing once: search Google for `"318-805-8288"` in quotes. Anything that comes back
is a listing carrying your phone number, and each one should match the table above.

---

## Part 4 — Getting reviews, ethically

Reviews are the most powerful local ranking factor you control, and the biggest
conversion lever. Going from 0 to 5 reviews moves the needle more than any change to the
website.

### Hard rules — breaking any of these risks the whole profile

- ❌ **Never buy reviews.** Google detects purchased review patterns and removes profiles.
- ❌ **Never write reviews yourself**, or have family who weren't customers write them.
- ❌ **Never offer discounts, entries, or anything of value for a review.** This is
  explicitly against Google's policy — even "leave us a review for $10 off" is a
  violation. You may not incentivise reviews at all.
- ❌ **Never review-gate** — don't screen for happy customers and only ask those. Asking
  a filtering question first ("were you satisfied?") and routing only the yeses to
  Google is a policy violation.
- ✅ **Ask every customer, the same way.** That's the whole rule.

### Get the review link

Once the profile is verified: Business Profile → **Ask for reviews**. Google generates a
short link like `https://g.page/r/XXXXXXXXXXXX/review` that opens the review box
directly. Copy it and save it in your phone.

### The workflow

```
Job finished
   ↓
Walk the property with the customer (or text them the after photos)
   ↓
Same day, or next morning at the latest — send one text
   ↓
If nothing after ~5 days: one polite follow-up. Then stop.
```

Same-day matters. Ask while they're looking at a clean driveway, not two weeks later.

### Text template — after the job

> Hey [Name], thanks again for having us out today. It was good to work with you.
>
> If you were happy with how it turned out, would you mind leaving us a quick Google
> review? We're a small family operation and it genuinely helps people find us.
>
> [review link]
>
> Either way, give us a shout any time. — Jase, Precision Wash & Landscape

### One follow-up, if there's no response

> Hey [Name], no worries if you've been busy — just wanted to put this in one place in
> case you still wanted to leave that review. Thanks again!
>
> [review link]

**One follow-up. Then let it go.** Pestering costs you a repeat customer for the sake of
a review.

### Where to start

**Cindy Young** already commented positively on Facebook ("Looks clean and fresh, love
the pine straw addition!"). She's the obvious first ask — someone who has already
volunteered that she's happy.

Then work backwards through recent jobs. Realistic target: **5 reviews in the first
month, 15+ by month six.**

### Replying to reviews

Reply to every one, positive or negative. Google states that responding to reviews
improves local visibility, and it's visible to everyone reading.

**Positive** — short and specific, and mention the service naturally:
> Thanks Cindy! The pine straw really did finish that bed off. Glad you're happy with
> it — call us any time.

**Negative** — never argue publicly. Acknowledge, take it offline, follow up:
> I'm sorry we missed the mark here, [Name]. That's not how we want to leave a job.
> Please give me a call at 318-805-8288 and let's make it right. — Jase

A single negative review among good ones isn't damaging. A defensive owner reply is.

---

## Part 5 — Keeping the profile active

Google rewards profiles that show activity. Small, consistent effort beats bursts.

| Cadence | Action |
|---|---|
| **Every job** | Take a before and after photo on the phone. Takes 10 seconds. |
| **Weekly** | Upload 2–3 of those photos to the profile |
| **Every 2 weeks** | Post an update — a recent job, a seasonal note ("pollen season is here"), a reminder that estimates are free |
| **Same day** | Reply to any new review or question |
| **Monthly** | Check the **Performance** tab: calls, direction requests, website clicks, and the search terms people used to find you |
| **Seasonally** | Update hours around holidays if they change |

That Performance tab is genuinely useful — it shows the actual phrases people searched
before tapping your profile, which is the same kind of demand data Search Console gives
you for the website, and it usually arrives sooner.

---

## What Britton must do manually — summary

Everything on this page. None of it can be automated, and none of it has been done:

1. ☐ Create the profile at business.google.com *(~30 min)*
2. ☐ Complete phone/video verification
3. ☐ Confirm real business hours with Garrett, then tell me so I can add them to schema
4. ☐ Upload 8–10 photos from `images/`
5. ☐ Paste in the description and the four services
6. ☐ Add the website URL *(only once the domain works)*
7. ☐ Get the review link and save it in your phone
8. ☐ Ask Cindy Young and 3–4 other recent customers for reviews
9. ☐ Work through the NAP checklist
10. ☐ Set a recurring reminder to post photos every couple of weeks
