# Official Dual Duty identity

This update applies the approved identity to the existing multi-page site. Page architecture, content, interactions, animations, and pre-launch restrictions are retained.

| Color | Hex | Use |
| --- | --- | --- |
| Deep Navy | #18364A | Main text, hero, footer, brand panels |
| Signature Teal | #147E83 | Primary buttons, icons, controls, active accents |
| Clean White | #F7FAF9 | Main page background and light text |
| Soft Mint | #D9E9E5 | Alternate sections, map, information surfaces, dark-section text |

Semantic CSS tokens are declared once at the start of `assets/style.css`. White cards use #FFFFFF, muted copy #526871, and control outlines #71858C. Teal hover is #10676B. Small text on mint uses this darker teal because the unmodified teal/mint pair does not meet the 4.5:1 normal-text threshold. Dark-section focus rings use mint for visibility.

## Authoritative artwork

`assets/brand/official-logo-source.png` is the original supplied image, copied without changing its pixels. It retains the flat box, simple diagonal strokes, overlapping rounded Ds, and original proportions. No substitute icon, vector trace, CSS recreation, or recoloring was used. Minor raster texture and artwork color variations are preserved as supplied.

The 128/256/512 logo copies and all favicon sizes are proportional reductions of the entire source canvas. The source artwork's padding is retained, so flaps are not cropped. Logo images reserve explicit square dimensions and use `object-fit: contain`.

The shared `brand()` markup supplies navigation, footer, and About branding. The hero uses an icon copy within its existing launch-status label. On narrow phones, the navigation uses the icon alone; the home link retains its accessible business name. White backing preserves the official navy outline on dark sections.

## Icon package

- `favicon.ico`: 16, 32, 48, 64 pixels
- `favicon-16x16.png`
- `favicon-32x32.png`
- `apple-touch-icon.png`: 180 pixels
- `icon-192.png`
- `icon-512.png`
- `site.webmanifest`

The manifest supplies icons and display metadata only. It adds no service worker, offline promise, analytics, or data collection.

## Supporting artwork

The original truck/trailer SVG geometry is unchanged and recolored in related teal/navy/mint tones with neutral material colors. The community map keeps its original sourced point geometry. `assets/social.png` uses the official logo on a navy composition with teal accents and the existing pre-launch location/tagline.

## Maintenance

`python3 tools/render.py` refreshes existing HTML from the shared templates. It does not require Node.js and is not needed to deploy the shipped files.

`python3 tools/brand_assets.py` regenerates raster assets from the supplied master. This optional maintenance script needs Pillow and a locally installed DejaVu font for the social card. Adjust its font path on other operating systems. The website itself uses the existing Space Grotesk / Inter font stacks with system fallbacks and makes no external font requests.
