**# Catalog journey — Saleor storefront**

Phase: P01 — Explore Saleor customer journeys.

Status: CORE MANUAL WALKTHROUGH COMPLETE — listing, direct search, no-results UI, category application/clearing, price sorting, cursor pagination, browser listing API, and key locator candidates observed. Remaining source/runtime limitations are listed below. P01 overall remains in progress.

Source review date: 2026-09-14. Reference: sibling \`storefront/\` working files.

**## Scope and evidence**

Map product listing, search, filtering, sorting, and a no-results path. Record

pagination if available in the seeded catalog. Product detail is a separate map.

Source findings are candidates until observed at runtime. Observations below are

supported by user-supplied screenshots; missing evidence remains pending.

Authentication's completed manual walkthrough is in \`auth.md\`.

Continue signed out, in English with channel \`default-channel\`. Keep the previous

Responsive viewport 759 × 762, Fit to window, and No throttling for comparable

captures. Record any change of viewport or zoom. Screenshots below are planned

paths under ignored \`artifacts/journey-mapping/catalog/\`, not saved files.

**## Initial source findings**

\| Area | Source finding | Runtime evidence |

\| --- | --- | --- |

\| All-products route | \`/{locale}/{channel}/products\` | CAT-01 confirms \`http\://localhost:3000/en/default-channel/products\` |

\| Initial listing | Products page calls \`getProductListingPage\`; renders breadcrumbs, content-configured hero, product cards, and \`PlpListingClient\` with category filtering enabled | CAT-01 and its scroll follow-up confirm heading, count, controls, and first two card names/prices |

\| Filter/sort traffic | Products page describes initial cached content followed by client grid updates through \`/api/listing\` | Observed: \`GET /api/listing\` returns HTTP 200 with product data, \`pageInfo\`, \`totalCount\`, and resolved category metadata; sort/cursor/direction reflected in query parameters |

\| Search route | \`/{locale}/{channel}/search?query=\<encoded-term>\`; source also accepts \`sort\`, \`cursor\`, and \`direction\` | CAT-02 confirms direct navigation with \`query=Apple\`; search-entry submission not exercised |

\| Search results | Search page calls \`searchProducts\`; renders result heading/count, sorting, cards, and pagination when another page exists | CAT-02 shows \`Results for "Apple"\`, \`1 product found\`, \`Relevance\`, and Apple Juice |

\| Empty search result | Zero total count renders an empty state with links to \`/products\` and the homepage | CAT-03 confirms no-results text, both recovery controls, and document HTTP 200; recovery navigation and raw backend result pending |

Inspected source files:

\- \`src/app/(storefront)/[locale]/[channel]/(main)/products/page.tsx\`

\- \`src/app/(storefront)/[locale]/[channel]/(main)/search/page.tsx\`

\- \`src/lib/search/index.ts\`, \`src/lib/search/saleor-provider.ts\`, \`src/graphql/SearchProducts.graphql\`

\- \`skills/saleor-paper-storefront/rules/product-filtering.md\` (architecture context)

Backend GraphQL operation mapping will be expanded alongside each observed action.

Keep browser HTTP requests separate from server-side GraphQL evidence. An absent

browser GraphQL request does not establish that no backend query ran.

Search source mapping: \`searchProducts\` executes \`SearchProductsDocument\` with

the search term, channel, locale-derived language variables, sorting, and cursor

pagination. The document defines query \`SearchProducts\` selecting \`products\`.

Runtime GraphQL requests/results have not been captured. The visible \`Relevance\`

option maps in this provider to \`RATING\` descending, not a verified text-relevance

ranking. With one observed result, ordering cannot be meaningfully checked.

Source limitation for CAT-03: a failed result or missing \`products\` is converted

by this provider into an empty list and total count zero. Therefore a no-results

screen alone does not distinguish a genuine zero-match query from a backend error.

**## Guided observation sequence**

Complete one step at a time; choose actual product names and available filter

values from the first capture instead of assuming sample data.

\| Step | Action | Expected result to verify | Screenshot checkpoint |

\| --- | --- | --- | --- |

\| CAT-01 | Open the all-products URL while signed out; wait for settled content | Listing visible; record final URL, heading, count, first two product names/prices, and available filter/sort controls | \`catalog-01-listing.png\` |

\| CAT-02 | Search using a distinctive word from an observed product name | Relevant results; record query URL, exact text, requests/status, and product destinations | \`catalog-02-search-results.png\` |

\| CAT-03 | Search for a deliberately unmatched term | No-results UI with recovery controls; confirm actual result rather than assuming a term is absent | \`catalog-03-no-results.png\` |

\| CAT-04 | Return to listing; apply one available filter, then clear it | Selection and URL reflected in results; clearing restores the unfiltered state | \`catalog-04-filter.png\` |

\| CAT-05 | Choose an available sort option | URL/selected option and visible ordering agree; record treatment of price ranges if relevant | \`catalog-05-sort.png\` |

\| CAT-06 | If pagination exists, visit the next page and return | Cards and navigation state change consistently; record cursor as dynamic | \`catalog-06-pagination.png\` |

For each step record: entry state, action, final URL, exact visible text, semantic

locator candidates, browser request method/URL/status and safe response summary,

GraphQL operation name/field with evidence source, expected versus observed result,

and screenshot reference. Use \`not observed\` for missing network evidence.

**## Observed record — CAT-01: initial product listing**

Evidence: user-supplied screenshot following the requested all-products navigation.

The screenshot includes the address bar, responsive viewport, and Network panel.

\| Item | Observation |

\| --- | --- |

\| Entry/action | Requested direct visit while signed out; resulting header shows guest account/person icon |

\| Final URL | \`http\://localhost:3000/en/default-channel/products\` |

\| Locale/channel | \`en\` / \`default-channel\` |

\| Breadcrumbs | \`Home\` followed by \`Products\` |

\| Heading and description | \`All Products\`; \`Browse our full catalog.\` |

\| Count | \`32 products\` — current data-dependent count, not a universal expectation |

\| Controls | \`Filters\` and \`Sort\` visible; both closed. Available options and selected sort order not yet observed. |

\| Grid | Two columns visible, with partial images of a green bottled drink and a blue shirt. Product names and prices are below the captured area; image filenames in Network are not substitutes for visible card text. |

\| Browser response | \`products\` document row shows HTTP 200. Method, full request URL, and response body not opened; final browser URL recorded separately above. |

\| Network context | All selected, blank text filter, recording enabled, Keep log checked; 45 requests shown. Some \`webp/\` rows show HTTP 302; full redirect chains uninspected. |

\| GraphQL | Not observed in this capture; document HTTP 200 does not independently prove downstream GraphQL success |

\| Expected versus observed | Correct listing route, heading, count, controls, and partial product grid displayed. Full card text and interaction behavior remain pending. |

\| Viewport | Responsive 759 × 762, Fit to window, No throttling; zoom and pixel ratio not supplied |

\| Development indicators | Development badge visible; DevTools shows 18 warnings, contents uninspected |

\| Screenshot checkpoint | Conversation attachment received; planned \`artifacts/journey-mapping/catalog/catalog-01-listing.png\`, not verified as a local file |

**### CAT-01 follow-up: first two product cards**

Evidence: user-supplied screenshot after the requested scroll, with no requested

filter or sort change. The address remains

\`http\://localhost:3000/en/default-channel/products\`; \`32 products\`, closed

\`Filters\`/\`Sort\` controls, and the guest icon remain visible. Responsive dimensions

remain 759 × 762, Fit to window, No throttling.

\| Position | Visible category | Product name | Displayed price |

\| --- | --- | --- | --- |

\| First row, left | \`JUICES\` | \`Apple Juice\` | \`$1.99\` |

\| First row, right | \`T-SHIRTS\` | \`Monospace Tee\` | \`$20.00\` |

Both images and card text are visible. These are observed data values for this

session; the dollar symbol alone does not establish an ISO currency code.

Product-link candidates can use these names, subject to accessible-name and

uniqueness checks. Product destinations have not yet been inspected.

Network remains on All with an empty text filter and Keep log enabled; 56 requests

are shown and the retained \`products\` document row has status 200. This capture

does not isolate scroll-triggered traffic or show a new GraphQL operation.

DevTools shows 22 warnings; their contents are uninspected.

Screenshot received in the conversation; planned local checkpoint

\`artifacts/journey-mapping/catalog/catalog-01-product-cards.png\` is not verified

as a file. Initial listing content observation is complete; interaction checks

remain pending. \`Apple\` from the observed product name is used for CAT-02 below.

**## Observed record — CAT-02: direct search for Apple**

Evidence: user-supplied screenshot after the requested direct search URL visit.

\| Item | Observation |

\| --- | --- |

\| Entry/action | From the signed-out listing walkthrough, navigate directly to the supplied search URL; this does not exercise a search form or menu entry |

\| Final URL | \`http\://localhost:3000/en/default-channel/search?query=Apple\` |

\| Heading | \`Results for "Apple"\` |

\| Result count | \`1 product found\` |

\| Sort control | \`Relevance\` visible; menu closed |

\| Product | \`Apple Juice\` name and bottled-drink image visible, consistent with CAT-01. Price lies outside this capture; do not carry the listing price forward as an observed search price. |

\| Guest state | Header shows account/person icon |

\| Browser response | \`search?query=Apple\` document row shows HTTP 200. Request method and response body not opened. |

\| Network context | All selected, text filter empty, recording enabled, Keep log checked; 38 requests shown |

\| Backend evidence | Query \`SearchProducts\` is source-mapped; execution, variables, and raw GraphQL result not directly observed |

\| Expected versus observed | The known product is returned for a word in its name, with a matching heading and one-result count. Search-form submission and product link destination remain unverified. |

\| Viewport | Responsive 759 × 762, Fit to window, No throttling |

\| Development indicators | 20 warnings shown, contents uninspected; development badge overlaps part of the category label |

\| Screenshot checkpoint | Conversation attachment received; planned \`artifacts/journey-mapping/catalog/catalog-02-search-results.png\`, not verified locally |

Locator candidates: heading named \`Results for "Apple"\`, text \`1 product found\`,

product link using \`Apple Juice\`, and sort control named \`Relevance\` after checking

its rendered role. Accessible names, uniqueness, and destination still require

DOM inspection. Query-specific heading/count and product data vary across cases.

**## Observed record — CAT-03: no-results search**

Evidence: user-supplied screenshot after direct navigation to the requested

deliberately unmatched search term.

\| Item | Observation |

\| --- | --- |

\| Entry/action | From CAT-02, directly visit search with \`query=zzzx-no-match-92741\` |

\| Final URL | \`http\://localhost:3000/en/default-channel/search?query=zzzx-no-match-92741\` |

\| Heading | \`No results for "zzzx-no-match-92741"\` (wraps across two lines) |

\| Message | \`We couldn't find any products matching your search. Try a different term or browse our categories.\` |

\| Recovery controls | \`Browse All Products\` and \`Go to Homepage\`, both visible and not yet exercised |

\| Visible state | Search icon above the message; no product grid or sorting control displayed. Guest account/person icon remains visible. |

\| Browser response | \`search?query=zzzx-no-match-92741\` document row shows HTTP 200; request method and response body not opened |

\| Network context | All selected, text filter empty, recording enabled, Keep log checked; 34 requests shown |

\| Backend evidence | \`SearchProducts\` remains the source-mapped query; raw GraphQL result, totalCount, and errors are not observed |

\| Expected versus observed | The requested unmatched term produces the expected no-results UI and recovery choices. Given the provider's error-to-empty fallback, this screenshot alone does not prove a successful backend zero-match result. |

\| Viewport | Responsive 759 × 762, Fit to window, No throttling |

\| Development indicators | 16 warnings shown; contents uninspected |

\| Screenshot checkpoint | Conversation attachment received; planned \`artifacts/journey-mapping/catalog/catalog-03-no-results.png\`, not verified locally |

Locator candidates: heading with the exact observed no-results text and links

named \`Browse All Products\` and \`Go to Homepage\` (source uses links styled as

buttons). Rendered roles, accessible names, hrefs, and uniqueness remain unverified.

The heading varies with the query and wraps at this viewport; the explanatory

message and recovery-control layout are candidate stable regions.

**## Observed record — CAT-03 recovery / CAT-04a filter panel**

Evidence: screenshot supplied after the requested \`Browse All Products\` recovery

action followed by opening \`Filters\`. The clicks themselves are not captured.

\| Item | Observation |

\| --- | --- |

\| Resulting UI | Product listing visible behind an open left-side \`Filters\` panel and dimmed backdrop; \`32 products\`, \`Sort\`, and part of the blue shirt card visible |

\| Recovery outcome | Supplied follow-up supports return to the listing UI from the no-results page; exact destination URL remains unconfirmed because the address bar is outside this capture |

\| Panel header | \`Filters\` and an X-shaped close control |

\| CATEGORY | \`Juices\`, \`T-shirts\`, \`Sneakers\`, \`Audiobooks\`, \`Sweatshirts\`; square controls appear unchecked |

\| SIZE | \`39\`, \`40\`, \`41\`, \`42\`, \`45\`, \`S\`, \`M\`, \`L\`, \`XL\`, \`XXL\`; none visibly highlighted |

\| PRICE | \`Under $50\`, \`$50 - $100\`, \`$100 - $200\`, \`$200+\`; circular controls appear unselected |

\| Scope of options | Only visible options are recorded; the capture does not establish whether additional controls exist below the panel's visible area |

\| Browser/network evidence | All selected, blank text filter, recording enabled, Keep log checked. Request table is empty while footer retains \`89 requests\`; no individual recovery/filter request or response status can be assigned from this capture. Do not infer zero network activity. |

\| GraphQL | Not observed; opening the panel alone does not establish a filter query ran |

\| Expected versus observed | Filter choices are available over the listing, with no visible active selection. Filter application and result changes have not yet been tested. |

\| Viewport | Responsive 759 × 762, Fit to window, No throttling |

\| Development indicators | 18 warnings, contents uninspected; development badge overlaps the lower panel area |

\| Screenshot checkpoint | Conversation attachment received; planned \`artifacts/journey-mapping/catalog/catalog-04a-filter-panel.png\`, not verified locally |

Locator candidates: category checkbox by label \`Juices\`, size button by its exact

label scoped to the SIZE section, and price option by its visible label after

confirming the rendered role. The close icon's accessible name is not visible.

Roles, label associations, selection properties, and uniqueness need DOM checks.

The open-panel layout and backdrop are a separate visual checkpoint from the

closed listing; do not compare these as the same UI state.

**## Observed record — CAT-04b: Juices category applied**

Evidence: user-supplied screenshot after the requested selection of only \`Juices\`

and closing the filter panel.

\| Item | Observation |

\| --- | --- |

\| Entry/action | Unfiltered listing with 32 products; requested select \`Juices\`, wait, and close the panel |

\| Final URL | \`http\://localhost:3000/en/default-channel/products?categories=juices\` |

\| Visible state | \`All Products\`, \`Browse our full catalog.\`, and guest icon retained; filter panel closed |

\| Active selection | \`Filters\` displays badge \`1\`; chip \`Category: Juices\` with X control; \`Clear all\` visible |

\| Result count | \`4 products\`, reduced from the previously observed 32 |

\| Product evidence | Tops of two bottled-drink images visible. Names, category labels, and prices below capture; membership of all four returned products is not independently verified. |

\| Browser navigation | \`products?categories=juices&\_rsc=\<dynamic>\` fetch row shows HTTP 200; method and body not supplied |

\| Listing request | Row begins \`listing?surface=all&locale=en&channel=default-chann…\`, HTTP 200, type fetch; displayed duration 9.68 s. Full URL, method, parameters, and response body are not opened. Source maps grid updates to \`/api/listing\`; the screenshot alone shows only the truncated request name. |

\| Network context | All selected, empty text filter, recording enabled, Keep log checked; eight requests displayed, including image responses with HTTP 304 |

\| GraphQL | Not directly observed; browser fetch HTTP 200 does not establish raw backend result contents |

\| Expected versus observed | Selected category appears in the URL and chip; count changes to four. This confirms visible filter state and a result update, with full product membership and filter clearing still pending. |

\| Viewport | Responsive 759 × 762, Fit to window, No throttling |

\| Development indicators | 38 warnings shown; contents uninspected |

\| Screenshot checkpoint | Conversation attachment received; planned \`artifacts/journey-mapping/catalog/catalog-04b-juices.png\`, not verified locally |

Candidate locators: active chip text \`Category: Juices\` and control named

\`Clear all\`, subject to rendered role/name and uniqueness verification. The chip's

X accessible name is uninspected. Active-filter badge/chip and result count are

intentional state changes; \`\_rsc\` values and request durations are dynamic.

The filtered URL confirms the current products route, but does not retrospectively

establish the exact URL immediately after the earlier recovery click.

**### CAT-04b follow-up: filtered product names and destinations**

The user supplied these four product names and links in response to the filtered

membership check. These are user-reported links, not independently opened pages

or inspected DOM hrefs. Prices were not supplied for this filtered state.

\| Product | Reported URL |

\| --- | --- |

\| Apple Juice | \`http\://localhost:3000/en/default-channel/products/apple-juice\` |

\| Banana Juice | \`http\://localhost:3000/en/default-channel/products/banana-juice\` |

\| Bean Juice | \`http\://localhost:3000/en/default-channel/products/bean-juice\` |

\| Carrot Juice | \`http\://localhost:3000/en/default-channel/products/carrot-juice\` |

The four reported products are consistent with the selected Juices category and

the observed count of four. Raw backend category membership remains unobserved.

**## Observed record — CAT-04c: clear category filter**

Evidence: user-supplied screenshot following the requested \`Clear all\` action,

provided together with the filtered product links above.

\| Item | Observation |

\| --- | --- |

\| Entry/action | Juices filter active with four products; requested click \`Clear all\` |

\| Final URL | \`http\://localhost:3000/en/default-channel/products\`; category query absent |

\| Visible state | \`All Products\`, \`Browse our full catalog.\`, and \`32 products\`; \`Filters\` has no count badge, category chip and \`Clear all\` are absent |

\| Product grid | Partial bottle and blue shirt images visible again; full post-clear card text is outside the capture |

\| Browser request | \`products?\_rsc=\<dynamic>\` fetch row shows HTTP 200; method and response body not supplied |

\| Network context | All selected, text filter empty, recording enabled, Keep log checked; 22 requests shown. Other visible rows include image-related HTTP 200/302/304 responses; full redirect chains uninspected. |

\| API / GraphQL limit | No \`/api/listing\` row visible in this capture; no conclusion about backend execution or cache use follows from that absence. Raw GraphQL result unobserved. |

\| Expected versus observed | Category query, chip, and badge disappear; count returns from four to the original 32. The observed UI reset matches the requested filter-clear behavior. |

\| Viewport | Responsive 759 × 762, Fit to window, No throttling; guest account icon visible |

\| Development indicators | 127 warnings shown, contents uninspected |

\| Screenshot checkpoint | Conversation attachment received; planned \`artifacts/journey-mapping/catalog/catalog-04c-cleared.png\`, not verified locally |

Category application and clearing are now observed. Size and price controls have

only been seen, not exercised. Available sort options are recorded below.

**## Observed record — CAT-05a: opened Sort menu**

Evidence: user-supplied screenshot after opening \`Sort\` on the cleared listing.

\| Item | Observation |

\| --- | --- |

\| Entry/action | Unfiltered listing after CAT-04c; requested open \`Sort\` without selecting another option |

\| Visible options, top to bottom | \`Featured\`, \`Newest\`, \`Price: Low to High\`, \`Price: High to Low\`, \`Best Selling\` |

\| Current selection | Dot beside \`Featured\`; the trigger still reads \`Sort\` |

\| Listing state | \`All Products\`, \`Browse our full catalog.\`, \`32 products\`; no active filter chip or filter-count badge visible |

\| URL | Address bar outside capture; preceding CAT-04c URL recorded separately |

\| Network evidence | All selected, empty text filter, recording enabled, Keep log checked. Table empty while footer retains 22 requests; no individual request/status attributable to opening the menu is established. |

\| GraphQL | Not observed; no sort change has been exercised yet |

\| Expected versus observed | Menu opens and exposes a marked default choice plus four alternatives. Result ordering remains untested. |

\| Viewport | Responsive 759 × 762, Fit to window, No throttling |

\| Development indicators | 129 warnings shown; contents uninspected |

\| Screenshot checkpoint | Conversation attachment received; planned \`artifacts/journey-mapping/catalog/catalog-05a-sort-menu.png\`, not verified locally |

Candidate locators: the \`Sort\` trigger and each option by exact visible name,

scoped to the opened menu. Confirm rendered roles, accessible names, selection

properties, and uniqueness before adopting them. The menu overlays part of the

product grid; this is an intentional open-menu checkpoint.

**## Observed record — CAT-05b: Price Low to High applied**

Evidence: user-supplied screenshots after selecting `Price: Low to High` and
scrolling through the first four products in reading order.

| Item | Observation |
| --- | --- |
| Entry/action | Unfiltered 32-product listing; select `Price: Low to High` from the observed Sort menu and wait for the grid to settle |
| Final URL | `http://localhost:3000/en/default-channel/products?sort=price_asc` |
| Product count | `32 products` |
| Closed sort trigger | Still displays `Sort`; the selected option is represented by URL/result state rather than trigger text |
| First product | `Own your stack and data` — active price `$1.00`; original `$2.00` shown struck through; `-50%` badge |
| Second product | `Apple Juice` — `$1.99` |
| Third product | `Banana Juice` — `$1.99` |
| Fourth product | `Bean Juice` — `$1.99` |
| Visible ordering | `$1.00 → $1.99 → $1.99 → $1.99`, a non-decreasing four-card sample consistent with ascending price order |
| Discount treatment | Use the active displayed sale price (`$1.00`) rather than the struck-through compare-at price (`$2.00`) when checking visible ordering |
| Browser response | `products?sort=price_asc` document row shows HTTP 200 in the supplied Network capture |
| Backend evidence | Raw Saleor GraphQL request/result not captured; browser listing API evidence is recorded below |
| Expected versus observed | URL sort state and visible price sample agree with `Price: Low to High`. This sample supports the journey check but does not prove global ordering across all 32 products. |
| Viewport | Responsive 759 × 762, Fit to window, No throttling |
| Screenshot checkpoint | Conversation attachments received for the sorted listing and first four products; local artifact files not verified |

