# vzw Werken Glorieux — statische herbouw

Statische HTML/CSS/JS herbouw van werken-glorieux.be, opgezet zodat er later een headless CMS kan boven worden geplaatst zonder de structuur te breken.

## Designprincipes

- **Refined editorial.** Sober, vertrouwenwekkend, afgestemd op de zorgsector.
- **Typografie:** Fraunces (display, serif, met italic) voor koppen en quotes. Inter voor body en UI. Source Sans 3 voor het wordmark.
- **Kleur:** lime `#cbd100` als hoofdaccent (huisstijl uit logo), met dieper `#6b6e00` voor tekst op licht. Zwart als donkere tegenkleur (footer). Warm-gebroken-wit als pagina-achtergrond.
- **Layout:** rustig, ruime witruimte, breadcrumbs, duidelijke hiërarchie. Lime accenten enkel als blok of streep, niet als tekstkleur (te weinig contrast op wit).

## Structuur

```
/
├── index.html                ← homepage
├── *.html                    ← gebouwde pagina's (output, 17 pagina's)
├── css/
│   └── styles.css            ← één design system, CSS-variabelen
├── js/
│   └── main.js               ← mobile nav, cookie banner, active nav
├── images/
│   └── logo-mark.svg         ← beeldmerk (cirkel + komma) als vector
├── pages/                    ← bron-fragmenten per pagina (alleen content)
│   └── *.html
├── build.py                  ← wikkelt header + footer rond elk fragment
└── download_assets.py        ← downloadt externe afbeeldingen → lokaal voor productie
```

## Pagina-overzicht (18 pagina's)

| URL | Bron-fragment |
|-----|---------------|
| `index.html` | (handmatig, hero-pagina) |
| `algemeen-ziekenhuis.html` | `pages/algemeen-ziekenhuis.html` |
| `vzw-werken-glorieux.html` | `pages/vzw-werken-glorieux.html` |
| `eh-glorieux.html` | `pages/eh-glorieux.html` |
| `organisatie.html` | `pages/organisatie.html` |
| `voorzieningen.html` | `pages/voorzieningen.html` |
| `opdrachtsverklaring.html` | `pages/opdrachtsverklaring.html` |
| `werken-van-barmhartigheid.html` | `pages/werken-van-barmhartigheid.html` |
| `info-voor-leveranciers.html` | `pages/info-voor-leveranciers.html` |
| `gezondheidszorg.html` | `pages/gezondheidszorg.html` |
| `kind-en-jeugdzorg.html` | `pages/kind-en-jeugdzorg.html` |
| `ouderenzorg.html` | `pages/ouderenzorg.html` |
| `nieuws.html` | `pages/nieuws.html` |
| `nieuws-jaarverslag-2024.html` | `pages/nieuws-jaarverslag-2024.html` |
| `bereikbaarheid.html` | `pages/bereikbaarheid.html` |
| `contact.html` | `pages/contact.html` |
| `gebruiksvoorwaarden.html` | `pages/gebruiksvoorwaarden.html` |
| `sitemap.html` | `pages/sitemap.html` |

## Lokaal bekijken

Open `index.html` rechtstreeks in een browser. Voor relatieve paths is een lokale server netter:
```
cd dit-mapje
python3 -m http.server 8000
# → http://localhost:8000
```

## Hercompileren na content-edits

Pas een fragment aan in `pages/`, daarna:
```
python3 build.py
```

## Logo

Het beeldmerk (cirkel + komma) zit als vector in `images/logo-mark.svg`. Het wordmark "vzwWerkenGlorieux" is geen pixel-asset maar wordt live gerenderd in HTML met **Source Sans 3 Light** (open-source equivalent van Myriad/Frutiger). Voordeel: scherp op elke resolutie.

Wanneer de klant het officiële vector-logo aanlevert (SVG of EPS), kan je `images/logo-mark.svg` vervangen, of als het één compleet SVG is, de hybride markup vervangen door één `<img src="images/logo.svg">`.

## Afbeeldingen

Inhoudelijke beelden worden momenteel rechtstreeks ingeladen vanaf de bestaande Drupal-server (`werken-glorieux.be/sites/default/files/...`). Dit werkt voor preview en als de oude site nog up is.

Voor productie: lokale assets ophalen met
```
python3 download_assets.py
```
Dit doorloopt alle HTML, downloadt elke `werken-glorieux.be`-afbeelding naar `images/`, en herschrijft de `src`-attributen. Run dit op een netwerk dat de oude site kan bereiken.

## Headless CMS plan

De fragmenten in `pages/` zijn pure content-blokken (zonder header, footer, head). Ze mappen 1-op-1 op een page-type in een headless CMS (Sanity, Storyblok, Strapi, Directus, Contentful, …).

Suggestie voor migratie:
1. Definieer een `Page` content-model met velden `title`, `slug`, `description`, `body`.
2. Voor specifieke pagina's: extra block-types zoals `Pillar`, `Stat`, `TimelineItem`, `Person`, `GlassSculpture`.
3. Vervang `build.py` door een SSG (Astro of Eleventy) die de CMS-API consumeert.
4. Bewaar exact dezelfde `styles.css` en `main.js`.

## Cookie banner

Eenvoudige opt-in flow met `localStorage`. Bij productie te vervangen door een GDPR-compliant CMP (Cookiebot, OneTrust, …) zodra er trackers worden ingeladen.

## Wat ontbreekt nog

- Backend voor het contactformulier (Formspree, eigen endpoint, …)
- 404 pagina
- Echte favicons en social-preview meta tags
- Volledig vector-logo (SVG met uitgelijnde paths) van klant
- Volledige set foto's voor productie (nu via externe URLs gelinkt)
