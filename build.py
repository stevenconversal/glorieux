#!/usr/bin/env python3
"""Build script: wrap each fragment in pages/ with shared header + footer."""
import re
from pathlib import Path

ROOT = Path(__file__).parent
PAGES_DIR = ROOT / "pages"
OUT_DIR = ROOT

HEADER = """<!-- ============== HEADER ============== -->
<header class="site-header">
  <div class="header-top">
    <div class="header-top__inner">
      <a href="http://www.hrglorieux.be">HR Glorieux</a>
      <a href="bereikbaarheid.html">Bereikbaarheid</a>
      <a href="contact.html">Contact</a>
    </div>
  </div>
  <div class="header-main">
    <a href="index.html" class="brand" aria-label="vzw Werken Glorieux home">
      <img src="images/logo-mark.svg" alt="" class="brand__svg" aria-hidden="true">
      <span class="brand__wordmark">vzwWerken<span class="secondary">Glorieux</span></span>
      <span class="brand__suffix hide-on-mobile">Ronse</span>
    </a>
    <nav class="nav-primary" aria-label="Hoofdnavigatie">
      <ul>
        <li><a href="index.html">Home</a></li>
        <li>
          <a href="vzw-werken-glorieux.html">vzw Werken Glorieux</a>
          <ul>
            <li><a href="eh-glorieux.html">E.H. Glorieux</a></li>
            <li><a href="organisatie.html">Organisatie</a></li>
            <li><a href="voorzieningen.html">Voorzieningen</a></li>
            <li><a href="opdrachtsverklaring.html">Opdrachtsverklaring</a></li>
            <li><a href="werken-van-barmhartigheid.html">Werken van barmhartigheid</a></li>
            <li><a href="info-voor-leveranciers.html">Overheidsopdrachten</a></li>
          </ul>
        </li>
        <li><a href="gezondheidszorg.html">Gezondheidszorg</a></li>
        <li><a href="kind-en-jeugdzorg.html">Kind- en Jeugdzorg</a></li>
        <li><a href="ouderenzorg.html">Ouderenzorg</a></li>
        <li><a href="nieuws.html">Nieuws</a></li>
      </ul>
    </nav>
    <button class="nav-toggle" aria-label="Open menu" aria-expanded="false">
      <span></span><span></span><span></span>
    </button>
  </div>
  <nav class="nav-mobile" aria-label="Mobiele navigatie">
    <ul>
      <li><a href="index.html">Home</a></li>
      <li>
        <a href="vzw-werken-glorieux.html">vzw Werken Glorieux</a>
        <ul>
          <li><a href="eh-glorieux.html">E.H. Glorieux</a></li>
          <li><a href="organisatie.html">Organisatie</a></li>
          <li><a href="voorzieningen.html">Voorzieningen</a></li>
          <li><a href="opdrachtsverklaring.html">Opdrachtsverklaring</a></li>
          <li><a href="werken-van-barmhartigheid.html">Werken van barmhartigheid</a></li>
          <li><a href="info-voor-leveranciers.html">Overheidsopdrachten</a></li>
        </ul>
      </li>
      <li><a href="gezondheidszorg.html">Gezondheidszorg</a></li>
      <li><a href="kind-en-jeugdzorg.html">Kind- en Jeugdzorg</a></li>
      <li><a href="ouderenzorg.html">Ouderenzorg</a></li>
      <li><a href="nieuws.html">Nieuws</a></li>
      <li><a href="bereikbaarheid.html">Bereikbaarheid</a></li>
      <li><a href="contact.html">Contact</a></li>
    </ul>
  </nav>
</header>"""

