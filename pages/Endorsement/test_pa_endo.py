import os
import sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from tips_endo import endorsement
import endo_reasons as er

DOWNLOADS_DIR = os.path.join(os.path.dirname(__file__), "downloads")

# Run Command: pytest -s endorsement\test_pa_endo.py --product=pa
def test_pa(page, request):
    try:
        policy_number = endorsement(page, request)

        # --- Endorsement Reason Selection ---
        #er.class_change(page)
        er.SI_change(page)

        # --- Endorsement Release ---
        endo_quote = er.endo_release(page)

        # --- Download Endorsement Schedule ---
        page.get_by_role("button", name="View Change Schedule").click()
        page.locator("form").get_by_text("Download Endorsement Schedule").click()

        with page.expect_download() as download_info:
            page.get_by_role("button", name="Submit").click()
        download = download_info.value
        download.save_as(os.path.join(DOWNLOADS_DIR, "PA_endo_schedule.pdf"))

        print("Endorsement Schedule downloaded successfully")


        # ====== Save to Excel ======
        er.save_excel(policy_number, endo_quote)

    finally:
        page.bring_to_front()
        page.get_by_text("playwright", exact=True).click()
        page.get_by_text("Sign Out", exact=True).click()
        page.wait_for_timeout(15000)