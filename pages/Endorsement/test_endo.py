from tips_endo import endorsement
from datetime import datetime, timedelta


#Run Command: pytest -s endorsement\test_endo.py
def test_motor_endo(page, request):
    try:
        endorsement(page, request)

        # --- Expiry Date of Policy ---
        expiry_date = page.locator(".col-md-3").filter(has_text="Expiry Date").locator("span.ng-star-inserted").first.inner_text()
        print("Expiry Date:", expiry_date)

        # ---- Endorsement Reason ----
        reason = "Extend Period of Insurance"
        page.get_by_text(reason).click()
        print(f"Endorsement Reason: {reason}")

        # --- Extending Period of Insurance ---
        expiry_date = datetime.strptime(expiry_date, "%d/%m/%Y")

        # --- Add 2 months manually ---
        month = expiry_date.month + 2
        year = expiry_date.year + (month - 1) // 12
        month = month % 12 or 12
        new_date = expiry_date.replace(year=year, month=month)
        
        # ---- Open Calendar ----
        page.locator("mat-form-field").filter(has_text="Expiry Date").get_by_label("Open calendar").click()

        # --- Extended Date ----
        while True:
            header = page.locator("button.mat-calendar-period-button").inner_text()
            current = datetime.strptime(header.strip().title(), "%b %Y")
            if current.year == new_date.year and current.month == new_date.month:
                break
            page.locator("button.mat-calendar-next-button").click()
            page.wait_for_timeout(300)

        # --- Click the correct day ---
        page.locator(f"button.mat-calendar-body-cell[aria-label='{new_date.strftime('%B')} {new_date.day}, {new_date.year}']").click()
        print("Extended period of Insurance till:", new_date.strftime("%d/%m/%Y"))

        page.get_by_role("button", name="Validate Owner ID # & NCD%").click()
        page.get_by_role("button", name="Save").click()
        print("Save Button Clicked")
        page.get_by_role("button", name="Next", exact=True).click()
        print("Next Button Clicked")

        page.get_by_role("button", name="Submit for Processing").click()
        page.get_by_role("button", name="Proceed").click()


        page.pause()



    finally:
        page.bring_to_front()
        page.get_by_text("playwright", exact=True).click()
        page.get_by_text("Sign Out", exact=True).click()
        page.wait_for_timeout(15000)