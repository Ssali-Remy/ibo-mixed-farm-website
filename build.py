#!/usr/bin/env python3
"""
Static site builder for IBO Mixed Farm Ltd.

Wraps each page body in `src/` with the shared head, header, navigation and
footer, and writes plain HTML files to the project root ready for upload to
any host. No dependencies.

    python build.py

Edit page content in `src/`. Edit the shared chrome in this file.
"""

from __future__ import annotations

import json
import re
from pathlib import Path

ROOT = Path(__file__).parent
SRC = ROOT / "src"

SITE_URL = "https://www.ibomixfarm.com"

# Order matters: this drives both the desktop and mobile navigation.
NAV = [
    ("index.html", "Home", "Home"),
    ("about.html", "About", "About the farm"),
    ("training.html", "Training", "Training &amp; skilling"),
    ("services.html", "Services", "Services &amp; products"),
    ("gallery.html", "Gallery", "Gallery"),
    ("journal.html", "Farming Tips", "Farming tips"),
    ("contact.html", "Contact", "Contact &amp; visit"),
]

ORG_SCHEMA = {
    "@context": "https://schema.org",
    "@type": ["Farm", "EducationalOrganization"],
    "name": "IBO Mixed Farm Ltd",
    "slogan": "Optimum Utilization of Land",
    "foundingDate": "2004",
    "url": SITE_URL,
    "description": (
        "A UVTAB-accredited agricultural skilling centre and commercial mixed farm in "
        "Bwizibwera, Mbarara, Uganda, offering practical training, banana macro-propagation "
        "plantlets, soil testing, farm layout design and plant clinic services."
    ),
    "email": "ibomixedfarm@gmail.com",
    "address": {
        "@type": "PostalAddress",
        "streetAddress": "Bwizibwera, Rwanyamahembe Sub-county",
        "addressLocality": "Mbarara",
        "addressRegion": "Western Region",
        "addressCountry": "UG",
    },
    "areaServed": "Uganda",
    "knowsAbout": [
        "Banana macro-propagation",
        "Dairy farming",
        "Soil testing",
        "Farm layout design",
        "Plant disease diagnosis",
        "Apiculture",
    ],
}


def head(meta: dict, page: str) -> str:
    extra = meta.get("head", "")
    schema = json.dumps(ORG_SCHEMA, indent=2) if page == "index.html" else None
    schema_block = (
        f'\n<script type="application/ld+json">\n{schema}\n</script>\n' if schema else ""
    )
    canonical = SITE_URL + ("/" if page == "index.html" else "/" + page)

    return f"""<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{meta['title']}</title>
<meta name="description" content="{meta['description']}">
<link rel="canonical" href="{canonical}">
<link rel="icon" type="image/png" href="assets/img/favicon-32.png">
<link rel="apple-touch-icon" href="assets/img/ibo-logo-128.png">

<meta property="og:type" content="website">
<meta property="og:site_name" content="IBO Mixed Farm Ltd">
<meta property="og:title" content="{meta.get('og_title', meta['title'])}">
<meta property="og:description" content="{meta['description']}">
<meta property="og:url" content="{canonical}">
<meta property="og:locale" content="en_UG">
<meta name="twitter:card" content="summary_large_image">
<meta name="theme-color" content="#10301c">

<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Fraunces:opsz,wght@9..144,400;9..144,600;9..144,700&amp;family=Inter:wght@400;500;600;700&amp;display=swap" rel="stylesheet">
<link rel="stylesheet" href="assets/css/style.css">
{extra}{schema_block}"""


