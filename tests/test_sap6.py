import re
from playwright.sync_api import Playwright, sync_playwright, expect


def run(playwright: Playwright) -> None:
    browser = playwright.firefox.launch(headless=False)
    context = browser.new_context()
    page = context.new_page()
    page.goto("https://tus4appsit.tuneprotect.com:44300/sap/bc/ui2/flp#Shell-home")

    page.get_by_role("textbox", name="User").click()
    page.get_by_role("textbox", name="User").fill("BAKASH")
    page.get_by_text("User Password LanguageDE -").click()
    page.get_by_role("textbox", name="Password").click()
    page.get_by_role("textbox", name="Password").fill("Serole@123")
    page.get_by_role("button", name="Log On").click()

    page.get_by_role("link", name="New Business").click()

    page.locator("iframe[title=\"Application\"]").content_frame.get_by_role("textbox", name="Policy Start Required").click()
    page.locator("iframe[title=\"Application\"]").content_frame.get_by_role("textbox", name="Policy Start Required").fill("20.01.2026")
    
    page.locator("iframe[title=\"Application\"]").content_frame.get_by_role("textbox", name="Submission To PP Date Required").click()
    page.locator("iframe[title=\"Application\"]").content_frame.get_by_role("textbox", name="Submission To PP Date Required").fill("20.01.2026")

    page.locator("iframe[title=\"Application\"]").content_frame.get_by_role("textbox", name="Received Date Required").click()
    page.locator("iframe[title=\"Application\"]").content_frame.get_by_role("textbox", name="Received Date Required").fill("20.01.2026")

    page.locator("iframe[title=\"Application\"]").content_frame.get_by_role("textbox", name="Sales Prod.Templ.ID Required").click()
    page.locator("iframe[title=\"Application\"]").content_frame.locator("#ls-inputfieldhelpbutton").click()
    page.locator("iframe[title=\"Application\"]").content_frame.locator("[id=\"sh[15,0]#sc\"] > .urBorderBox > .urST5SCMetricInner").click()
    page.locator("iframe[title=\"Application\"]").content_frame.get_by_role("button", name="Copy").click()
    page.locator("iframe[title=\"Application\"]").content_frame.get_by_role("button", name="Create  Emphasized").click()

    page.locator("iframe[title=\"Application\"]").content_frame.locator("[id=\"M0:46:2:1:2B256:1::10:22-btn\"]").click()
    page.locator("iframe[title=\"Application\"]").content_frame.get_by_role("option", name="PA_PASA_CON Personal Accident Safe").click()

    #----- PH BP -----
    page.locator("iframe[title=\"Application\"]").content_frame.get_by_role("button", name="Detail").click()
    page.locator("iframe[title=\"Application\"]").content_frame.get_by_role("textbox", name="Business Partner Required").click()
    page.locator("iframe[title=\"Application\"]").content_frame.get_by_role("textbox", name="Business Partner Required").fill("1000024810")
    page.locator("iframe[title=\"Application\"]").content_frame.get_by_role("textbox", name="Business Partner Required").press("Enter")
    page.locator("iframe[title=\"Application\"]").content_frame.get_by_role("button", name="Copy  Emphasized").click()

    #----- Commission -----
    page.locator("iframe[title=\"Application\"]").content_frame.get_by_role("tab", name="Commission").click()
    page.locator("iframe[title=\"Application\"]").content_frame.get_by_role("button", name="Add").click()
    page.locator("iframe[title=\"Application\"]").content_frame.get_by_role("textbox", name="Comm. Contract No. :").click()
    page.locator("iframe[title=\"Application\"]").content_frame.get_by_role("textbox", name="Comm. Contract No. :").fill("2210002487")
    page.locator("iframe[title=\"Application\"]").content_frame.get_by_role("textbox", name="Comm. Contract No. :").press("Enter")
    page.locator("iframe[title=\"Application\"]").content_frame.get_by_role("button", name="Copy  Emphasized").click()

    page.locator("iframe[title=\"Application\"]").content_frame.get_by_role("button", name="Complete Business Transaction").click()

    page.locator("iframe[title=\"Application\"]").content_frame.locator("[id=\"tree#C197-mrss-cont-none-Row-2\"]").get_by_text("Personal Accident").click()
    page.locator("iframe[title=\"Application\"]").content_frame.get_by_role("button", name="Personal Accident").dblclick()

    page.locator("iframe[title=\"Application\"]").content_frame.get_by_role("cell").filter(has_text=re.compile(r"^$")).nth(5).dblclick()
    page.locator("iframe[title=\"Application\"]").content_frame.get_by_role("button", name="Personal Accident").dblclick()

    page.locator("iframe[title=\"Application\"]").content_frame.locator("[id=\"M0:46:2:1:2B256:1:3::3:77-btn\"]").click()
    page.locator("iframe[title=\"Application\"]").content_frame.get_by_role("option", name="Class 1").click()

    page.locator("iframe[title=\"Application\"]").content_frame.locator("[id=\"M0:46:2:1:2B256:1:3::11:12-btn\"]").click()
    page.locator("iframe[title=\"Application\"]").content_frame.get_by_role("option", name="001").click()
    page.locator("iframe[title=\"Application\"]").content_frame.get_by_role("button", name="Complete Business Transaction").click()

    
    page.locator("iframe[title=\"Application\"]").content_frame.get_by_title("Expand Node").click()

    page.locator("iframe[title=\"Application\"]").content_frame.get_by_text("Renewal Bonus").click()
    page.locator("iframe[title=\"Application\"]").content_frame.get_by_role("button", name="Renewal Bonus").dblclick()

    page.locator("iframe[title=\"Application\"]").content_frame.get_by_text("Personal Liability").click()
    page.locator("iframe[title=\"Application\"]").content_frame.get_by_role("button", name="Personal Liability").dblclick()

    page.locator("iframe[title=\"Application\"]").content_frame.get_by_role("button", name="Check").click()

    page.locator("iframe[title=\"Application\"]").content_frame.get_by_role("button", name="Calculate Application").click()

    page.locator("iframe[title=\"Application\"]").content_frame.get_by_role("button", name="Release Application").click()

    page.locator("iframe[title=\"Application\"]").content_frame.get_by_role("button", name="Continue Release").click()

    page.locator("iframe[title=\"Application\"]").content_frame.get_by_role("button", name="Continue Release").click()



with sync_playwright() as playwright:
    run(playwright)