The literal trigger text `Sort` should not be used to assert the selected sort after
closing the menu. Prefer the URL sort parameter plus result behavior, or inspect the
menu's selected state when automation is implemented.

**## Observed record — CAT-06: cursor pagination**

Evidence: user-supplied screenshots for first-page pagination, one forward step,
and one backward step, followed by direct inspection of the browser listing API.

### CAT-06a — first-page pagination state

| Item | Observation |
| --- | --- |
| URL | `http://localhost:3000/en/default-channel/products?sort=price_asc` |
| Product count | `32 products` |
| Controls | `Previous` visually disabled; `Next` available |
| Products near bottom | `Mighty Mug` — `$11.99`; `Monokai Dimmed Sunnies` — `$17.00` |
| Expected versus observed | Pagination exists for the seeded 32-product catalog. First page has a usable forward control and visually disabled backward control. |

### CAT-06b — move forward with Next

| Item | Observation |
| --- | --- |
| Action | Click `Next` once and wait for the new page/grid state |
| URL state | `sort=price_asc` preserved and a dynamic `cursor` parameter added |
| Controls | Both `Previous` and `Next` available |
| Visible products near bottom | `Dark Polygon Tee` — `$45.00`; `Darko Polo` — `$45.00` |
| Browser traffic | `products?sort=price_asc&cursor=<dynamic>` fetch HTTP 200; `/api/listing?...` fetch HTTP 200 visible in Network |
| Expected versus observed | Forward pagination changes the product page while preserving sort state and enables backward navigation |

