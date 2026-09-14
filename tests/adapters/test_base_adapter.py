import pytest

from adapters.base import (
    AdapterConfigError,
    TargetAdapterConfig,
    TargetEnvironment,
    TargetMetadata,
    WorkflowAction,
    WorkflowStepConfig,
    LocatorConfig,
    LocatorType
)


def make_base_config(**overrides):
    data = {
        "metadata": TargetMetadata(
            key="demo",
            name="Demo Adapter",
        ),
        "environment": TargetEnvironment(
            storefront_url="http://localhost:3000",
        ),
        "routes": {
            "home": "/",
            "login": "/login",
        },
    }

    data.update(overrides)

    return TargetAdapterConfig(**data)


def test_valid_config_loads():
    config = make_base_config()

    assert config.metadata.key == "demo"
    assert config.route("login") == "/login"
    assert config.url_for("login") == "http://localhost:3000/login"


def test_invalid_storefront_url_fails():
    with pytest.raises(
        AdapterConfigError,
        match="storefront_url must be a valid",
    ):
        TargetEnvironment(
            storefront_url="not-a-url",
        )


def test_unknown_route_fails():
    config = make_base_config()

    with pytest.raises(
        AdapterConfigError,
        match="Route 'checkout' is not defined",
    ):
        config.route("checkout")


def test_workflow_with_unknown_selector_fails():
    with pytest.raises(
        AdapterConfigError,
        match="unknown selector 'missing.button'",
    ):
        make_base_config(
            workflows={
                "broken_flow": (
                    WorkflowStepConfig(
                        action=WorkflowAction.CLICK,
                        selector_name="missing.button",
                    ),
                ),
            }
        )


def test_invalid_test_data_reference_format_fails():
    with pytest.raises(
        AdapterConfigError,
        match="Expected format: 'group.key'",
    ):
        make_base_config(
            selectors={
                "field": LocatorConfig(
                    by=LocatorType.LABEL,
                    value="Field",
                ),
            },
            workflows={
                "broken_flow": (
                    WorkflowStepConfig(
                        action=WorkflowAction.FILL,
                        selector_name="field",
                        value_from="invalid.reference.format",
                    ),
                ),
            },
        )