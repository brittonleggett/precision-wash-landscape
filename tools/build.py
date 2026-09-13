#!/usr/bin/env python3
"""
Precision Wash & Landscape — static site builder.

The site is plain HTML served straight off GitHub Pages. This script exists so the
header, nav, footer, metadata and JSON-LD stay identical on every page. Edit the
content here, run `python tools/build.py`, and commit the regenerated HTML.

    python tools/build.py

EVERY .html file in this repo is generated. Do not hand-edit them.
"""

import io
import os
import re
from datetime import date

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SITE = "https://precisionwashlandscape.com"
TODAY = date.today().isoformat()

# --------------------------------------------------------------------------
# Verified business facts. Nothing here may be invented — every value below is
# sourced from the existing site copy or google_business_profile_setup.txt.
# --------------------------------------------------------------------------
BIZ = {
    "name": "Precision Wash & Landscape",
    # Spelling per Jase's own Facebook bio, which writes "Jase LaBorde" (capital B)
    # twice. The site previously said "Laborde".
    "jase_name": "Jase LaBorde",
    "jase_tel": "3188058288",
    "jase_display": "318-805-8288",
    "garrett_name": "Garrett Smith",
    "garrett_tel": "3186148665",
    "garrett_display": "318-614-8665",
    "facebook": "https://www.facebook.com/profile.php?id=61590393561873",
}

NAV = [
    ("/", "Home"),
    ("/pressure-washing/", "Pressure Washing"),
    ("/landscaping/", "Lawns & Beds"),
    ("/junk-removal/", "Junk Removal"),
    ("/window-washing/", "Windows"),
    ("/service-area/", "Service Area"),
    ("/contact/", "Free Estimate"),
]

# Each service owns a colour. Blue washes, green grows, amber hauls, teal is glass.
# The page sets data-accent and every component repaints itself.
ACCENT = {
    "/pressure-washing/": "wash",
    "/landscaping/": "leaf",
    "/junk-removal/": "amber",
    "/window-washing/": "glass",
}

SERVICE_CARDS = {
    "/pressure-washing/": (
        "Soft &amp; pressure washing",
        "House washing, driveways, patios, sidewalks, gutters, fences &mdash; any concrete or exterior surface.",
    ),
    "/landscaping/": (
        "Flowerbeds, sod &amp; trimming",
        "Weeding, mulch and pine straw, bush trimming, planting, plant removal &mdash; and laying new sod.",
    ),
    "/junk-removal/": (
        "Junk removal &amp; hauling",
        "Tree limbs, trash, old furniture, and anything else that needs to leave your property.",
    ),
    "/window-washing/": (
        "Window washing",
        "Hand-washed frames, sills, and exterior glass &mdash; streak-free, done with care.",
    ),
}

# Real customer words. Cathy's is a Facebook recommendation on the business page;
# Cindy's is a Facebook comment. Nothing here is paraphrased or invented, and there
# is deliberately no star rating or review schema attached to them.
REVIEWS = [
    ("Jase come to our house to clean up our flower beds, trim bushes, and wash the "
     "exterior of our house. He came early, worked through the rain, and did an "
     "excellent job!", "Cathy Salsbury", "Recommended us on Facebook"),
    ("Looks clean and fresh, love the pine straw addition!",
     "Cindy Young", "On Facebook"),
]

ICONS = {
    "/pressure-washing/": '<path d="M4 20c2-8 6-9 8-16 2 7 6 8 8 16" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" fill="none"/><path d="M12 4v9" stroke="currentColor" stroke-width="1.6" stroke-linecap="round"/>',
    "/landscaping/": '<path d="M12 21c4-2 6-5.5 6-9a6 6 0 0 0-12 0c0 3.5 2 7 6 9Z" stroke="currentColor" stroke-width="1.6" fill="none"/><path d="M12 12v9" stroke="currentColor" stroke-width="1.6"/>',
    "/junk-removal/": '<path d="M5 7h14M9 7V5a1 1 0 0 1 1-1h4a1 1 0 0 1 1 1v2m-8 0 1 13a1 1 0 0 0 1 1h6a1 1 0 0 0 1-1l1-13" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round" fill="none"/>',
    "/window-washing/": '<rect x="4" y="4" width="16" height="16" rx="1.5" stroke="currentColor" stroke-width="1.6"/><path d="M12 4v16M4 12h16" stroke="currentColor" stroke-width="1.6"/>',
}

FAVICON = ("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 26 26'%3E"
           "%3Cpath d='M13 2C13 2 6 11 6 16.2C6 20.2 9.13 23 13 23C16.87 23 20 20.2 20 16.2C20 11 13 2 13 2Z' "
           "fill='%230a0d12' stroke='%232f80ff' stroke-width='1.8'/%3E%3C/svg%3E")


# --------------------------------------------------------------------------
# Shared chrome
# --------------------------------------------------------------------------
def depth_prefix(path):
    """Relative prefix back to site root for a page at `path`."""
    return "../" * (path.strip("/").count("/") + 1) if path != "/" else ""


def topbar(path):
    pre = depth_prefix(path)
    links = []
    for href, label in NAV:
        current = ' aria-current="page"' if href == path else ""
        links.append('<a href="%s"%s>%s</a>' % (href, current, label))
    return '''  <header class="topbar">
    <div class="wrap">
      <div class="brandmark">
        <a href="/" aria-label="Precision Wash &amp; Landscape home">
          <svg width="26" height="26" viewBox="0 0 26 26" fill="none" aria-hidden="true">
            <path d="M13 2C13 2 6 11 6 16.2C6 20.2 9.13 23 13 23C16.87 23 20 20.2 20 16.2C20 11 13 2 13 2Z" fill="none" stroke="#7fc0ff" stroke-width="1.6"/>
          </svg>
          <span>Precision<br><small>Wash &amp; Landscape</small></span>
        </a>
      </div>
      <nav class="site-nav" aria-label="Primary">
        %s
        <a class="nav-call" href="tel:1%s">%s</a>
      </nav>
    </div>
  </header>
''' % ("\n        ".join(links), BIZ["jase_tel"], BIZ["jase_display"])


def breadcrumbs(trail):
    """trail: list of (href, label); last item is the current page."""
    if not trail:
        return ""
    items = []
    for i, (href, label) in enumerate(trail):
        if i == len(trail) - 1:
            items.append("<li><span>%s</span></li>" % label)
        else:
            items.append('<li><a href="%s">%s</a></li>' % (href, label))
    return '''  <nav class="breadcrumbs" aria-label="Breadcrumb">
    <div class="wrap">
      <ol>
        %s
      </ol>
    </div>
  </nav>
''' % ("\n        ".join(items))


def contact_section(heading="Call, text, or find us on Facebook",
                    eyebrow="Get a free estimate", intro=None):
    intro_html = '\n      <p class="lede" style="margin-top:0.75rem;">%s</p>' % intro if intro else ""
    return '''  <section class="contact-section" id="contact">
    <div class="wrap">
      <p class="eyebrow">%s</p>
      <h2 class="section-title">%s</h2>%s
      <div class="contact-grid">
        <a class="contact-card" href="tel:1%s" data-track="call-jase">
          <span class="role">Owner &middot; call or text</span>
          <span class="name">%s</span>
          <span class="num">%s</span>
        </a>
        <a class="contact-card" href="tel:1%s" data-track="call-garrett">
          <span class="role">Owner &middot; call or text</span>
          <span class="name">%s</span>
          <span class="num">%s</span>
        </a>
        <a class="contact-card" href="%s" target="_blank" rel="noopener noreferrer" data-track="facebook">
          <span class="role">Follow us</span>
          <span class="name">Facebook</span>
          <span class="num">Precision Wash &amp; Landscape</span>
        </a>
      </div>
    </div>
  </section>
''' % (eyebrow, heading, intro_html,
       BIZ["jase_tel"], BIZ["jase_name"], BIZ["jase_display"],
       BIZ["garrett_tel"], BIZ["garrett_name"], BIZ["garrett_display"],
       BIZ["facebook"])


def footer():
    links = "\n        ".join(
        '<a href="%s">%s</a>' % (h, l) for h, l in NAV if h != "/"
    )
    return '''  <footer>
    <div class="wrap">
      <nav class="footer-nav" aria-label="Footer">
        <a href="/">Home</a>
        %s
      </nav>
      <div class="footer-legal">
        <span>Precision Wash &amp; Landscape &mdash; pressure washing, flowerbed care, junk removal and window washing in Ouachita &amp; Lincoln Parish, Louisiana. Call or text %s.</span>
        <span class="verse">&ldquo;Whatever you do, work at it with all your heart&rdquo; &mdash; Colossians 3:23</span>
      </div>
    </div>
  </footer>
''' % (links, BIZ["jase_display"])


CALLBAR = '''<div class="callbar" aria-label="Contact Precision Wash &amp; Landscape">
  <a class="call" href="tel:1%s" data-track="callbar-call">Call %s</a>
  <a class="text" href="sms:+1%s" data-track="callbar-text">Text for a quote</a>
</div>
''' % (BIZ["jase_tel"], BIZ["jase_display"], BIZ["jase_tel"])


# Fires GA4 events only if gtag() has already been installed. Inert until then —
# see docs/ANALYTICS_PLAN.md for how to turn analytics on.
TRACK_JS = '''<script>
(function () {
  document.addEventListener('click', function (e) {
    var a = e.target.closest && e.target.closest('[data-track]');
    if (!a || typeof window.gtag !== 'function') return;
    var href = a.getAttribute('href') || '';
    window.gtag('event', 'contact_click', {
      method: href.indexOf('tel:') === 0 ? 'phone'
            : href.indexOf('sms:') === 0 ? 'sms'
            : href.indexOf('mailto:') === 0 ? 'email' : 'social',
      link_id: a.getAttribute('data-track'),
      page_path: location.pathname
    });
  });
})();
</script>
'''


# --------------------------------------------------------------------------
# Structured data
# --------------------------------------------------------------------------
BUSINESS_ID = SITE + "/#business"

