
def login(page):
    page.goto("https://ath-uat.tuneinsurance.com/realms/tune/protocol/openid-connect/auth?response_type=code&client_id=1003&state=VEJYMU9YQ3pVaGZGemotRTNLMGN4OHhFaXc3ZmQ1cldaRXRFMG4wbDJBT0Rr&redirect_uri=https%3A%2F%2Fagent-uat.tuneinsurance.com%2F%23%2Fhome&scope=openid%20profile&code_challenge=TSCey8KaEFyGzZ5lgGfWXplgcJ1ivvARav8R4bnYPfM&code_challenge_method=S256&nonce=VEJYMU9YQ3pVaGZGemotRTNLMGN4OHhFaXc3ZmQ1cldaRXRFMG4wbDJBT0Rr")

    page.get_by_role("textbox", name="Username or email").fill("playwright.test@serole.com")
    page.get_by_role("textbox", name="Password").fill("Serole@123")
    page.get_by_role("button", name="Login").click()


def navigation(page):
    page.get_by_text("request_quote QMS Quotation").click()
    page.get_by_role("button", name="New Quote").click()
    page.get_by_role("heading", name="Motor").click()

    # === for Private car & Motorcycle ====
    #page.get_by_role("heading", name="Reg. Motorcar/Motorcycle").click()

    # === for commercial vehicle ====
    page.get_by_role("heading", name="Reg. Commercial Vehicle").click()

    page.get_by_role("button", name="Next").click()
    page.get_by_role("textbox").click()

    