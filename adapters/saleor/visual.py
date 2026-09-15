from adapters.base import VisualCheckpointConfig


VISUAL_CHECKPOINTS = {
    # Authentication
    "auth.login": VisualCheckpointConfig(
        route_name="login",
        expected_components=(
            "login_form",
            "email_input",
            "password_input",
            "sign_in_button",
        ),
    ),

    # Catalog
    "catalog.products": VisualCheckpointConfig(
        route_name="products",
        expected_components=(
            "product_grid",
            "product_card",
            "sort_control",
        ),
    ),

    "catalog.no_results": VisualCheckpointConfig(
        route_name="search",
        expected_components=(
            "search_results",
            "empty_state",
        ),
    ),

    # Product
    "product.default": VisualCheckpointConfig(
        route_name="product_base",
        expected_components=(
            "product_image",
            "product_title",
            "product_price",
            "add_to_bag_button",
        ),
    ),

    "product.not_found": VisualCheckpointConfig(
        route_name="product_base",
        expected_components=(
            "error_state",
            "recovery_actions",
        ),
    ),

    # Cart
    "cart.one_item": VisualCheckpointConfig(
        route_name="product_base",
        expected_components=(
            "cart_drawer",
            "cart_item",
            "quantity_control",
            "checkout_button",
        ),
    ),

    "cart.empty": VisualCheckpointConfig(
        route_name="product_base",
        expected_components=(
            "cart_drawer",
            "empty_state",
            "start_shopping_button",
        ),
    ),

    # Checkout
    "checkout.information_validation": VisualCheckpointConfig(
        route_name="checkout",
        expected_components=(
            "checkout_form",
            "validation_error",
            "order_summary",
        ),
    ),

    "checkout.shipping": VisualCheckpointConfig(
        route_name="checkout",
        expected_components=(
            "shipping_methods",
            "order_summary",
            "continue_button",
        ),
    ),

    "checkout.payment": VisualCheckpointConfig(
        route_name="checkout",
        expected_components=(
            "payment_panel",
            "billing_address",
            "order_summary",
            "pay_button",
        ),
    ),

    "checkout.payment_failure": VisualCheckpointConfig(
        route_name="checkout",
        expected_components=(
            "payment_panel",
            "error_message",
            "order_summary",
        ),
    ),
}