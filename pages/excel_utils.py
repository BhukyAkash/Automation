from openpyxl import load_workbook
import os

CURRENT_DIR = os.path.dirname(__file__)
EXCEL_PATH = os.path.join(CURRENT_DIR, "STPTestData.xlsx")

def get_vehicle_data():
    wb = load_workbook(EXCEL_PATH)
    sheet = wb.active

    data = {
        "vehicle_reg_no": sheet["A6"].value,
        "mykad": sheet["B6"].value
    
    }
    return data
