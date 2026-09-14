from adapters.saleor import SALEOR_CONFIG


def test_saleor_config_loads():
    assert SALEOR_CONFIG.metadata.key == "saleor"


def test_saleor_login_route():
    assert (
        SALEOR_CONFIG.route("login")
        == "/en/default-channel/login"
    )


def test_saleor_auth_selector():
    selector = SALEOR_CONFIG.selector(
        "auth.submit"
    )

    assert selector.role == "button"
    assert selector.name == "Sign In"


def test_saleor_test_data():
    assert (
        SALEOR_CONFIG.test_value(
            "guest_checkout.email"
        )
        == "guest.test@example.com"
    )


def test_saleor_workflow_loads():
    workflow = SALEOR_CONFIG.workflow(
        "auth.invalid_login"
    )

    assert len(workflow) == 4


def test_saleor_visual_checkpoint():
    checkpoint = SALEOR_CONFIG.visual_checkpoint(
        "checkout.payment"
    )

    assert checkpoint.route_name == "checkout"
    assert "payment_panel" in checkpoint.expected_components