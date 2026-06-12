from base_login import incep_date, issue_policy, login, navigation, cv_moto, manager_approval
from excel_utils import get_vehicle_data
from extension import cv_extension
from popup_utils import ask_popup

def test_cv_motor(page):

    try:
        print("====================== Issuance of CV policy ==================")
        page.wait_for_load_state()
        login(page)
        navigation(page)
        cv_moto(page)

        # ========= FIRST SCREEN ===========

        vehicle_data = get_vehicle_data("CV")
        page.get_by_role("textbox").first.fill(vehicle_data["vehicle_reg_no"])
        print("Registration Number:", vehicle_data["vehicle_reg_no"])

        page.locator(".mat-select-placeholder").click()
        page.get_by_role("option", name="Johor").click()

        page.get_by_role("button", name="search Vehicle Search").click()

        page.locator(".mat-select-placeholder").first.click()
        page.get_by_role("option", name="Commercial Vehicle").click()

        # ---- VEHICLE USE ----
        page.locator(".mat-select-placeholder").first.click()
        page.get_by_role("option", name="C permit").click()

        page.locator("mat-form-field").filter(has_text="Engine # *").locator("#engineNo").fill("63547")
        page.locator("mat-form-field").filter(has_text="Chassis # *").locator("#chassisNo").fill("34576657")

        # ---- MAKE & MODEL ----
        page.locator("mat-form-field", has_text="Make").click()
        page.get_by_role("option", name="VOLVO").click()

        page.locator("mat-form-field", has_text="Model").click()
        page.get_by_role("option", name="F16").click()

        # ---- Year of Manufacture ----
        page.locator("mat-form-field", has_text="Year of Manufacture").click()
        page.get_by_role("option", name="2015").click()
        page.wait_for_timeout(2000)

        # ---- Vehicle Age (to determine coverage type) ---- 
        vehicle_age_locator = page.locator("mat-form-field").filter(has_text="Vehicle Age").locator("#vehicleAge")
        vehicle_age_text = vehicle_age_locator.input_value().strip()

        vehicle_age = int(vehicle_age_text)
        print(f"Vehicle Age: {vehicle_age} years")

        # ---- VARIANT ----
        page.locator("mat-form-field").filter(has_text="Variant").locator("mat-select").click()
        page.get_by_role("option", name="NA").click()

        # ---- Seating Capacity ----
        page.locator("mat-form-field").filter(has_text="Seating Capacity *").locator("#seatCapacity").fill("5")
        # ---- Carrying Capacity ----
        page.locator("mat-form-field").filter(has_text="Carrying Capacity *").locator("#carryingCapacity").fill("20")

        page.locator("mat-form-field").filter(has_text="Tonnes / Kilogram").locator("mat-select").click()
        page.get_by_role("option", name="Tonnes").click()

        page.locator("mat-form-field").filter(has_text="Carriage Goods").click()
        page.get_by_role("option", name="Beverages Bottles").click()

        # ---- Save Vehicle Info Button ----
        page.get_by_role("button", name="Save Vehicle Info").click()


        # ========== SECOND SCREEN ==========

        # ---- Coverage Type ----
        page.locator("#mat-select-value-31").click()
        if vehicle_age >= 20:
            page.get_by_role("option", name="TP, Fire & Theft").click()
        else:
            page.get_by_role("option", name="Comprehensive").click()

        selected_coverage = page.locator("#mat-select-value-31").inner_text().strip()
        print("Selected Coverage type: ", selected_coverage)

        # ---- COVERAGE DATE -----
        incep_date(page)

        # ----- SUM INSURED ----
        page.get_by_role("region", name="Coverage").locator("input[type=\"text\"]").click()
        page.get_by_role("region", name="Coverage").locator("input[type=\"text\"]").fill("20000")

        # ---- BUSINESS REGISTRATION NUMBER ----
        page.locator("mat-form-field").filter(has_text="Business Registration # *").locator("#id").fill(vehicle_data["mykad"])
        print("MyKad Number:", vehicle_data["mykad"])

        # ---- NAME AS PER ID / LEGAL NAME ----
        page.locator("dx-input").filter(has_text="* Name as per ID / Legal Name").locator("#legalName").fill("CV C Permit")
        page.get_by_role("button", name="search Validate Owner as per").click()

        # ==== Multi Contract / Extensions ====
        print("======== Extension Coverage Selection ========")

        answer = ask_popup(
            question="Do you want to explore Extensions screen?",
            title="Extension Coverage Selection",
        )

        if answer == "yes":
            cv_extension(page, selected_coverage)
            print("Extensions added successfully")
        else:
            print("No Extensions Selected")

        page.pause()

        # ---- NCD value ----
        page.wait_for_timeout(7000)
        ncd_value = page.locator("#currentNCD input.mat-input-element").input_value()
        print("NCD Value:", ncd_value)
        
        # --- SAVE & NEXT BUTTON ----
        page.get_by_role("button", name="Save & Next").click()
        print("Registration Number is Triggered to ISM")

        page.wait_for_timeout(15000)
        
        # ========== THIRD SCREEN ==== PH Details ======
        
        # ---- CHECK IF YES BUTTON EXISTS AND IS ENABLED ----
        page.wait_for_timeout(10000)
        try:
            yes_button = page.get_by_role("button", name="Yes").first
            yes_button.wait_for(state="visible", timeout=5000)
            yes_button.click()
            page.wait_for_timeout(1000)
            print("Yes button clicked")
        except:
            print("Yes button not visible, skipping")

        # ---- CHECK IF ADDRESS ALREADY EXISTS ----
        try:
            add_button = page.locator("button[name='Add'], button:has-text('Add')").first
            add_button.wait_for(state="visible", timeout=5000)
            add_button.click()
            print("Add button clicked")
            page.wait_for_timeout(2000)
        except:
            print("Add button not visible, skipping")

        # ---- STATE ---- (runs for both cases)
        page.locator(".mat-select-placeholder").first.click()
        page.get_by_role("option", name="Johor").click()
        page.wait_for_timeout(2000)

        # ---- PINCODE ----
        page.locator(".mat-select-placeholder").first.click()
        page.get_by_role("option", name="81100").click()
        page.wait_for_timeout(1000)

        # ---- STREET ADDRESS ----
        page.get_by_role("combobox", name="Address Line").click()
        page.get_by_role("option", name="Taman Desa Harmoni", exact=True).click()
        page.wait_for_timeout(1000)

        # ---- SAVE BUTTON (if address is added) ----
        address_save = page.locator("button#save")
        if address_save.is_visible():
            address_save.click()

        # ---- Declaration Statements ----
        page.get_by_text("We respect your privacy and").click()
        page.get_by_text("I hereby confirm that I have").click()

        # ---- Get Quote Number ----
        quote_text = page.locator("text=Quote Reference #").locator("xpath=following-sibling::*").inner_text()
        quote_number = quote_text.strip()
        print("Quote Number:", quote_number)

        # ====== NSTP FLOW FUNCTION CALL ======
        submit_approval_btn = page.get_by_role("button", name="Submit for TPM Staff Approval")

        if submit_approval_btn.is_visible():
            # ---- Submit for Review Button ----
            submit_approval_btn.click()
            print("Clicked on Submit for TPM Staff Approval button")
            page.wait_for_timeout(17000)

            # ---- Browser launch ---
            browser = page.context.browser
            manager_context = browser.new_context()
            manager_page = manager_context.new_page()

            url_segment = "rcv"
            manager_page.goto(f"https://agent-uat.tuneinsurance.com/#/qms/quote/motor/{url_segment}/cover-details?edit=true&quoteNr={quote_number}")
            manager_approval(manager_page)

        # === PROCEED TO POLICY ISSUANCE ===
        issue_policy(page)

    finally:
        page.bring_to_front()
        page.get_by_text("NMF Smart Resources", exact=True).click()
        page.get_by_text("Sign Out", exact=True).click()
        page.wait_for_timeout(15000)