LOCAL_BUSINESS = '''{
  "@context": "https://schema.org",
  "@type": "HomeAndConstructionBusiness",
  "@id": "%(site)s/#business",
  "name": "Precision Wash & Landscape",
  "alternateName": "Precision Wash and Landscape",
  "url": "%(site)s/",
  "image": "%(site)s/images/front-entry.jpg",
  "logo": "%(site)s/images/front-entry.jpg",
  "description": "Pressure washing, soft washing, flowerbed care, sod, junk removal and window washing for homes in Ouachita and Lincoln Parish, Louisiana \\u2014 Monroe, West Monroe and Ruston. Free estimates on every job.",
  "telephone": "+1-318-805-8288",
  "email": null,
  "priceRange": "$$",
  "currenciesAccepted": "USD",
  "address": {
    "@type": "PostalAddress",
    "addressRegion": "LA",
    "addressCountry": "US"
  },
  "areaServed": [
    { "@type": "AdministrativeArea", "name": "Ouachita Parish, Louisiana" },
    { "@type": "AdministrativeArea", "name": "Lincoln Parish, Louisiana" },
    { "@type": "City", "name": "Monroe, Louisiana" },
    { "@type": "City", "name": "West Monroe, Louisiana" },
    { "@type": "City", "name": "Ruston, Louisiana" }
  ],
  "employee": [
    { "@type": "Person", "name": "Jase LaBorde", "telephone": "+1-318-805-8288" },
    { "@type": "Person", "name": "Garrett Smith", "telephone": "+1-318-614-8665" }
  ],
  "sameAs": [ "%(facebook)s" ],
  "hasOfferCatalog": {
    "@type": "OfferCatalog",
    "name": "Exterior cleaning and yard services",
    "itemListElement": [
      { "@type": "Offer", "itemOffered": { "@type": "Service", "name": "Soft and pressure washing", "url": "%(site)s/pressure-washing/" } },
      { "@type": "Offer", "itemOffered": { "@type": "Service", "name": "Flowerbed, sod and landscape cleanup", "url": "%(site)s/landscaping/" } },
      { "@type": "Offer", "itemOffered": { "@type": "Service", "name": "Junk removal and hauling", "url": "%(site)s/junk-removal/" } },
      { "@type": "Offer", "itemOffered": { "@type": "Service", "name": "Window washing", "url": "%(site)s/window-washing/" } }
    ]
  }
}''' % {"site": SITE, "facebook": BIZ["facebook"]}

# `email: null` is a placeholder we strip — the business has no published email.
LOCAL_BUSINESS = LOCAL_BUSINESS.replace('  "email": null,\n', "")


def breadcrumb_schema(trail):
    if len(trail) < 2:
        return None
    items = []
    for i, (href, label) in enumerate(trail):
        items.append(
            '    { "@type": "ListItem", "position": %d, "name": %s, "item": "%s%s" }'
            % (i + 1, jstr(label), SITE, href)
        )
    return ('{\n  "@context": "https://schema.org",\n  "@type": "BreadcrumbList",\n'
            '  "itemListElement": [\n%s\n  ]\n}' % ",\n".join(items))


def service_schema(name, description, path, service_type):
    return '''{
  "@context": "https://schema.org",
  "@type": "Service",
  "name": "%s",
  "serviceType": "%s",
  "description": "%s",
  "url": "%s%s",
  "provider": { "@id": "%s" },
  "areaServed": [
    { "@type": "AdministrativeArea", "name": "Ouachita Parish, Louisiana" },
    { "@type": "AdministrativeArea", "name": "Lincoln Parish, Louisiana" },
    { "@type": "City", "name": "Monroe, Louisiana" },
    { "@type": "City", "name": "West Monroe, Louisiana" },
    { "@type": "City", "name": "Ruston, Louisiana" }
  ]
}''' % (name, service_type, description, SITE, path, BUSINESS_ID)


def faq_schema(faqs):
    entries = []
    for q, a in faqs:
        plain = re.sub(r"<[^>]+>", "", a)
        plain = plain.replace("&amp;", "&").replace("&mdash;", "—").replace("&rsquo;", "'")
        entries.append('''    {
      "@type": "Question",
      "name": %s,
      "acceptedAnswer": { "@type": "Answer", "text": %s }
    }''' % (jstr(q), jstr(plain)))
    return ('{\n  "@context": "https://schema.org",\n  "@type": "FAQPage",\n'
            '  "mainEntity": [\n%s\n  ]\n}' % ",\n".join(entries))


def jstr(s):
    s = s.replace("&amp;", "&").replace("&mdash;", "—").replace("&rsquo;", "'")
    s = s.replace("&ldquo;", '"').replace("&rdquo;", '"').replace("&middot;", "·")
    return '"' + s.replace("\\", "\\\\").replace('"', '\\"') + '"'


# --------------------------------------------------------------------------
# Reusable content blocks
# --------------------------------------------------------------------------
def faq_block(faqs, heading="Frequently asked questions", eyebrow="Questions"):
    items = "\n        ".join(
        '<details class="faq-item">\n          <summary>%s</summary>\n          <p>%s</p>\n        </details>'
        % (q, a) for q, a in faqs
    )
    return '''  <section class="faq-section">
    <div class="wrap">
      <p class="eyebrow">%s</p>
      <h2 class="section-title">%s</h2>
      <div class="faq-list">
        %s
      </div>
    </div>
  </section>
''' % (eyebrow, heading, items)


def related_block(current, heading="Other things we do"):
    cards = []
    for href, (name, note) in SERVICE_CARDS.items():
        if href == current:
            continue
        cards.append('<a class="related-card" href="%s"><span class="name">%s</span>'
                     '<span class="note">%s</span></a>' % (href, name, note))
    cards.append('<a class="related-card" href="/service-area/"><span class="name">Where we work</span>'
                 '<span class="note">Monroe, West Monroe, Ruston and the rest of Ouachita &amp; Lincoln Parish.</span></a>')
    return '''  <section>
    <div class="wrap">
      <h2 class="section-title">%s</h2>
      <div class="related-grid">
        %s
      </div>
    </div>
  </section>
''' % (heading, "\n        ".join(cards))


def picture(base, alt, w, h, caption=None, lazy=True, sizes="(max-width: 480px) 92vw, (max-width: 780px) 46vw, 356px"):
    loading = ' loading="lazy" decoding="async"' if lazy else ' decoding="async" fetchpriority="high"'
    return '''<picture>
            <source type="image/webp" srcset="/images/%(b)s-450.webp 450w, /images/%(b)s.webp %(w)dw" sizes="%(s)s">
            <img src="/images/%(b)s.jpg" alt="%(alt)s" width="%(w)d" height="%(h)d"%(l)s>
          </picture>''' % {"b": base, "alt": alt, "w": w, "h": h, "l": loading, "s": sizes}


def ba_figure(base, label, caption, w, h):
    """Before/after drag-to-compare figure."""
    sizes = "(max-width: 480px) 92vw, (max-width: 780px) 46vw, 356px"
    return '''        <figure class="gallery-item">
          <div class="ba" data-ba role="slider" tabindex="0" aria-label="%(label)s: drag to compare before and after" aria-valuemin="0" aria-valuemax="100" aria-valuenow="50">
            <picture>
              <source type="image/webp" srcset="/images/%(b)s-after-450.webp 450w, /images/%(b)s-after.webp %(w)dw" sizes="%(s)s">
              <img class="ba-after" src="/images/%(b)s-after.jpg" alt="After: %(label)s" width="%(w)d" height="%(h)d" loading="lazy" decoding="async">
            </picture>
            <picture>
              <source type="image/webp" srcset="/images/%(b)s-before-450.webp 450w, /images/%(b)s-before.webp %(w)dw" sizes="%(s)s">
              <img class="ba-before" src="/images/%(b)s-before.jpg" alt="Before: %(label)s" width="%(w)d" height="%(h)d" loading="lazy" decoding="async">
            </picture>
            <span class="ba-handle"></span>
            <span class="ba-tag ba-tag-before">Before</span>
            <span class="ba-tag ba-tag-after">After</span>
          </div>
          <figcaption>%(cap)s</figcaption>
        </figure>''' % {"b": base, "label": label, "cap": caption, "w": w, "h": h, "s": sizes}


GALLERY_ITEMS = [
    ("siding", "Vinyl siding soft washed on a north Louisiana home", 900, 446),
    ("patio", "Flagstone patio pressure washed", 585, 1157),
    ("stairway", "Stone stairway pressure washed", 585, 1168),
    ("walkway", "Concrete walkway pressure washed", 585, 1154),
    ("flowerbed-pinestraw", "Flowerbed cleaned out and topped with fresh pine straw", 900, 448),
    ("flowerbed-roses", "Front flowerbed weeded and remulched around the roses", 900, 446),
]


def gallery_block(subset=None, heading="See the transformation &mdash; drag to compare",
                  eyebrow="Recent work", intro=None, include_front=False):
    """Before/after sliders for the named jobs.

    `include_front` adds the single (non-slider) front-entry shot. It's off by
    default so the same photo doesn't turn up on three different pages.
    """
    items = [g for g in GALLERY_ITEMS if subset is None or g[0] in subset]
    figs = [ba_figure(b, label, label + ", before and after", w, h)
            for b, label, w, h in items]
    if include_front:
        figs.append('''        <figure class="gallery-item">
          %s
          <figcaption>Front entry washed and flowerbeds refreshed &mdash; Ouachita Parish, Louisiana</figcaption>
        </figure>''' % picture("front-entry", "Pressure washed front entry and refreshed flowerbeds on a home in Ouachita Parish, Louisiana", 1316, 918))
    intro_html = '\n      <p class="lede" style="margin-top:0.75rem;">%s</p>' % intro if intro else ""
    return '''  <section class="gallery-section">
    <div class="wrap">
      <p class="eyebrow">%s</p>
      <h2 class="section-title">%s</h2>%s
      <div class="gallery-grid">
%s
      </div>
    </div>
  </section>
''' % (eyebrow, heading, intro_html, "\n".join(figs))


BA_JS = '''<script>
(function () {
  document.querySelectorAll('[data-ba]').forEach(function (el) {
    function setPos(clientX) {
      var rect = el.getBoundingClientRect();
      var pct = ((clientX - rect.left) / rect.width) * 100;
      pct = Math.max(0, Math.min(100, pct));
      el.style.setProperty('--pos', pct + '%');
      el.setAttribute('aria-valuenow', Math.round(pct));
    }
    el.addEventListener('pointermove', function (e) { setPos(e.clientX); });
    el.addEventListener('pointerdown', function (e) {
      setPos(e.clientX);
      try { el.setPointerCapture(e.pointerId); } catch (err) {}
    });
    el.addEventListener('keydown', function (e) {
      var cur = parseFloat(getComputedStyle(el).getPropertyValue('--pos')) || 50;
      if (e.key === 'ArrowLeft') { cur = Math.max(0, cur - 5); }
      else if (e.key === 'ArrowRight') { cur = Math.min(100, cur + 5); }
      else { return; }
      el.style.setProperty('--pos', cur + '%');
      el.setAttribute('aria-valuenow', Math.round(cur));
      e.preventDefault();
    });
  });
})();
</script>
'''

