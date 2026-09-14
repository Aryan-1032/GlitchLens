from adapters.base import (
    LocatorConfig,
    LocatorType,
    TargetAdapterConfig,
    TargetEnvironment,
    TargetMetadata,
)


DEMO_CONFIG = TargetAdapterConfig(
    metadata=TargetMetadata(
        key="demo",
        name="Demo Adapter",
        description="Minimal non-Saleor adapter used to prove generic core behavior.",
    ),
    environment=TargetEnvironment(
        storefront_url="http://localhost:4000",
    ),
    routes={
        "home": "/",
        "login": "/login",
    },
    selectors={
        "auth.email": LocatorConfig(
            by=LocatorType.LABEL,
            value="Email",
        ),
        "auth.submit": LocatorConfig(
            by=LocatorType.ROLE,
            role="button",
            name="Login",
        ),
    },
    test_data={
        "user": {
            "email": "demo@example.com",
        },
    },
    expected_text={
        "auth.heading": "Demo Login",
    },
)