### CAT-06c — return with Previous

| Item | Observation |
| --- | --- |
| Action | Click `Previous` once from the later page |
| URL state | Cursor remains dynamic; backward navigation includes `direction=prev` while `sort=price_asc` is preserved |
| Visible products restored | `Mighty Mug` — `$11.99`; `Monokai Dimmed Sunnies` — `$17.00` |
| Controls | `Previous` returns to the visually disabled first-page state; `Next` remains available |
| Browser traffic | Products fetch and `/api/listing` fetch both show HTTP 200 |
| Expected versus observed | Earlier product state is restored. Cursor values are runtime pagination data and must not be hardcoded. |

The exact cursor token is intentionally omitted from journey expectations. Tests
should assert pagination behavior, direction, product-state change, and pageInfo
rather than literal cursor strings.

**## Browser listing API mapping**

Observed request during backward pagination:

```text
GET http://localhost:3000/api/listing
```

Observed query parameters:

```text
surface=all
locale=en
channel=default-channel
cursor=<dynamic>
direction=prev
sort=price_asc
```

Observed result:

```text
HTTP 200
```

The response contains product records with fields observed including:

```text
id
name
slug
brand
price
compareAtPrice
discountPercent
currency
image
href
category
createdAt
variant metadata
```

Example observed record: `Apple Juice`, slug `apple-juice`, price `1.99`, currency
`USD`, category `Juices`, and href `/en/default-channel/products/apple-juice`.