# Hero ripple. Pauses when the hero scrolls out of view so it stops burning CPU
# (and input-responsiveness) on the rest of the page.
RIPPLE_JS = '''<script>
(function () {
  var canvas = document.getElementById('ripple');
  if (!canvas) return;
  var ctx = canvas.getContext('2d');
  var reduceMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  var hero = canvas.closest('.hero');
  var w, h, dpr, running = false, rafId = 0, visible = true;
  var drops = [];

  function resize() {
    var rect = hero.getBoundingClientRect();
    dpr = Math.min(window.devicePixelRatio || 1, 2);
    w = rect.width; h = rect.height;
    canvas.width = w * dpr;
    canvas.height = h * dpr;
    ctx.setTransform(dpr, 0, 0, dpr, 0, 0);
  }

  function spawn() {
    drops.push({
      x: Math.random() * w,
      y: h * (0.55 + Math.random() * 0.45),
      r: 0,
      maxR: 60 + Math.random() * 140,
      speed: 0.35 + Math.random() * 0.4,
      alpha: 0.35 + Math.random() * 0.25
    });
  }

  var lastSpawn = 0;
  function frame(t) {
    ctx.clearRect(0, 0, w, h);
    if (t - lastSpawn > 900) { spawn(); lastSpawn = t; }
    for (var i = drops.length - 1; i >= 0; i--) {
      var d = drops[i];
      d.r += d.speed * 2.2;
      var life = d.r / d.maxR;
      if (life >= 1) { drops.splice(i, 1); continue; }
      ctx.beginPath();
      ctx.arc(d.x, d.y, d.r, 0, Math.PI * 2);
      ctx.strokeStyle = 'rgba(127,192,255,' + (d.alpha * (1 - life)) + ')';
      ctx.lineWidth = 1.4;
      ctx.stroke();
    }
    if (running) rafId = requestAnimationFrame(frame);
  }

  function start() { if (!running) { running = true; rafId = requestAnimationFrame(frame); } }
  function stop() { running = false; cancelAnimationFrame(rafId); }

  resize();
  window.addEventListener('resize', resize);

  if (reduceMotion) {
    for (var i = 0; i < 5; i++) { spawn(); drops[i].r = drops[i].maxR * Math.random(); }
    frame(0);
    return;
  }

  if ('IntersectionObserver' in window) {
    new IntersectionObserver(function (entries) {
      visible = entries[0].isIntersecting;
      if (visible && !document.hidden) { start(); } else { stop(); }
    }, { threshold: 0 }).observe(hero);
  } else {
    start();
  }
  document.addEventListener('visibilitychange', function () {
    if (document.hidden) { stop(); } else if (visible) { start(); }
  });
})();
</script>
'''


# --------------------------------------------------------------------------
# Page shell
# --------------------------------------------------------------------------
def reviews_block(heading="What customers actually said", eyebrow="In their words",
                  intro=None, only=None):
    """Real Facebook reviews, quoted verbatim. No ratings, no schema, no invention."""
    items = REVIEWS if only is None else [REVIEWS[i] for i in only]
    cards = "\n        ".join(
        '<figure class="review-card">\n'
        '          <blockquote class="quote">&ldquo;%s&rdquo;</blockquote>\n'
        '          <figcaption class="who"><strong>%s</strong>%s</figcaption>\n'
        '        </figure>' % (q, who, src) for q, who, src in items
    )
    intro_html = '\n      <p class="lede" style="margin-top:0.75rem;">%s</p>' % intro if intro else ""
    return '''  <section class="band-warm">
    <div class="wrap">
      <p class="eyebrow">%s</p>
      <h2 class="section-title">%s</h2>%s
      <div class="reviews-grid">
        %s
      </div>
    </div>
  </section>
''' % (eyebrow, heading, intro_html, cards)


def render(path, title, description, body, schemas, og_image="/images/og-precision-wash-landscape.jpg",
           scripts="", noindex=False, trail=None, accent=None):
    canonical = SITE + path
    robots = '<meta name="robots" content="noindex, follow">\n' if noindex else ""
    ld = "\n".join(
        '<script type="application/ld+json">\n%s\n</script>' % s for s in schemas if s
    )
    bc = breadcrumbs(trail) if trail else ""
    return '''<!doctype html>
<!-- GENERATED FILE - do not edit by hand. Edit tools/build.py and re-run it. -->
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>%(title)s</title>
<meta name="description" content="%(desc)s">
%(robots)s<link rel="canonical" href="%(canonical)s">
<link rel="icon" href="%(favicon)s">
<meta name="theme-color" content="#0a0d12">
<meta name="geo.region" content="US-LA">
<meta name="geo.placename" content="Monroe, Louisiana">
<meta property="og:site_name" content="Precision Wash &amp; Landscape">
<meta property="og:title" content="%(title)s">
<meta property="og:description" content="%(desc)s">
<meta property="og:type" content="website">
<meta property="og:url" content="%(canonical)s">
<meta property="og:image" content="%(site)s%(og)s">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta property="og:image:alt" content="Precision Wash &amp; Landscape &mdash; pressure washing and flowerbed care in Ouachita and Lincoln Parish, Louisiana">
<meta property="og:locale" content="en_US">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="%(title)s">
<meta name="twitter:description" content="%(desc)s">
<meta name="twitter:image" content="%(site)s%(og)s">
<link rel="stylesheet" href="/assets/site.css">
%(ld)s
</head>
<body>
<div class="stack"%(accentattr)s>

%(topbar)s%(bc)s%(body)s%(footer)s</div>

%(callbar)s%(scripts)s%(track)s</body>
</html>
''' % {
        "title": title, "desc": description, "canonical": canonical, "robots": robots,
        "favicon": FAVICON, "site": SITE, "og": og_image, "ld": ld,
        "topbar": topbar(path), "bc": bc, "body": body, "footer": footer(),
        "callbar": CALLBAR, "scripts": scripts, "track": TRACK_JS,
        "accentattr": (' data-accent="%s"' % accent) if accent else "",
    }


def write(path, html):
    out = os.path.join(ROOT, "index.html" if path == "/" else path.strip("/") + "/index.html")
    if path.endswith(".html"):
        out = os.path.join(ROOT, path.lstrip("/"))
    os.makedirs(os.path.dirname(out), exist_ok=True)
    io.open(out, "w", encoding="utf-8", newline="\n").write(html)
    return os.path.relpath(out, ROOT).replace("\\", "/")


# --------------------------------------------------------------------------
# PAGES
# --------------------------------------------------------------------------
PAGES = []


