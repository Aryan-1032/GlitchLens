from playwright.sync_api import Locator, Page, Response

from adapters.base import TargetAdapterConfig
from glitchlens.browser.locators import resolve_locator, wait_for_locator


class TargetPage:
    def __init__(
        self,
        page: Page,
        adapter: TargetAdapterConfig,
    ):
        self.page = page
        self.adapter = adapter

    def goto(
        self,
        route_name: str,
        timeout_ms: int = 30_000,
    ) -> Response | None:
        return self.page.goto(
            self.adapter.url_for(route_name),
            wait_until="domcontentloaded",
            timeout=timeout_ms,
        )

    def locator(self, selector_name: str) -> Locator:
        config = self.adapter.selector(selector_name)

        return resolve_locator(
            self.page,
            config,
        )

    def wait_for(
        self,
        selector_name: str,
        timeout_ms: int = 5_000,
    ) -> Locator:
        config = self.adapter.selector(selector_name)

        return wait_for_locator(
            self.page,
            config,
            state="visible",
            timeout_ms=timeout_ms,
        )