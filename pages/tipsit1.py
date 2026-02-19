import re
from playwright.sync_api import sync_playwright


def run(playwright):
    browser = playwright.firefox.launch(headless=False, slow_mo=1000)
    context = browser.new_context()
    page = context.new_page()

    page.goto("https://auth.sit.indigit.io/realms/Tune/protocol/openid-connect/auth?response_type=code&client_id=1003&state=Mk5yZjlVVkVTeDB0dnlOQWdhY1ZydHNLYXlGcy0uRlZMUjFzMWRQRXpkRFBt&redirect_uri=https%3A%2F%2Ftune.sit.indigit.io%2F%23%2Fhome&scope=openid%20profile&code_challenge=Fl3fwnRezgUIllwG2OcjrNcZ_jjADgxBsA70tIfwRhk&code_challenge_method=S256&nonce=Mk5yZjlVVkVTeDB0dnlOQWdhY1ZydHNLYXlGcy0uRlZMUjFzMWRQRXpkRFBt")

    page.get_by_role("textbox", name="Username or email").fill("keerthi.SIT@gmail.com")
    page.get_by_role("textbox", name="Password").fill("Serole@456")
    page.get_by_role("button", name="Login").click()

    page.get_by_text("request_quote QMS Quotation").click()
    page.get_by_role("button", name="New Quote").click()

    page.get_by_role("heading", name="Motor").click()
    page.get_by_role("button", name="Next").click()


    page.get_by_role("textbox").fill("WER3384") #NDR4735
    
    page.locator(".mat-select-placeholder").click()
    page.get_by_role("option", name="Kedah").click()
    page.get_by_role("button", name="search Vehicle Search").click()

    #page.wait_for_timeout(5000)

    page.get_by_role("button", name="Save Vehicle Info").click()

    page.locator("mat-form-field").filter(has_text="Inception Date * event").get_by_label("Open calendar").click()
    page.get_by_role("button", name="February 20,").click()

    #page.wait_for_timeout(5000)
    page.locator("dx-input-currency").filter(has_text="* Vehicle Sum Insured *").locator("#sumInsured").click()
    page.locator("dx-input-currency").filter(has_text="* Vehicle Sum Insured *").locator("#sumInsured").fill("5000")

    page.locator("mat-form-field").filter(has_text="ID # * help").locator("#id").click()
    page.locator("mat-form-field").filter(has_text="ID # * help").locator("#id").fill("831211-11-5543") #750501-01-7031

    #--------NAME OF THE PH ---------
    page.locator("mat-form-field").filter(has_text="Name as per ID *").locator("#legalName").fill("PC")
    page.get_by_role("button", name="search Validate Owner as per").click()


    page.get_by_role("button", name="Save & Next").click()

    #page.wait_for_timeout(5000)

    page.locator(".mat-select-placeholder").first.click()
    page.get_by_role("option", name="Less than 2 years").click()

    page.get_by_role("button", name="Yes").click()
    
    page.locator(".mat-select-placeholder").first.click()
    page.get_by_role("option", name="Public Road").click()

    page.locator(".mat-select-placeholder").first.click()
    page.get_by_role("option", name="No Alarm(WITHOUT MECHANICAL").click()

    page.locator(".mat-select-placeholder").click()
    page.get_by_role("option", name="Driver’s Side Airbags (1)").click()

    page.pause()

    page.locator("#dx-checkbox-4 > .mat-checkbox-layout > .mat-checkbox-inner-container").click()
    page.locator("#dx-checkbox-5 > .mat-checkbox-layout > .mat-checkbox-inner-container").click()


    page.get_by_text("Submit for TPM Staff Approval", exact=True).click()

        # After Submit for TPM
    quote_no = page.locator("#quoteNumber").inner_text().strip()
    print("Quote Number:", quote_no)


    
    
            # ===== INCOGNITO SESSION (Branch Manager) =====
    manager_context = browser.new_context()
    manager_page = manager_context.new_page()

    manager_page.goto("https://tune.sit.indigit.io/#/qms/quote/motor/reg/cover-details?edit=true&quoteNr={quote_no}")

    manager_page.get_by_role("textbox", name="Username or email").fill("chinyap.oh@tuneprotect.com")
    manager_page.get_by_role("textbox", name="Password").fill("Serole@123")
    manager_page.get_by_role("button", name="Login").click()

    manager_context.close()
    


    #page.get_by_role("button", name="Proceed to Policy Issuance").click()
    #page.get_by_role("button", name="Issue Policy").click()

with sync_playwright() as playwright:
    run(playwright)
