from get_policy import get_policy_number
from datetime import date
from base_login import login, endo_navigation
import pytest


def test_pa_endo(page, request):
    try:
        # ---- Get Product From CLI ----
        product = request.config.getoption("--product")

        # ---- Get Policy Number ----
        policy_number, motor_type, policy_date = get_policy_number(product)

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

        # ---- Select Policy ----
        page.locator(".d-flex.align-items-center.ms-3 > div > .d-flex.align-items-center.justify-content-between").click()
        page.get_by_role("button", name="Next", exact=True).click()
        print("Endorsement first screen")
        page.get_by_text("Confirm this is the policy to").click()

    finally:
        try:
            page.bring_to_front()
            page.get_by_text("playwright", exact=True).click(timeout=5000)
            page.get_by_text("Sign Out", exact=True).click()
            page.wait_for_timeout(15000)
        except Exception:
            pass