def header(page: str) -> str:
    desktop = "\n".join(
        '        <li><a class="nav__link" href="{href}"{cur}>{label}</a></li>'.format(
            href=href, label=label, cur=' aria-current="page"' if href == page else ""
        )
        for href, label, _ in NAV
    )
    mobile = "\n".join(
        '        <li><a class="mobile-nav__link" href="{href}"{cur}>{label}</a></li>'.format(
            href=href, label=long, cur=' aria-current="page"' if href == page else ""
        )
        for href, _, long in NAV
    )

    return f"""<div class="topbar">
  <div class="wrap topbar__inner">
    <span>UVTAB-accredited skilling centre &middot; Bwizibwera, Mbarara</span>
    <span class="topbar__sep">&bull;</span>
    <span class="topbar__item--optional">Trainings run on demand — <a href="training.html#book">book your dates</a></span>
  </div>
</div>

<header class="site-header">
  <div class="wrap site-header__inner">
    <a class="brand" href="index.html">
      <img class="brand__logo" src="assets/img/ibo-logo-128.png" alt="" width="44" height="44" aria-hidden="true">
      <span class="brand__text">
        <span class="brand__name">IBO Mixed Farm</span>
        <span class="brand__tag">Optimum Utilization of Land</span>
      </span>
    </a>

    <nav class="nav" aria-label="Main">
      <ul class="nav__list">
{desktop}
      </ul>
    </nav>

    <a class="btn btn--primary btn--sm header__cta" href="training.html#book">Book a training</a>

    <button class="nav-toggle" type="button" aria-expanded="false" aria-controls="mobile-nav">
      <span class="nav-toggle__bars" aria-hidden="true"></span>
      <span class="nav-toggle__label">Menu</span>
    </button>
  </div>

  <div class="mobile-nav" id="mobile-nav">
    <div class="wrap">
      <ul class="mobile-nav__list">
{mobile}
      </ul>
      <a class="btn btn--primary btn--block" href="training.html#book">Book a training</a>
    </div>
  </div>
</header>"""