# ---------- Home ----------
def home():
    path = "/"
    cards = []
    for href, (name, note) in SERVICE_CARDS.items():
        cards.append('''        <a class="service-card" data-accent="%s" href="%s">
          <div class="service-icon" aria-hidden="true">
            <svg width="22" height="22" viewBox="0 0 24 24" fill="none">%s</svg>
          </div>
          <div>
            <h3>%s</h3>
            <p>%s</p>
            <span class="more">See what&rsquo;s included &rarr;</span>
          </div>
        </a>''' % (ACCENT[href], href, ICONS[href], name, note))

    faqs = [
        ("What areas do you serve?",
         "We work across Ouachita and Lincoln Parish in north Louisiana &mdash; Monroe, West Monroe, Ruston and the "
         "communities around them. If you&rsquo;re on the edge of that, call and ask; we&rsquo;ll tell you straight "
         "whether we can get to you. Full detail on our <a href=\"/service-area/\">service area page</a>."),
        ("Do I need to be home, or provide water and power?",
         "Most jobs just need access to an outdoor water spigot and an outlet &mdash; we bring our own equipment. "
         "You don&rsquo;t need to be home; just let us know how to get to the areas being cleaned."),
        ("Is pressure washing safe for my siding, roof, or paint?",
         "Yes, when the right method is used. We <a href=\"/pressure-washing/\">soft wash</a> delicate surfaces "
         "&mdash; low pressure plus a cleaning solution that kills the mildew and algae instead of blasting it off "
         "&mdash; and save high pressure for concrete, brick and stone."),
        ("How often should I get my house or driveway washed?",
         "In Louisiana&rsquo;s humidity most homes benefit from a wash once or twice a year to stay ahead of mildew, "
         "algae and pollen buildup. Shaded north-facing walls and concrete under trees usually need it more often "
         "than sun-exposed surfaces."),
        ("Can I book more than one service at once?",
         "That&rsquo;s how most of our jobs go. Wash the house, redo the beds, haul off what&rsquo;s piled up behind "
         "the shed &mdash; one visit, one estimate. It&rsquo;s cheaper than booking three separate trades and the "
         "whole property matches when we leave."),
        ("What does it cost?",
         "Every property is different, so we give free, no-obligation estimates before any work starts. Call or text "
         "Jase or Garrett with a few photos or a description and we&rsquo;ll get you a number fast."),
    ]

    body = '''  <section class="hero">
    <canvas id="ripple" aria-hidden="true"></canvas>
    <div class="wrap">
      <div class="hero-badge"><span class="dot"></span> Free estimates &middot; Ouachita &amp; Lincoln Parish</div>
      <h1>
        <span class="hero-brand">Precision<br>Wash <span class="accent">&amp;</span> Landscape</span>
        <span class="hero-sub">We make the outside of your house look new again &mdash; Monroe, West Monroe &amp; Ruston</span>
      </h1>
      <p class="lede">Soft washing and pressure washing. Flowerbeds, sod and trimming. Junk hauled off. Windows washed. One family-run crew for the whole outside of your property, and a free estimate before anything starts.</p>
      <div class="hero-ctas">
        <a class="btn btn-primary" href="tel:1%(jt)s" data-track="hero-call-jase">Call or Text Jase &mdash; %(jd)s</a>
        <a class="btn btn-ghost" href="tel:1%(gt)s" data-track="hero-call-garrett">Call or Text Garrett &mdash; %(gd)s</a>
      </div>
      <div class="hero-meta">
        <span><strong>Free</strong> estimates on every job</span>
        <span><strong>Owner-operated</strong> &mdash; Jase &amp; Garrett do the work</span>
        <span><strong>Colossians 3:23</strong> &mdash; work as for the Lord</span>
      </div>
    </div>
  </section>

  <section class="band-warm">
    <div class="wrap">
      <p class="eyebrow">Why you&rsquo;re here</p>
      <h2 class="section-title">It doesn&rsquo;t happen all at once</h2>
      <p class="lede" style="margin-top:0.75rem;">Nobody wakes up one morning to a dirty house. It creeps. A north Louisiana summer does it a little at a time, and one day you pull into the driveway and the place just looks tired.</p>
      <div class="story-grid">
        <div class="story-item">
          <h3>The green crawls up the siding</h3>
          <p>It starts low, on the shaded wall you never look at, and works upward. By the time you notice it, it has been there a year.</p>
        </div>
        <div class="story-item">
          <h3>The driveway stops being white</h3>
          <p>Algae film under the tree cover, then spring pollen on top of it. The concrete isn&rsquo;t old. It&rsquo;s coated.</p>
        </div>
        <div class="story-item">
          <h3>The beds fill in</h3>
          <p>The straw thins out, weeds take the gaps, and the shrubs grow into the windows. One good season is all it takes.</p>
        </div>
        <div class="story-item">
          <h3>The pile behind the shed grows</h3>
          <p>Limbs from the last storm, the old recliner, a busted grill. Every month it&rsquo;s easier to leave than to deal with.</p>
        </div>
      </div>
      <p class="lede" style="margin-top:var(--space-4);">None of it is hard to fix. It&rsquo;s just nobody&rsquo;s job. <strong style="color:var(--steel);">That&rsquo;s ours.</strong></p>
    </div>
  </section>

  <section class="services-section">
    <div class="wrap">
      <p class="eyebrow">What we do</p>
      <h2 class="section-title">Four services, one crew</h2>
      <p class="lede" style="margin-top:0.75rem;">Book any one on its own, or have us handle the whole exterior in a single visit.</p>
      <div class="services-grid">
%(cards)s
      </div>
    </div>
  </section>

  <section class="band-accent">
    <div class="wrap">
      <p class="eyebrow">The way most jobs go</p>
      <h2 class="section-title">One visit, one estimate, whole property</h2>
      <p class="lede" style="margin-top:0.75rem;">A clean house makes the beds in front of it look worse. Fresh beds make a gray driveway stand out. Fixing one thing just moves your eye to the next one &mdash; which is why most of our customers have us do the lot while we&rsquo;re already there.</p>
      <div class="bundle">
        <div class="bundle-step">
          <span class="n">1</span>
          <h3>Wash first</h3>
          <p>Siding, roof, gutters, then the concrete. Everything rinses downward, so this has to come before the beds.</p>
        </div>
        <div class="bundle-step">
          <span class="n">2</span>
          <h3>Clear what&rsquo;s in the way</h3>
          <p>Limbs, old furniture, whatever&rsquo;s piled up. It leaves on the same truck.</p>
        </div>
        <div class="bundle-step">
          <span class="n">3</span>
          <h3>Reset the beds</h3>
          <p>Weeded, sprayed, trimmed back off the siding, then fresh pine straw or mulch.</p>
        </div>
        <div class="bundle-step">
          <span class="n">4</span>
          <h3>Glass last</h3>
          <p>Windows, frames and sills, after all the runoff is done. Otherwise you&rsquo;d be paying to clean them twice.</p>
        </div>
      </div>
      <p class="lede" style="margin-top:var(--space-3);">One crew, one price agreed up front, and the whole place matches when we pull out of the driveway.</p>
    </div>
  </section>

%(gallery)s%(reviews)s
  <section class="band-accent">
    <div class="wrap">
      <p class="eyebrow">Who shows up</p>
      <h2 class="section-title">You&rsquo;re hiring the two people doing the work</h2>
      <div class="prose" style="margin-top:var(--space-2);">
        <p>Precision Wash &amp; Landscape is family-run and owner-operated. <strong>%(jn)s</strong> and <strong>%(gn)s</strong> own it, and they&rsquo;re the ones in your driveway &mdash; you won&rsquo;t talk to one person on the phone and find strangers at your house.</p>
        <p>That&rsquo;s the whole pitch, really. Call the owner, get a straight answer about what your property needs and what it&rsquo;ll cost, and then have the person who quoted it turn up and do it.</p>
      </div>
      <blockquote class="pullquote">
        <p>&ldquo;He came early, worked through the rain, and did an excellent job!&rdquo;</p>
        <cite>Cathy Salsbury &middot; Facebook</cite>
      </blockquote>
    </div>
  </section>

  <section class="area-section">
    <div class="wrap">
      <div>
        <p class="eyebrow">Where we work</p>
        <h2 class="section-title">Serving Ouachita &amp; Lincoln Parish</h2>
        <p class="lede" style="margin-top: 0.75rem;">Based in north Louisiana and taking jobs across both parishes. Not sure if you&rsquo;re in range? Call &mdash; we&rsquo;ll tell you straight.</p>
        <div class="parish-list">
          <div class="parish-item"><span class="name">Ouachita Parish</span><span class="note">Monroe, West Monroe &amp; surrounding areas</span></div>
          <div class="parish-item"><span class="name">Lincoln Parish</span><span class="note">Ruston &amp; surrounding areas</span></div>
        </div>
        <p style="margin-top:var(--space-3);"><a class="btn btn-ghost" href="/service-area/">See the full service area</a></p>
      </div>
      <div class="map-card">
        <svg viewBox="0 0 320 220" width="100%%" role="img" aria-label="Simplified map showing Ouachita and Lincoln Parish service area">
          <rect x="20" y="30" width="130" height="140" rx="4" fill="none" stroke="#22303f" stroke-width="1.5"/>
          <rect x="150" y="30" width="130" height="140" rx="4" fill="none" stroke="#22303f" stroke-width="1.5"/>
          <rect x="20" y="30" width="130" height="140" rx="4" fill="#17335c" opacity="0.35"/>
          <rect x="150" y="30" width="130" height="140" rx="4" fill="#17335c" opacity="0.2"/>
          <circle cx="85" cy="100" r="4" fill="#7fc0ff"/>
          <circle cx="215" cy="95" r="4" fill="#7fc0ff"/>
          <text x="85" y="185" text-anchor="middle" fill="#93a4b6" font-size="12" font-family="sans-serif">Ouachita</text>
          <text x="215" y="185" text-anchor="middle" fill="#93a4b6" font-size="12" font-family="sans-serif">Lincoln</text>
        </svg>
      </div>
    </div>
  </section>

%(faq)s%(contact)s''' % {
        "jt": BIZ["jase_tel"], "jd": BIZ["jase_display"], "jn": BIZ["jase_name"],
        "gt": BIZ["garrett_tel"], "gd": BIZ["garrett_display"], "gn": BIZ["garrett_name"],
        "cards": "\n".join(cards),
        "gallery": gallery_block(
            subset={"siding", "walkway", "flowerbed-pinestraw"},
            heading="Same house, same week &mdash; drag to compare",
            intro="Real jobs in Ouachita Parish. Drag the slider across each photo.",
            include_front=True),
        "reviews": reviews_block(),
        "faq": faq_block(faqs),
        "contact": contact_section(
            intro="Tell us the address, what you want done, and send a photo or two if you can. "
                  "We&rsquo;ll come back with a free estimate."),
    }

    website = '''{
  "@context": "https://schema.org",
  "@type": "WebSite",
  "@id": "%s/#website",
  "url": "%s/",
  "name": "Precision Wash & Landscape",
  "publisher": { "@id": "%s" },
  "inLanguage": "en-US"
}''' % (SITE, SITE, BUSINESS_ID)

    return render(
        path,
        "Pressure Washing &amp; Yard Cleanup in Monroe, LA | Precision Wash",
        "Pressure washing, flowerbed cleanup, sod, junk hauling and window washing in Monroe, West Monroe and "
        "Ruston, LA. Family-run. Free estimates &mdash; call or text 318-805-8288.",
        body,
        [LOCAL_BUSINESS, website, faq_schema(faqs)],
        scripts=RIPPLE_JS + BA_JS,
    )


PAGES.append(("/", home))


