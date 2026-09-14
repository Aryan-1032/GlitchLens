# Product detail journey — Saleor storefront

Phase: P01 — Explore Saleor customer journeys.

Status: COMPLETE — normal product state, add-to-bag behavior, and invalid-product negative path observed.

Target: Saleor storefront
Locale: `en`
Channel: `default-channel`

## Scope

Map a representative product detail page, its main purchase action, visible product information, and a negative path for an invalid product slug.

Primary product:

```text
Apple Juice
```

Route:

```text
/en/default-channel/products/apple-juice
```

## Observed product state

Observed URL:

```text
http://localhost:3000/en/default-channel/products/apple-juice
```

Breadcrumbs:

```text
Home → Juices → Apple Juice
```

Observed details:

| Field | Observation |
| --- | --- |
| Category | `Juices` |
| Product name | `Apple Juice` |
| Price | `$1.99` |
| Main image | Apple Juice bottle image visible |
| Main action | `Add to bag` |
| Quantity selector on product page | None observed |
| Variant selector | None observed |
| Stock text | None observed |
| Supporting text | `Secure checkout`; `Free delivery over $75.00` |

Observed description:

```text
Fell straight from the tree, on to Newton’s head, then into the bottle.
The autumn taste of English apples. Brought to you by gravity.
```

Observed sections:

```text
Description
Product Details
Shipping & Returns
```

A sticky lower purchase bar can also show `Add to bag`.

## Add-to-bag behavior

Action:

```text
Click Add to bag once
```

Observed result:

```text
Bag count changes from 0 to 1.
Product page remains visible.
No cart drawer opens automatically.
```

The bag-count change is the main observed success signal.

A related `apple-juice` fetch returned HTTP 200 during the interaction, but the exact backend GraphQL operation was not captured at runtime.

## Negative path — invalid product

Requested URL:

```text
/en/default-channel/products/does-not-exist-92741
```

Observed state:

```text
404
Product Not Found
```

Observed message:

```text
This product may have been removed, renamed, or is temporarily unavailable.
```

Observed recovery controls:

```text
Browse Products
Go Home
Go back
```

The bag count remained visible, showing cart state survived navigation to the invalid route.

## Stable locator candidates

```python
page.get_by_role("heading", name="Apple Juice")
page.get_by_role("button", name="Add to bag")
page.get_by_role("heading", name="Product Not Found")
page.get_by_role("link", name="Browse Products")
```

Because two `Add to bag` presentations may exist, scope the locator to the intended purchase region during Playwright implementation.

## Visual checkpoints

```text
product-default
product-purchase-section
product-added-to-bag
product-not-found
```

Potentially dynamic regions:

```text
product image loading
sticky purchase bar visibility
bag-count badge
promotional/free-shipping text
development UI
```

Formal visual baselines are deferred to P09.

## Expected automation assertions

```text
Valid product route loads expected product
Product name and price are visible
Add to bag is available
Add to bag increments bag count
Invalid product slug renders Product Not Found
Recovery actions are visible
```

## Known limitations

- Runtime GraphQL operation names were not captured.
- Variant behavior was not exercised.
- Stock/availability text was not visible.
- Final accessible-role uniqueness should be verified during Playwright implementation.