FOOTER = """<footer class="site-footer">
  <div class="wrap">
    <div class="footer__grid">
      <div class="footer__brand">
        <a class="brand" href="index.html">
          <img class="brand__logo" src="assets/img/ibo-logo-128.png" alt="" width="44" height="44" aria-hidden="true">
          <span class="brand__text">
            <span class="brand__name">IBO Mixed Farm Ltd</span>
            <span class="brand__tag">Optimum Utilization of Land</span>
          </span>
        </a>
        <p>
          A UVTAB-accredited agricultural skilling centre and commercial mixed
          farm in Bwizibwera, Mbarara, Uganda. Family owned and farming since
          2004.
        </p>
        <div class="social-row">
          <a href="https://www.facebook.com/share/1DissK6T9m/" aria-label="Facebook" title="Facebook" target="_blank" rel="noopener"><svg viewBox="0 0 24 24" aria-hidden="true"><path d="M22 12a10 10 0 1 0-11.6 9.9v-7H7.9V12h2.5V9.8c0-2.5 1.5-3.9 3.8-3.9 1.1 0 2.2.2 2.2.2v2.5h-1.3c-1.2 0-1.6.8-1.6 1.6V12h2.8l-.4 2.9h-2.4v7A10 10 0 0 0 22 12Z"/></svg></a>
          <a href="https://www.instagram.com/ibomixedfarm" aria-label="Instagram" title="Instagram" target="_blank" rel="noopener"><svg viewBox="0 0 24 24" aria-hidden="true"><path d="M12 2.2c3.2 0 3.6 0 4.9.1 1.2.1 1.8.2 2.2.4.6.2 1 .5 1.4.9.4.4.7.8.9 1.4.2.4.4 1 .4 2.2.1 1.3.1 1.7.1 4.9s0 3.6-.1 4.9c-.1 1.2-.2 1.8-.4 2.2-.2.6-.5 1-.9 1.4-.4.4-.8.7-1.4.9-.4.2-1 .4-2.2.4-1.3.1-1.7.1-4.9.1s-3.6 0-4.9-.1c-1.2-.1-1.8-.2-2.2-.4-.6-.2-1-.5-1.4-.9-.4-.4-.7-.8-.9-1.4-.2-.4-.4-1-.4-2.2-.1-1.3-.1-1.7-.1-4.9s0-3.6.1-4.9c.1-1.2.2-1.8.4-2.2.2-.6.5-1 .9-1.4.4-.4.8-.7 1.4-.9.4-.2 1-.4 2.2-.4 1.3-.1 1.7-.1 4.9-.1Zm0 3.8a6 6 0 1 0 0 12 6 6 0 0 0 0-12Zm0 9.9a3.9 3.9 0 1 1 0-7.8 3.9 3.9 0 0 1 0 7.8Zm7.6-10.1a1.4 1.4 0 1 1-2.8 0 1.4 1.4 0 0 1 2.8 0Z"/></svg></a>
          <a href="https://www.tiktok.com/@ibo.mixed.farm" aria-label="TikTok" title="TikTok" target="_blank" rel="noopener"><svg viewBox="0 0 24 24" aria-hidden="true"><path d="M16.6 2h-3.3v13.9c0 1.6-1.3 2.9-2.9 2.9a2.9 2.9 0 0 1-2.9-2.9 2.9 2.9 0 0 1 2.9-2.9c.3 0 .6 0 .9.1v-3.4a6.3 6.3 0 0 0-.9-.1A6.3 6.3 0 0 0 4 15.9a6.3 6.3 0 0 0 6.4 6.3 6.3 6.3 0 0 0 6.3-6.3V8.6a8.2 8.2 0 0 0 4.8 1.5V6.8a4.8 4.8 0 0 1-4.9-4.8Z"/></svg></a>
          <a href="#" aria-label="YouTube" title="YouTube — link to be added"><svg viewBox="0 0 24 24" aria-hidden="true"><path d="M23 12s0-3.5-.4-5.1a2.7 2.7 0 0 0-1.9-1.9C19 4.5 12 4.5 12 4.5s-7 0-8.7.5a2.7 2.7 0 0 0-1.9 1.9C1 8.5 1 12 1 12s0 3.5.4 5.1a2.7 2.7 0 0 0 1.9 1.9c1.7.5 8.7.5 8.7.5s7 0 8.7-.5a2.7 2.7 0 0 0 1.9-1.9C23 15.5 23 12 23 12ZM9.8 15.3V8.7l5.7 3.3-5.7 3.3Z"/></svg></a>
          <a href="https://x.com/ibomixedfarm" aria-label="X" title="X" target="_blank" rel="noopener"><svg viewBox="0 0 24 24" aria-hidden="true"><path d="M17.5 3h3.1l-6.8 7.8L21.8 21h-6.2l-4.9-6.4L5.1 21H2l7.3-8.3L2.4 3h6.4l4.4 5.8L17.5 3Zm-1.1 16.1h1.7L7.7 4.8H5.9l10.5 14.3Z"/></svg></a>
        </div>
      </div>

      <div>
        <h4>Explore</h4>
        <ul class="footer__list">
          <li><a href="about.html">About the farm</a></li>
          <li><a href="training.html">Training &amp; skilling</a></li>
          <li><a href="services.html">Services &amp; products</a></li>
          <li><a href="gallery.html">Gallery</a></li>
          <li><a href="journal.html">Farming tips</a></li>
          <li><a href="contact.html">Contact</a></li>
        </ul>
      </div>

      <div>
        <h4>Popular</h4>
        <ul class="footer__list">
          <li><a href="training.html#book">Book a training</a></li>
          <li><a href="services.html#plantlets">Order banana plantlets</a></li>
          <li><a href="services.html#soil">Soil testing</a></li>
          <li><a href="services.html#layout">Farm layout design</a></li>
          <li><a href="services.html#clinic">Plant clinic</a></li>
          <li><a href="contact.html#visit">Arrange a farm visit</a></li>
        </ul>
      </div>

      <div>
        <h4>Find us</h4>
        <ul class="footer__list">
          <li>Bwizibwera, Rwanyamahembe Sub-county<br>Mbarara, Uganda</li>
          <li><a data-email-link href="mailto:ibomixedfarm@gmail.com"><span data-email-text>ibomixedfarm@gmail.com</span></a></li>
          <li><a data-phone-link href="tel:"><span data-phone-text>+256 700 000 000</span></a></li>
          <li><a href="#" data-whatsapp>Chat on WhatsApp</a></li>
        </ul>
        <p style="font-size:.8rem;opacity:.75;margin-top:1rem">
          Visits and trainings by prior arrangement.
        </p>
      </div>
    </div>

    <div class="footer__legal">
      <p>&copy; <span data-year>2026</span> IBO Mixed Farm Ltd. All rights reserved.</p>
      <p>Company Reg. No. 800100012599401 &middot; TIN 1049266795 &middot; UVTAB / DIT Centre No. MAC/1269</p>
    </div>
  </div>
</footer>

<a class="wa-float" href="#" data-whatsapp aria-label="Chat with us on WhatsApp">
  <svg viewBox="0 0 24 24" aria-hidden="true"><path d="M12 2a10 10 0 0 0-8.6 15L2 22l5.2-1.4A10 10 0 1 0 12 2Zm0 18.2a8.2 8.2 0 0 1-4.2-1.2l-.3-.2-3.1.8.8-3-.2-.3A8.2 8.2 0 1 1 12 20.2Zm4.5-6.1c-.2-.1-1.5-.7-1.7-.8s-.4-.1-.6.1-.6.8-.8 1-.3.2-.6.1a6.7 6.7 0 0 1-2-1.2 7.5 7.5 0 0 1-1.4-1.7c-.1-.3 0-.4.1-.5l.4-.5.3-.4v-.4l-.8-1.9c-.2-.5-.4-.4-.6-.4h-.5a1 1 0 0 0-.7.3 3 3 0 0 0-.9 2.2A5.2 5.2 0 0 0 8 13a11.9 11.9 0 0 0 4.6 4 15.5 15.5 0 0 0 1.5.6 3.7 3.7 0 0 0 1.7.1 2.8 2.8 0 0 0 1.8-1.3 2.3 2.3 0 0 0 .2-1.3c-.1-.1-.3-.2-.5-.3Z"/></svg>
  <span class="wa-float__text">WhatsApp</span>
</a>

<script src="assets/js/main.js"></script>"""