# ---------- Pressure washing ----------
def pressure_washing():
    path = "/pressure-washing/"
    trail = [("/", "Home"), (path, "Pressure Washing")]

    surfaces = [
        ("Vinyl &amp; painted siding",
         "Soft washed at low pressure so we lift the green and black mildew without forcing water behind the siding or stripping paint."),
        ("Concrete driveways",
         "High pressure plus a surface cleaner for an even finish instead of the striped &ldquo;zebra&rdquo; look a wand leaves behind. Oil spots and red-clay staining get pre-treated."),
        ("Patios, walkways &amp; steps",
         "Stamped concrete, flagstone, pavers and stone stairs &mdash; pressure dialed to the surface so joints and sealer survive it."),
        ("Brick &amp; masonry",
         "Cleans up well, but old mortar needs a lighter touch. We test a small area first."),
        ("Gutters (outside faces)",
         "Removes the black vertical streaking that shows up on white gutters and makes an otherwise clean house look tired."),
        ("Roofs",
         "Soft wash only. Algae streaking on shingles is a living organism &mdash; the cleaning solution kills it. High pressure on shingles strips granules and shortens the roof&rsquo;s life."),
        ("Wood &amp; vinyl fences",
         "Years of green growth come off and the wood grain shows again."),
        ("Porches, columns &amp; soffits",
         "The spots that collect dirt film and wasp nests and never get touched otherwise."),
    ]
    surface_html = "\n        ".join(
        '<div class="surface-item"><span class="name">%s</span><span class="note">%s</span></div>' % s
        for s in surfaces
    )

    faqs = [
        ("What&rsquo;s the difference between pressure washing and soft washing?",
         "Pressure washing uses water force to clean &mdash; right for concrete, brick and stone. Soft washing uses "
         "low pressure and a cleaning solution that kills the mildew, algae and lichen at the root &mdash; right for "
         "siding, roofs, painted wood and screens. Using the wrong one is how siding gets water behind it and shingles "
         "lose granules, so we match the method to the surface."),
        ("Will pressure washing damage my siding or roof?",
         "Not the way we do it. Siding and roofing get soft washed at low pressure. We also wet down landscaping before "
         "and rinse it after, so plants around the house aren&rsquo;t sitting in cleaning solution."),
        ("How long does the clean last?",
         "A soft wash that kills the organism lasts longer than a rinse that just knocks it off &mdash; usually a year "
         "or more on siding. In north Louisiana the shaded, north-facing side of a house and any concrete under trees "
         "always comes back first."),
        ("Do you need my water and electricity?",
         "Yes &mdash; an outdoor spigot and an outlet. We bring everything else. You don&rsquo;t need to be home as "
         "long as we can get to the areas being cleaned and the spigot is on."),
        ("Can you get rid of the black streaks on my roof?",
         "Usually, yes. Those streaks are Gloeocapsa magma, an algae that feeds on the limestone filler in asphalt "
         "shingles. It shows up worst on north-facing slopes here because they stay damp longest. A soft wash kills it "
         "rather than grinding it off."),
        ("How much does pressure washing cost?",
         "It depends on square footage, how many stories, and how bad the buildup is &mdash; so we quote each property "
         "rather than posting a flat rate. Call or text a couple of photos and we&rsquo;ll give you a free estimate."),
    ]

    body = '''  <section class="page-hero">
    <div class="wrap">
      <p class="eyebrow">Soft &amp; pressure washing</p>
      <h1>House, Driveway &amp; Exterior Pressure Washing in Monroe, West Monroe &amp; Ruston</h1>
      <p class="lede">North Louisiana humidity puts green mildew on siding, black streaks on roofs and a gray film on every slab of concrete you own. We take it off &mdash; soft washing where the surface is delicate, real pressure where it isn&rsquo;t.</p>
      <div class="hero-ctas">
        <a class="btn btn-primary" href="tel:1%(jt)s" data-track="svc-call">Call or Text for a Free Estimate</a>
        <a class="btn btn-ghost" href="/contact/">Other ways to reach us</a>
      </div>
    </div>
  </section>

  <section>
    <div class="wrap">
      <div class="prose">
        <h2>What we wash</h2>
        <p>Most of our washing work is residential exteriors &mdash; the house itself plus everything around it that has gone gray, green or black since the last time it was cleaned. We also take rental turnovers and small commercial buildings.</p>
      </div>
      <div class="surface-grid">
        %(surfaces)s
      </div>
      <div class="callout">
        <p><strong>Not on the list?</strong> Boat docks, carports, dumpster pads, playsets, brick mailboxes, retaining walls &mdash; if it&rsquo;s outside and it&rsquo;s dirty, call or text a photo and we&rsquo;ll tell you whether we can clean it and what it would run.</p>
      </div>
    </div>
  </section>

  <section class="band-warm">
    <div class="wrap">
      <div class="prose">
        <h2>Why north Louisiana is hard on exteriors</h2>
        <p>This is a humid, heavily wooded part of the state, and it shows up on buildings in three predictable ways:</p>
        <ul>
          <li><strong>Green and black mildew on siding.</strong> Shaded walls, especially north-facing ones, stay damp long enough for mildew to take hold. It starts near the ground and creeps up.</li>
          <li><strong>Black streaking on roofs.</strong> That is <em>Gloeocapsa magma</em>, an algae that feeds on the limestone filler in asphalt shingles. It runs downhill in dark streaks and does not wash off in the rain.</li>
          <li><strong>Gray-green concrete.</strong> Driveways, walkways and patios under tree cover grow their own algae film, and spring pine pollen mats on top of it. The slab looks &ldquo;old&rdquo; when it is really just coated.</li>
        </ul>
        <p>None of that comes off with a garden hose, and most of it comes back if you only knock it loose instead of killing it. That is the whole argument for soft washing over blasting.</p>

        <h2>How a wash day goes</h2>
        <h3>1. Free estimate</h3>
        <p>Call or text Jase at <a href="tel:1%(jt)s">%(jd)s</a> or Garrett at <a href="tel:1%(gt)s">%(gd)s</a>. Tell us the address and what you want cleaned; a couple of photos gets you a faster, more accurate number. No charge and no obligation.</p>
        <h3>2. Setup and protection</h3>
        <p>We hook to an outside spigot and an outlet, pre-wet plants and beds around the work area, and move what needs moving &mdash; furniture, grills, door mats.</p>
        <h3>3. Wash</h3>
        <p>Soft wash on siding, roofs and painted surfaces; surface cleaner and higher pressure on concrete. Delicate or unusual surfaces get tested in an out-of-the-way spot first.</p>
        <h3>4. Rinse and walk-through</h3>
        <p>Everything gets rinsed down, including the landscaping. If you&rsquo;re home we&rsquo;ll walk it with you before we pack up.</p>

        <h2>Finish the job while we&rsquo;re there</h2>
        <p>A clean house tends to make the beds in front of it look worse. Plenty of our customers pair a wash with <a href="/landscaping/">flowerbed cleanup and fresh pine straw</a>, <a href="/window-washing/">window washing</a>, or a <a href="/junk-removal/">haul-off</a> of the limbs and junk we uncover &mdash; all in one visit, one estimate.</p>
      </div>
    </div>
  </section>

%(gallery)s%(reviews)s%(faq)s%(related)s%(contact)s''' % {
        "jt": BIZ["jase_tel"], "jd": BIZ["jase_display"],
        "gt": BIZ["garrett_tel"], "gd": BIZ["garrett_display"],
        "surfaces": surface_html,
        "reviews": reviews_block(
            heading="What customers said about the washing",
            only=[0],
            intro="Cathy booked a wash and a flowerbed cleanup in the same visit &mdash; the most common way "
                  "we get called out."),
        "gallery": gallery_block(
            subset={"siding", "patio", "stairway", "walkway"},
            heading="Washes we&rsquo;ve done &mdash; drag to compare",
            eyebrow="Proof",
            intro="Every one of these is a real job in Ouachita Parish, photographed the same day. "
                  "Drag the slider across each photo to see what came off."),
        "faq": faq_block(faqs, "Pressure washing questions we get asked"),
        "related": related_block(path),
        "contact": contact_section(
            heading="Get a free pressure washing estimate",
            intro="Send the address and a photo of what needs cleaning. We&rsquo;ll come back with a number."),
    }

    return render(
        path,
        "House &amp; Driveway Pressure Washing, Monroe LA | Precision Wash",
        "Soft washing and pressure washing for siding, roofs, driveways, patios and gutters in Monroe, West Monroe "
        "and Ruston, LA. Free estimates &mdash; call or text 318-805-8288.",
        body,
        [
            service_schema(
                "Soft and pressure washing",
                "Soft washing and pressure washing of house siding, roofs, driveways, patios, walkways, gutters, "
                "fences and other exterior surfaces in Ouachita and Lincoln Parish, Louisiana.",
                path, "Pressure washing service"),
            breadcrumb_schema(trail),
            faq_schema(faqs),
        ],
        scripts=BA_JS,
        trail=trail,
        accent="wash",
    )


PAGES.append(("/pressure-washing/", pressure_washing))


