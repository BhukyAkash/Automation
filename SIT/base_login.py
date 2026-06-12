from datetime import datetime

def login(page):
    page.goto("https://tune.sit.indigit.io/#/home#Apps")
    username = "test001.60@gmail.com"
    page.get_by_role("textbox", name="Username or email").fill(username)
    page.get_by_role("textbox", name="Password").fill("Tune@123")
    page.get_by_role("button", name="Login").click()
    print("\nLogged into:", username)

def navigation(page):
    page.get_by_text("request_quote QMS Quotation").click()
    page.get_by_role("button", name="New Quote").click()
    page.get_by_role("heading", name="Motor").click()

def pc_moto(page):
    # === for Private car & Motorcycle ====
    page.get_by_role("heading", name="Reg. Motorcar/Motorcycle").click()
    page.get_by_role("button", name="Next").click()
    page.get_by_role("textbox").click()

def cv_moto(page):
    # === for commercial vehicle ====
    page.get_by_role("heading", name="Reg. Commercial Vehicle").click()
    page.get_by_role("button", name="Next").click()
    page.get_by_role("textbox").click()

def navi_pa(page):
    page.get_by_text("request_quote QMS Quotation").click()
    page.get_by_role("button", name="New Quote").click()
    page.get_by_role("heading", name="Personal Accident, Travel & Health").click()
    page.get_by_role("heading", name="Personal Accident", exact=True).click()
    page.get_by_role("button", name="Next").click()

def endo_navigation(page, product):
    page.get_by_text("Policy Servicing (Endorsement)").click()
    print("Navigated to Endorsement Tile")
    # ---- Endorsement Product Selection ----
    page.locator(".mat-select-placeholder").click()

    # ---- Motor ----
    if product.lower() == "motor":
        page.get_by_role("option", name="Motor").click()
        print("**Performing Motor Endorsement**")

    # ---- Personal Accident ----
    elif product.lower() == "pa":
        page.get_by_role("option", name="Personal Accident").click()
        print("**Performing Personal Accident Endorsement**")

def incep_date(page):
    inception_date = page.locator("input#inceptionDate").input_value().strip()
    if inception_date:
        print("Default Inception Date: ", inception_date)
    else:
        print("Inception Date is blank, setting today's date")
        # today date
        today = datetime.today()
        # Angular Material aria-label format
        aria_date = today.strftime("%B %d, %Y").replace(" 0", " ")
        # Open calendar
        page.locator("mat-form-field").filter(has_text="Inception Date") .get_by_label("Open calendar").click()   
        # Select today
        page.get_by_role("gridcell", name=aria_date).click()
        inception_date = today.strftime("%d-%m-%Y")
        print("Inception Date: ", inception_date)

def manager_approval(manager_page):
    manager_page.get_by_role("textbox", name="Username or email").fill("arpi.ramreddy@gmail.com")
    manager_page.get_by_role("textbox", name="Password").fill("Tune@123")
    manager_page.get_by_role("button", name="Login").click()
    manager_page.wait_for_timeout(25000)
    # === Approve the quote ===
    manager_page.get_by_role("button", name="Accept & Process").click()
    print("Manager approval done")
    manager_page.wait_for_timeout(10000)
    manager_page.close()

def issue_policy(page):
        # === PROCEED TO POLICY ISSUANCE ===
        page.get_by_role("button", name="Proceed to Policy Issuance").click()

        # ==== POLICY ISSUANCE ====
        page.get_by_role("button", name="Issue Policy").click()
        print("Issue Policy button clicked")
        page.wait_for_timeout(30000)

        # ---- Wait until Policy number is released  ----
        max_wait = 100
        interval = 35
        elapsed = 0     
        policy_number = "-"

        while elapsed < max_wait:
            try:
                policy_element = page.locator("span.fw-bold").filter(has_text="Policy #:")
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

        return policy_number