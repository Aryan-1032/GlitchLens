# P01 Journey Map — Saleor storefront

Phase: P01 — Explore Saleor customer journeys.

Status: COMPLETE FOR CORE JOURNEYS

This document links the core customer journeys to routes, important UI states, browser/API evidence, negative paths, and future automation strategy.

## Core journey coverage

| Journey | Primary route/state | Main success signal | Negative/error path | Status |
| --- | --- | --- | --- | --- |
| Authentication | `/en/default-channel/login` | HTTP 200 login + authenticated account UI | Invalid credentials → HTTP 401 + error banner | Complete |
| Catalog | `/en/default-channel/products` | Listing/search/filter/sort/pagination update correctly | No-results search | Complete |
| Product detail | `/en/default-channel/products/apple-juice` | Product visible; Add to bag increments bag count | Invalid slug → Product Not Found | Complete |
| Cart | Bag drawer | Quantity/totals update correctly | Remove last item → empty bag | Complete |
| Checkout | `/checkout?...` | Reach Information → Shipping → Payment | Empty required fields; final payment config failure | Complete for P01 |

## Route map

```text
Home
/en/default-channel
    |
    +--> Login
    |    /en/default-channel/login
    |
    +--> Products
    |    /en/default-channel/products
    |        |
    |        +--> Search
    |        |    /en/default-channel/search?query=<term>
    |        |
    |        +--> Product
    |             /en/default-channel/products/apple-juice
    |
    +--> Account
    |    /en/default-channel/account
    |
    +--> Bag / Cart drawer
             |
             +--> Checkout
                  /checkout?checkout=<dynamic>&step=<dynamic>&locale=en
```

## Stable locator summary

### Authentication

```python
page.get_by_role("link", name="Log in")
page.get_by_role("heading", name="Welcome Back")
page.get_by_label("Email")
page.get_by_label("Password")
page.get_by_role("button", name="Sign In")
```

### Catalog

Runtime DOM confirmed:

```python
page.get_by_role("button", name="Filters")
page.get_by_role("button", name="Sort")
page.get_by_role("link", name="Apple Juice")
page.get_by_role("link", name="Next")
page.get_by_role("link", name="Previous")
```

Notes:

```text
Filters was observed in responsive/mobile layout.
Sort opens a menu.
Product link has aria-label="Apple Juice".
Pagination cursor values are dynamic.
```

### Product

```python
page.get_by_role("heading", name="Apple Juice")
page.get_by_role("button", name="Add to bag")
page.get_by_role("heading", name="Product Not Found")
```

Scope `Add to bag` because a sticky purchase presentation may create multiple matches.

### Cart

Candidates:

```text
Your Bag
Apple Juice
Checkout
Continue Shopping
Start Shopping
```

Quantity and remove-control accessible names still need DOM verification.

### Checkout

```python
page.get_by_label("Email address")
page.get_by_label("First name")
page.get_by_label("Last name")
page.get_by_label("Street address")
page.get_by_label("City")
page.get_by_role("button", name="Continue to shipping")
page.get_by_role("button", name="Continue to payment")
```

Country, State, shipping methods, and Pay should be finalized during Playwright implementation.

## Browser/API mapping

### Authentication

Observed browser endpoint:

```text
POST /api/auth/login
```

Observed outcomes:

```text
Invalid credentials → HTTP 401
Valid credentials   → HTTP 200 {"ok": true}
```

Source-mapped Saleor operations:

```text
tokenCreate
CurrentUser
CurrentUserProfile
CheckoutCustomerDetach
tokenRefresh / refreshToken
```

Raw backend GraphQL traffic was not directly captured.

### Catalog

Observed browser listing endpoint:

```text
GET /api/listing
```

Observed parameters include:

```text
surface=all
locale=en
channel=default-channel
cursor=<dynamic>
direction=next|prev
sort=price_asc
```

Observed status:

```text
200
```

Observed response data includes:

```text
products[]
id
name
slug
brand
price
currency
image
href
category
createdAt
pageInfo
totalCount
resolvedCategories
```

Observed pagination metadata:

```text
pageInfo.hasNextPage
pageInfo.hasPreviousPage
pageInfo.startCursor
pageInfo.endCursor
totalCount
```

Cursor values must never be hardcoded.

Source-mapped search GraphQL operation:

```text
SearchProducts
```

### Product / Cart / Checkout

Runtime backend GraphQL operation names were not captured.

Browser behavior and UI evidence were sufficient for P01.

Identify exact backend operations during P02/P06 where they are required by adapter/API tests.

## Negative/error path summary

| Journey | Negative case | Observed result |
| --- | --- | --- |
| Auth | Empty form | Native required-field validation |
| Auth | Invalid email | Native email-format validation |
| Auth | Unknown/wrong credentials | HTTP 401 + `Invalid email or password. Please try again.` |
| Catalog | Unmatched search | No-results state + recovery controls |
| Product | Invalid slug | `404 Product Not Found` |
| Cart | Remove final item | `Your bag is empty` |
| Checkout | Empty required fields | Inline required-field errors; remain on Information |
| Checkout | Local payment app unavailable | `Payment failed — App with provided identifier not found.` |

## Expected visible text

Important stable text:

```text
Welcome Back
Sign In
Invalid email or password. Please try again.
All Products
Filters
Sort
Product Not Found
Add to bag
Your Bag
Your bag is empty
Start Shopping
Continue to shipping
Continue to payment
Payment failed
```

Product names, prices, counts, shipping options, account identity, and totals are data-dependent.

## Dynamic / flaky visual regions

Potentially unstable regions:

```text
account initials/name/email
product images while loading
product count
prices
promotional homepage content
free-shipping progress text
pagination cursor values
checkout identifiers
shipping methods/prices
final totals
responsive layout differences
focus/caret
browser-native validation bubbles
drawer/open-menu animation
loading states
development badge
Next.js development overlays
transient development warnings/errors
```

Separate visual baselines should be used for different viewport classes.

Do not classify responsive layout changes as regressions.

## Screenshot/evidence policy

P01 screenshots are exploratory evidence, useful for:

```text
journey understanding
future visual-baseline design
future YOLO dataset planning
locator/context review
```

They are not approved visual baselines.

Formal baselines belong to P09.

## Checkout limitation

Guest checkout reaches Payment successfully.

Final payment currently fails locally with:

```text
App with provided identifier not found.
```

Treat this as a known local payment-app configuration dependency.

Do not block P02/P03/P04 on fixing it.

Resolve it when implementing the successful checkout regression path.

## Handoff to P02

P01 established enough target knowledge to begin the Saleor adapter.

P02 should convert the observations into target-specific configuration for:

```text
base URLs
routes
semantic locator definitions
expected text
customer workflows
browser endpoints
GraphQL operation references
test data
visual checkpoints
dynamic-region rules
known environment limitations
```

Saleor-specific details must remain under:

```text
adapters/saleor/
```

The generic core must not import Saleor constants directly.