# ---------- Landscaping / flowerbeds ----------
def landscaping():
    path = "/landscaping/"
    trail = [("/", "Home"), (path, "Lawns, Beds &amp; Landscape Cleanup")]

    work = [
        ("Weeding &amp; spraying",
         "Beds pulled clean by hand and treated so the weeds stay gone longer than a weekend."),
        ("Fresh pine straw",
         "The north Louisiana standard. It knits together on slopes instead of washing out, and it goes down fast over a big bed."),
        ("Fresh mulch",
         "Where you want a darker, more finished edge &mdash; front beds, around roses, along walkways."),
        ("Trimming bushes &amp; shrubs",
         "Shaping overgrown foundation plantings back off the siding and windows."),
        ("Planting",
         "Putting in the shrubs, perennials or color you&rsquo;ve picked out."),
        ("Removing plants",
         "Taking out what&rsquo;s dead, overgrown, or in the wrong place &mdash; roots and all."),
        ("Laying sod",
         "New turf over bare, patchy or torn-up ground. Hot, heavy work that goes a lot faster with a crew."),
    ]
    work_html = "\n        ".join(
        '<div class="surface-item"><span class="name">%s</span><span class="note">%s</span></div>' % w
        for w in work
    )

    faqs = [
        ("Pine straw or mulch &mdash; which should I use?",
         "Pine straw is the north Louisiana default for good reason: it&rsquo;s cheaper to cover a large bed with, it "
         "locks together so it doesn&rsquo;t float away in a hard rain or wash off a slope, and it suits the pines and "
         "azaleas most yards around here already have. Mulch gives a darker, more formal look and holds moisture "
         "better, so it tends to win on smaller front beds you see up close. We&rsquo;ll tell you which we&rsquo;d use "
         "on your beds and why."),
        ("When is the best time to redo my beds?",
         "Late winter to early spring, before everything leafs out, is the easiest time &mdash; you can actually see "
         "what you&rsquo;re working with, and fresh straw or mulch is in place before the weeds start. Fall is the "
         "other good window. That said, a bed full of weeds in July still looks better cleaned out than left alone."),
        ("Do you haul off what you cut and pull?",
         "Yes. Trimmings, pulled weeds and removed plants leave with us &mdash; it&rsquo;s the same truck we use for "
         "<a href=\"/junk-removal/\">junk removal and hauling</a>."),
        ("Can you do the beds and wash the house in the same visit?",
         "That&rsquo;s the most common way we get booked. We&rsquo;ll <a href=\"/pressure-washing/\">wash the house "
         "and driveway</a> first so the rinse-off doesn&rsquo;t land on fresh straw, then clean out and re-dress the "
         "beds. One trip, one estimate."),
        ("Do you handle jobs beyond flowerbeds?",
         "Tell us what you have in mind. Beds, trimming, planting and cleanup are our bread and butter; for anything "
         "outside that, call or text and we&rsquo;ll give you a straight answer about whether it&rsquo;s something we "
         "take on."),
    ]

    body = '''  <section class="page-hero">
    <div class="wrap">
      <p class="eyebrow">Lawns, beds &amp; trimming</p>
      <h1>Flowerbeds, Sod &amp; Landscape Cleanup in Ouachita &amp; Lincoln Parish</h1>
      <p class="lede">Beds get away from you fast in this climate. We clean them out to the dirt, treat the weeds, trim back what&rsquo;s overgrown, and finish with fresh pine straw or mulch. Bare ground gets new sod. Either way, the front of your house looks looked-after again.</p>
      <div class="hero-ctas">
        <a class="btn btn-primary" href="tel:1%(jt)s" data-track="svc-call">Call or Text for a Free Estimate</a>
        <a class="btn btn-ghost" href="/contact/">Other ways to reach us</a>
      </div>
    </div>
  </section>

  <section>
    <div class="wrap">
      <div class="prose">
        <h2>What flowerbed work includes</h2>
        <p>Most bed jobs are some mix of the following. You can book the whole thing or just the part you need.</p>
      </div>
      <div class="surface-grid">
        %(work)s
      </div>
      <div class="callout">
        <p><strong>Not sure what your beds need?</strong> Send a couple of photos to Jase at <a href="tel:1%(jt)s">%(jd)s</a>. We&rsquo;ll tell you what we&rsquo;d do, roughly what it costs, and whether it&rsquo;s worth doing now or waiting for the season.</p>
      </div>
    </div>
  </section>

  <section class="band-warm">
    <div class="wrap">
      <div class="prose">
        <h2>Laying sod</h2>
        <p>If the ground is bare &mdash; a patch that never took, ruts from a build, somewhere a tree used to be &mdash; we lay new sod over it. It is genuinely hard work in a Louisiana summer, which is most of the reason people call rather than do it themselves.</p>
        <p>Tell us roughly how much ground you&rsquo;re covering and we&rsquo;ll quote it. The same visit can take in a <a href="/pressure-washing/">driveway wash</a> and a <a href="/junk-removal/">haul-off</a> of whatever came out of the yard.</p>

        <h2>Why beds go downhill here</h2>
        <p>Long growing season, heavy summer rain and plenty of shade mean three things happen to a north Louisiana flowerbed:</p>
        <ul>
          <li><strong>Weeds outrun you.</strong> The season effectively runs most of the year, so a bed that was clean in April is unrecognizable by July.</li>
          <li><strong>The straw or mulch disappears.</strong> It breaks down, gets stepped on, and washes toward the low side of the yard after a hard rain. Beds end up thin and patchy with bare dirt showing through.</li>
          <li><strong>Shrubs swallow the house.</strong> Foundation plantings grow into the siding and over the windows, which traps moisture against the wall &mdash; and that&rsquo;s exactly where mildew starts.</li>
        </ul>
        <p>A cleanout plus fresh straw resets all three at once, and it&rsquo;s the single cheapest thing you can do to change how a house looks from the street.</p>

        <h2>How it works</h2>
        <h3>1. We look at the beds</h3>
        <p>Photos are usually enough for an estimate. For bigger jobs we&rsquo;ll come by and measure so the straw or mulch quantity is right.</p>
        <h3>2. Clean out</h3>
        <p>Weeds pulled, old straw and debris removed, dead and overgrown material cut back or taken out.</p>
        <h3>3. Treat and edge</h3>
        <p>Beds get sprayed so the weeds don&rsquo;t come straight back, and the bed line gets cleaned up.</p>
        <h3>4. Dress and haul off</h3>
        <p>Fresh pine straw or mulch goes down, and everything we pulled leaves with us.</p>

        <h2>Pairs well with a wash</h2>
        <p>Clean beds next to a mildewed wall look half-finished. Most customers have us <a href="/pressure-washing/">wash the house, driveway and walkway</a> in the same visit, and a lot of them add a <a href="/junk-removal/">haul-off</a> for the limbs and junk that turn up once the beds are cleared.</p>
      </div>
    </div>
  </section>

%(gallery)s%(reviews)s%(faq)s%(related)s%(contact)s''' % {
        "jt": BIZ["jase_tel"], "jd": BIZ["jase_display"],
        "work": work_html,
        "reviews": reviews_block(
            heading="What customers said about the bed work",
            intro="Both of these are real Facebook comments from customers in Ouachita Parish."),
        "gallery": gallery_block(
            subset={"flowerbed-pinestraw", "flowerbed-roses"},
            heading="Beds we&rsquo;ve reworked &mdash; drag to compare",
            eyebrow="Proof",
            intro="Real flowerbed jobs in Ouachita Parish. Drag across each photo to see before and after.",
            include_front=True),
        "faq": faq_block(faqs, "Flowerbed questions we get asked"),
        "related": related_block(path),
        "contact": contact_section(
            heading="Get a free flowerbed estimate",
            intro="Send a photo of the beds and we&rsquo;ll tell you what they need and what it costs."),
    }

    return render(
        path,
        "Flowerbed Cleanup, Sod &amp; Pine Straw in Monroe, LA | Precision Wash",
        "Flowerbed cleanout, fresh pine straw and mulch, bush trimming and new sod in Monroe, West Monroe and "
        "Ruston, LA. Free estimates &mdash; call or text 318-805-8288.",
        body,
        [
            service_schema(
                "Flowerbed, sod and landscape cleanup",
                "Flowerbed cleanout, weeding and spraying, fresh pine straw and mulch, bush trimming, planting, "
                "plant removal and sod installation in Ouachita and Lincoln Parish, Louisiana.",
                path, "Landscaping service"),
            breadcrumb_schema(trail),
            faq_schema(faqs),
        ],
        scripts=BA_JS,
        trail=trail,
        accent="leaf",
    )


PAGES.append(("/landscaping/", landscaping))


# ---------- Junk removal ----------
def junk_removal():
    path = "/junk-removal/"
    trail = [("/", "Home"), (path, "Junk Removal &amp; Hauling")]

    items = [
        ("Tree limbs &amp; storm debris",
         "The pile at the curb after a storm, or the limbs that have been stacked behind the shed since the last one."),
        ("Yard debris",
         "Old pine straw, hedge trimmings, leaves, stumps you&rsquo;ve already pulled."),
        ("Old furniture",
         "Couches, mattresses, recliners, dressers &mdash; the things too big for the trash can and too awkward to move alone."),
        ("Appliances &amp; scrap",
         "Call first so we can confirm what we can take and how it has to be handled."),
        ("Garage, shed &amp; attic cleanouts",
         "Years of accumulated boxes, tools and whatever else ended up out there."),
        ("Rental &amp; estate turnovers",
         "Whole-property clear-outs when a tenant leaves or a house is being sold."),
    ]
    items_html = "\n        ".join(
        '<div class="surface-item"><span class="name">%s</span><span class="note">%s</span></div>' % i
        for i in items
    )

    faqs = [
        ("What can you take?",
         "Tree limbs, yard debris, old furniture, general household junk and most of what comes out of a garage or "
         "shed cleanout. Some items &mdash; appliances, tires, chemicals, anything with refrigerant &mdash; have "
         "disposal rules attached, so call or text first and we&rsquo;ll tell you straight whether we can take it."),
        ("Do I have to move it to the curb?",
         "No. We load it from wherever it is &mdash; backyard, garage, side of the house. If it&rsquo;s already at "
         "the curb, that&rsquo;s faster and cheaper, but it isn&rsquo;t required."),
        ("How is hauling priced?",
         "By how much there is and how hard it is to get to. Send a photo of the pile and we&rsquo;ll give you a free "
         "estimate before we come out &mdash; no surprise number once the truck is in your driveway."),
        ("Can you come after a storm?",
         "Storm limb cleanup is one of the most common calls we get. Call or text and we&rsquo;ll tell you honestly "
         "when we can get to you &mdash; the days after a big blow are busy for everybody."),
        ("Do you clean up after loading?",
         "Yes. We rake or blow the area down before we leave so there isn&rsquo;t a debris outline where the pile "
         "used to be."),
    ]

    body = '''  <section class="page-hero">
    <div class="wrap">
      <p class="eyebrow">Junk removal &amp; hauling</p>
      <h1>Junk Removal &amp; Debris Hauling in Monroe, West Monroe &amp; Ruston</h1>
      <p class="lede">Limbs, old furniture, yard debris, garage cleanouts &mdash; we load it and it&rsquo;s gone. You don&rsquo;t have to drag it to the curb or find somebody with a truck.</p>
      <div class="hero-ctas">
        <a class="btn btn-primary" href="tel:1%(jt)s" data-track="svc-call">Call or Text for a Free Estimate</a>
        <a class="btn btn-ghost" href="/contact/">Other ways to reach us</a>
      </div>
    </div>
  </section>

  <section>
    <div class="wrap">
      <div class="prose">
        <h2>What we haul off</h2>
      </div>
      <div class="surface-grid">
        %(items)s
      </div>
      <div class="callout">
        <p><strong>Not sure we&rsquo;ll take it?</strong> Text a photo to Jase at <a href="tel:1%(jt)s">%(jd)s</a>. It takes us thirty seconds to tell you yes or no, and you&rsquo;ll get a price at the same time.</p>
      </div>
    </div>
  </section>

  <section class="band-warm">
    <div class="wrap">
      <div class="prose">
        <h2>How it works</h2>
        <h3>1. Send a photo</h3>
        <p>A picture of the pile, the room or the corner of the yard tells us more than a description does. That&rsquo;s usually all we need to quote it.</p>
        <h3>2. Free estimate</h3>
        <p>You get a number before we come out, based on volume and access &mdash; not after the truck is already parked in your driveway.</p>
        <h3>3. We load it</h3>
        <p>From wherever it sits. You don&rsquo;t need to move anything to the curb or be home, as long as we can get to it.</p>
        <h3>4. We clean up behind us</h3>
        <p>The spot gets raked or blown off so there&rsquo;s no outline left where the pile was.</p>

        <h2>Storm and seasonal cleanup</h2>
        <p>North Louisiana gets its share of wind, and limbs come down. Parish and city pickup schedules for storm debris can run long, and a brush pile sitting in the front yard for weeks is its own problem. If you&rsquo;d rather not wait, we&rsquo;ll come get it.</p>
        <p>The same goes for seasonal work &mdash; bagged leaves, old straw stripped out of beds during a <a href="/landscaping/">flowerbed cleanup</a>, or the accumulation that shows up when you finally clean out the shed.</p>

        <h2>While we&rsquo;re already there</h2>
        <p>A cleared yard is the right moment to <a href="/pressure-washing/">wash the driveway, patio and siding</a> &mdash; you can actually reach all of it once the pile is gone. Ask for both on the same estimate.</p>
      </div>
    </div>
  </section>

%(faq)s%(related)s%(contact)s''' % {
        "jt": BIZ["jase_tel"], "jd": BIZ["jase_display"],
        "items": items_html,
        "faq": faq_block(faqs, "Hauling questions we get asked"),
        "related": related_block(path),
        "contact": contact_section(
            heading="Get a free hauling estimate",
            intro="Text a photo of the pile and we&rsquo;ll price it before we come out."),
    }

    return render(
        path,
        "Junk Removal &amp; Hauling in Monroe &amp; Ruston, LA | Precision Wash",
        "Junk removal and debris hauling in Monroe, West Monroe and Ruston, LA &mdash; tree limbs, storm debris, "
        "old furniture, garage cleanouts. Free estimates. Call 318-805-8288.",
        body,
        [
            service_schema(
                "Junk removal and hauling",
                "Junk removal and debris hauling in Ouachita and Lincoln Parish, Louisiana &mdash; tree limbs, storm "
                "debris, yard waste, old furniture and garage cleanouts.",
                path, "Junk removal service"),
            breadcrumb_schema(trail),
            faq_schema(faqs),
        ],
        trail=trail,
        accent="amber",
    )


