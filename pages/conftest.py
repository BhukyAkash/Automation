import pytest
from playwright.sync_api import sync_playwright
import os


@pytest.fixture(scope="function")
def page(request):
    os.makedirs("traces", exist_ok=True)

    # 🔥 trace file (will be overwritten every run)
    trace_path = os.path.abspath("traces/latest_trace.zip")

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

        # ---------- STOP TRACE (OVERWRITE) ----------
        context.tracing.stop(path=trace_path)

        context.close()
        browser.close()

