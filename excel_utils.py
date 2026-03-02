from openpyxl import load_workbook
import os

CURRENT_DIR = os.path.dirname(__file__)
EXCEL_PATH = os.path.join(CURRENT_DIR, "STPTestData.xlsx")

def get_vehicle_data(vehicle_type):
    wb = load_workbook(EXCEL_PATH)
    sheet = wb.active

    cell_map = {
        "CV": ("A17", "B17"),
        "MC": ("A18", "B18"),
        "PC": ("A6", "B7"),
    }

    reg_cell, mykad_cell = cell_map[vehicle_type]

    return {
        "vehicle_reg_no": sheet[reg_cell].value,
        "mykad": sheet[mykad_cell].value
    }