PAGES.append(("/junk-removal/", junk_removal))


# ---------- Window washing ----------
def window_washing():
    path = "/window-washing/"
    trail = [("/", "Home"), (path, "Window Washing")]

    faqs = [
        ("Do you clean the inside of the windows too?",
         "Our standard window work is exterior glass, frames and sills. If you want interiors done as well, say so "
         "when you call and we&rsquo;ll work it into the estimate."),
        ("Why do my windows look worse right after the house is washed?",
         "Because the wall behind them just got clean. It&rsquo;s the same reason a fresh flowerbed makes dingy siding "
         "stand out. That&rsquo;s why we usually recommend booking <a href=\"/pressure-washing/\">house washing</a> "
         "and window washing together."),
        ("What about screens and tracks?",
         "Screens hold a surprising amount of dust and pollen and can re-dirty clean glass the first time it rains. "
         "Tell us whether you want them pulled and rinsed and we&rsquo;ll include it."),
        ("How often should windows be washed?",
         "Once or twice a year suits most homes here. Spring &mdash; after the pine pollen has finished &mdash; is the "
         "single best time, since that yellow film is what makes glass look hazy from inside."),
        ("How much does it cost?",
         "It depends on how many windows, how many stories, and whether screens and interiors are included. Call or "
         "text and we&rsquo;ll give you a free estimate."),
    ]

    body = '''  <section class="page-hero">
    <div class="wrap">
      <p class="eyebrow">Window washing</p>
      <h1>Exterior Window Cleaning in Monroe, West Monroe &amp; Ruston</h1>
      <p class="lede">Hand-washed glass, frames and sills &mdash; not just a spray-down from the ground. Streak-free, and done carefully around screens, seals and trim.</p>
      <div class="hero-ctas">
        <a class="btn btn-primary" href="tel:1%(jt)s" data-track="svc-call">Call or Text for a Free Estimate</a>
        <a class="btn btn-ghost" href="/contact/">Other ways to reach us</a>
      </div>
    </div>
  </section>

  <section class="band-warm">
    <div class="wrap">
      <div class="prose">
        <h2>What&rsquo;s included</h2>
        <ul>
          <li><strong>Exterior glass</strong>, hand-washed and squeegeed rather than blasted with a pressure washer.</li>
          <li><strong>Frames and sills</strong>, where the dirt film, cobwebs and dead bugs actually collect.</li>
          <li><strong>Screens on request</strong> &mdash; pulled, rinsed and put back, so they don&rsquo;t redeposit dust on glass you just paid to clean.</li>
        </ul>
        <p>Windows are one of the few exterior jobs where high pressure is the wrong tool. Force water at an older window and you can push it past the seal or damage the glazing. So this is hand work.</p>

        <h2>Spring pollen is the reason most people call</h2>
        <p>Pine pollen coats everything in this part of Louisiana for a few weeks each spring, and glass shows it worse than anything else &mdash; a yellow-green haze you notice from inside every time the sun hits it. Washing once the pollen drop is finished gets you clear windows for the rest of the year.</p>

        <h2>Book it with a house wash</h2>
        <p>Windows and <a href="/pressure-washing/">house washing</a> belong on the same visit. We wash the siding first, then do the glass &mdash; otherwise the runoff from the walls lands on windows we just cleaned. Add <a href="/landscaping/">flowerbed cleanup</a> and the whole front of the house gets handled in one trip.</p>
      </div>
    </div>
  </section>

%(faq)s%(related)s%(contact)s''' % {
        "jt": BIZ["jase_tel"],
        "faq": faq_block(faqs, "Window washing questions we get asked"),
        "related": related_block(path),
        "contact": contact_section(
            heading="Get a free window washing estimate",
            intro="Tell us roughly how many windows and how many stories and we&rsquo;ll get you a number."),
    }

    return render(
        path,
        "Window Cleaning in Monroe &amp; West Monroe, LA | Precision Wash",
        "Hand-washed exterior windows, frames and sills in Monroe, West Monroe and Ruston, LA. Screens on request. "
        "Free estimates &mdash; call or text 318-805-8288.",
        body,
        [
            service_schema(
                "Window washing",
                "Hand-washed exterior window cleaning including glass, frames and sills, with screen cleaning on "
                "request, in Ouachita and Lincoln Parish, Louisiana.",
                path, "Window cleaning service"),
            breadcrumb_schema(trail),
            faq_schema(faqs),
        ],
        trail=trail,
        accent="glass",
    )


PAGES.append(("/window-washing/", window_washing))


# ---------- Service area ----------
def service_area():
    path = "/service-area/"
    trail = [("/", "Home"), (path, "Service Area")]

    faqs = [
        ("I&rsquo;m outside Monroe, West Monroe and Ruston &mdash; will you still come?",
         "Often, yes. Those three are simply where most of our work is. If you&rsquo;re elsewhere in Ouachita or "
         "Lincoln Parish, or just over a parish line, call or text with your address and we&rsquo;ll tell you straight "
         "away whether we can get to you."),
        ("Do you charge a travel fee?",
         "Any travel is built into the estimate you approve before work starts. You will not get a separate trip "
         "charge added afterward."),
        ("Do you work on commercial property?",
         "Yes &mdash; rentals, small commercial buildings and turnover cleanups get the same washing, flowerbed and "
         "hauling services as houses."),
    ]

    body = '''  <section class="page-hero">
    <div class="wrap">
      <p class="eyebrow">Where we work</p>
      <h1>Our Service Area: Ouachita &amp; Lincoln Parish, Louisiana</h1>
      <p class="lede">Precision Wash &amp; Landscape is a service-area business &mdash; we come to you. Most of our pressure washing, flowerbed and hauling work is in Monroe, West Monroe and Ruston and the communities around them.</p>
      <div class="hero-ctas">
        <a class="btn btn-primary" href="tel:1%(jt)s" data-track="svc-call">Call or Text &mdash; %(jd)s</a>
      </div>
    </div>
  </section>

  <section class="area-section">
    <div class="wrap">
      <div>
        <h2 class="section-title">The two parishes we cover</h2>
        <div class="parish-list">
          <div class="parish-item"><span class="name">Ouachita Parish</span><span class="note">Monroe, West Monroe and the surrounding communities</span></div>
          <div class="parish-item"><span class="name">Lincoln Parish</span><span class="note">Ruston and the surrounding communities</span></div>
        </div>
        <p class="lede" style="margin-top:var(--space-3);">On the edge of that? Call &mdash; we&rsquo;ll tell you straight whether we can get to you rather than leave you guessing.</p>
      </div>
      <div class="map-card">
        <svg viewBox="0 0 320 220" width="100%%" role="img" aria-label="Simplified map showing Ouachita and Lincoln Parish service area">
          <rect x="20" y="30" width="130" height="140" rx="4" fill="none" stroke="#22303f" stroke-width="1.5"/>
          <rect x="150" y="30" width="130" height="140" rx="4" fill="none" stroke="#22303f" stroke-width="1.5"/>
          <rect x="20" y="30" width="130" height="140" rx="4" fill="#17335c" opacity="0.35"/>
          <rect x="150" y="30" width="130" height="140" rx="4" fill="#17335c" opacity="0.2"/>
          <circle cx="85" cy="100" r="4" fill="#7fc0ff"/>
          <circle cx="215" cy="95" r="4" fill="#7fc0ff"/>
          <text x="85" y="185" text-anchor="middle" fill="#93a4b6" font-size="12" font-family="sans-serif">Ouachita</text>
          <text x="215" y="185" text-anchor="middle" fill="#93a4b6" font-size="12" font-family="sans-serif">Lincoln</text>
        </svg>
      </div>
    </div>
  </section>

  <section class="band-warm">
    <div class="wrap">
      <div class="prose">
        <h2>Monroe &amp; West Monroe</h2>
        <p>The bulk of our work sits on both sides of the Ouachita River. It&rsquo;s a mix of older established neighborhoods with mature tree cover and newer subdivisions &mdash; and the tree cover is exactly what drives the calls. Shade keeps siding and concrete damp, and damp is what mildew and algae need. If your driveway is green and your north wall is streaked, that&rsquo;s why.</p>
        <p>What we do most here: <a href="/pressure-washing/">house and driveway washing</a>, <a href="/landscaping/">flowerbed cleanout with fresh pine straw</a>, and limb and furniture <a href="/junk-removal/">haul-off</a>.</p>

        <h2>Ruston</h2>
        <p>About half an hour east on I-20, and a different mix &mdash; a college town with a heavy rental and turnover market alongside owner-occupied homes. Rental turnovers tend to need the full run: wash the exterior, clear out what the last tenant left, reset the beds. We take those.</p>

        <h2>Everywhere else in Ouachita &amp; Lincoln Parish</h2>
        <p>We don&rsquo;t keep a list of every community we&rsquo;ll drive to, because the honest answer depends on the day and the size of the job. Call or text your address and what you need done. If it isn&rsquo;t a fit we&rsquo;ll say so rather than waste your time.</p>

        <h2>What we bring to you</h2>
        <p>Because we&rsquo;re a service-area business, there&rsquo;s no shop for you to visit &mdash; the equipment and the truck come to your property. All four services travel:</p>
        <ul>
          <li><a href="/pressure-washing/">Soft and pressure washing</a> &mdash; siding, roofs, driveways, patios, gutters, fences</li>
          <li><a href="/landscaping/">Flowerbed cleanup</a> &mdash; weeding, mulch, pine straw, trimming, planting</li>
          <li><a href="/junk-removal/">Junk removal and hauling</a> &mdash; limbs, furniture, cleanouts</li>
          <li><a href="/window-washing/">Window washing</a> &mdash; exterior glass, frames, sills</li>
        </ul>
        <p>All we need on site is an outdoor water spigot and an outlet.</p>
      </div>
    </div>
  </section>

%(faq)s%(contact)s''' % {
        "jt": BIZ["jase_tel"], "jd": BIZ["jase_display"],
        "faq": faq_block(faqs, "Service area questions"),
        "contact": contact_section(
            heading="Not sure if you&rsquo;re in range? Just ask",
            intro="Send your address and what you need done. We&rsquo;ll tell you yes or no and price it either way."),
    }

    return render(
        path,
        "Service Area: Monroe, West Monroe &amp; Ruston, LA | Precision Wash",
        "Precision Wash &amp; Landscape serves Ouachita and Lincoln Parish, LA &mdash; Monroe, West Monroe, Ruston "
        "and nearby communities. Free estimates &mdash; call or text 318-805-8288.",
        body,
        [breadcrumb_schema(trail), faq_schema(faqs)],
        trail=trail,
    )


