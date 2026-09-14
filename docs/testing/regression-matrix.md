# Regression Test Matrix

This matrix defines the approved test scenarios for the AI Web Testing Platform.

Initial validation target: Saleor.

## Layer meaning

- Browser = verify behavior through the real UI
- API = verify the backend/API contract directly
- Both = run browser verification and a corresponding direct API/backend verification
- Network = supporting evidence captured during a browser test; it does not replace a direct API test when the layer is `Both`

## Test scenarios

| ID | Journey | Scenario | User State | Layer | Evidence | Pass Criteria |
| --- | --- | --- | --- | --- | --- | --- |
| AUTH-001 | Authentication | Login with valid customer credentials | Anonymous → Authenticated | Both | DOM + Network + Screenshot | Login request succeeds and authenticated account state is visible |
| CAT-001 | Catalog | Open product listing | Anonymous | Browser | DOM + Screenshot | Product listing loads and at least one product card is visible |
| CAT-002 | Catalog | Search for an existing product | Anonymous | Both | DOM + Network + Screenshot | Search request succeeds and matching product is visible |
| CAT-003 | Catalog | Filter products by category | Anonymous | Browser | DOM + Screenshot | Selected category is applied and only matching products are shown |
| CAT-004 | Catalog | Sort products by price low-to-high | Anonymous | Browser | DOM | Visible product prices are in non-decreasing order |
| CAT-005 | Catalog | Navigate to next and previous listing pages | Anonymous | Browser | DOM + URL | Next page changes the product set and Previous returns to the earlier set |
| PROD-001 | Product | Open valid product detail page | Anonymous | Both | DOM + Screenshot + Network | Product title, price, image and add-to-bag action are visible |
| PROD-002 | Product | Add product to bag | Anonymous | Both | DOM + Screenshot | Bag quantity increases after add-to-bag |
| CART-001 | Cart | Open bag containing product | Anonymous | Browser | DOM + Screenshot | Added product, quantity and cart totals are visible |
| CART-002 | Cart | Increase product quantity | Anonymous | Both | DOM + Screenshot | Quantity increases and line/cart totals update consistently |
| CART-003 | Cart | Remove one product while another product remains in the bag | Anonymous | Both | DOM + API + Screenshot | Selected product is removed, remaining product stays in the cart, and cart does not enter empty state |
| CHK-001 | Checkout | Enter guest checkout from cart | Anonymous | Browser | DOM + Screenshot | Information step and order summary are visible |
| CHK-002 | Checkout | Submit valid guest shipping information | Anonymous | Both | DOM + Network + Screenshot | Valid address is accepted and checkout advances to Shipping |
| CHK-003 | Checkout | Select shipping method | Anonymous | Both | DOM + Screenshot | Selected shipping method is reflected in the order total |
| CHK-004 | Checkout | Continue to payment | Anonymous | Browser | DOM + Screenshot | Payment step loads and dummy test payment option is visible |
| AUTH-002 | Authentication | Login with invalid credentials | Anonymous | Both | DOM + Network + Screenshot | Login is rejected, HTTP/auth request indicates failure, and `Invalid email or password. Please try again.` is visible |
| CART-004 | Cart | Remove the last product from the bag | Anonymous | Browser | DOM + Screenshot | Cart becomes empty, checkout controls disappear, and `Your bag is empty` is visible |
| CHK-005 | Checkout | Submit checkout Information step with required fields empty | Anonymous | Browser | DOM + Screenshot | Checkout stays on Information step and required-field validation messages are visible |
| CHK-006 | Checkout | Attempt payment when local payment app is unavailable | Anonymous | Both | DOM + Network + Screenshot | Payment does not complete and `Payment failed` with `App with provided identifier not found.` is shown |


## Test data requirements

| Test ID | Test data required | Source |
| --- | --- | --- |
| AUTH-001 | Valid test customer email and password | Environment variables / secrets |
| AUTH-002 | Invalid email and password | `invalid_login` adapter test data |
| CAT-001 | Seeded catalog with at least one product | Saleor seed data |
| CAT-002 | Search query `Apple` | `search.valid_query` |
| CAT-003 | Category `Juices` | Saleor seed data |
| CAT-004 | Sort mode `price_asc` | Scenario configuration |
| CAT-005 | Product listing with more than one page | Saleor seed data; pagination cursor generated at runtime |
| PROD-001 | Product slug `apple-juice` | `product.slug` |
| PROD-002 | Product slug `apple-juice` | `product.slug` |
| CART-001 | Bag containing one Apple Juice | Setup step using `product.slug` |
| CART-002 | Bag containing one Apple Juice | Setup step using `product.slug` |
| CART-003 | Bag containing Apple Juice and one additional seeded product | Setup step using seeded product data |
| CART-004 | Bag containing exactly one Apple Juice | Setup step using `product.slug` |
| CHK-001 | Bag containing one product | Cart setup |
| CHK-002 | Valid fake guest shipping address | `guest_checkout` adapter test data |
| CHK-003 | Valid checkout plus an available shipping method | Guest checkout setup; shipping method discovered at runtime |
| CHK-004 | Valid checkout with selected shipping method | Guest checkout setup |
| CHK-005 | Empty required checkout fields | No input data; intentional validation test |
| CHK-006 | Valid checkout reaching Payment | Guest checkout setup; local payment-app failure condition |

