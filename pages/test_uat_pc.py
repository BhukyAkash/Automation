from excel_utils import get_vehicle_data
from datetime import datetime

from pages.conftest import page


def test_tipuat_motor(page):

    page.goto("https://ath-uat.tuneinsurance.com/realms/tune/protocol/openid-connect/auth?response_type=code&client_id=1003&state=VEJYMU9YQ3pVaGZGemotRTNLMGN4OHhFaXc3ZmQ1cldaRXRFMG4wbDJBT0Rr&redirect_uri=https%3A%2F%2Fagent-uat.tuneinsurance.com%2F%23%2Fhome&scope=openid%20profile&code_challenge=TSCey8KaEFyGzZ5lgGfWXplgcJ1ivvARav8R4bnYPfM&code_challenge_method=S256&nonce=VEJYMU9YQ3pVaGZGemotRTNLMGN4OHhFaXc3ZmQ1cldaRXRFMG4wbDJBT0Rr")
    
    page.get_by_role("textbox", name="Username or email").click()
    page.get_by_role("textbox", name="Username or email").fill("playwright.test@serole.com")
    page.get_by_role("textbox", name="Password").click()
    page.get_by_role("textbox", name="Password").fill("Serole@123")
    page.get_by_role("button", name="Login").click()

    page.pause()

    # =========== NAVIGATION ===========

    page.get_by_text("request_quote QMS Quotation").click()
    page.get_by_role("button", name="New Quote").click()
    page.get_by_role("heading", name="Motor").click()
    page.get_by_role("button", name="Next").click()

    page.get_by_role("textbox").click()


    # ========= FIRST SCREEN ===========
    
    # ---- VEHICLE REG ----
    vehicle_data = get_vehicle_data()
    page.get_by_role("textbox").first.fill(vehicle_data["vehicle_reg_no"])

    #---- Place of Use ----
    page.locator(".mat-select-placeholder").click()
    page.get_by_role("option", name="Johor").click()

    #---- Vehicle Search ----
    page.get_by_role("button", name="search Vehicle Search").click()

    #---- VEHICLE DETAILS SAVE ----
    page.get_by_role("button", name="Save Vehicle Info").click()


    # ===========SECOND SCREEN ==========

    #---- COVERAGE DATE -----
        # today date
    today = datetime.today()

        # Angular Material aria-label format
    aria_date = today.strftime("%B %d, %Y").replace(" 0", " ")

        # Open calendar
    page.locator("mat-form-field") \
        .filter(has_text="Inception Date * event") \
        .get_by_label("Open calendar") \
        .click()

        # Select today
    page.get_by_role("gridcell", name=aria_date).click()


    #---- VEHICLE SUM INSURED ----
    page.locator("dx-input-currency").filter(has_text="* Vehicle Sum Insured *").locator("#sumInsured").click()
    page.locator("dx-input-currency").filter(has_text="* Vehicle Sum Insured *").locator("#sumInsured").fill("5000")

    #---- MYKAD ID ----
    page.locator("mat-form-field").filter(has_text="ID # * help").locator("#id").fill(vehicle_data["mykad"])

    #----NAME OF THE PH ----
    page.locator("mat-form-field").filter(has_text="Name as per ID *").locator("#legalName").fill("PC")
    page.get_by_role("button", name="search Validate Owner as per").click()

    #---- SAVE & NEXT BUTTON -----
    page.get_by_role("button", name="Save & Next").click()



    # ========== THIRD SCREEN === COVER DETAILS ==========

    page.locator(".mat-select-placeholder").first.click()
    page.get_by_role("option", name="Less than 2 years").click()

    page.get_by_role("button", name="Yes").click()
    
    page.locator(".mat-select-placeholder").first.click()
    page.get_by_role("option", name="Public Road").click()

    page.locator(".mat-select-placeholder").first.click()
    page.get_by_role("option", name="No Alarm(WITHOUT MECHANICAL").click()

    page.locator(".mat-select-placeholder").click()
    page.get_by_role("option", name="Driver’s Side Airbags (1)").click()


    page.locator("#dx-checkbox-4 > .mat-checkbox-layout > .mat-checkbox-inner-container").click()
    page.locator("#dx-checkbox-5 > .mat-checkbox-layout > .mat-checkbox-inner-container").click()

    page.locator("#isUploadLater-desktop > .mat-checkbox-layout > .mat-checkbox-inner-container").click()
    page.locator("dx-evidence-upload").get_by_role("textbox").click()
    page.locator("dx-evidence-upload").get_by_role("textbox").fill("Will Upload later")


    # Locate the element that contains the quote reference
    quote_text = page.locator("text=Quote Reference #").locator("xpath=following-sibling::*").inner_text()
    quote_number = quote_text.strip()
    print("Captured Quote Number:", quote_number)

    page.get_by_role("button", name="Submit for TPM Staff Approval").click()

    page.wait_for_timeout(17000)


    
            # ===== INCOGNITO SESSION (Branch Manager) =====
    browser = page.context.browser
    manager_context = browser.new_context()
    manager_page = manager_context.new_page()

    manager_page.goto(f"https://tune.sit.indigit.io/#/qms/quote/motor/reg/cover-details?edit=true&quoteNr={quote_number}")
    

    manager_page.get_by_role("textbox", name="Username or email").fill("chinyap.oh@tuneprotect.com")
    manager_page.get_by_role("textbox", name="Password").fill("Serole@123")
    manager_page.get_by_role("button", name="Login").click()

    manager_page.wait_for_timeout(10000)
    
    #-----Approving the quote--
    manager_page.get_by_role("button", name="Accept & Process").click()

    manager_page.close()


            # ====== BACK TO ORIGINAL SESSION (TPM AGENT) =====
    page.reload()
    page.wait_for_load_state("networkidle")

    #---------- POLICY ISSUANCE ----------
    page.get_by_role("button", name="Issue Policy").click()

    page.reload()

    #----Printing the policy number---
    policy_number = page.get_by_text("Policy #:").locator("xpath=following-sibling::*").inner_text()
    print("Policy Number:", policy_number)


    page.pause()
