from excel_utils import get_vehicle_data
from datetime import datetime


def test_tipuat_motor(page):

    page.goto("https://ath-uat.tuneinsurance.com/realms/tune/protocol/openid-connect/auth?response_type=code&client_id=1003&state=VEJYMU9YQ3pVaGZGemotRTNLMGN4OHhFaXc3ZmQ1cldaRXRFMG4wbDJBT0Rr&redirect_uri=https%3A%2F%2Fagent-uat.tuneinsurance.com%2F%23%2Fhome&scope=openid%20profile&code_challenge=TSCey8KaEFyGzZ5lgGfWXplgcJ1ivvARav8R4bnYPfM&code_challenge_method=S256&nonce=VEJYMU9YQ3pVaGZGemotRTNLMGN4OHhFaXc3ZmQ1cldaRXRFMG4wbDJBT0Rr")
    
    page.get_by_role("textbox", name="Username or email").click()
    page.get_by_role("textbox", name="Username or email").fill("akash.bhukya@serole.com")
    page.get_by_role("textbox", name="Password").click()
    page.get_by_role("textbox", name="Password").fill("Serole@321")
    page.get_by_role("button", name="Login").click()


    page.goto("https://agent-uat.tuneinsurance.com/#/home#QMS%20Agent")


    page.get_by_text("request_quote QMS Quotation").click()
    page.get_by_role("button", name="New Quote").click()
    page.get_by_role("heading", name="Motor").click()
    page.get_by_role("button", name="Next").click()

    page.get_by_role("textbox").click()
    
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

