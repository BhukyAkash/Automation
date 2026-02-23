from conftest import page
from excel_utils import get_vehicle_data
from datetime import datetime

from base_login import login, navigation


def test_tipuat_motor(page):

    login(page)

    #----- NAVIGATION ----
    page.get_by_text("request_quote QMS Quotation").click()
    page.get_by_role("button", name="New Quote").click()
    page.get_by_role("heading", name="Motor").click()
    page.get_by_role("heading", name="Reg. Commercial Vehicle").click()
    page.get_by_role("button", name="Next").click()
    page.get_by_role("textbox").click()

    # ========= FIRST SCREEN ===========
    
    # ---- VEHICLE REG ----
    vehicle_data = get_vehicle_data()
    page.get_by_role("textbox").first.fill(vehicle_data["vehicle_reg_no"])

    #---- Place of Use ----
    page.locator(".mat-select-placeholder").click()
    page.get_by_role("option", name="Johor").click()

    #---- Vehicle Search ----
    page.get_by_role("button", name="search Vehicle Search").click()
