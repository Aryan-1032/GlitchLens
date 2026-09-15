from typing import Literal

from playwright.sync_api import Locator, Page

from adapters.base import LocatorConfig, LocatorType


LocatorState = Literal["attached", "detached", "visible", "hidden"]


def resolve_locator(page: Page, config: LocatorConfig) -> Locator:
    if config.by == LocatorType.ROLE:
        return page.get_by_role(
            config.role,
            name=config.name,
            exact=config.exact,
        )

    if config.by == LocatorType.LABEL:
        return page.get_by_label(
            config.value,
            exact=config.exact,
        )

    if config.by == LocatorType.TEXT:
        return page.get_by_text(
            config.value,
            exact=config.exact,
        )

    if config.by == LocatorType.TEST_ID:
        return page.get_by_test_id(config.value)

    if config.by == LocatorType.PLACEHOLDER:
        return page.get_by_placeholder(
            config.value,
            exact=config.exact,
        )

    if config.by == LocatorType.CSS:
        return page.locator(config.value)

    raise ValueError(f"Unsupported locator type: {config.by}")


def wait_for_locator(
    page: Page,
    config: LocatorConfig,
    state: LocatorState = "visible",
    timeout_ms: int = 5_000,
) -> Locator:
    locator = resolve_locator(page, config)

    locator.wait_for(
        state=state,
        timeout=timeout_ms,
    )

    return locator