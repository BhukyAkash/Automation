from popup_utils import ask_popup

# ------ PC Extensions ------
def pc_extension(page,coverage_type):

    page.get_by_role("button", name="Extension Coverage").click()

    # --- Package Type Selection ----
    autobuddy = ask_popup("Do you want to select Autobuddy package?", title="PC Extensions")
    if autobuddy == "yes":
        page.get_by_text("NAPackage Type").click()
        page.wait_for_timeout(1000)
        page.get_by_role("option", name="Autobuddy").click()
        page.wait_for_timeout(1000)
        # --- Selected Package type ----
        selected_package = page.locator("#mat-select-value-11 span.mat-select-min-line").inner_text()
        print("Selected Package:", selected_package)

        if "Autobuddy" in selected_package:
            page.locator(".mat-select-placeholder").first.click()
            plan = "PLAN A"
            page.get_by_role("option", name=plan).click()
        else:
            print("Autobuddy not selected → skipping PLAN selection")
        print("Plan Type:", plan)
    else:
        print("No Autobuddy package selected")

    # ---- Comprehensive ----
    extension_select = ask_popup("Do you want to select extensions?", title="PC Extensions")
    if extension_select == "yes":
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

    else:
        print("No extensions selected")

# ------ MC Extensions ------
def mc_extension(page, coverage_type):
    page.get_by_role("button", name="Extension Coverage").click()

    # --- Package Type Selection ----
    autobuddy = ask_popup("Do you want to select Motorcyclist PA Contract?", title="MC Multi Contract")
    if autobuddy == "yes":
        page.get_by_text("NAPackage Type").click()
        page.wait_for_timeout(1000)
        page.get_by_role("option", name="Motorcyclist PA").click()
        page.wait_for_timeout(1000)
        # --- Selected Package type ----
        selected_package = page.locator("#mat-select-value-11 span.mat-select-min-line").inner_text()
        print("Selected Package:", selected_package)

        if "Motorcyclist PA" in selected_package:
            page.locator(".mat-select-placeholder").first.click()
            plan = "PLAN A"
            page.get_by_role("option", name=plan).click()
        else:
            print("Motorcyclist PA not selected → skipping PLAN selection")
        print("Plan Type:", plan)
    else:
        print("MPA Contract not selected")

    # ---- Comprehensive ----
    extension_select = ask_popup("Do you want to select extensions?", title="MC Extensions")
    if extension_select == "yes":
        if coverage_type == "Comprehensive":
            extensions = [
                "All Riders",
                "Inclusion of Special Perils",
                "Legal Liability to Pillion",
                "Accessories fixed to motorcycle",
                "Ferry Transit to and / or from Sabah and Labuan",
                "Strike Riot and Civil Commotion",                
            ]

        # ---- TPL ----
        elif coverage_type == "Third Party":
            extensions = [
                "All Riders",               
            ]

        for extension_name in extensions:
            page.locator("span").filter(has_text=extension_name).get_by_role("button").click()

            if extension_name == "Accessories fixed to motorcycle":
                container = page.locator(".additional-benefit-wrapper").filter(has_text=extension_name)
                container.locator("input#sumInsured").fill("800")

            print(f"{extension_name} selected successfully")

    else:
        print("No extensions selected")

# ------ CV Extensions ----
def cv_extension(page, coverage_type):
    page.get_by_role("button", name="Extension Coverage").click()

    # --- Package Type Selection ----
    autobuddy = ask_popup("Do you want to select Motorist PA package?", title="PC Extensions")
    if autobuddy == "yes":
        page.get_by_text("NAPackage Type").click()
        page.wait_for_timeout(1000)
        page.get_by_role("option", name="Motorist PA").click()
        page.wait_for_timeout(1000)
        # --- Selected Package type ----
        selected_package = page.locator("#mat-select-value-11 span.mat-select-min-line").inner_text()
        print("Selected Package:", selected_package)

        if "Motorist PA" in selected_package:
            page.locator(".mat-select-placeholder").first.click()
            plan = "PLAN D"
            page.get_by_role("option", name=plan).click()
        else:
            print("Motorist PA not selected → skipping PLAN selection")
        print("Plan Type:", plan)
    else:
        print("Motorist PA package is not selected")

    # ---- Comprehensive ----
    extension_select = ask_popup("Do you want to select extensions?", title="PC Extensions")
    if extension_select == "yes":
        if coverage_type == "Comprehensive":
            extensions = [                
                "Windscreen Damage",
                "Strike riot and civil commotion",
                "Ferry Transit to and / or from Sabah and Labuan"
                "Inclusion of Special Perils",
                "Passenger Risk",
                "Passenger Risk-Employees of the Insured-good carrying vehicle only",
            ]

        # ---- TPFT ----
        elif coverage_type == "TP, Fire & Theft":
            extensions = [
                "Passenger Risk",
                "Passenger Risk-Employees of the Insured-good carrying vehicle only",
            ]

        # --- TPL ----
        elif coverage_type == "TP, Fire & Theft":
            extensions = [
                "Passenger Risk",
                "Passenger Risk-Employees of the Insured-good carrying vehicle only",
            ]

        for extension_name in extensions:
            page.locator("span").filter(has_text=extension_name).get_by_role("button").click()

            if extension_name == "Windscreen Damage":
                page.locator("mat-form-field").filter(has_text="Sum Insured").locator("#sumInsured").fill("800")

            print(f"{extension_name} selected successfully")

    else:
        print("No extensions selected")