Observed pagination metadata:

```json
{
  "pageInfo": {
    "hasNextPage": true,
    "hasPreviousPage": false,
    "startCursor": "<dynamic>",
    "endCursor": "<dynamic>"
  },
  "totalCount": 32,
  "resolvedCategories": []
}
```

This browser endpoint is directly observed. Its downstream Saleor GraphQL operation
and raw GraphQL response were not captured in this walkthrough. Search remains
source-mapped to `SearchProducts` selecting `products`.

**## Stable locator candidates**

The following runtime DOM snippets were inspected after the visual walkthrough.
Dynamic CSS classes and generated IDs are not locator contracts.

| Element | Runtime evidence | Preferred future Playwright locator |
| --- | --- | --- |
| Filters | Rendered as a real `button` with visible text `Filters` and `aria-haspopup="dialog"`; responsive element includes `md:hidden` | `page.get_by_role("button", name="Filters")` |
| Sort | Rendered as a real `button` with visible text `Sort` and `aria-haspopup="menu"`; generated Radix `id` is dynamic | `page.get_by_role("button", name="Sort")` |
| Apple Juice product | Rendered as an `a` with `aria-label="Apple Juice"` and href `/en/default-channel/products/apple-juice` | `page.get_by_role("link", name="Apple Juice")` |
| Next | Rendered as an `a` with visible text `Next`; later-page capture has `aria-disabled="false"` and `direction=next` in href | `page.get_by_role("link", name="Next")` |
| Previous | Rendered as an `a` with visible text `Previous`; later-page capture has `aria-disabled="false"` and `direction=prev` in href | `page.get_by_role("link", name="Previous")` |