## Visual validation plan

| Test ID | Screenshot checkpoint | Expected UI components for YOLO | Expected OCR text |
| --- | --- | --- | --- |
| AUTH-001 | After successful login | account_state, navigation | N/A — authenticated state is verified primarily by DOM/UI state |
| AUTH-002 | After invalid login attempt | login_form, error_message | Invalid email or password. Please try again. |
| CAT-001 | Product listing loaded | product_grid, product_card, filters_control, sort_control | Product names and prices |
| CAT-002 | Search results loaded | product_grid, product_card | Apple Juice |
| PROD-001 | Product detail loaded | product_image, product_title, product_price, add_to_bag_button | Apple Juice, $1.99, Add to bag |
| PROD-002 | After Add to bag | product_page, bag_badge | Apple Juice |
| CART-001 | Cart drawer open | cart_drawer, cart_item, quantity_control, checkout_button | Your Bag, Apple Juice |
| CART-002 | Quantity increased | cart_drawer, cart_item, quantity_control | Apple Juice, 2, $3.98 |
| CART-003 | One item removed while another remains | cart_drawer, cart_item, checkout_button | Remaining product name and updated cart total |
| CART-004 | Last item removed | cart_drawer, empty_state, start_shopping_button | Your bag is empty, Start Shopping |
| CHK-001 | Checkout Information step | checkout_form, order_summary | Information |
| CHK-002 | Shipping step loaded | shipping_methods, order_summary, continue_button | Shipping |
| CHK-003 | Shipping method selected | shipping_methods, order_summary | Shipping; runtime-selected shipping method; runtime-derived total |
| CHK-004 | Payment step loaded | payment_panel, billing_address, order_summary, pay_button | Payment, Dummy, Pay |
| CHK-005 | Information validation errors | checkout_form, validation_error, order_summary | Email is required, First name is required, Last name is required, Street address is required, City is required |
| CHK-006 | Payment failure | payment_panel, error_message, order_summary | Payment failed, App with provided identifier not found. |

## Execution priority and state management

| Test ID | Suite | Priority | Setup | Cleanup |
| --- | --- | --- | --- | --- |
| AUTH-001 | Smoke | High | Start logged out; valid credentials available from environment | Log out after test |
| AUTH-002 | Smoke, Negative | High | Start logged out | Clear login form/session |
| CAT-001 | Smoke | High | Seeded catalog available | None |
| CAT-002 | Smoke | High | Seeded Apple Juice product available | Clear search state |
| CAT-003 | Regression | Medium | Seeded Juices category available | Clear filters |
| CAT-004 | Regression | Medium | Seeded catalog with multiple prices | Reset sort state |
| CAT-005 | Regression | Medium | Catalog has multiple pages | Return to initial listing state |
| PROD-001 | Smoke | High | Apple Juice exists | None |
| PROD-002 | Smoke | High | Empty bag; Apple Juice exists | Remove product from bag |
| CART-001 | Smoke | High | Add one Apple Juice to bag | Empty bag |
| CART-002 | Regression | High | Bag contains one Apple Juice | Empty bag |
| CART-003 | Regression | Medium | Bag contains Apple Juice and one additional product | Empty bag |
| CART-004 | Negative | Medium | Bag contains exactly one Apple Juice | Ensure bag empty |
| CHK-001 | Smoke | High | Bag contains one product | Discard checkout/cart state |
| CHK-002 | Regression | High | Checkout at Information step | Discard checkout/cart state |
| CHK-003 | Regression | High | Valid checkout at Shipping step | Discard checkout/cart state |
| CHK-004 | Smoke | High | Valid checkout with shipping selected | Discard checkout/cart state |
| CHK-005 | Negative | High | Checkout at Information step with empty fields | Discard checkout/cart state |
| CHK-006 | Negative | High | Checkout reaches Payment; payment app remains unavailable | Discard checkout/cart state |

## Known environment limitation

Successful order placement is not currently part of the approved regression matrix.

The local Saleor checkout reaches the Payment step, but payment submission currently fails with:

`App with provided identifier not found.`

A successful order-completion scenario will be added after the local payment-app configuration is repaired. Until then, CHK-006 intentionally validates the observed payment failure state.