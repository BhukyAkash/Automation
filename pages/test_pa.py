from openpyxl import Workbook, load_workbook
from base_login import login, navi_pa

def test_PA(page):

    try:
        login(page)
        navi_pa(page)

        print("User successfully logged in and navigated to Personal Accident section")

        # ========= FIRST SCREEN ===========

        # ---- MYKAD ID ----
        page.locator("#dx-input-0").nth(1).click()
        page.locator("#dx-input-0").nth(1).fill("900506-12-1232")

        # ---- PH NAME ----
        page.locator("#dx-input-1").nth(1).click()
        page.locator("#dx-input-1").nth(1).fill("PERSONAL ACCIDENT")

        # ---- INTERNAL CLASSIFICATION ----
        page.locator(".mat-select-placeholder").first.click()
        page.get_by_role("option", name="Class 1").click()

        # ---- PLAN TYPE ----
        page.locator(".mat-select-placeholder").click()
        page.get_by_role("option", name="100,000").click()

        # ---- WEEKLY BENEFIT ----
        #page.locator("#mat-radio-9 > .mat-radio-label > .mat-radio-container > .mat-radio-outer-circle").click()
        page.locator("mat-radio-button:has-text('No')").nth(1).click()
        print("Weekly Benefit not selected")

        page.locator("#dx-checkbox-1 > .mat-checkbox-layout > .mat-checkbox-inner-container").click()

        # ---- SAVE & NEXT ----
        page.get_by_role("button", name="Save & Next").click()

        # ========== SECOND SCREEN ==========

        #page.get_by_role("button", name="Add").first.click()

        '''# ---- STATE ----
        page.locator(".mat-select-placeholder").first.click()
        page.get_by_role("option", name="Johor").click()
        page.wait_for_timeout(5000)

        # ---- PINCODE ----
        page.locator(".mat-select-placeholder").first.click()
        page.get_by_role("option", name="81100").click()
        page.wait_for_timeout(3000)

        # ---- STREET ADDRESS ----
        page.locator(".mat-select-placeholder").click()
        page.get_by_role("option", name="Desa Harmoni", exact=True).click()
        page.wait_for_timeout(2000)'''

        # ---- CONTACT DETAILS ----
        page.get_by_role("textbox", name="123456789").fill("123456789")
        page.get_by_role("textbox", name="Enter").fill("akash@serole.com")


        # ---- UNDERWRITING QUESTIONS ----
        radios = page.get_by_role("radio", name="No")
        for i in range(5):
            radios.nth(i).check()

        # ---- Declaration Statements ----
        page.get_by_text("1. Are any of the Insured").click()
        page.get_by_text("We respect your privacy").click()
        page.get_by_text("I hereby confirm that I have").click()

        # ---- Get Quote Number ----
        quote_text = page.locator("text=Quote Reference #").locator("xpath=following-sibling::*").inner_text()
        quote_number = quote_text.strip()
        print("Quote Number:", quote_number)
        
        # ---- GENERATE & DOWNLOAD QUOTE -----
        page.get_by_role("button", name="Generate Quote").click()
        page.wait_for_timeout(10000)

        page.get_by_role("button", name="Download Quote & PDS Documents").click()
        page.locator("form").get_by_text("Download Quote & PDS Documents").click()

        with page.expect_download() as download_info:
            page.get_by_role("button", name="Download").click()
        download = download_info.value
        download.save_as("downloads/PA_quote.pdf")

        page.wait_for_timeout(10000)

        # ---- ISSUE POLICY & DOWNLOAD POLICY SCHEDULE ----
        page.get_by_role("button", name="Issue Policy").click()
        page.get_by_role("button", name="Accept & Proceed").click()

        page.wait_for_timeout(15000)
        page.reload()

        # ---- Download the policy schedule ----
        page.get_by_role("button", name="Download & e-mail Policy").click()
        page.get_by_text("Download Policy Schedule").click()

        page.wait_for_timeout(10000)

        with page.expect_download() as download_info:
            page.get_by_role("button", name="Download").click()
        download = download_info.value
        download.save_as("downloads/PA_policy.pdf")

        # ---- Printing the policy number ----
        policy_locator = page.locator("text=Policy #:")
        policy_locator.wait_for()
        policy_text = policy_locator.text_content()
        policy_number = policy_text.replace("Policy #:", "").strip()
        print("Policy Number:", policy_number)



        # ------- SAVE TO EXCEL -------
        import os
        file_path = "UATStability.xlsx"

        if os.path.exists(file_path):
            wb = load_workbook(file_path)
        else:
            wb = Workbook()

        ws = wb.active

        # PA values
        ws["F5"] = quote_number
        ws["G5"] = policy_number
        wb.save(file_path)

    finally:
        page.wait_for_timeout(15000)
        page.get_by_text("playwright", exact=True).click()
        page.get_by_text("Sign Out", exact=True).click()
        page.wait_for_timeout(7000)