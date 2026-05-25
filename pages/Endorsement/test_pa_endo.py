from tips_endo import endorsement


#Run Command: pytest -s endorsement\test_pa_endo.py --product=pa
def test_pa(page, request):
    try:
        endorsement(page, request)


        # ---- Endorsement Reason ----
        reason = "Correct Insured Person Details"
        page.get_by_text(reason).click()
        print(f"Endorsement Reason: {reason}")

        # --- Sub Reason Drop down Selection ---
        page.locator(".mat-select-placeholder").click()
        page.get_by_role("option", name="Occupation").click()

        # --- Occupation Class ---
        page.locator(".mat-select-placeholder").click()
        page.get_by_role("option", name="Class 1").click()

        # --- Declaration Statement ---
        page.get_by_text("I/We declare that the Policy Information Provided").click()

        # --- Save & Next ----
        page.get_by_role("button", name="Save").click()
        page.get_by_role("button", name="Next").click()

        # --- Quote Reference Number ---
        quote_text = page.locator("text=Quote Reference #").locator("xpath=following-sibling::*").inner_text()
        quote_number = quote_text.strip()
        print("Quote Number:", quote_number)

        page.get_by_role("button", name="Proceed").click()
        page.get_by_role("button", name="Submit for Processing").click()

        print("Endorsement performed successfully")

    finally:
        page.bring_to_front()
        page.get_by_text("playwright", exact=True).click()
        page.get_by_text("Sign Out", exact=True).click()
        page.wait_for_timeout(15000)