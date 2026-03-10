import pytest
from playwright.sync_api import sync_playwright
import os


@pytest.fixture(scope="function")
def page(request):
    os.makedirs("traces", exist_ok=True)

    test_file = os.path.splitext(os.path.basename(request.node.fspath))[0]
    trace_path = os.path.abspath(f"traces/{test_file}.zip")

    print(f"\n[TRACE] Saving trace to: {trace_path}")

    with sync_playwright() as playwright:
        browser = playwright.firefox.launch(headless=False)
        context = browser.new_context()

        context.tracing.start(
            screenshots=True,
            snapshots=True,
            sources=True
        )

        page = context.new_page()
        yield page

        context.tracing.stop(path=trace_path)

        context.clear_cookies()
        context.close()
        browser.close()


# -------- Screenshot if test fails --------

@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    report = outcome.get_result()

    if report.when == "call" and report.failed:
        page = item.funcargs.get("page", None)

        if page:
            os.makedirs("screenshots", exist_ok=True)
            screenshot_path = f"screenshots/{item.name}.png"
            page.screenshot(path=screenshot_path)
            print(f"\n[SCREENSHOT] Saved to: {screenshot_path}")