from base_login import incep_date, login, navigation, pc_moto
from excel_utils import get_vehicle_data
from base_login import manager_approval
from extension import extension

import threading


def test_pc_motor(page):

    try:
        print("\n====================== Issuance of DEV - PC policy ==================")
        login(page)
        navigation(page)
        pc_moto(page)

        # ========= FIRST SCREEN ===========
        
        # ---- VEHICLE REG ----
        vehicle_data = get_vehicle_data("PC")
        page.get_by_role("textbox").first.fill(vehicle_data["vehicle_reg_no"])

        # ---- Place of Use ----
        page.locator(".mat-select-placeholder").click()
        page.get_by_role("option", name="Melaka").click()

        # ---- Vehicle Search ----
        page.get_by_role("button", name="search Vehicle Search").click()
        page.wait_for_timeout(5000)

        # --- Engine Capacity field ----
        cc_input = page.locator('input#cc')
        if cc_input.is_visible():
            current_value = cc_input.input_value().strip()
            if current_value == "" or current_value == "0":
                cc_input.dblclick()
                cc_input.fill("1200")
            else:
                print(f"Engine Capacity: {current_value}")

        # --- Seating Capacity field ----
        seat_input = page.locator('input#seatCapacity')

        if seat_input.is_visible():
            current_value = seat_input.input_value().strip()
            if current_value == "" or current_value == "0":
                seat_input.dblclick()
                seat_input.fill("2")
            else:
                print(f"Seating Capacity: {current_value}")
        
        # ---- Vehicle Age (to determine coverage type) ---- 
        vehicle_age_locator = page.locator("mat-form-field").filter(has_text="Vehicle Age").locator("#vehicleAge")
        vehicle_age_text = vehicle_age_locator.input_value().strip()

        vehicle_age = int(vehicle_age_text)
        print(f"Vehicle Age: {vehicle_age} years")

        # ---- SAVE VEHICLE DETAILS  ----
        search_vehicle = page.get_by_role("button", name="Save Vehicle Info").first
        try:
            search_vehicle.wait_for(state="visible", timeout=5000)
            search_vehicle.click()
            page.wait_for_load_state("networkidle")
        except:
            print("Save Vehicle Info button not available")

        # ========== SECOND SCREEN ==========

        # ---- COVERAGE TYPE (read default) ----
        selected_coverage = page.locator("#mat-select-value-9 span.mat-select-min-line").inner_text().strip()
        print("Default Coverage type: ", selected_coverage)

        # ---- COVERAGE TYPE ----
        page.locator("#mat-select-value-9").click()
        page.get_by_role("option", name="TP, Fire & Theft").click()

        # --- Condition for coverage if needed ----
        '''page.locator("#mat-select-value-9").click()
        if vehicle_age >= 20:
            page.get_by_role("option", name="TP, Fire & Theft").click()
        else:
            page.get_by_role("option", name="Comprehensive").click()

        selected_coverage = page.locator("#mat-select-value-9").inner_text().strip()
        print("Selected Coverage type: ", selected_coverage)'''

        # ---- COVERAGE DATE -----
        incep_date(page)

        # ---- MARKET VALUE ----
        market_value_text = page.locator("mat-form-field").filter(has_text="Market Value").locator("#ismMarketValue").input_value().strip()
        market_value = int(float(market_value_text.replace(",", "")))
        print(f"Market Value: {market_value}")

        # ---- VEHICLE SUM INSURED ----
        sum_insured = str(market_value) if market_value > 5000 else "5000"
        print(f"Sum Insured: {sum_insured}")

        page.locator("dx-input-currency").filter(has_text="* Vehicle Sum Insured *").locator("#sumInsured").click()
        page.locator("dx-input-currency").filter(has_text="* Vehicle Sum Insured *").locator("#sumInsured").fill(sum_insured)

        #---- MYKAD ID ----
        page.locator("mat-form-field").filter(has_text="ID # * help").locator("#id").fill(vehicle_data["mykad"])

        #----NAME OF THE PH ----
        page.locator("mat-form-field").filter(has_text="Name as per ID *").locator("#legalName").fill("PC")
        page.get_by_role("button", name="search Validate Owner as per").click()

        # ==== Multi Contract / Extensions ====
        answer = [None]
        def ask_input():
            answer[0] = input("Do you need extensions? (yes/no): ").strip().lower()

        thread = threading.Thread(target=ask_input)
        thread.daemon = True
        thread.start()
        thread.join(timeout=20)

        if answer[0] == "yes":
            extension(page, selected_coverage)
            print("Extensions added successfully")
        else:
            if answer[0] is None:
                print("No response, Extensions skipped")
            else:
                print("No Extensions Selected")

        page.pause()

        # ---- NCD value ----
        page.wait_for_timeout(7000)
        ncd_value = page.locator("#currentNCD input.mat-input-element").input_value()
        print("NCD Value:", ncd_value, "%")

        #---- SAVE & NEXT BUTTON -----
        page.get_by_role("button", name="Save & Next").click()
        print("Registration Number is Triggered to ISM")


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
            # close any open dropdown/overlay
            page.keyboard.press("Escape")
            page.wait_for_timeout(1000)
            # scroll button into view
            add_button.scroll_into_view_if_needed()
            page.wait_for_timeout(1000)
            # force click to bypass overlay interception
            add_button.click(force=True)

            print("Clicked on Add button")

        # ---- STATE ---- (runs for both cases)
        page.locator(".mat-select-placeholder").first.click()
        page.get_by_role("option", name="Johor").click()
        page.wait_for_timeout(3000)

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
            page.locator("div.box-card").nth(1).click()
        
        # ---- Garage Types ----
        page.locator(".mat-select-placeholder").first.click()
        page.get_by_role("option", name="Public Road").click()
        page.locator(".mat-select-placeholder").first.click()
        page.get_by_role("option", name="No Alarm(WITHOUT MECHANICAL").click()
        page.locator(".mat-select-placeholder").click()
        page.get_by_role("option", name="ABS(No Airbags)").click()

        # ---- Declaration Statements ----
        page.get_by_text("We respect your privacy and").click()
        page.get_by_text("I hereby confirm that I have").click()

        # ---- Get Quote Number -----
        quote_text = page.locator("text=Quote Reference #").locator("xpath=following-sibling::*").inner_text()
        quote_number = quote_text.strip()
        print("Quote Number:", quote_number)

        # ====== NSTP FLOW FUNCTION CALL ======
        submit_approval_btn = page.get_by_role("button", name="Submit for TPM Staff Approval")
        
        # ---- Upload Doc later (PC only) ----
        upload_later = page.get_by_text("Upload Supporting documents later").first
        try:
            upload_later.wait_for(state="visible", timeout=5000)
            if upload_later.is_enabled():
                upload_later.click()
                page.locator("dx-evidence-upload").get_by_role("textbox").click()
                page.locator("dx-evidence-upload").get_by_role("textbox").fill("will upload documents later")
                print("NSTP - Upload later of Documents")
            else:
                print("STP case - Upload later disabled, skipping")
        except:
            print("Upload later option not present, skipping")

        if submit_approval_btn.is_visible():
            # ---- Submit for Review Button ----
            submit_approval_btn.click()
            print("Clicked on Submit for TPM Staff Approval button")
            page.wait_for_timeout(17000)

            # ---- Browser launch ---
            browser = page.context.browser
            manager_context = browser.new_context()
            manager_page = manager_context.new_page()

            url_segment = "reg"
            manager_page.goto(f"https://agent-uat.tuneinsurance.com/#/qms/quote/motor/{url_segment}/cover-details?edit=true&quoteNr={quote_number}")
            manager_approval(manager_page)

        # === PROCEED TO POLICY ISSUANCE ===
        page.get_by_role("button", name="Proceed to Policy Issuance").click()

        # ==== POLICY ISSUANCE ====
        page.get_by_role("button", name="Issue Policy").click()
        print("Issue Policy button clicked")
        page.wait_for_timeout(30000)
        page.reload()
        page.wait_for_load_state("networkidle")

        # ---- Printing Policy number ----
        page.wait_for_timeout(10000)
        policy_element = page.locator("span.fw-bold").filter(has_text="Policy #:")
        policy_element.wait_for(state="visible", timeout=10000)
        policy_text = policy_element.inner_text().strip()
        policy_number = policy_text.replace("Policy #:", "").strip()
        print("DEV - PC")
        print("Quote Reference:", quote_number)
        print("Policy Number:", policy_number)



    finally:
        page.get_by_text("Murali Mohan", exact=True).click()
        page.get_by_text("Sign Out", exact=True).click()
        page.wait_for_timeout(15000)
