import os
from base_login import login, navi_pa
from test_mykad_id import generate_mykad, child_mykad, young_mykad
from popup_utils import select_popup

def test_pa(page):
    try:
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
        print(f"Occupation Class: {class_ques}")

        if class_ques in ("Full-Time Student"):
            # ---- PROPOSER IS NOT THE INSURED ----
            page.get_by_text("Proposer is not the Insured").click()

            page.locator("#dx-input-3").nth(1).click()
            mykad = young_mykad()   # ---> child age between 18-23 for FTS
            page.locator("#dx-input-3").nth(1).fill(mykad)
            print("Child MyKad ID: ", mykad)

            page.locator("#dx-input-4").nth(1).click()
            page.locator("#dx-input-4").nth(1).fill("Insurer")

            # ---- INTERNAL CLASSIFICATION ----
            page.locator(".mat-select-placeholder").first.click()
            page.get_by_role("option", name=class_ques).click()

            # ---- PLAN TYPE ----
            page.locator(".mat-select-placeholder").click()
            page.get_by_role("option", name="200,000").click()

        elif class_ques in ("Class 1", "Class 2"):
            # ---- INTERNAL CLASSIFICATION ----
            page.locator(".mat-select-placeholder").first.click()
            page.get_by_role("option", name=class_ques).click()

            # ---- PLAN TYPE ----
            page.locator(".mat-select-placeholder").click()
            page.get_by_role("option", name="200,000").click()

            # ---- WEEKLY BENEFIT ----
            page.locator("mat-radio-button:has-text('No')").nth(1).click()
            print("Weekly Benefit not selected")

        elif class_ques in ("Dependent"):
            # ---- PROPOSER IS NOT THE INSURED ----
            page.get_by_text("Proposer is not the Insured").click()

            page.locator("#dx-input-3").nth(1).click()
            mykad = child_mykad()   # ---> child age less than 18 Dependent
            page.locator("#dx-input-3").nth(1).fill(mykad)
            print("Child MyKad ID: ", mykad)

            page.locator("#dx-input-4").nth(1).click()
            page.locator("#dx-input-4").nth(1).fill("Insurer")

            # ---- INTERNAL CLASSIFICATION ----
            page.locator(".mat-select-placeholder").first.click()
            page.get_by_role("option", name=class_ques).click()

            # ---- PLAN TYPE ----
            page.locator(".mat-select-placeholder").click()
            page.get_by_role("option", name="200,000").click()

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
        page

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
        download.save_as(os.path.join(r"Letters\PA_quote.pdf"))
        page.get_by_text("close", exact=True).click()
        print("Quote PDF Generated successfully")

        page.wait_for_timeout(10000)

        # ---- ISSUE POLICY & DOWNLOAD POLICY SCHEDULE ----
        page.get_by_role("button", name="Issue Policy").click()
        page.get_by_role("button", name="Accept & Proceed").click()
        page.wait_for_timeout(30000)
        print("Issue Policy button clicked")

        # ---- Wait until Policy number is released  ----
        max_wait = 100
        interval = 35
        elapsed = 0     
        policy_number = "-"

        while elapsed < max_wait:
            try:
                policy_element = page.locator("span.policy-wrapper span").filter(has_text="Policy #:")
                policy_element.wait_for(state="visible", timeout=10000)
                policy_text = policy_element.inner_text().strip()

                policy_number = policy_text.replace("Policy #:", "").strip()
                if policy_number and policy_number != "-":
                    print("Policy Number:", policy_number)
                    break
                else:
                    print(f"Policy not yet issued, retrying... ({elapsed}s)")
            except:
                print(f"Policy locator not found, retrying... ({elapsed}s)")

            # Only reload if policy not found
            page.reload()
            page.wait_for_timeout(interval * 1000)
            elapsed += interval

        if policy_number == "-":
            print("Policy not issued after 2 minutes, something went wrong")

        print("SIT - PA")
        print("Quote Reference:", quote_number)
        print("Policy Number:", policy_number)


    finally:
        page.get_by_text("NMF Smart Resources", exact=True).click()
        page.get_by_text("Sign Out", exact=True).click()
        page.wait_for_timeout(15000)
