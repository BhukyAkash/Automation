import os
from openpyxl import Workbook, load_workbook
from excel_utils import get_vehicle_data
from datetime import datetime
from base_login import login, navigation, pc_moto
from pages.test_mail import send_email


def test_pc_motor(page):

    try:
        login(page)
        navigation(page)
        pc_moto(page)

        # ========= FIRST SCREEN ===========
        
        # ---- VEHICLE REG ----
        vehicle_data = get_vehicle_data("PC")
        page.get_by_role("textbox").first.fill(vehicle_data["vehicle_reg_no"])

        #---- Place of Use ----
        page.locator(".mat-select-placeholder").click()
        page.get_by_role("option", name="Johor").click()

        #---- Vehicle Search ----
        page.get_by_role("button", name="search Vehicle Search").click()

        #---- VEHICLE DETAILS SAVE ----
        page.get_by_role("button", name="Save Vehicle Info").click()


        # ========== SECOND SCREEN ==========

        #---- COVERAGE TYPE ----
        page.locator("#mat-select-value-9").click()
        page.get_by_role("option", name="TP, Fire & Theft").click()


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

        # ---- NCD value ----
        page.wait_for_timeout(7000)
        ncd_value = page.locator("#currentNCD input.mat-input-element").input_value()
        print("NCD Value:", ncd_value)

        #---- SAVE & NEXT BUTTON -----
        page.get_by_role("button", name="Save & Next").click()


        # ========== THIRD SCREEN === COVER DETAILS ==========

        # ---- DRIVER EXPERIENCE ----
        page.locator(".mat-select-placeholder").first.click()
        page.get_by_role("option", name="Less than 2 years").click()

        # ---- CHECK IF YES BUTTON EXISTS AND IS ENABLED ----
        yes_button = page.get_by_role("button", name="Yes").first

        if yes_button.is_visible():
                yes_button.click()
                page.wait_for_timeout(1000)

        # ---- CHECK IF ADDRESS ALREADY EXISTS ----
        add_button = page.locator("button[name='Add'], button:has-text('Add')").first
        if add_button.is_visible():
            add_button.click()
            page.wait_for_timeout(1000)

        # ---- STATE ---- (runs for both cases)
        page.locator(".mat-select-placeholder").first.click()
        page.get_by_role("option", name="Johor").click()
        page.wait_for_timeout(5000)

        # ---- PINCODE ----
        page.locator(".mat-select-placeholder").first.click()
        page.get_by_role("option", name="81100").click()
        page.wait_for_timeout(2000)

        # ---- STREET ADDRESS ----
        page.get_by_role("combobox", name="Address Line").click()
        page.get_by_role("option", name="Taman Desa Harmoni", exact=True).click()
        page.wait_for_timeout(2000)

        # ---- SAVE BUTTON (if address is added) ----
        address_save = page.locator("button#save")
        if address_save.is_visible():
            address_save.click()
            page.locator("//label[@for='3']//div[@class='box-card justify-content-between']").wait_for(state="visible")
            page.locator("//label[@for='3']//div[@class='box-card justify-content-between']").click()

        
        # ---- Garage Types ----
        page.locator(".mat-select-placeholder").first.click()
        page.get_by_role("option", name="Public Road").click()
        page.locator(".mat-select-placeholder").first.click()
        page.get_by_role("option", name="No Alarm(WITHOUT MECHANICAL").click()
        page.locator(".mat-select-placeholder").click()
        page.get_by_role("option", name="Driver’s Side Airbags (1)").click()

        # ---- DECLARATION STATEMENTS ----
        page.get_by_text("We respect your privacy and").click()
        page.get_by_text("I hereby confirm that I have").click()

        # ---- Uploading the document later option ----
        page.locator("#isUploadLater-desktop > .mat-checkbox-layout > .mat-checkbox-inner-container").click()
        page.locator("dx-evidence-upload").get_by_role("textbox").click()
        page.locator("dx-evidence-upload").get_by_role("textbox").fill("Will Upload later")


        # Locate the element that contains the quote reference
        quote_text = page.locator("text=Quote Reference #").locator("xpath=following-sibling::*").inner_text()
        quote_number = quote_text.strip()
        print("Quote Number:", quote_number)


        page.get_by_role("button", name="Submit for TPM Staff Approval").click()

        page.wait_for_timeout(17000)

        
                # ===== INCOGNITO SESSION (Branch Manager) =====
        browser = page.context.browser
        manager_context = browser.new_context()
        manager_page = manager_context.new_page()

        manager_page.goto(f"https://agent-uat.tuneinsurance.com/#/qms/quote/motor/reg/cover-details?edit=true&quoteNr={quote_number}")
        

        manager_page.get_by_role("textbox", name="Username or email").fill("rahul@serole.com")
        manager_page.get_by_role("textbox", name="Password").fill("Serole@321")
        manager_page.get_by_role("button", name="Login").click()

        manager_page.wait_for_timeout(30000)
        
        #-----Approving the quote--
        manager_page.get_by_role("button", name="Accept & Process").click()

        manager_page.close()


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



    finally:
        page.get_by_text("playwright", exact=True).click()
        page.get_by_text("Sign Out", exact=True).click()
        page.wait_for_timeout(15000)