First-page `Previous` is visually confirmed disabled, but its exact disabled DOM
semantics were not separately copied. Do not hardcode generated IDs, Tailwind class
lists, complete pagination hrefs, or cursor values. The inspected `Filters` element
is responsive/mobile-specific, so desktop control parity should be verified when
desktop automation coverage is introduced.

**## Locator and visual evidence**

Runtime DOM inspection now supports semantic role/name locators for the primary
catalog controls and one representative product card. Prefer these over CSS class
chains, generated Radix IDs, or cursor-bearing hrefs.

Additional candidates that remain source/visual-backed rather than DOM-confirmed:
heading `All Products`, breadcrumb `Home` scoped to breadcrumb navigation, active
chip `Category: Juices`, `Clear all`, no-results heading, `Browse All Products`, and
`Go to Homepage`.

Candidate stable visual regions: settled heading, product-card structure, filter
controls, sort menu structure, pagination controls, and empty-state layout.

Data-dependent regions: product names, prices, total count, stock/availability,
product images, sale badges, and account state.

Transient/dynamic regions: loading states, focus/caret, open popovers/dialogs,
native browser validation UI, development UI, request cursors, request durations,
and generated `_rsc` values.

Prefer DOM assertions for accessible text and structured API assertions for product
records/pageInfo. No OCR requirement has been established for the catalog journey.

