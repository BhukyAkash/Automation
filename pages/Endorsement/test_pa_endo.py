from urllib3 import request
from base_login import login, endo_navigation

def test_pa_endo(page, request):
    try:
        product = request.config.getoption("--product")
        login(page)
        endo_navigation(page, product)

        # ---- Search Policy ----
        page.locator("mat-form-field").filter(has_text="Policy #").click()
        page.locator("mat-form-field").filter(has_text="Policy #").locator("input").fill("00000402000069675")
        page.get_by_role("button", name="search Search Policy").click()

        # ---- Select Policy ----
        page.locator(".d-flex.align-items-center.ms-3 > div > .d-flex.align-items-center.justify-content-between").click()
        page.get_by_role("button", name="Next", exact=True).click()

        print("Endorsement first screen")
        page.get_by_text("Confirm this is the policy to").click()



    finally:
        page.bring_to_front()
        page.get_by_text("playwright", exact=True).click()
        page.get_by_text("Sign Out", exact=True).click()
        page.wait_for_timeout(15000)