PAGES.append(("/service-area/", service_area))


# ---------- Contact ----------
def contact():
    path = "/contact/"
    trail = [("/", "Home"), (path, "Free Estimate")]

    body = '''  <section class="page-hero">
    <div class="wrap">
      <p class="eyebrow">Free estimates</p>
      <h1>Get a Free Estimate from Precision Wash &amp; Landscape</h1>
      <p class="lede">There&rsquo;s no form to fill out and no call center. Call or text Jase or Garrett directly and you&rsquo;ll get a real answer from the people who will do the work.</p>
      <div class="hero-ctas">
        <a class="btn btn-primary" href="tel:1%(jt)s" data-track="contact-call-jase">Call %(jd)s</a>
        <a class="btn btn-ghost" href="sms:+1%(jt)s" data-track="contact-sms-jase">Text %(jd)s</a>
      </div>
    </div>
  </section>

  <section class="band-warm">
    <div class="wrap">
      <div class="prose">
        <h2>Texting is usually fastest</h2>
        <p>We&rsquo;re on job sites most of the day, so a text often gets answered sooner than a call. Four things get you an accurate estimate in one message:</p>
        <ul>
          <li><strong>Your address</strong> &mdash; or at least the city, so we know it&rsquo;s in range.</li>
          <li><strong>What you want done</strong> &mdash; wash the house, redo the beds, haul off a pile, clean the windows, or some combination.</li>
          <li><strong>A photo or two.</strong> This is the big one. Pictures of the driveway, the siding, the beds or the junk pile tell us more than a paragraph does, and they&rsquo;re the difference between a rough guess and a real number.</li>
          <li><strong>When you&rsquo;d like it done</strong> &mdash; if you have a deadline, say so up front.</li>
        </ul>

        <h2>What happens next</h2>
        <p>We come back with a free, no-obligation estimate. If it works for you, we find a date. If it doesn&rsquo;t, no hard feelings and no follow-up pestering. Nothing gets charged and no work starts until you&rsquo;ve approved the number.</p>

        <h2>Who you&rsquo;re calling</h2>
        <p>Precision Wash &amp; Landscape is family-run and owner-operated. Jase LaBorde and Garrett Smith own the business and do the work themselves &mdash; you&rsquo;re not going to get one person on the phone and strangers in the driveway.</p>
      </div>
    </div>
  </section>

  <section class="contact-section" id="contact">
    <div class="wrap">
      <p class="eyebrow">Reach us</p>
      <h2 class="section-title">Call, text, or message us on Facebook</h2>
      <div class="contact-grid">
        <a class="contact-card" href="tel:1%(jt)s" data-track="call-jase">
          <span class="role">Owner &middot; call</span>
          <span class="name">%(jn)s</span>
          <span class="num">%(jd)s</span>
        </a>
        <a class="contact-card" href="sms:+1%(jt)s" data-track="sms-jase">
          <span class="role">Owner &middot; text a photo</span>
          <span class="name">Text Jase</span>
          <span class="num">%(jd)s</span>
        </a>
        <a class="contact-card" href="tel:1%(gt)s" data-track="call-garrett">
          <span class="role">Owner &middot; call</span>
          <span class="name">%(gn)s</span>
          <span class="num">%(gd)s</span>
        </a>
        <a class="contact-card" href="sms:+1%(gt)s" data-track="sms-garrett">
          <span class="role">Owner &middot; text a photo</span>
          <span class="name">Text Garrett</span>
          <span class="num">%(gd)s</span>
        </a>
        <a class="contact-card" href="%(fb)s" target="_blank" rel="noopener noreferrer" data-track="facebook">
          <span class="role">Follow us</span>
          <span class="name">Facebook</span>
          <span class="num">Precision Wash &amp; Landscape</span>
        </a>
        <a class="contact-card" href="/service-area/">
          <span class="role">Before you call</span>
          <span class="name">Service area</span>
          <span class="num">Ouachita &amp; Lincoln</span>
        </a>
      </div>
    </div>
  </section>

  <section>
    <div class="wrap">
      <h2 class="section-title">What can we quote for you?</h2>
      <div class="related-grid">
        <a class="related-card" href="/pressure-washing/"><span class="name">Pressure washing</span><span class="note">Siding, roofs, driveways, patios, gutters, fences.</span></a>
        <a class="related-card" href="/landscaping/"><span class="name">Flowerbed work</span><span class="note">Cleanout, weeding, mulch, pine straw, trimming.</span></a>
        <a class="related-card" href="/junk-removal/"><span class="name">Junk removal</span><span class="note">Limbs, storm debris, furniture, cleanouts.</span></a>
        <a class="related-card" href="/window-washing/"><span class="name">Window washing</span><span class="note">Exterior glass, frames and sills.</span></a>
      </div>
    </div>
  </section>
''' % {
        "jt": BIZ["jase_tel"], "jd": BIZ["jase_display"], "jn": BIZ["jase_name"],
        "gt": BIZ["garrett_tel"], "gd": BIZ["garrett_display"], "gn": BIZ["garrett_name"],
        "fb": BIZ["facebook"],
    }

    contact_page = '''{
  "@context": "https://schema.org",
  "@type": "ContactPage",
  "url": "%s/contact/",
  "name": "Contact Precision Wash & Landscape",
  "about": { "@id": "%s" }
}''' % (SITE, BUSINESS_ID)

    return render(
        path,
        "Free Estimate &mdash; Call or Text | Precision Wash &amp; Landscape",
        "Free pressure washing, flowerbed, hauling and window washing estimates in Monroe, West Monroe and Ruston, "
        "LA. Call or text Jase at 318-805-8288.",
        body,
        [contact_page, breadcrumb_schema(trail)],
        trail=trail,
    )


PAGES.append(("/contact/", contact))


# ---------- 404 ----------
def not_found():
    path = "/404.html"
    body = '''  <section class="notfound">
    <div class="wrap">
      <p class="code">404</p>
      <h1 class="section-title" style="margin-top:var(--space-2);">That page isn&rsquo;t here</h1>
      <p class="lede" style="margin-top:var(--space-2);">The link may be old or mistyped. Here&rsquo;s everything on the site &mdash; or just call or text us and we&rsquo;ll answer directly.</p>
      <div class="hero-ctas">
        <a class="btn btn-primary" href="tel:1%(jt)s" data-track="404-call">Call or Text &mdash; %(jd)s</a>
        <a class="btn btn-ghost" href="/">Back to the homepage</a>
      </div>
      <div class="related-grid" style="margin-top:var(--space-4);">
        <a class="related-card" href="/pressure-washing/"><span class="name">Pressure washing</span><span class="note">House, driveway, patio, roof and gutter washing.</span></a>
        <a class="related-card" href="/landscaping/"><span class="name">Flowerbed work</span><span class="note">Cleanout, mulch, pine straw, trimming, planting.</span></a>
        <a class="related-card" href="/junk-removal/"><span class="name">Junk removal</span><span class="note">Limbs, storm debris, furniture, cleanouts.</span></a>
        <a class="related-card" href="/window-washing/"><span class="name">Window washing</span><span class="note">Exterior glass, frames and sills.</span></a>
        <a class="related-card" href="/service-area/"><span class="name">Service area</span><span class="note">Monroe, West Monroe, Ruston and beyond.</span></a>
        <a class="related-card" href="/contact/"><span class="name">Free estimate</span><span class="note">Call or text Jase or Garrett directly.</span></a>
      </div>
    </div>
  </section>
''' % {"jt": BIZ["jase_tel"], "jd": BIZ["jase_display"]}

    return render(
        path,
        "Page Not Found | Precision Wash &amp; Landscape",
        "That page isn&rsquo;t on our site. Browse our pressure washing, flowerbed, junk removal and window washing "
        "services, or call 318-805-8288.",
        body,
        [],
        noindex=True,
    )


PAGES.append(("/404.html", not_found))


# --------------------------------------------------------------------------
# robots.txt + sitemap.xml
# --------------------------------------------------------------------------
def robots_txt():
    return """User-agent: *
Allow: /

# Every customer-facing page is meant to be indexed. The two folders below are
# repo housekeeping (SEO notes and the page generator), not site content, and
# nothing on the site links to them.
Disallow: /docs/
Disallow: /tools/

Sitemap: %s/sitemap.xml
""" % SITE


def sitemap_xml(paths):
    # Only canonical, indexable, 200-status URLs belong here. 404.html is excluded
    # because it is noindex.
    urls = []
    for p in paths:
        priority = "1.0" if p == "/" else ("0.9" if p in ("/pressure-washing/", "/contact/") else "0.8")
        urls.append('''  <url>
    <loc>%s%s</loc>
    <lastmod>%s</lastmod>
    <changefreq>monthly</changefreq>
    <priority>%s</priority>
  </url>''' % (SITE, p, TODAY, priority))
    return '''<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
%s
</urlset>
''' % "\n".join(urls)


# --------------------------------------------------------------------------
def main():
    written = []
    indexable = []
    for path, fn in PAGES:
        written.append(write(path, fn()))
        if not path.endswith(".html"):
            indexable.append(path)

    io.open(os.path.join(ROOT, "robots.txt"), "w", encoding="utf-8", newline="\n").write(robots_txt())
    io.open(os.path.join(ROOT, "sitemap.xml"), "w", encoding="utf-8", newline="\n").write(sitemap_xml(indexable))
    written += ["robots.txt", "sitemap.xml"]

    for f in written:
        print("wrote", f)
    print("\n%d pages, %d in sitemap" % (len(PAGES), len(indexable)))


if __name__ == "__main__":
    main()
