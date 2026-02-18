from excel_utils import get_vehicle_data
from datetime import datetime


def test_tipsit_motor_quote(page):

        # ---------- LOGIN ----------
        page.goto(
        "https://auth.sit.indigit.io/realms/Tune/protocol/openid-connect/auth"
        "?response_type=code&client_id=1003"
        "&redirect_uri=https%3A%2F%2Ftune.sit.indigit.io%2F%23%2Fhome"
        "&scope=openid%20profile"
        )

        page.get_by_role("textbox", name="Username or email").fill("akash.bhukya@serole.com")
        page.get_by_role("textbox", name="Password").fill("Serole@123")
        page.get_by_role("button", name="Login").click()

        page.pause()

        page.wait_for_load_state("networkidle")

        # ---------- NAVIGATION ----------
        page.get_by_text("request_quote QMS Quotation").click()
        page.get_by_role("button", name="New Quote").click()
        page.get_by_role("heading", name="Motor").click()
        page.get_by_role("button", name="Next").click()

        # ---------- VEHICLE REG ----------
        vehicle_data = get_vehicle_data()
        page.get_by_role("textbox").first.fill(vehicle_data["vehicle_reg_no"])

        #----------Place of Use----------
        page.locator(".mat-select-placeholder").click()
        page.get_by_role("option", name="Kedah").click()

        #--------Vehicle Search--------
        page.get_by_role("button", name="search Vehicle Search").click()

        #---------- VEHICLE DETAILS SAVE ----------
        page.get_by_role("button", name="Save Vehicle Info").click()


        #---------- SECOND SCREEN ----------

        #---------- COVERAGE DATE ----------

                # today date
        today = datetime.today()

                # Angular Material aria-label format
        aria_date = today.strftime("%B %d, %Y").replace(" 0", " ")

                # Open calendar
        page.locator("mat-form-field") \
                .filter(has_text="Inception Date * event") \
                .get_by_label("Open calendar") \
                .click()

                # Select today
        page.get_by_role("gridcell", name=aria_date).click()


        '''page.locator("mat-form-field").filter(has_text="Inception Date * event").get_by_label("Open calendar").click()
        page.get_by_role("button", name="February 5,").click()'''


        #---------- VEHICLE SUM INSURED ----------
        page.locator("dx-input-currency").filter(has_text="* Vehicle Sum Insured *").locator("#sumInsured").click()
        page.locator("dx-input-currency").filter(has_text="* Vehicle Sum Insured *").locator("#sumInsured").fill("5000")

        #---------- MYKAD ID ----------
        page.locator("mat-form-field").filter(has_text="ID # * help").locator("#id").fill(vehicle_data["mykad"])

        #--------NAME OF THE PH ---------
        page.locator("mat-form-field").filter(has_text="Name as per ID *").locator("#legalName").fill("PC")
        page.get_by_role("button", name="search Validate Owner as per").click()

        #---------- SAVE & NEXT BUTTON ----------
        page.get_by_role("button", name="Save & Next").click()


        #---------- THIRD SCREEN---COVER DETAILS ----------

        page.goto("https://tune.sit.indigit.io/#/qms/quote/motor/reg/cover-details?quoteNr=1000118172")

        #page.get_by_role("button", name="Yes").click()
        
        page.locator(".mat-select-placeholder").first.click()
        page.get_by_role("option", name="unlocked Garage").click()

        page.locator(".mat-select-placeholder").first.click()
        page.get_by_role("option", name="Others(WITH MECHANICAL DEVICE)").click()

        page.locator(".mat-select-placeholder").click()
        page.get_by_role("option", name="Driver & Passenger Airbags(2)").click()

        page.pause()

        page.locator("#dx-checkbox-4 > .mat-checkbox-layout > .mat-checkbox-inner-container").click()
        page.locator("#dx-checkbox-5 > .mat-checkbox-layout > .mat-checkbox-inner-container").click()


        #---------- APPROVED & VERIFIED ----------
        page.get_by_role("button", name="Proceed to Policy Issuance").click()


        page.goto("https://tune.sit.indigit.io/#/qms/quote/motor/reg/review?quoteNr=1000118172")

        #---------- ISSUE POLICY BUTTON ----------
        #page.get_by_role("button", name="Issue Policy").click()
        page.pause()

