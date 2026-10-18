# Verification report

## Checks performed

- JavaScript syntax checks: `assets/app.js`, `assets/engine.mjs` — passed.
- 12 pure planner engine tests — passed, including item arithmetic, quantities, manual override, malformed saved states, private-field stripping, rate gating, minimum charges, heavy/special adjustments, capacity labeling, and persistence round trips.
- Static checks on all 9 HTML files — passed: one h1 per page, unique IDs, metadata present, image alt attributes, 254 local links/assets/anchors resolved on disk, disabled personal fields, no form action endpoint, expected initial feature flags, CNAME, `.nojekyll`, eight sitemap URLs, SVG XML validity, and no runtime `innerHTML` use.
- Original truck illustration and social sharing PNG inspected as rendered image assets.
- All required directory routes have real `index.html` files; no SPA history routing.
- All initial company price values are null; synthetic test prices exist only in the test file.

## Verification limits

A supported browser automation surface was unavailable in the build environment. No browser preview server was started. Consequently **live browser interactions, visual page layout, mobile overflow, keyboard focus behavior, clipboard/download/print behavior, storage failures, browser console errors, network/direct HTTP page loads, and reduced-motion behavior have not been verified in a real browser**. Their implementation was source-reviewed, but that is not a substitute for device testing.

Lighthouse was not run. Performance, Accessibility, Best Practices, and SEO scores of 95+ remain targets, not measured results. WCAG 2.2 AA principles informed the implementation; this is not an accessibility certification. No public deployment or DNS verification was performed.

## Manual browser checklist

Serve the site root with `python3 -m http.server 8080` and use current desktop and mobile browsers:

1. Visit all eight pages and `/404.html` directly. Confirm navigation and assets. Test an unknown URL on GitHub Pages after deployment.
2. Check widths of 320, 360, 390, 768, 1024, and 1440 pixels; confirm no horizontal page overflow and legible map labels.
3. Open/close the mobile menu by touch and keyboard; Escape closes it and returns focus to the toggle. Check navigation without JavaScript (links remain available).
4. Tab from the skip link through navigation, cards, inputs, buttons, map points, community buttons, FAQ summaries, and footer. Confirm visible focus and readable labels.
5. Add multiple items; edit quantity and per-item volume; delete an item. Check the summary immediately changes and survives refresh.
6. Try invalid numeric values, blanks, maximums, manual volume override, and a rural location. Invalid entries must not yield NaN or a fabricated price.
7. Copy, download, print, and clear the plan. Refresh after clearing. Disable browser storage and verify the fallback message. Block clipboard access and use Download.
8. Confirm empty plans show no dollar amount. In an isolated local test copy, configure all rates; check the preliminary breakdown and missing-rate gate. Restore production null rates afterward.
9. Search services and FAQs, including no-results and case-insensitive terms. Open/close native accordions with Enter or Space.
10. Select map communities with click, touch, Enter, and Space; check the equivalent HTML buttons and selected community message.
11. Turn reduced motion on; check effects stop and all content remains visible.
12. Disable JavaScript; check content, links, FAQ, and policy remain usable; planner should explain that JavaScript is required.
13. Confirm every personal field and photo control is disabled; no requests, booking confirmations, payment collection, or analytics network calls occur.
14. Test under HTTPS for clipboard use; inspect the browser console and network panel for errors.
15. Run Lighthouse on a mobile profile after deployment; investigate measured issues rather than assuming a score.

## Known design boundaries

- The map is a coordinate-based point diagram, not a navigational map or service boundary.
- System fonts avoid third-party requests. Font appearance varies by platform.
- Root-relative paths require the custom-domain/root deployment described in the deployment guide.
- JSON changes require the optional local renderer for corresponding static SEO/no-JavaScript content updates.
- Pricing is a planning model, not an automatic weight, tax, or route calculation.
- All interactive data stays local until the visitor explicitly follows a configured external integration link.


## Official-brand update verification

- Original supplied logo used directly, with full square canvas and all box flaps preserved. Pixel comparisons confirm derived logo and PNG icon assets equal proportional resizes of the original.
- Favicon ICO contains 16, 32, 48, and 64 pixel entries. Required 16/32 PNGs, 180 Apple touch icon, 192/512 icons, and manifest exist. Every HTML page references the complete package and navy theme color.
- New social PNG is 1200×630 and was visually inspected, along with the resized official mark.
- Obsolete cobalt/orange hexadecimal colors were absent from generated HTML, CSS, SVG, and JavaScript in the automated scan.
- SHA-256 comparison confirms `app.js`, `engine.mjs`, business JSON, CNAME, sitemap, and robots.txt are unchanged from the preceding published source.
- All 12 planner tests still pass. Static link/asset tests still pass.
- Contrast calculations: primary button 4.84:1; navy text on clean white 12.01:1; muted text on mint 4.68:1; dark teal small text on mint 5.27:1; mint text on navy 10.05:1; input outlines on white 3.86:1. These cover the specified palette pairs, not a full browser accessibility audit.
- Run `python3 tests/brand_check.py` with Pillow installed to repeat brand checks.

Browser/device testing remains unavailable in this environment. Mobile navigation, live calculator UI, focus traversal, rendered page layout/overflow, favicon display in browser chrome, and browser-console behavior require the manual checklist above. No Lighthouse scores or full WCAG conformance are claimed. The existing private preview is updated separately; the custom domain and DNS remain untouched.
