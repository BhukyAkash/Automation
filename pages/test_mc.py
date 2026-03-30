from conftest import page
from excel_utils import get_vehicle_data
from datetime import datetime
from base_login import login, navigation, pc_moto

def test_mc_motor(page):

    try:
        login(page)
        navigation(page)
        pc_moto(page)

        # ========= FIRST SCREEN ===========
        
        # ---- VEHICLE REG ----
        vehicle_data = get_vehicle_data("MC")
        page.get_by_role("textbox").first.fill(vehicle_data["vehicle_reg_no"])

        #---- Place of Use ----
        page.locator(".mat-select-placeholder").click()
        page.get_by_role("option", name="Johor").click()

        #---- Vehicle Search ----
        page.get_by_role("button", name="search Vehicle Search").click()

        page.wait_for_timeout(5000)

        #---- MYKAD ID ----
        page.locator("mat-form-field").filter(has_text="ID # * help").locator("#id").fill(vehicle_data["mykad"])

        #----NAME OF THE PH ----
        page.locator("mat-form-field").filter(has_text="Name as per ID *").locator("#legalName").fill("MC")
        page.get_by_role("button", name="search Validate Owner as per").click()

        #---- SAVE & NEXT BUTTON -----
        page.get_by_role("button", name="Save & Next").click()

        # ---- CHECK IF ADDRESS ALREADY EXISTS ----
        add_button = page.get_by_role("button", name="Add").first

        if add_button.is_visible():
            add_button.click()
            page.wait_for_timeout(3000)

        # ---- STATE ---- (runs for both cases)
        page.locator(".mat-select-placeholder").first.click()
        page.get_by_role("option", name="Johor").click()
        page.wait_for_timeout(5000)

        # ---- PINCODE ----
        page.locator(".mat-select-placeholder").first.click()
        page.get_by_role("option", name="81100").click()
        page.wait_for_timeout(3000)

        # ---- STREET ADDRESS ----
        page.get_by_role("combobox", name="Address Line").click()
        page.get_by_role("option", name="Desa Harmoni", exact=True).click()
        page.wait_for_timeout(2000)

        page.get_by_role("button", name="Save").click()

        # Locate the element that contains the quote reference
        quote_text = page.locator("text=Quote Reference #").locator("xpath=following-sibling::*").inner_text()
        quote_number = quote_text.strip()
        print("Quote Number:", quote_number)

        # ---- Drving Experience ----
        page.locator(".mat-select-placeholder").first.click()
        page.get_by_role("option", name="Less than 2 years").click()

        # ---- CHECK IF ADDRESS ALREADY EXISTS ----
        add_button = page.get_by_role("button", name="Add").first

        if add_button.is_visible():
            add_button.click()
            page.wait_for_timeout(3000)

        # ---- STATE ----
        page.locator(".mat-select-placeholder").first.click()
        page.get_by_role("option", name="Johor").click()
        page.wait_for_timeout(3000)

        # ---- PINCODE ----
        page.locator(".mat-select-placeholder").first.click()
        page.get_by_role("option", name="81100").click()
        page.wait_for_timeout(2000)

        # ---- STREET ADDRESS ----
        page.get_by_role("combobox", name="Address Line").click()
        page.get_by_role("option", name="Desa Harmoni", exact=True).click()
        page.wait_for_timeout(2000)

        page.get_by_role("button", name="Save").click()

        page.locator("//label[@for='2']//div[@class='box-card d-flex align-items-center gap-2 px-2 py-1']").click()




    finally:
        page.get_by_text("playwright", exact=True).click()
        page.get_by_text("Sign Out", exact=True).click()
        page.wait_for_timeout(15000)