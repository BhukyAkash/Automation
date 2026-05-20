import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from base_login import manager_approval

def nstp_flow(page, quote_number, vehicle_type="cv"):

    submit_approval_btn = page.get_by_role("button", name="Submit for TPM Staff Approval")
    generate_quote_btn = page.get_by_role("button", name="Generate Quote")
    
    # ---- Upload Doc later ----
    if vehicle_type == "pc":
        page.get_by_text("Upload Supporting documents later").first.click()
        page.locator("dx-evidence-upload").get_by_role("textbox").click()
        page.locator("dx-evidence-upload").get_by_role("textbox").fill("will upload documents later")

    if submit_approval_btn.is_visible():
        # ---- Submit for Review Button ----
        submit_approval_btn.click()
        print("Clicked on Submit for TPM Staff Approval button")
        page.wait_for_timeout(17000)

        browser = page.context.browser
        manager_context = browser.new_context()
        manager_page = manager_context.new_page()

        url_segment = "reg" if vehicle_type == "pc" else "rcv"
        manager_page.goto(
            f"https://agent-uat.tuneinsurance.com/#/qms/quote/motor/{url_segment}/cover-details"
            f"?edit=true&quoteNr={quote_number}"
        )
        manager_approval(manager_page)

        # ---- Back button ----
        page.get_by_role("button", name="Back").click()
        page.wait_for_timeout(3000)

    return generate_quote_btn