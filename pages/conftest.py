import pytest
from playwright.sync_api import sync_playwright
import os


@pytest.fixture(scope="function")
def page(request):
    # Base traces directory
    os.makedirs("traces", exist_ok=True)

    # 🔹 Get test file name (without .py)
    test_file = os.path.splitext(os.path.basename(request.node.fspath))[0]

    # 🔹 Trace path per test file
    trace_path = os.path.abspath(f"traces/{test_file}.zip")

    print(f"\n[TRACE] Saving trace to: {trace_path}")

    with sync_playwright() as playwright:
        browser = playwright.firefox.launch(headless=False)
        context = browser.new_context()

        # ---------- START TRACE ----------
        context.tracing.start(
            screenshots=True,
            snapshots=True,
            sources=True
        )

        page = context.new_page()
        yield page

        # ---------- STOP TRACE (overwrite per file) ----------
        context.tracing.stop(path=trace_path)

        context.clear_cookies()   # 👈 forces logout
        context.close()
        browser.close()
        