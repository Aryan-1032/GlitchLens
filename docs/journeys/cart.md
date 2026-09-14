# Cart journey — Saleor storefront

Phase: P01 — Explore Saleor customer journeys.

Status: COMPLETE — cart open state, quantity update, totals, removal, and empty-cart state observed.

Target: Saleor storefront
Mode: Guest user
Locale: `en`
Channel: `default-channel`

## Scope

Map the guest bag/cart starting from one Apple Juice item already added from the product page.

## Initial bag state

Observed drawer:

```text
Your Bag
```

Observed initial state:

| Field | Observation |
| --- | --- |
| Item count | `1 item` |
| Product | `Apple Juice` |
| Quantity | `1` |
| Price | `$1.99` |
| Subtotal | `$1.99` |
| Shipping | `Calculated at checkout` |
| Total | `$1.99` |
| Free-shipping message | `Add $73.01 more for free shipping` |
| Primary action | `Checkout` |
| Secondary action | `Continue Shopping` |
| Remove control | Trash/delete icon visible |

The bag opens as a side drawer over the current page.

## Quantity update

Action:

```text
Increase Apple Juice quantity from 1 to 2.
```

Observed result:

```text
Your Bag (2 items)
Quantity: 2
Line total: $3.98
Subtotal: $3.98
Total: $3.98
Free-shipping remaining: $71.02
```

Observed arithmetic:

```text
$1.99 × 2 = $3.98
```

The bag count therefore represents total item quantity, not only distinct product lines.

## Remove item / empty-cart state

Action:

```text
Remove Apple Juice using the trash control.
```

Observed result:

```text
Your Bag (0 items)
Your bag is empty
Looks like you haven't added anything to your bag yet.
Start Shopping
```

Observed state changes:

```text
Product row disappears
Quantity controls disappear
Subtotal/total disappear
Checkout action disappears
```

## Stable locator candidates

Candidates for later automation:

```text
Your Bag
Apple Juice
Checkout
Continue Shopping
Start Shopping
```

Quantity and remove-control accessible names still need DOM verification.

Because the cart is a drawer, future locators should be scoped to the cart region.

## Visual checkpoints

```text
cart-one-item
cart-quantity-two
cart-empty
```

Potentially dynamic regions:

```text
product thumbnail loading
bag-count badge
free-shipping remaining amount
line/subtotal/total values
drawer animation
development UI
```

## Expected automation assertions

```text
Opening bag shows added product
Quantity can increase
Line total updates correctly
Subtotal/total update correctly
Bag count reflects quantity
Removing the final item produces empty-cart state
Checkout is unavailable when cart is empty
```

## Known limitations

- Exact backend mutations for quantity update/removal were not captured.
- Product thumbnail loading looked inconsistent in some screenshots; this was not classified as a defect.
- Accessible names for plus/minus/remove controls still need DOM verification.