FOOTER = """<!-- ============== FOOTER ============== -->
<footer class="site-footer">
  <div class="container">
    <div class="footer-grid">
      <div class="footer-brand">
        <div class="brand-row">
          <img src="images/logo-mark.svg" alt="" class="brand__svg" aria-hidden="true">
          <span class="brand__wordmark">vzwWerken<span class="secondary">Glorieux</span></span>
        </div>
        <p>Glorieuxlaan 55<br>9600 Ronse</p>
        <p>Tel. <a href="tel:+3255233011">+32 55 23 30 11</a><br>Fax. +32 55 23 30 22</p>
        <div class="social-links">
          <a href="https://www.facebook.com/pages/VZW-Werken-Glorieux-en-AZ-Glorieux/218232794972510" aria-label="Facebook">
            <svg viewBox="0 0 24 24" fill="currentColor"><path d="M9 8h-3v4h3v12h5v-12h3.642l.358-4h-4v-1.667c0-.955.192-1.333 1.115-1.333h2.885v-5h-3.808c-3.596 0-5.192 1.583-5.192 4.615v3.385z"/></svg>
          </a>
          <a href="https://www.linkedin.com/company/vzw-werken-glorieux" aria-label="LinkedIn">
            <svg viewBox="0 0 24 24" fill="currentColor"><path d="M4.98 3.5c0 1.381-1.11 2.5-2.48 2.5s-2.48-1.119-2.48-2.5c0-1.38 1.11-2.5 2.48-2.5s2.48 1.12 2.48 2.5zm.02 4.5h-5v16h5v-16zm7.982 0h-4.968v16h4.969v-8.399c0-4.67 6.029-5.052 6.029 0v8.399h4.988v-10.131c0-7.88-8.922-7.593-11.018-3.714v-2.155z"/></svg>
          </a>
        </div>
      </div>

      <div class="footer-col">
        <h4>vzw Werken Glorieux</h4>
        <ul>
          <li><a href="eh-glorieux.html">E.H. Glorieux</a></li>
          <li><a href="organisatie.html">Organisatie</a></li>
          <li><a href="voorzieningen.html">Voorzieningen</a></li>
          <li><a href="opdrachtsverklaring.html">Opdrachtsverklaring</a></li>
          <li><a href="werken-van-barmhartigheid.html">Werken van barmhartigheid</a></li>
          <li><a href="info-voor-leveranciers.html">Overheidsopdrachten</a></li>
        </ul>
      </div>

      <div class="footer-col">
        <h4>Direct</h4>
        <ul>
          <li><a href="nieuws.html">Nieuws</a></li>
          <li><a href="contact.html">Contact</a></li>
          <li><a href="bereikbaarheid.html">Bereikbaarheid</a></li>
          <li><a href="http://hrglorieux.be">Vacatures (HR Glorieux)</a></li>
        </ul>
      </div>
    </div>

    <div class="footer-bottom">
      <span>&copy; <span id="yr">2026</span> vzw Werken Glorieux. Alle rechten voorbehouden.</span>
      <ul>
        <li><a href="gebruiksvoorwaarden.html">Gebruiksvoorwaarden</a></li>
        <li><a href="sitemap.html">Sitemap</a></li>
      </ul>
    </div>
  </div>
</footer>

<div class="cookie-banner" role="dialog" aria-live="polite">
  <p>vzw Werken Glorieux gebruikt cookies om het gebruik van onze site voor u gemakkelijker te maken. <a href="gebruiksvoorwaarden.html#cookiebeleid">Meer weten</a></p>
  <button type="button">Akkoord</button>
</div>

<script src="js/main.js"></script>
<script>document.getElementById('yr').textContent = new Date().getFullYear();</script>"""

WRAPPER = """<!DOCTYPE html>
<html lang="nl">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{title}</title>
  <meta name="description" content="{description}">
  <link rel="stylesheet" href="css/styles.css">
</head>
<body>

{header}

<main id="main-content">
{content}
</main>

{footer}

</body>
</html>"""

def build_pages():
    if not PAGES_DIR.exists():
        print("No pages dir found.")
        return
    for src in sorted(PAGES_DIR.glob("*.html")):
        text = src.read_text(encoding="utf-8")
        title_m = re.search(r"<!--\s*title:\s*(.*?)\s*-->", text)
        desc_m = re.search(r"<!--\s*desc:\s*(.*?)\s*-->", text)
        title = title_m.group(1) if title_m else src.stem.replace('-', ' ').title()
        desc = desc_m.group(1) if desc_m else ""
        content = re.sub(r"<!--\s*title:.*?-->\s*", "", text, count=1)
        content = re.sub(r"<!--\s*desc:.*?-->\s*", "", content, count=1)
        out = WRAPPER.format(title=title, description=desc, header=HEADER, content=content, footer=FOOTER)
        out_path = OUT_DIR / src.name
        out_path.write_text(out, encoding="utf-8")
        print(f"Built: {out_path.name}")

if __name__ == "__main__":
    build_pages()