**## Completion checklist**

- [x] Observe listing URL, visible content, count, controls, and first product cards (CAT-01).
- [x] Observe direct search results for a known product (CAT-02); search-entry control itself was not exercised.
- [x] Observe no-results UI and recovery controls (CAT-03); raw backend zero-match result was not captured.
- [x] Observe return to listing UI after the requested recovery action; exact recovery destination URL was not separately captured.
- [x] Observe category filter application and clearing, including four returned Juices products (CAT-04).
- [x] Record available sort options/default selection and verify `Price: Low to High` with URL state and a non-decreasing four-card sample (CAT-05).
- [x] Observe cursor pagination forward and backward while preserving sort state (CAT-06).
- [x] Observe browser `/api/listing` request/response shape, HTTP 200, product data, `pageInfo`, and `totalCount`.
- [x] Map search GraphQL operation from source (`SearchProducts` → `products`) and explicitly record that raw runtime GraphQL traffic for listing/search was not captured.
- [x] Confirm primary semantic locator candidates for Filters, Sort, product link, Next, and Previous from rendered DOM.
- [x] Record screenshot checkpoints and stable/dynamic visual regions; no approved visual baselines claimed.
- [x] Review remaining gaps. Core manual catalog walkthrough is complete; search-entry submission, desktop filter DOM parity, exact first-page Previous DOM-disabled semantics, and raw backend GraphQL captures are follow-ups rather than blockers.
