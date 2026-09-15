import os
import re
from pathlib import Path

import pytest
from playwright.sync_api import (
    Browser,
    BrowserContext,
    ConsoleMessage,
    Page,
    Playwright,
    Request,
    Response,
    sync_playwright,
)


ARTIFACT_ROOT = Path("artifacts") / "playwright"


def env_bool(name: str, default: bool = True) -> bool:
    value = os.getenv(name)

    if value is None:
        return default

    return value.strip().lower() not in {"0", "false", "no", "off"}


def safe_test_name(name: str) -> str:
    return re.sub(r"[^a-zA-Z0-9_.-]+", "_", name)


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    report = outcome.get_result()

    setattr(item, f"rep_{report.when}", report)


@pytest.fixture(scope="session")
def playwright_instance() -> Playwright:
    with sync_playwright() as playwright:
        yield playwright


@pytest.fixture(scope="session")
def browser(playwright_instance: Playwright) -> Browser:
    headless = env_bool("PW_HEADLESS", default=True)

    browser = playwright_instance.chromium.launch(
        headless=headless,
    )

    yield browser

    browser.close()


@pytest.fixture
def artifact_dir(request) -> Path:
    test_name = safe_test_name(request.node.name)

    path = ARTIFACT_ROOT / test_name
    path.mkdir(parents=True, exist_ok=True)

    return path


@pytest.fixture
def context(
    browser: Browser,
    artifact_dir: Path,
) -> BrowserContext:
    context = browser.new_context(
        viewport={
            "width": 1440,
            "height": 900,
        }
    )

    context.tracing.start(
        screenshots=True,
        snapshots=True,
        sources=True,
    )

    yield context

    context.tracing.stop(
        path=artifact_dir / "trace.zip",
    )

    context.close()


@pytest.fixture
def page(
    context: BrowserContext,
    artifact_dir: Path,
    request,
) -> Page:
    page = context.new_page()

    console_messages: list[str] = []
    network_failures: list[str] = []

    def handle_console(message: ConsoleMessage):
        console_messages.append(
            f"[{message.type}] {message.text}"
        )

    def handle_request_failed(request_obj: Request):
        failure = request_obj.failure

        network_failures.append(
            f"REQUEST FAILED | {request_obj.method} "
            f"{request_obj.url} | {failure}"
        )

    def handle_response(response: Response):
        if response.status >= 400:
            network_failures.append(
                f"HTTP {response.status} | "
                f"{response.request.method} "
                f"{response.url}"
            )

    page.on("console", handle_console)
    page.on("requestfailed", handle_request_failed)
    page.on("response", handle_response)

    yield page

    console_path = artifact_dir / "console.log"
    console_path.write_text(
        "\n".join(console_messages),
        encoding="utf-8",
    )

    network_path = artifact_dir / "network_failures.log"
    network_path.write_text(
        "\n".join(network_failures),
        encoding="utf-8",
    )

    report = getattr(request.node, "rep_call", None)

    if report is not None and report.failed:
        page.screenshot(
            path=artifact_dir / "failure.png",
            full_page=True,
        )