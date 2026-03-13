from datetime import datetime
from base_login import login, navi_pa

def test_PA(page):

    try:

        login(page)
        navi_pa(page)


        # ========= FIRST SCREEN ===========

        page.locator("#dx-input-0").nth(1).click()
        page.locator("#dx-input-0").nth(1).fill("980506-12-1232")

        page.locator("#dx-input-1").nth(1).click()
        page.locator("#dx-input-1").nth(1).fill("PERSONAL ACCIDENT")

        page.locator(".mat-select-placeholder").first.click()
        page.get_by_role("option", name="Class 1").click()

        page.locator(".mat-select-placeholder").click()
        page.get_by_role("option", name="100,000").click()

        page.locator("#mat-radio-9 > .mat-radio-label > .mat-radio-container > .mat-radio-outer-circle").click()

        page.locator("#dx-checkbox-1 > .mat-checkbox-layout > .mat-checkbox-inner-container").click()

        page.get_by_role("button", name="Save & Next").click()

        #page.get_by_role("button", name="Yes").first.click()

        page.get_by_role("textbox", name="123456789").click()
        page.get_by_role("textbox", name="123456789").fill("98765432")

        page.get_by_role("textbox", name="Enter").click()
        page.get_by_role("textbox", name="Enter").fill("akash@serole.com")

        page.locator("#mat-radio-16-input").check()
        page.locator("#mat-radio-18-input").check()
        page.locator("#mat-radio-20-input").check()
        page.locator("#mat-radio-22-input").check()
        page.locator("#mat-radio-24-input").check()
        page.locator("#dx-checkbox-8 > .mat-checkbox-layout > .mat-checkbox-inner-container").click()
        page.get_by_role("button", name="Generate Quote").click()



    finally:
        page.get_by_text("playwright", exact=True).click()
        page.get_by_text("Sign Out", exact=True).click()
        page.wait_for_timeout(15000)