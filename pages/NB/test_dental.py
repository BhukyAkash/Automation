import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from base_login import login, navi_dental
from mykad_id import generate_mykad
from excel_file import dental

# ---- Path References ----
BASE_DIR = os.path.join(os.path.dirname(__file__), "..")               # D:\Automation\pages
DOWNLOADS_DIR = os.path.join(os.path.dirname(__file__), "downloads")  # D:\Automation\pages\NB\downloads

def test_dental(page):
    try:
        print("\n===================== Issuance of Dental policy ==================")
        login(page)
        navi_dental(page)

        page.wait_for_timeout(5000)

        # ---- MyKad -----
        mykad = generate_mykad()
        page.locator("mat-form-field").filter(has_text="ID #").locator("#dx-input-0").fill(mykad)

        # --- Insured Name ----
        page.locator("mat-form-field").filter(has_text="Name as per ID").locator("#dx-input-1").fill("Dental Shield")

        # # ---- INCEPTION DATE ----
        # date_field = page.locator("input#inceptionDate")
        # date_field.click()
        # date_field.press("Control+A")
        # date_field.fill("01-06-2026")

        # --- Declaration  ----
        page.wait_for_timeout(5000)
        page.get_by_text("The Proposer/Person(s) to be").click()

        # ---- Proceed to Quote ----
        page.wait_for_timeout(2000)
        page.get_by_role("button",name="Proceed Quote").click()
        page.wait_for_load_state("networkidle")

        # ---- CHECK IF ADDRESS ALREADY EXISTS ----
        add_button = page.locator("button[name='Add'], button:has-text('Add')").first
        try:
            add_button.wait_for(state="visible", timeout=3000)
            add_button.click()
            page.wait_for_timeout(1000)
        except:
            pass  

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
        address_save = page.get_by_role("button", name="Save")
        if address_save.is_visible():
            address_save.click()

        # ---- CONTACT DETAILS ----
        page.get_by_role("textbox", name="123456789").fill("123456789")
        page.get_by_role("textbox", name="Enter").fill("akash@serole.com")

        # ---- Declaration Statements ----
        page.get_by_text("We respect your privacy and").click()
        page.get_by_text("I hereby confirm that I have").click()

        # ---- GENERATE & DOWNLOAD QUOTE -----
        page.get_by_role("button", name="Generate Quote").wait_for()
        page.get_by_role("button", name="Generate Quote").click()
    
        page.get_by_role("button", name="Download Quote & PDS Documents").click()
        page.locator("form").get_by_text("Download Quote & PDS Documents").click()

        with page.expect_download() as download_info:
            page.get_by_role("button", name="Send").click()
        download = download_info.value
        download.save_as(os.path.join(DOWNLOADS_DIR, "Dental_quote.pdf"))
        page.get_by_text("close", exact=True).click()
        print("Quote PDF Generated successfully")

        # ---- Get Quote Number ----
        quote_text = page.locator("text=Quote Reference #").locator("xpath=following-sibling::*").inner_text()
        quote_number = quote_text.strip()
        print("Quote Number:", quote_number)

        # --- Issue Policy ----
        page.get_by_role("button", name="Issue Policy").click()
        page.get_by_role("button", name="Accept & Proceed").click()
        print("Issue Policy clicked, waiting for processing...")

        page.wait_for_timeout(15000)

        # ---- Printing the policy number ----
        page.wait_for_selector("text=Policy #", timeout=30000)
        policy_number = (page.locator("div.-second").filter(has_text="Policy #").locator("span").last.inner_text())
        print("Policy Number:", policy_number)

        # ---- Download the policy schedule ----
        page.get_by_role("button", name="Download & Email Policy").click()
        page.get_by_text("Download Policy Schedule").click()
        print("Policy Issued successfully")

        page.wait_for_timeout(10000)

        with page.expect_download() as download_info:
            page.get_by_role("button", name="Send").click()
        download = download_info.value
        download.save_as(os.path.join(DOWNLOADS_DIR, "Dental_policy.pdf"))

        print("Policy Schedule PDF downloaded successfully")

        # --- Save to Excel ----
        dental(quote_number, policy_number)

    finally:
        page.wait_for_timeout(15000)
        page.get_by_text("playwright", exact=True).click()
        page.get_by_text("Sign Out", exact=True).click()
        page.wait_for_timeout(7000)