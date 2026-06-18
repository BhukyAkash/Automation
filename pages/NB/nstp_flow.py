import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from base_login import manager_approval

def nstp_flow(page, quote_number, vehicle_type="cv"):

    submit_approval_btn = page.get_by_role("button", name="Submit for TPM Staff Approval")
    generate_quote_btn = page.get_by_role("button", name="Generate Quote")
    
    # ---- Upload Doc later (PC only) ----
    if vehicle_type == "pc":
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

        browser = page.context.browser
        manager_context = browser.new_context(no_viewport = True)
        manager_page = manager_context.new_page()

        url_segment = "reg" if vehicle_type == "pc" else "rcv"
        manager_page.goto(
            f"https://agent-uat.tuneinsurance.com/#/qms/quote/motor/{url_segment}/cover-details"
            f"?edit=true&quoteNr={quote_number}"
        )
        manager_approval(manager_page)

        # ---- Back button ----
        page.get_by_role("button", name="Back").click()
        print("Navigated to Back for Quote letter")
        page.wait_for_timeout(3000)

    return generate_quote_btn