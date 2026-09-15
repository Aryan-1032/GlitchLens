import pytest
from playwright.sync_api import Page, expect

from adapters.saleor.config import SALEOR_CONFIG
from glitchlens.browser.target_page import TargetPage


@pytest.mark.smoke
def test_product_listing_loads(page: Page):
    target = TargetPage(
        page=page,
        adapter=SALEOR_CONFIG,
    )

    response = target.goto("products")

    assert response is not None
    assert response.ok

    expect(page).to_have_title(
        "All Products | Saleor Store"
    )

    expect(
        target.locator("catalog.sort")
    ).to_be_visible()

    expect(
        target.locator("catalog.apple_juice")
    ).to_be_visible()