META_RE = re.compile(r"^<!--META\s*(\{.*?\})\s*-->\s*", re.S)


def build_page(src_file: Path) -> str:
    raw = src_file.read_text(encoding="utf-8")
    match = META_RE.match(raw)
    if not match:
        raise SystemExit(f"{src_file.name}: missing <!--META {{...}}--> block at top of file")

    meta = json.loads(match.group(1))
    body = raw[match.end():].rstrip()
    page = src_file.name

    return (
        "<!DOCTYPE html>\n"
        '<html lang="en">\n'
        "<head>\n"
        + head(meta, page)
        + "</head>\n"
        "<body>\n\n"
        '<a class="skip-link" href="#main">Skip to content</a>\n\n'
        + header(page)
        + '\n\n<main id="main">\n\n'
        + body
        + "\n\n</main>\n\n"
        + FOOTER
        + "\n</body>\n</html>\n"
    )


def write_sitemap(pages: list[str]) -> None:
    """Emit sitemap.xml and robots.txt so they can never drift from the page list."""
    urls = []
    for page in pages:
        loc = SITE_URL + ("/" if page == "index.html" else "/" + page)
        priority = "1.0" if page == "index.html" else "0.8"
        urls.append(
            f"  <url>\n    <loc>{loc}</loc>\n"
            f"    <changefreq>monthly</changefreq>\n"
            f"    <priority>{priority}</priority>\n  </url>"
        )

    (ROOT / "sitemap.xml").write_text(
        '<?xml version="1.0" encoding="UTF-8"?>\n'
        '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
        + "\n".join(urls)
        + "\n</urlset>\n",
        encoding="utf-8",
    )

    (ROOT / "robots.txt").write_text(
        "User-agent: *\nAllow: /\n\nSitemap: " + SITE_URL + "/sitemap.xml\n",
        encoding="utf-8",
    )


def main() -> None:
    sources = sorted(SRC.glob("*.html"))
    if not sources:
        raise SystemExit("No page sources found in src/")

    for src_file in sources:
        out = ROOT / src_file.name
        out.write_text(build_page(src_file), encoding="utf-8")
        print(f"  built  {src_file.name}")

    # index.html first, then the rest in navigation order
    ordered = [href for href, _, _ in NAV if (SRC / href).exists()]
    write_sitemap(ordered)
    print("  built  sitemap.xml, robots.txt")

    print(f"\n{len(sources)} pages written to {ROOT}")


if __name__ == "__main__":
    main()
