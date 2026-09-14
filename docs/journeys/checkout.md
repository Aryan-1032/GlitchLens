# Checkout journey — Saleor storefront

Phase: P01 — Explore Saleor customer journeys.

Status: COMPLETE FOR P01 — guest checkout mapped through payment submission. Successful order completion is blocked by local payment-app configuration.

Target: Saleor storefront
Mode: Guest checkout
Locale: `en`

## Scope

Map guest checkout from Cart through Information, Shipping, and Payment, including validation and the final local payment failure.

The checkout ID in the URL is dynamic and must never be hardcoded.

## Checkout structure

Observed flow:

```text
1. Information
2. Shipping
3. Payment
```

At responsive width the checkout is mostly single-column.

At wider desktop width it becomes two-column with the form on the left and order summary on the right.

Responsive layout changes are expected behavior, not visual regressions.

## Step 1 — Information

Observed order summary:

```text
1 item
$1.99
```

Observed contact controls:

```text
Email address
Have an account? Log in
Create an account for faster checkout next time
Email me with news and offers
```

Observed shipping-address fields:

```text
Country/Region
First name
Last name
Company (optional)
Street address
Apt, suite, etc. (optional)
City
Postal code
Phone (optional)
```

Primary action:

```text
Continue to shipping
```

### Empty-form negative path

Submitting with required fields empty produced:

```text
Email is required
First name is required
Last name is required
Street address is required
City is required
```

The form remained on Step 1.

### Country-dependent validation

With Afghanistan selected, Postal code appeared optional and no State field was visible.

After selecting India:

```text
Postal code → required
State       → required
```

Automation must not assume one universal address schema.

### Fake test data used

```text
Email: guest.test@example.com
Country: India
First name: Test
Last name: User
Street address: 123 Test Street
City: Pune
Postal code: 411001
State: Maharashtra
```

Optional fields were left empty.

## Step 2 — Shipping

Observed state:

```text
Step 2 of 3 — Shipping
```

Observed contact/address:

```text
guest.test@example.com
123 Test Street, PUNE 411001, India
```

Observed shipping methods:

| Method | Price | Initial selection |
| --- | ---: | --- |
| Aramex | `$21.15` | Selected |
| TNT | `$28.87` | Not selected |
| EMS | `$75.71` | Not selected |
| China Post | `$82.33` | Not selected |

Primary action:

```text
Continue to payment
```

The checkout URL contained dynamic checkout state plus:

```text
step=shipping
locale=en
```

Do not assert the literal checkout identifier.

## Step 3 — Payment

Observed mode:

```text
Dummy — Test mode
```

Observed message:

```text
No card details needed — use Pay to complete a test order.
```

Displayed dummy card:

```text
•••• •••• •••• 4242
TEST CARDHOLDER
12/28
```

Billing:

```text
Same as shipping address = checked
```

Observed total:

```text
Product:  $1.99
Aramex:  $21.15
----------------
Total:   $23.14
```

Primary action:

```text
Pay $23.14
```

## Final payment result

Observed after clicking Pay:

```text
Payment failed
App with provided identifier not found.
```

The checkout remained on Payment.

This is recorded as a local environment / payment-app configuration limitation, not a form-validation defect.

For P01, the checkout journey is sufficiently mapped.

Successful order placement is deferred until the checkout regression test is implemented and the local payment app/configuration is fixed.

## Stable locator candidates

```python
page.get_by_label("Email address")
page.get_by_label("First name")
page.get_by_label("Last name")
page.get_by_label("Street address")
page.get_by_label("City")
page.get_by_role("button", name="Continue to shipping")
page.get_by_role("button", name="Continue to payment")
```

Country, State, shipping methods, and Pay should be finalized against rendered roles during Playwright implementation.

## Dynamic values

Never hardcode:

```text
checkout ID
shipping availability
shipping prices
country/state requirements
final total
test-data-specific address
responsive layout dimensions
```

## Visual checkpoints

```text
checkout-information-empty
checkout-information-validation
checkout-information-filled
checkout-shipping
checkout-payment
checkout-payment-failure
```

Separate visual baselines should be maintained per viewport.

## Expected automation assertions

```text
Guest cart can enter checkout
Required-field validation blocks progress
Country can change required address schema
Valid fake address reaches Shipping
Shipping method can be selected
Shipping selection contributes to total
Payment step renders dummy test mode
Billing defaults to shipping address
Payment configuration failure is surfaced clearly when payment app is unavailable
```

A separate future regression should cover successful order confirmation once local payment configuration is fixed.
