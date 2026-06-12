def extension(page,coverage_type):

    print("======== Extension Coverage Selection ========")
    page.get_by_role("button", name="Extension Coverage").click()

    # --- Package Type Selection ----
    page.get_by_text("NAPackage Type").click()
    page.wait_for_timeout(1000)
    page.get_by_role("option", name="Autobuddy").click()
    page.wait_for_timeout(1000)
    # --- Selected Package type ----
    selected_package = page.locator("#mat-select-value-11 span.mat-select-min-line").inner_text()
    print("Selected Package:", selected_package)

    if "Autobuddy" in selected_package:
        page.locator(".mat-select-placeholder").first.click()
        page.get_by_role("option", name="PLAN A").click()

    else:
        print("Autobuddy not selected → skipping PLAN selection")

    # ---- Comprehensive ----
    if coverage_type == "Comprehensive":
        extensions = [
            "check All Drivers",
            "Windscreen Damage",
            "Inclusion of Special Perils",
            "Legal Liability to Passenger (LLP)",
            "Legal Liability to Third Party caused by Passenger",
            "Strike Riot and Civil Commotions",
            "Ferry Transit to and / or from Sabah and Labuan"
        ]

    # ---- TPFT ----
    elif coverage_type == "TP, Fire & Theft":
        extensions = [
            "Legal Liability to Passenger (LLP)",
            "Legal Liability to Third Party caused by Passenger"
        ]

    for extension_name in extensions:
        page.locator("span").filter(has_text=extension_name).get_by_role("button").click()

        if extension_name == "Windscreen Damage":
            page.locator("mat-form-field").filter(has_text="Sum Insured *MYR").locator("#sumInsured").fill("800")

        elif extension_name == "Inclusion of Special Perils":
            page.get_by_label("Extension Coverage").get_by_text("Vehicle Sum Insured",exact=True).click()

        print(f"{extension_name} selected successfully")



















    # # ======== Comprehensive ========
    # page.wait_for_timeout(2000)
    # extension_selected = "check All Drivers" 
    # page.locator("span").filter(has_text=extension_selected).get_by_role("button").click()
    # print(f"{extension_selected} selected successfully")

    # extension_selected = "Windscreen Damage" 
    # page.locator("span").filter(has_text=extension_selected).get_by_role("button").click()
    # page.locator("mat-form-field").filter(has_text="Sum Insured *MYR").locator("#sumInsured").fill("800")
    # print(f"{extension_selected} selected successfully")

    # extension_selected = "Inclusion of Special Perils"
    # page.locator("span").filter(has_text=extension_selected).get_by_role("button").click()
    # page.get_by_label("Extension Coverage").get_by_text("Vehicle Sum Insured", exact=True).click()
    # print(f"{extension_selected} selected successfully")

    # extension_selected = "Legal Liability to Passenger (LLP)"
    # page.locator("span").filter(has_text=extension_selected).get_by_role("button").click()
    # print(f"{extension_selected} selected successfully")

    # extension_selected = "Legal Liability to Third Party caused by Passenger"
    # page.locator("span").filter(has_text=extension_selected).get_by_role("button").click()
    # print(f"{extension_selected} selected successfully")

    # extension_selected = "Strike Riot and Civil Commotions" 
    # page.locator("span").filter(has_text=extension_selected).get_by_role("button").click()
    # print(f"{extension_selected} selected successfully")

    # extension_selected = "Ferry Transit to and / or from Sabah and Labuan" 
    # page.locator("span").filter(has_text=extension_selected).get_by_role("button").click()
    # print(f"{extension_selected} selected successfully")


    # # ========= TPFT ==========

    # # page.locator("span").filter(has_text="check Legal Liability to Passenger (LLP)").get_by_role("button").click()
    # # print("LLP selected successfully")

    # # page.locator("span").filter(has_text="Legal Liability to Third Party caused by Passenger").get_by_role("button").click()
    # # print("LLTP selected successfully")
