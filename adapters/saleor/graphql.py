from adapters.base import (
    GraphQLOperationConfig,
    GraphQLOperationType,
)


GRAPHQL_OPERATIONS = {
    "auth.token_create": GraphQLOperationConfig(
        operation_name="tokenCreate",
        operation_type=GraphQLOperationType.MUTATION,
        purpose="Authenticate a customer and create an access token.",
        runtime_verified=False,
    ),

    "auth.current_user": GraphQLOperationConfig(
        operation_name="CurrentUser",
        operation_type=GraphQLOperationType.QUERY,
        purpose="Load the currently authenticated customer.",
        runtime_verified=False,
    ),

    "auth.current_user_profile": GraphQLOperationConfig(
        operation_name="CurrentUserProfile",
        operation_type=GraphQLOperationType.QUERY,
        purpose="Load authenticated customer profile information.",
        runtime_verified=False,
    ),

    "auth.checkout_customer_detach": GraphQLOperationConfig(
        operation_name="CheckoutCustomerDetach",
        operation_type=GraphQLOperationType.MUTATION,
        purpose="Detach the authenticated customer from a checkout.",
        runtime_verified=False,
    ),

    "catalog.search_products": GraphQLOperationConfig(
        operation_name="SearchProducts",
        operation_type=GraphQLOperationType.QUERY,
        purpose="Search products in the storefront catalog.",
        runtime_verified=False,
    ),
}