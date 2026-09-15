from adapters.base import LocatorConfig, LocatorType


SELECTORS = {
    # Authentication
    "auth.email": LocatorConfig(
        by=LocatorType.LABEL,
        value="Email",
    ),
    "auth.password": LocatorConfig(
        by=LocatorType.LABEL,
        value="Password",
    ),
    "auth.submit": LocatorConfig(
        by=LocatorType.ROLE,
        role="button",
        name="Sign In",
    ),

    # Catalog
    "catalog.sort": LocatorConfig(
        by=LocatorType.ROLE,
        role="button",
        name="Sort",
    ),
    "catalog.apple_juice": LocatorConfig(
        by=LocatorType.ROLE,
        role="link",
        name="Apple Juice",
    ),
    "catalog.next": LocatorConfig(
        by=LocatorType.ROLE,
        role="link",
        name="Next",
    ),
    "catalog.previous": LocatorConfig(
        by=LocatorType.ROLE,
        role="link",
        name="Previous",
    ),

    # Product
    "product.add_to_bag": LocatorConfig(
        by=LocatorType.ROLE,
        role="button",
        name="Add to bag",
    ),

    # Checkout
    "checkout.email": LocatorConfig(
        by=LocatorType.LABEL,
        value="Email address",
    ),
    "checkout.first_name": LocatorConfig(
        by=LocatorType.LABEL,
        value="First name",
    ),
    "checkout.last_name": LocatorConfig(
        by=LocatorType.LABEL,
        value="Last name",
    ),
    "checkout.street": LocatorConfig(
        by=LocatorType.LABEL,
        value="Street address",
    ),
    "checkout.city": LocatorConfig(
        by=LocatorType.LABEL,
        value="City",
    ),
    "checkout.continue_shipping": LocatorConfig(
        by=LocatorType.ROLE,
        role="button",
        name="Continue to shipping",
    ),
    "checkout.continue_payment": LocatorConfig(
        by=LocatorType.ROLE,
        role="button",
        name="Continue to payment",
    ),
}