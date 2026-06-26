import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

import pytest
import random
from base_login import login, navi_pa, pa_prem
from mykad_id import generate_mykad, child_mykad, young_mykad
from test_mail import send_email
from excel_utils import pa_excel, get_pa_data

# ---- Path References ----
BASE_DIR = os.path.join(os.path.dirname(__file__), "..")
DOWNLOADS_DIR = os.path.join(os.path.dirname(__file__), "downloads")

# ---- For multiple rows executions ---
@pytest.mark.parametrize("pa_row", [3])     # Test case row

def test_PA(page, pa_row):

    try:
        print("\n===================== Issuance of PA policy ==================")
        username = login(page)
        navi_pa(page)
        print("User successfully logged in and navigated to Personal Accident section")

        # ---- Read test data from PA sheet ----
        pa_data = get_pa_data(row=pa_row)
        class_ques     = pa_data["occupation_cls"]   # e.g. "Class 1"
        selected_title = pa_data["pa_product"]        # e.g. "Personal Accident Safe"
        plan_type      = pa_data["sum_insured"]       # e.g. "200,000"

        print(f"Occupation Class  : {class_ques}")
        print(f"PA Product        : {selected_title}")
        print(f"Sum Insured (Plan): {plan_type}")

        # ========= FIRST SCREEN ===========

        # ---- MYKAD ID ----
        page.locator("#dx-input-0").nth(1).click()
        mykad = generate_mykad()
        page.locator("#dx-input-0").nth(1).fill(mykad)
        print("MyKad ID:", mykad)

        # ---- PH NAME ----
        page.locator("#dx-input-1").nth(1).click()
        page.locator("#dx-input-1").nth(1).fill("PERSONAL ACCIDENT")

        # ---- BRANCH LOGIC BASED ON OCCUPATION CLASS ----
        if class_ques == "Full-Time Student":
            # ---- PROPOSER IS NOT THE INSURED ----
            page.get_by_text("Proposer is not the Insured").click()

            page.locator("#dx-input-3").nth(1).click()
            insured_mykad = young_mykad()
            page.locator("#dx-input-3").nth(1).fill(insured_mykad)
            print("Insured MyKad ID:", insured_mykad)

            page.locator("#dx-input-4").nth(1).click()
            page.locator("#dx-input-4").nth(1).fill("Insurer")

            # ---- INTERNAL CLASSIFICATION ----
            page.locator(".mat-select-placeholder").first.click()
            page.get_by_role("option", name=class_ques).click()

            # ---- PRODUCT SELECTION ----
            page.locator("[formcontrolname='paProducts']").click()
            page.get_by_role("option", name=selected_title).click()

            # ---- PLAN TYPE ----
            page.locator(".mat-select-placeholder").click()
            page.get_by_role("option", name=plan_type).click()

        elif class_ques in ("Class 1", "Class 2"):
            # ---- INTERNAL CLASSIFICATION ----
            page.locator(".mat-select-placeholder").first.click()
            page.get_by_role("option", name=class_ques).click()

            # ---- PRODUCT SELECTION ----
            page.locator("[formcontrolname='paProducts']").click()
            page.get_by_role("option", name=selected_title).click()

            # ---- PLAN TYPE ----
            page.locator(".mat-select-placeholder").click()
            page.get_by_role("option", name=plan_type).click()

            # ---- WEEKLY BENEFIT ----
            page.locator("mat-radio-button:has-text('No')").nth(1).click()
            print("Weekly Benefit: No")

        elif class_ques == "Dependent":
            # ---- PROPOSER IS NOT THE INSURED ----
            page.get_by_text("Proposer is not the Insured").click()

            page.locator("#dx-input-3").nth(1).click()
            insured_mykad = child_mykad()
            page.locator("#dx-input-3").nth(1).fill(insured_mykad)
            print("Insured MyKad ID:", insured_mykad)

            page.locator("#dx-input-4").nth(1).click()
            page.locator("#dx-input-4").nth(1).fill("Insurer")

            # ---- INTERNAL CLASSIFICATION ----
            page.locator(".mat-select-placeholder").first.click()
            page.get_by_role("option", name=class_ques).click()

            # ---- PRODUCT SELECTION ----
            page.locator("[formcontrolname='paProducts']").click()
            page.get_by_role("option", name=selected_title).click()

            # ---- PLAN TYPE ----
            page.locator(".mat-select-placeholder").click()
            page.get_by_role("option", name=plan_type).click()
        else:
            raise ValueError(f"Unknown occupation class '{class_ques}' in PA sheet row {pa_row}. "
                            f"Expected: Class 1, Class 2, Full-Time Student, Dependent")

        page.get_by_text("The Proposer/Person to be").click()

        # ---- SAVE & NEXT ----
        page.get_by_role("button", name="Save & Next").click()
        page.wait_for_timeout(10000)

        # ========== SECOND SCREEN ==========

        page.wait_for_timeout(3000)

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

        # ---- STATE ----
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

        # rebate_value = str(random.randint(10, 25))
        # rebate_locator = page.locator("mat-form-field").filter(has_text="Rebate to Proposer%").locator("#rebate")
        # rebate_locator.click()
        # rebate_locator.fill(rebate_value)
        # print(f"Rebate: {rebate_value}%")

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

        # ---- GENERATE & DOWNLOAD QUOTE ----
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

        # ---- Premiums -------
        sum_insured, gross_premium, rebate, sst, stamp_duty, total = pa_prem(page)

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

        page.wait_for_timeout(6000)

        with page.expect_download() as download_info:
            page.get_by_role("button", name="Download").click()
        download = download_info.value
        download.save_as(os.path.join(DOWNLOADS_DIR, "PA_policy.pdf"))
        page.get_by_text("close", exact=True).click()

        # ---- Policy Number ----
        policy_locator = page.locator("text=Policy #:")
        policy_locator.wait_for()
        policy_text = policy_locator.text_content()
        policy_number = policy_text.replace("Policy #:", "").strip()
        print("Policy Number:", policy_number)

        print("Policy Schedule downloaded successfully")

        # ---- SAVE TO EXCEL ----
        pa_excel(selected_title, quote_number, policy_number, sum_insured,
                gross_premium, rebate, sst, stamp_duty, total)

        # ---- SEND EMAIL ----
        # try:
        #     send_email()
        # except Exception as e:
        #     print("Email failed:", e)

    finally:
        page.get_by_text(username, exact=True).click()
        page.get_by_text("Sign Out", exact=True).click()
        print("Terminated the session")
        page.wait_for_timeout(15000)