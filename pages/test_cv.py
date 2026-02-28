from conftest import page
from excel_utils import get_vehicle_data
from datetime import datetime

from base_login import cv_moto, login, navigation, cv_moto


def test_tipuat_motor(page):

    login(page)
    navigation(page)
    cv_moto(page)

    # ========= FIRST SCREEN ===========
    
    # ---- VEHICLE REG ----
    vehicle_data = get_vehicle_data()
    page.get_by_role("textbox").first.fill(vehicle_data["vehicle_reg_no"])

    #---- Place of Use ----
    page.locator(".mat-select-placeholder").click()
    page.get_by_role("option", name="Johor").click()

    #---- Vehicle Search ----
    page.get_by_role("button", name="search Vehicle Search").click()

    page.locator(".mat-select-placeholder").first.click()
    page.get_by_role("option", name="Commercial Vehicle").click()

    page.locator(".mat-select-placeholder").first.click()
    page.get_by_role("option", name="C permit").click()

    page.locator("mat-form-field").filter(has_text="Engine # *").locator("#engineNo").fill("63547")
    #page.locator("mat-form-field").filter(has_text="Engine # *").locator("#engineNo").fill("63547")

    page.locator("mat-form-field").filter(has_text="Chassis # *").locator("#chassisNo").fill("34576657")
    #page.locator("mat-form-field").filter(has_text="Chassis # *").locator("#chassisNo").fill("34576657")

    page.locator("mat-form-field", has_text="Make").click()
    page.get_by_role("option", name="VOLVO").click()
    
    page.locator(".mat-select-placeholder.mat-select-min-line.ng-tns-c176-72").click()
    page.get_by_role("option", name="F16").click()

    page.locator(".mat-select-placeholder.mat-select-min-line.ng-tns-c176-74").click()
    page.get_by_role("option", name="2016").click()

    page.locator(".mat-select-placeholder.mat-select-min-line.ng-tns-c176-76").click()
    page.get_by_role("option", name="NA").click()


    page.locator("mat-form-field").filter(has_text="Seating Capacity *").locator("#seatCapacity").fill("5")
    #page.locator("mat-form-field").filter(has_text="Seating Capacity *").locator("#seatCapacity").fill("5")

    page.locator("mat-form-field").filter(has_text="Carrying Capacity *").locator("#carryingCapacity").fill("11")
    #page.locator("mat-form-field").filter(has_text="Carrying Capacity *").locator("#carryingCapacity").fill("11")


    page.locator(".mat-select-placeholder.mat-select-min-line.ng-tns-c176-84").click()
    page.get_by_role("option", name="Tonnes").click()

    page.locator(".mat-select-placeholder.mat-select-min-line.ng-tns-c176-86").click()
    page.get_by_role("option", name="Beverages Bottles").click()

    page.get_by_role("button", name="Save Vehicle Info").click()

    page.locator("#mat-select-value-31").click()
    page.get_by_role("option", name="Comprehensive").click()


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


    page.get_by_role("region", name="Coverage").locator("input[type=\"text\"]").click()
    page.get_by_role("region", name="Coverage").locator("input[type=\"text\"]").fill("45000")

    '''page.locator("dx-input").filter(has_text="* Business Registration # *").locator("#id").click()
    page.locator("dx-input").filter(has_text="* Business Registration # *").locator("#id").fill("54375347")'''

    page.locator("mat-form-field").filter(has_text="Business Registration # *").locator("#id").fill(vehicle_data["mykad"])

    page.locator("dx-input").filter(has_text="* Name as per ID / Legal Name").locator("#legalName").click()
    page.locator("dx-input").filter(has_text="* Name as per ID / Legal Name").locator("#legalName").fill("CV C")
    
    page.get_by_role("button", name="search Validate Owner as per").click()

    page.get_by_role("button", name="Save & Next").click()


    yes_btn = page.get_by_role("button", name="Yes")
    state_dd = page.locator(".mat-select-placeholder").first

    page.wait_for_timeout(1000)

    '''page.locator(".mat-select-placeholder").first.click()
    page.get_by_role("option", name="Kelantan").click()

    page.locator(".mat-select-placeholder").click()
    page.get_by_role("option", name="15500").click()

    page.get_by_role("combobox", name="Address Line").click()
    page.get_by_role("option", name="Dymm Sultan Kelantan").click()'''

    page.locator("#dx-checkbox-3 > .mat-checkbox-layout > .mat-checkbox-inner-container").click()
    page.locator("#dx-checkbox-4 > .mat-checkbox-layout > .mat-checkbox-inner-container").click()

    # ---- Locate the element that contains the quote reference ----
    quote_text = page.locator("text=Quote Reference #").locator("xpath=following-sibling::*").inner_text()
    quote_number = quote_text.strip()
    print("Quote Number:", quote_number)

    page.get_by_role("button", name="Submit for TPM Staff Approval").click()

    page.wait_for_timeout(17000)

    
            # ===== INCOGNITO SESSION (Branch Manager) =====
    browser = page.context.browser
    manager_context = browser.new_context()
    manager_page = manager_context.new_page()

    page.goto(f"https://agent-uat.tuneinsurance.com/#/qms/quote/motor/rcv/cover-details?edit=true&quoteNr={quote_number}")

    manager_page.get_by_role("textbox", name="Username or email").fill("rahul@serole.com")
    manager_page.get_by_role("textbox", name="Password").fill("Serole@321")
    manager_page.get_by_role("button", name="Login").click()

    manager_page.wait_for_timeout(30000)
    
    #-----Approving the quote--
    manager_page.get_by_role("button", name="Accept & Process").click()

    manager_page.close()

'''
            # ====== BACK TO ORIGINAL SESSION (TPM AGENT) =====
    page.wait_for_timeout(10000)
    page.reload()
    page.wait_for_load_state("networkidle")

    #---------- POLICY ISSUANCE ----------
    page.get_by_role("button", name="Issue Policy").click()

    page.wait_for_timeout(30000)

    page.reload()

    page.wait_for_timeout(7000)

    #----Printing the policy number---
    policy_locator = page.locator("text=Policy #:")
    policy_text = policy_locator.text_content()
    policy_number = policy_text.replace("Policy #:", "").strip()

    print("Policy Number:", policy_number)

'''