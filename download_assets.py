#!/usr/bin/env python3
"""Download alle externe afbeeldingen naar /images en herschrijf de img src's.

Gebruik: python3 download_assets.py

Dit script:
1. Doorloopt alle .html en pages/*.html bestanden
2. Vindt alle <img src="https://www.werken-glorieux.be/..."> referenties
3. Downloadt de bestanden naar images/
4. Herschrijft de src naar de lokale path

Run dit op een netwerk dat werken-glorieux.be wel kan bereiken.
"""

import re
import os
import urllib.request
import urllib.parse
from pathlib import Path

ROOT = Path(__file__).parent
IMAGES_DIR = ROOT / 'images'
IMAGES_DIR.mkdir(exist_ok=True)

EXTERNAL_HOSTS = ('www.werken-glorieux.be', 'werken-glorieux.be')

def safe_filename(url):
    """Maak een veilige bestandsnaam uit een URL."""
    parsed = urllib.parse.urlparse(url)
    path = urllib.parse.unquote(parsed.path)
    # Pak laatste segment als basis
    name = os.path.basename(path)
    # Vervang spaties en speciale chars
    name = re.sub(r'[^\w\-.]', '_', name)
    return name

def download(url, dest):
    if dest.exists():
        return
    print(f"  download: {url} → {dest.name}")
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    with urllib.request.urlopen(req, timeout=30) as resp:
        dest.write_bytes(resp.read())

def process_file(path):
    text = path.read_text(encoding='utf-8')
    pattern = re.compile(r'src="(https?://[^"]+)"')
    changed = False
    new_text = text
    for match in pattern.finditer(text):
        url = match.group(1)
        parsed = urllib.parse.urlparse(url)
        if parsed.netloc not in EXTERNAL_HOSTS:
            continue
        filename = safe_filename(url)
        local_path = IMAGES_DIR / filename
        try:
            download(url, local_path)
        except Exception as e:
            print(f"  ! kon niet downloaden: {url} ({e})")
            continue
        # Herschrijf de src
        new_url = f'images/{filename}'
        new_text = new_text.replace(f'src="{url}"', f'src="{new_url}"')
        changed = True
    if changed:
        path.write_text(new_text, encoding='utf-8')
        print(f"  bijgewerkt: {path.relative_to(ROOT)}")

def main():
    files = list(ROOT.glob('*.html')) + list((ROOT / 'pages').glob('*.html'))
    print(f"Verwerk {len(files)} bestanden...")
    for f in files:
        process_file(f)
    print("Klaar.")

if __name__ == '__main__':
    main()
