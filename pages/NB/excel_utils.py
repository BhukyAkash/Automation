from openpyxl import load_workbook
import os

CURRENT_DIR = os.path.dirname(__file__)
EXCEL_PATH = os.path.join(CURRENT_DIR, "STPTestData.xlsx")

def get_vehicle_data(vehicle_type):
    wb = load_workbook(EXCEL_PATH)
    sheet = wb.active

    cell_map = {
        "CV": ("A21", "B21"),
        "MC": ("I28", "J28"),
        "PC": ("E2", "F2"),
    }

    reg_cell, mykad_cell = cell_map[vehicle_type]

    return {
        "vehicle_reg_no": sheet[reg_cell].value,
        "mykad": sheet[mykad_cell].value
    }
