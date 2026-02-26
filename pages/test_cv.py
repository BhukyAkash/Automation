from conftest import page
from excel_utils import get_vehicle_data
from datetime import datetime

from base_login import login, navigation


def test_tipuat_motor(page):

    login(page)
    navigation(page)


    # ========= FIRST SCREEN ===========
    
    # ---- VEHICLE REG ----
    vehicle_data = get_vehicle_data()
    page.get_by_role("textbox").first.fill(vehicle_data["vehicle_reg_no"])

    #---- Place of Use ----
    page.locator(".mat-select-placeholder").click()
    page.get_by_role("option", name="Johor").click()

    #---- Vehicle Search ----
    page.get_by_role("button", name="search Vehicle Search").click()

    page.locator(".mat-select-placeholder").first.click()
    page.get_by_role("option", name="Commercial Vehicle").click()

    page.locator(".mat-select-placeholder").first.click()
    page.get_by_role("option", name="C permit").click()

    page.locator("mat-form-field").filter(has_text="Engine # *").locator("#engineNo").fill("63547")
    #page.locator("mat-form-field").filter(has_text="Engine # *").locator("#engineNo").fill("63547")

    page.locator("mat-form-field").filter(has_text="Chassis # *").locator("#chassisNo").fill("34576657")
    #page.locator("mat-form-field").filter(has_text="Chassis # *").locator("#chassisNo").fill("34576657")



    page.locator("mat-form-field", has_text="Make").click()
    page.get_by_role("option", name="VOLVO").click()
    
    page.locator(".mat-select-placeholder.mat-select-min-line.ng-tns-c176-72").click()
    page.get_by_role("option", name="F16").click()

    page.locator(".mat-select-placeholder.mat-select-min-line.ng-tns-c176-74").click()
    page.get_by_role("option", name="2016").click()

    page.locator(".mat-select-placeholder.mat-select-min-line.ng-tns-c176-76").click()
    page.get_by_role("option", name="NA").click()


    page.locator("mat-form-field").filter(has_text="Seating Capacity *").locator("#seatCapacity").fill("5")
    #page.locator("mat-form-field").filter(has_text="Seating Capacity *").locator("#seatCapacity").fill("5")

    page.locator("mat-form-field").filter(has_text="Carrying Capacity *").locator("#carryingCapacity").fill("11")
    #page.locator("mat-form-field").filter(has_text="Carrying Capacity *").locator("#carryingCapacity").fill("11")


    page.locator(".mat-select-placeholder.mat-select-min-line.ng-tns-c176-84").click()
    page.get_by_role("option", name="Tonnes").click()

    page.locator(".mat-select-placeholder.mat-select-min-line.ng-tns-c176-86").click()
    page.get_by_role("option", name="Beverages Bottles").click()

    page.get_by_role("button", name="Save Vehicle Info").click()

    page.locator("#mat-select-value-31").click()
    page.get_by_role("option", name="Comprehensive").click()

    
    page.pause()

    page.get_by_role("region", name="Coverage").locator("input[type=\"text\"]").click()
    page.get_by_role("region", name="Coverage").locator("input[type=\"text\"]").fill("15000")

    '''page.locator("dx-input").filter(has_text="* Business Registration # *").locator("#id").click()
    page.locator("dx-input").filter(has_text="* Business Registration # *").locator("#id").fill("54375347")'''

    page.locator("mat-form-field").filter(has_text="Business Registration # *").locator("#id").fill(vehicle_data["mykad"])

    page.locator("dx-input").filter(has_text="* Name as per ID / Legal Name").locator("#legalName").click()
    page.locator("dx-input").filter(has_text="* Name as per ID / Legal Name").locator("#legalName").fill("CV C")
    
    page.get_by_role("button", name="search Validate Owner as per").click()

