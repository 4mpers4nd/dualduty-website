# Dual Duty Junk Removal

A complete, buildless, multi-page static website for a pre-launch Sanpete County startup. Designed for **https://dualdutyjunk.com** and GitHub Pages. No production Node.js, package installation, API keys, database, or backend.

## Start here

1. Unzip this project.
2. Upload the **contents** of `dual-duty-junk/` to your hosting repository root. `index.html` must be at that root, not inside another nested folder.
3. Follow [Deployment](docs/DEPLOYMENT.md).
4. Before changing business information, read [Configuration](docs/CONFIGURATION.md).
5. Review [Launch readiness](docs/LAUNCH-CHECKLIST.md) and [QA results](docs/QA.md).

The shipped HTML and assets are already generated and ready to serve. No build is needed to deploy this version. Never enter customer information into config files: all files in this project are public.

## Included

- Home, Services, Service Areas, Pricing / Load Planner, About, Contact, FAQ, draft Privacy Policy, and custom 404.
- Official supplied interlocking-D raster logo, full favicon/app-icon package, pickup/trailer SVG hero illustration, geographic SVG point map, and 1200×630 PNG social card.
- Browser-local planner: catalog categories, quantities, editable sizes, stairs, access difficulty, service community, special handling, manual volume override, local saving, copy, download, and print.
- Rates start as `null`; no invented prices. A complete rate configuration and feature flag are both required before preliminary prices appear.
- Searchable FAQ and services, keyboard-operable map markers with equivalent HTML community buttons, native accordions, mobile navigation, reduced-motion support.
- Static rendered content for search engines and readers without JavaScript. Interactivity requires JavaScript.
- Canonicals, unique metadata, LocalBusiness JSON-LD using supplied facts only, sitemap, robots.txt, CNAME, `.nojekyll`.
- Disabled future contact form: no POST, no endpoint, no personal-data storage, no file uploads, no fake success.

## Files

```text
index.html               Home
services/index.html      Planned services
areas/index.html         Community map and sources
pricing/index.html       Load planner
about/index.html         Founder story
contact/index.html       Launch status and disabled preview
faq/index.html           Searchable FAQ
privacy/index.html       Draft privacy policy
404.html                 Custom missing-page response
assets/style.css         Responsive visual system
assets/app.js            Browser interactions and integration gates
assets/engine.mjs        Pure planner calculations and sanitization
assets/logo-*.png        Optimized official logo at 128, 256, and 512 pixels
assets/brand/            Untouched supplied logo master
assets/*.svg             Recolored vector illustration and map
favicon.ico, *.png        Favicon and app-icon package
site.webmanifest         App-icon metadata (no service worker)
assets/social.png        Social sharing image
data/config.json         Authoritative business/content/rate configuration
tools/render.py          Optional HTML maintenance generator (Python stdlib)
tests/                   Repeatable engine and static QA checks
docs/                    Deployment, configuration, readiness, QA
CNAME                    dualdutyjunk.com
robots.txt, sitemap.xml  Search discovery
.nojekyll                Serve assets directly on GitHub Pages
```

## Local testing

From this directory, run:

```bash
python3 -m http.server 8080
```

Then open `http://localhost:8080/`. Do not double-click HTML files: `file://` prevents module and JSON loading. All URLs are root-relative for the requested custom domain. An unconfigured GitHub project URL such as `username.github.io/repository/` is **not** a supported base path; use your custom domain or an account-root Pages repository.

## Updating content without editing every page

Edit `data/config.json`. The browser reads it for the planner and contact information. To refresh the static service/FAQ content, coordinate map, navigation metadata, and no-JavaScript fallback after changes, run once locally:

```bash
python3 tools/render.py
```

Commit the JSON **and generated HTML/SVG/XML files**. This is an optional maintenance step when changing content, not a hosting build requirement. Editorial page layouts and narrative copy live in `tools/render.py`; generated pages should not be hand-edited unless you intentionally stop using the generator.

## Run automated checks

Python 3 and Node.js are needed only for these development checks:

```bash
node --check assets/app.js
node --check assets/engine.mjs
node --test tests/engine.test.mjs
python3 tests/check_site.py
```

Synthetic dollar amounts appear only inside tests, never in the business configuration. Tests are intentionally checking the **pre-launch default configuration**; update the corresponding assertions when you deliberately launch.

## Privacy and integrations

Only non-personal planner selections are persisted as `dualDuty.plan.v1`. No analytics, remote fonts, map tiles, or tracking cookies. Hosting providers may maintain technical logs; see the draft privacy page. The frontend never stores or transmits addresses, emails, phone numbers, dates, free text, or photos.

Future integrations are explicitly gated HTTPS links to reviewed external providers. Merely changing a feature flag does not activate the disabled form. A true in-page submission integration requires a real secure backend and privacy review; see the configuration guide. No secrets belong in this repository.

## Design and assets

The official navy / teal / white / mint color tokens live at the start of `assets/style.css`. See [Brand guide](docs/BRAND.md). The supplied logo is used directly; its geometry has not been traced or redesigned. Typography uses `Space Grotesk`, `Inter`, then local system fallbacks; no web fonts are fetched or bundled. The shipped experience uses the system fallback unless those fonts are installed. You can self-host appropriately licensed WOFF2 fonts if desired.

The truck is an original stylized brand illustration, explicitly labeled as such. It does not document actual equipment or capacities. There are no fake testimonials, stock job photos, invented credentials, or customer ratings. The point map uses cited coordinates, with no invented county boundary or route distances.

No DNS changes or deployment to the existing business domain were made as part of this source delivery.
