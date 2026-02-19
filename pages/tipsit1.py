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


    page.locator("#dx-checkbox-3 > .mat-checkbox-layout > .mat-checkbox-inner-container").click()
    page.locator("#dx-checkbox-4 > .mat-checkbox-layout > .mat-checkbox-inner-container").click()
    
    page.locator("#isUploadLater-desktop > .mat-checkbox-layout > .mat-checkbox-inner-container").click()
    page.locator("dx-evidence-upload").get_by_role("textbox").click()
    page.locator("dx-evidence-upload").get_by_role("textbox").fill("Will Upload later")


    # Locate the element that contains the quote reference
    quote_text = page.locator("text=Quote Reference #").locator("xpath=following-sibling::*").inner_text()

    # Extract only the number
    quote_number = quote_text.strip()

    print("Captured Quote Number:", quote_number)

    page.get_by_role("button", name="Submit for TPM Staff Approval").click()

    page.wait_for_timeout(10000)
    
            # ===== INCOGNITO SESSION (Branch Manager) =====
    manager_context = browser.new_context()
    manager_page = manager_context.new_page()

    manager_page.goto(f"https://tune.sit.indigit.io/#/qms/quote/motor/reg/cover-details?edit=true&quoteNr={quote_number}")
    

    manager_page.get_by_role("textbox", name="Username or email").fill("sbuhead@gmail.com")
    manager_page.get_by_role("textbox", name="Password").fill("Tune@112")
    manager_page.get_by_role("button", name="Login").click()

    manager_page.wait_for_timeout(10000)
    manager_page.pause()


    #page.get_by_role("button", name="Proceed to Policy Issuance").click()
    #page.get_by_role("button", name="Issue Policy").click()

with sync_playwright() as playwright:
    run(playwright)
