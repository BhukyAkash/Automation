from get_policy import get_policy_number
from datetime import date
from base_login import login, endo_navigation
import pytest


def endorsement(page, request):
    # ---- Get Product From CLI ----
    product = request.config.getoption("--product")

    # ---- Get Policy Number ----
    policy_number, motor_type, policy_date = get_policy_number(product)

    print("====================== Endorsement Starts ==================")

    if policy_number is None:
        print(f"No {product.upper()} policy found for today ({date.today()}). Skipping endorsement.")
        pytest.skip(f"No {product.upper()} policy found for today. Skipping endorsement.")

    print(f"Product: {product.upper()} - {motor_type} | Policy Number: {policy_number} | Date: {policy_date}")

    # ---- Login ----
    login(page)
    endo_navigation(page, product)

    # ---- Search Policy ----
    page.locator("mat-form-field").filter(has_text="Policy #").locator("input").fill(policy_number)
    page.get_by_role("button", name="search Search Policy").click()

    # --- Verify Policy Duration ---
    page.wait_for_timeout(3000)
    duration = page.locator("div:has-text('Period of Insurance:') + div span.status-text").first.inner_text()
    print("Duration:", duration)

    # ---- Select Policy ----
    page.locator(".d-flex.align-items-center.ms-3 > div > .d-flex.align-items-center.justify-content-between").click()
    page.get_by_role("button", name="Next", exact=True).click()
    page.get_by_text("Confirm this is the policy to").click()