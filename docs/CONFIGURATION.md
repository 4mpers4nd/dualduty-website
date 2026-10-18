# Business configuration

`data/config.json` is the single data source. JSON does not allow comments or trailing commas. Use `null` for unknown rates or information, not `0`, empty strings, or made-up values.

## Two ways the site consumes data

- The browser reads config for the calculator, contact links, and future integration gating.
- `python3 tools/render.py` renders static content from the same data so search engines and no-JavaScript visitors get complete pages. Run it after changes to business information, areas, services, FAQs, or the domain and commit its output.

Shipping and serving the current site needs no generator or production runtime. Python is only a local editing convenience. Narrative marketing copy is intentionally editorial: review `tools/render.py` when changing launch status or promises. Setting `status` alone does not silently rewrite policies or activate the disabled form.

## Business information

`business.name`, `domain`, `base`, `status`, `phone`, `email`, `hours`, `socials`, and `founders` hold public facts. `domain` must be an HTTPS origin without a trailing slash. Keep `status` at `pre-launch` until operations are actually ready. Supported integration-ready status is `launched`.

Set a real public phone and email only when approved for publication. `hours` is a plain public display string. Socials have this structure:

```json
{"label":"Account name", "url":"https://your-confirmed-profile-url"}
```

Use only confirmed links. Keep the array empty until then. Runtime links reject non-HTTPS social URLs. Never publish home addresses, private founder contact details, credentials, or API secrets.

## Planned services and FAQs

- `services`: `id`, `title`, `tagline`, `description`, supported `icon`, and `enabled`. Disabled service cards disappear after rendering. Icon options: box, garage, stairs, sofa, washer, leaf, tools, building.
- `restrictedMaterials`: exclusion list on the services page.
- `faqs`: category, question, and answer. Searches index all three fields.
- Re-render after edits. FAQ answers and narrative copy should be reviewed together so policy statements agree.

## Service areas and map

Each area contains a name, latitude, longitude, and public coordinate source. Use sourced coordinates; never estimate positions from a decorative graphic. The generator creates both the embedded SVG and `assets/communities.svg` with an equirectangular projection adjusted to 39.4° north. The map shows points only; it does not imply service boundaries, distances, or routes.

The supplied projection is framed for Sanpete County. If expanding beyond that area, adjust the viewBox/projection and labels in `map_svg()` and inspect the result. Add corresponding `pricing.travelCharges` entries (initially null). New locations are not automatically approved operational coverage.

## Item catalog and trailer

`items` defines id, name, category, approximate `volume` in cubic yards per item, and `heavy` / `special` flags. Values are editable assumptions, not measurements or company promises. Keep IDs stable to preserve saved plans. Changes to default volumes apply to newly added items; existing saved plans retain their explicit edited values.

`trailer.usableCubicYards` remains null until measured and confirmed. When null, the progress bar uses a clearly labeled 10 yd³ **planning scale**, not a claimed trailer size. Confirmed capacity enables a volume percentage and warns about multiple volume loads. `payloadLimitPounds` is a documentation/configuration field reserved for actual approved equipment limits; there are no item weight measurements, so the planner does not calculate towing safety or promise a number of safe trips.

## Pricing engine

Every rate is unconfigured initially. To enable prices, set `features.pricingEstimates` true **and** configure every applicable value below with a finite, nonnegative number. Explicit zero means a deliberate zero charge; null means unknown and suppresses the price.

| Key | Meaning / unit |
| --- | --- |
| baseCharge | Flat service charge, USD per plan |
| volumeRatePerYard | USD per estimated cubic yard |
| laborRatePerHour | USD per estimated crew-hour (define your billing basis consistently) |
| laborHours.easy / moderate / difficult | Approved estimated billable hours for the selected access tier |
| stairsHoursPerFlight | Extra estimated billable hours per flight |
| travelCharges[community] | Flat approved travel allowance for that community |
| disposalAllowance | Estimated disposal allowance in USD per plan |
| heavyItemAdjustment | USD per flagged heavy item |
| specialHandlingCharge | USD per plan if any special item/flag is present |
| minimumCharge | Minimum preliminary plan charge in USD |

Formula:

```text
subtotal = base + volume × volumeRate
         + (tierHours + stairs × stairsHours) × laborRate
         + communityTravel + disposalAllowance
         + heavyQuantity × heavyAdjustment
         + (anySpecialHandling ? specialHandlingCharge : 0)
preliminary = max(minimumCharge, subtotal), rounded to cents
```

The summary displays an itemized breakdown. If one relevant rate is missing, invalid, or negative, or the occupied volume is zero, no dollar estimate appears. Rural/other plans require a separately confirmed `travelCharges["Rural Sanpete / other"]` value; otherwise they remain volume-only. The current model deliberately uses flat location allowances, not fabricated road distances. It does not compute measured weight charges, taxes, or actual disposal receipts; these remain subject to business confirmation. Review your pricing model before enabling any public figures.

Do not copy synthetic values from unit tests into business rates. They exist only to test arithmetic.

## Future requests, booking, and payments

The contact form remains a disabled frontend preview. It has no submission endpoint and no personal-data event handlers. This is intentional, not a hidden unfinished submission function.

For a safe first integration, use a legitimate hosted provider:

1. Select and configure the real provider outside this project.
2. Review its security, data handling, consent, retention/deletion controls, spam protection, file validation, and operational workflow.
3. Update the draft privacy policy and business policies; publish a real privacy contact.
4. Set the relevant HTTPS URL in `integrations`: `quoteRequestUrl`, `bookingUrl`, or `paymentUrl`.
5. Set `integrations.privacyReviewed` true only after that review, set `business.status` to `launched`, and enable the corresponding `features.quoteRequests`, `booking`, or `paymentLinks` flag.
6. Review launch copy in the generator, then regenerate and test.

All three conditions (launched status, reviewed integration, feature enabled) and a valid HTTPS URL are required. These links open the real provider; they do not imply a successful booking or payment on this website. No personal details are appended to URLs.

For a future in-page form, replace the disabled preview deliberately with a provider-specific adapter only after configuring a secure endpoint. Keep secrets server-side, validate on the server, implement real failure/success responses, protect uploads, and do not save personal fields in localStorage. Never point a form at a guessed endpoint or make it show a success message without receiving a genuine success response.

`features.reviews` is reserved and false. There is no testimonial component or invented review content; enabling this flag alone displays nothing. Add a component only once you have approved, genuine reviews and appropriate attribution. No star-rating schema is shipped.

## Branding

- Colors, spacing, and typography: `assets/style.css`.
- Official unmodified source: `assets/brand/official-logo-source.png`.
- Navigation / scalable raster sizes: `assets/logo-128.png`, `logo-256.png`, `logo-512.png`.
- Favicon ICO/PNGs, Apple touch icon, 192/512 app icons, and `site.webmanifest` live at the site root.
- Regenerate raster assets with `python3 tools/brand_assets.py` (Pillow required only for maintenance). This script uses local DejaVu fonts for the social card; adjust the font path if needed.
- Wordmark markup: `brand()` in `tools/render.py`.
- Hero art: `assets/rig.svg`.
- Social image: `assets/social.png`, 1200×630. Replace with your updated brand image if changing the name or tagline.
- Canonicals and sitemap derive from `business.domain` when rendered. The generator preserves an existing CNAME byte-for-byte; only a missing CNAME is created.

Keep images local and fonts optional to preserve the dependency-free, tracking-free site. Respect reduced motion when adding effects.
