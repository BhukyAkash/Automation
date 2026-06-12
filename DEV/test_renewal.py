from base_login import login, renewal

def test_renewal(page):
    try:
        login(page)
        renewal(page)

        # fields = page.locator("mat-form-field")
        # for i in range(fields.count()):
        #     print(i, fields.nth(i).inner_text())
        policy_field = page.locator("mat-form-field", has=page.locator("dx-label:text-is('Policy #')"))
        policy_field.locator("input").fill("4020001221")
        page.get_by_role("button", name="search Search Policy").click()


    finally:
        page.get_by_text("Murali Mohan", exact=True).click()
        page.get_by_text("Sign Out", exact=True).click()
        page.wait_for_timeout(15000) 