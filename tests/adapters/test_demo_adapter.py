from adapters.demo_adapter import DEMO_CONFIG


def test_demo_adapter_loads():
    assert DEMO_CONFIG.metadata.key == "demo"


def test_demo_adapter_is_not_saleor_specific():
    assert DEMO_CONFIG.route("login") == "/login"
    assert DEMO_CONFIG.url_for("login") == "http://localhost:4000/login"


def test_demo_adapter_selector():
    selector = DEMO_CONFIG.selector("auth.submit")

    assert selector.role == "button"
    assert selector.name == "Login"