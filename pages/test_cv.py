from openpyxl import Workbook, load_workbook
from excel_utils import get_vehicle_data
from datetime import datetime
from base_login import login, navigation, cv_moto


def test_cv_motor(page):

    try:
        login(page)
        navigation(page)
        cv_moto(page)

        # ========= FIRST SCREEN ===========

        vehicle_data = get_vehicle_data("CV")
        page.get_by_role("textbox").first.fill(vehicle_data["vehicle_reg_no"])

        page.locator(".mat-select-placeholder").click()
        page.get_by_role("option", name="Johor").click()

        page.get_by_role("button", name="search Vehicle Search").click()

        page.locator(".mat-select-placeholder").first.click()
        page.get_by_role("option", name="Commercial Vehicle").click()

        page.locator(".mat-select-placeholder").first.click()
        page.get_by_role("option", name="C permit").click()

        page.locator("mat-form-field").filter(has_text="Engine # *").locator("#engineNo").fill("63547")
        page.locator("mat-form-field").filter(has_text="Chassis # *").locator("#chassisNo").fill("34576657")

        page.locator("mat-form-field", has_text="Make").click()
        page.get_by_role("option", name="VOLVO").click()

        page.locator("mat-form-field", has_text="Model").click()
        page.get_by_role("option", name="F16").click()

        page.locator(".mat-select-placeholder.mat-select-min-line.ng-tns-c176-74").click()
        page.get_by_role("option", name="2016").click()

        page.locator(".mat-select-placeholder.mat-select-min-line.ng-tns-c176-76").click()
        page.get_by_role("option", name="NA").click()

        page.locator("mat-form-field").filter(has_text="Seating Capacity *").locator("#seatCapacity").fill("5")
        page.locator("mat-form-field").filter(has_text="Carrying Capacity *").locator("#carryingCapacity").fill("11")

        page.locator(".mat-select-placeholder.mat-select-min-line.ng-tns-c176-84").click()
        page.get_by_role("option", name="Tonnes").click()

        page.locator(".mat-select-placeholder.mat-select-min-line.ng-tns-c176-86").click()
        page.get_by_role("option", name="Beverages Bottles").click()

        page.get_by_role("button", name="Save Vehicle Info").click()


        # ========== SECOND SCREEN ==========

        page.locator("#mat-select-value-31").click()
        page.get_by_role("option", name="Comprehensive").click()

        today = datetime.today()
        aria_date = today.strftime("%B %d, %Y").replace(" 0", " ")

        page.locator("mat-form-field") \
            .filter(has_text="Inception Date * event") \
            .get_by_label("Open calendar") \
            .click()

        page.get_by_role("gridcell", name=aria_date).click()

        page.get_by_role("region", name="Coverage").locator("input[type=\"text\"]").click()
        page.get_by_role("region", name="Coverage").locator("input[type=\"text\"]").fill("45000")

        page.locator("mat-form-field").filter(has_text="Business Registration # *").locator("#id").fill(vehicle_data["mykad"])

        page.locator("dx-input").filter(has_text="* Name as per ID / Legal Name").locator("#legalName").fill("CV C Permit")

        page.get_by_role("button", name="search Validate Owner as per").click()

        page.get_by_role("button", name="Save & Next").click()
        

        # ========== THIRD SCREEN ==========

        page.get_by_role("button", name="Yes").click()

        page.wait_for_timeout(1000)

        page.locator("#dx-checkbox-3 > .mat-checkbox-layout > .mat-checkbox-inner-container").click()
        page.locator("#dx-checkbox-4 > .mat-checkbox-layout > .mat-checkbox-inner-container").click()

        # ---- Get Quote Number ----
        quote_text = page.locator("text=Quote Reference #").locator("xpath=following-sibling::*").inner_text()
        quote_number = quote_text.strip()
        print("Quote Number:", quote_number)

        #--------- SUBMIT FOR APPROVAL ---------
        page.get_by_role("button", name="Submit for TPM Staff Approval").click()
        page.wait_for_timeout(17000)

        # ===== INCOGNITO SESSION (Branch Manager) =====

        browser = page.context.browser
        manager_context = browser.new_context()
        manager_page = manager_context.new_page()

        manager_page.goto(f"https://agent-uat.tuneinsurance.com/#/qms/quote/motor/rcv/cover-details?edit=true&quoteNr={quote_number}")
        manager_page.get_by_role("textbox", name="Username or email").fill("rahul@serole.com")
        manager_page.get_by_role("textbox", name="Password").fill("Serole@321")
        manager_page.get_by_role("button", name="Login").click()

        manager_page.wait_for_timeout(20000)
        manager_page.reload()

        # --------- APPROVE THE QUOTE ---------
        manager_page.get_by_role("button", name="Accept & Process").click()
        manager_page.close()

        # ===== BACK TO ORIGINAL SESSION =====

        page.wait_for_timeout(10000)
        page.reload()
        page.wait_for_load_state("networkidle")

        #---------- POLICY ISSUANCE ----------
        page.get_by_role("button", name="Issue Policy").click()

        page.wait_for_timeout(30000)

        page.reload()

        page.wait_for_timeout(20000)

        
        #----Printing the policy number---
        policy_locator = page.locator("text=Policy #:")
        policy_locator.wait_for()
        policy_text = policy_locator.text_content()
        policy_number = policy_text.replace("Policy #:", "").strip()
        print("Policy Number:", policy_number)


        # ---------- SAVE TO EXCEL ----------

        import os
        file_path = "UATStability.xlsx"

        if os.path.exists(file_path):
            wb = load_workbook(file_path)
        else:
            wb = Workbook()

        ws = wb.active

        # CV values
        ws["F4"] = quote_number
        ws["G4"] = policy_number

        wb.save(file_path)

    finally:
        page.get_by_text("playwright", exact=True).click()
        page.get_by_text("Sign Out", exact=True).click()
        page.wait_for_timeout(15000)