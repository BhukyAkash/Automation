import re
from datetime import datetime

def login(page):
    page.goto("https://agent-uat.tuneinsurance.com/")
    username = "playwright.test@serole.com" #"vijaykumar.likki@serole.com"        # 
    page.get_by_role("textbox", name="Username or email").fill(username)
    page.get_by_role("textbox", name="Password").fill("Serole@321")
    page.get_by_role("button", name="Login").click()
    print("Logged into: ", username)
    return username

def navigation(page):
    page.get_by_text("request_quote QMS Quotation").click()
    page.get_by_role("button", name="New Quote").click()
    page.wait_for_timeout(2000)
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

def navi_dental(page):
    page.get_by_text("request_quote QMS Quotation").click()
    page.get_by_role("button", name="New Quote").click()
    page.get_by_role("heading",name="Personal Accident, Travel & Health").click()
    page.get_by_role("heading",name="Dental Shield").click()
    page.get_by_role("button",name="Next").click()

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

def start_date(page):
    # today date
    today = datetime.today()
    # Angular Material aria-label format
    aria_date = today.strftime("%B %d, %Y").replace(" 0", " ")
    # Open calendar
    page.locator("mat-form-field").filter(has_text="Start Date").get_by_label("Open calendar").click()   
    # Select today
    page.get_by_role("gridcell", name=aria_date).click()
    inception_date = today.strftime("%d-%m-%Y")
    print("Inception Date: ", inception_date)

def manager_approval(manager_page):
    manager_page.get_by_role("textbox", name="Username or email").fill("rahul@serole.com")
    manager_page.get_by_role("textbox", name="Password").fill("Serole@123")
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

# ---- Premiums -----
def extract_myr(text: str) -> float:
    is_negative = "-" in text
    match = re.search(r"[\d,]+\.?\d*", text)
    value = float(match.group().replace(",", "")) if match else 0.0
    return -value if is_negative else value

def motor_prem(page):

    # ---- Premiums ----
    sum_insured1 = page.locator("li").filter(has_text="Vehicle Sum Insured").locator(".summary-result-value").inner_text().strip()
    sum_insured = extract_myr(sum_insured1)
    print("\nSum Insured:", sum_insured)

    ap = page.locator("li").filter(has_text="Act Premium").locator(".summary-result-value").inner_text().strip()
    act_prem = extract_myr(ap)
    print("Act Premium:", act_prem)

    bp = page.locator("li").filter(has_text="Basic Premium").locator(".summary-result-value").inner_text().strip()
    basic_prem = extract_myr(bp)
    print("Basic Premium:", basic_prem)

    ncd_value = page.locator("(//li[contains(.,'NCD')]//span[contains(@class,'summary-result-value')])[1]").inner_text().strip()
    ncd = extract_myr(ncd_value)
    print("NCD Premium:", ncd)

    ncd_after = page.locator("li").filter(has_text="Premium after NCD").locator(".summary-result-value").inner_text().strip()
    after_ncd = extract_myr(ncd_after)
    print("Premium after NCD:", after_ncd)

    gp = page.locator("li").filter(has_text="Gross Premium").locator(".summary-result-value").inner_text().strip()
    gross_premium = extract_myr(gp)
    print("Gross Premium:", gross_premium)

    tax = page.locator("li").filter(has_text="SST").locator(".summary-result-value").inner_text().strip()
    sst = extract_myr(tax)
    print("SST:", sst)

    sd = page.locator("li").filter(has_text="Stamp Duty").locator(".summary-result-value").inner_text().strip()
    stamp_duty = extract_myr(sd)
    print("Stamp Duty:", stamp_duty)

    total_payable = page.locator("div").filter(has_text="Total Payable Premium").locator(".final-amount").inner_text().strip()
    total = extract_myr(total_payable)
    print("Total Premium:", total)

    return sum_insured, act_prem, basic_prem, ncd, after_ncd, gross_premium, sst, stamp_duty, total

def pa_prem(page):
    value = page.locator("li").filter(has_text="Sum Insured").locator(".summary-result-value").inner_text().strip()
    sum_insured = extract_myr(value)
    print("\nSum Insured:", sum_insured)

    gp = page.locator("li").filter(has_text="Gross Premium").locator(".summary-result-value").inner_text().strip()
    gross_premium = extract_myr(gp)
    print("Gross Premium:", gross_premium)

    try:
        re = page.locator("li").filter(has_text="Rebate").locator(".summary-result-value").inner_text().strip()
        rebate = extract_myr(re)
        print("Rebate:", rebate)
    except:
        rebate = None  
        print("No Rebate")

    tax = page.locator("li").filter(has_text="SST").locator(".summary-result-value").inner_text().strip()
    sst = extract_myr(tax)
    print("SST:", sst)

    sd = page.locator("li").filter(has_text="Stamp Duty").locator(".summary-result-value").inner_text().strip()
    stamp_duty = extract_myr(sd)
    print("Stamp Duty:", stamp_duty)

    total_payable = page.locator("div").filter(has_text="Total Payable Premium").locator(".final-amount").inner_text().strip()
    total = extract_myr(total_payable)
    print("Total Premium:", total)

    return sum_insured, gross_premium, rebate, sst, stamp_duty, total

def dental_prem(page):
    gp = page.locator("li").filter(has_text="Gross Premium").locator(".summary-result-value").inner_text().strip()
    gross_premium = extract_myr(gp)
    print("Gross Premium:", gross_premium)

    re = page.locator("li").filter(has_text="Rebate").locator(".summary-result-value").inner_text().strip()
    rebate = extract_myr(re)
    print("Rebate:", rebate)

    tax = page.locator("li").filter(has_text="SST").locator(".summary-result-value").inner_text().strip()
    sst = extract_myr(tax)
    print("SST:", sst)

    sd = page.locator("li").filter(has_text="Stamp Duty").locator(".summary-result-value").inner_text().strip()
    stamp_duty = extract_myr(sd)
    print("Stamp Duty:", stamp_duty)

    total_payable = page.locator("div").filter(has_text="Total Payable Premium").locator(".final-amount").inner_text().strip()
    total = extract_myr(total_payable)
    print("Total Premium:", total)

    return gross_premium, rebate, sst, stamp_duty, total 