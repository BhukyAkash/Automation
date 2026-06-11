import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from base_login import login, navi_pa
from mykad_id import generate_mykad, child_mykad
from popup_utils import select_popup
from test_mail import send_email
from excel_file import pa_excel

# ---- Path References ----
BASE_DIR = os.path.join(os.path.dirname(__file__), "..")               # D:\Automation\pages
DOWNLOADS_DIR = os.path.join(os.path.dirname(__file__), "downloads")  # D:\Automation\pages\NB\downloads

def test_PA(page):

    try:
        print("===================== Issuance of PA policy ==================")
        login(page)
        navi_pa(page)
        print("User successfully logged in and navigated to Personal Accident section")

        # ========= FIRST SCREEN ===========

        # ---- MYKAD ID ----
        page.locator("#dx-input-0").nth(1).click()
        mykad = generate_mykad()
        page.locator("#dx-input-0").nth(1).fill(mykad)
        print("MyKad ID: ", mykad)

        # ---- PH NAME ----
        page.locator("#dx-input-1").nth(1).click()
        page.locator("#dx-input-1").nth(1).fill("PERSONAL ACCIDENT")

        # --- Occupation Class ----
        class_ques = select_popup(
            "What occupation class do you want to select?",
            ["Class 1", "Class 2", "Full-Time Student", "Dependent"]
        )
        print(f"Occupation Class selected: {class_ques}")

        if class_ques in ("Full-Time Student", "Dependent"):
            # ---- PROPOSER IS NOT THE INSURED ----
            page.get_by_text("Proposer is not the Insured").click()

            page.locator("#dx-input-3").nth(1).click()
            mykad = child_mykad()
            page.locator("#dx-input-3").nth(1).fill(mykad)
            print("Child MyKad ID: ", mykad)

            page.locator("#dx-input-4").nth(1).click()
            page.locator("#dx-input-4").nth(1).fill("Insurer")

            # ---- INTERNAL CLASSIFICATION ----
            page.locator(".mat-select-placeholder").first.click()
            page.get_by_role("option", name=class_ques).click()

            # ---- PRODUCT SELECTION ----
            selected_title = "Personal Accident Safe"    
            #selected_title = "PA Shield"
            page.locator("[formcontrolname='paProducts']").click()
            page.get_by_role("option", name=selected_title).click()
            print("Selected Product:", selected_title)

            # ---- PLAN TYPE ----
            page.locator(".mat-select-placeholder").click()
            page.get_by_role("option", name="200,000").click()

        elif class_ques in ("Class 1", "Class 2"):
            # ---- INTERNAL CLASSIFICATION ----
            page.locator(".mat-select-placeholder").first.click()
            page.get_by_role("option", name=class_ques).click()

            # ---- PRODUCT SELECTION ----
            selected_title = "Personal Accident Safe"    
            #selected_title = "PA Shield"
            page.locator("[formcontrolname='paProducts']").click()
            page.get_by_role("option", name=selected_title).click()
            print("Selected Product:", selected_title)

            # ---- PLAN TYPE ----
            page.locator(".mat-select-placeholder").click()
            page.get_by_role("option", name="200,000").click()

            # ---- WEEKLY BENEFIT ----
            page.locator("mat-radio-button:has-text('No')").nth(1).click()
            print("Weekly Benefit not selected")

        '''# ---- INCEPTION DATE ----
        date_field = page.locator("input#inceptionDate")
        date_field.click()
        date_field.press("Control+A")
        date_field.fill("01-06-2026")'''

        page.get_by_text("The Proposer/Person to be").click()

        # ---- SAVE & NEXT ----
        page.get_by_role("button", name="Save & Next").click()
        page.wait_for_timeout(10000)

        # ========== SECOND SCREEN ==========


        # ========== SCREEN 2 DEBUG ==========
        page.wait_for_timeout(3000)

        '''print("=== SCREEN 2 DEBUG ===")
        print("URL:", page.url)
        print("All buttons:")
        for btn in page.get_by_role("button").all():
            print(f"  BUTTON: '{btn.inner_text().strip()}'")

        print("All mat-select (formcontrolname):")
        for sel in page.locator("mat-select").all():
            print(f"  MAT-SELECT formcontrolname: '{sel.get_attribute('formcontrolname')}'")

        print("mat-select-placeholder count:", page.locator(".mat-select-placeholder").count())
        print("Yes visible:", page.get_by_role("button", name="Yes").first.is_visible())
        print("Add visible:", page.get_by_role("button", name="Add").first.is_visible())
        print("=== END SCREEN 2 DEBUG ===")'''

        # ---- CHECK IF YES BUTTON EXISTS AND IS ENABLED ----
        try:
            page.get_by_role("button", name="Yes").first.wait_for(state="visible", timeout=5000)
            page.get_by_role("button", name="Yes").first.click()
            page.wait_for_timeout(2000)
        except:
            pass

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

        # ---- UNDERWRITING QUESTIONS ----
        radios = page.get_by_role("radio", name="No")
        for i in range(5):
            radios.nth(i).check()

        # ---- Declaration Statements ----
        page.get_by_text("We respect your privacy").click()
        page.get_by_text("I hereby confirm that I have").click()

        # ---- Get Quote Number ----
        quote_text = page.locator("text=Quote Reference #").locator("xpath=following-sibling::*").inner_text()
        quote_number = quote_text.strip()
        print("Quote Number:", quote_number)
        
        # ---- GENERATE & DOWNLOAD QUOTE -----
        page.get_by_role("button", name="Generate Quote").wait_for()
        page.get_by_role("button", name="Generate Quote").click()
    
        page.get_by_role("button", name="Download Quote & PDS Documents").click()
        page.locator("form").get_by_text("Download Quote & PDS Documents").click()

        with page.expect_download() as download_info:
            page.get_by_role("button", name="Download").click()
        download = download_info.value
        download.save_as(os.path.join(DOWNLOADS_DIR, "PA_quote.pdf"))
        page.get_by_text("close", exact=True).click()
        print("Quote PDF Generated successfully")

        page.wait_for_timeout(10000)

        # ---- ISSUE POLICY & DOWNLOAD POLICY SCHEDULE ----
        page.get_by_role("button", name="Issue Policy").click()
        page.get_by_role("button", name="Accept & Proceed").click()
        print("Issue Policy clicked, waiting for processing...")
        
        page.wait_for_timeout(30000)
        page.reload()

        # ---- Download the policy schedule ----
        page.get_by_role("button", name="Download & Email Policy").click()
        page.get_by_text("Download Policy Schedule").click()
        print("Policy Issued successfully")

        page.wait_for_timeout(10000)

        with page.expect_download() as download_info:
            page.get_by_role("button", name="Download").click()
        download = download_info.value
        download.save_as(os.path.join(DOWNLOADS_DIR, "PA_policy.pdf"))
        page.get_by_text("close", exact=True).click()

        # ---- Printing the policy number ----
        policy_locator = page.locator("text=Policy #:")
        policy_locator.wait_for()
        policy_text = policy_locator.text_content()
        policy_number = policy_text.replace("Policy #:", "").strip()
        print("Policy Number:", policy_number)

        print("Policy Schedule downloaded successfully")

        # ------- SAVE TO EXCEL -------
        pa_excel(selected_title, quote_number, policy_number)

        # ---- SEND EMAIL ----
        try:
            send_email()
        except Exception as e:
            print("Email failed:", e)

    finally:
        page.wait_for_timeout(15000)
        page.get_by_text("playwright", exact=True).click()
        page.get_by_text("Sign Out", exact=True).click()
        page.wait_for_timeout(7000)