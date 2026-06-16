import os
from datetime import datetime
from openpyxl import Workbook, load_workbook

CURRENT_DIR = os.path.dirname(__file__)
EXCEL_PATH = os.path.join(CURRENT_DIR, "STPTestData.xlsx")
BASE_DIR = os.path.join(os.path.dirname(__file__), "..")
DOWNLOADS_DIR = os.path.join(os.path.dirname(__file__), "downloads")

# ==== Input of Motor Test Data ======
def get_vehicle_data(vehicle_type):
    wb = load_workbook(EXCEL_PATH)
    sheet = wb.active

    cell_map = {
        "CV": ("A21", "B21"),
        "MC": ("J38", "K38"),
        "PC": ("E26", "F26"),
    }

    reg_cell, mykad_cell = cell_map[vehicle_type]

    return {
        "vehicle_reg_no": sheet[reg_cell].value,
        "mykad": sheet[mykad_cell].value
    }

# ==== Input: PA Test Data (Sheet 2 - "PA") ======
def get_pa_data(row=2):
    wb = load_workbook(EXCEL_PATH)
    ws = wb["PA"]

    pa_product     = ws.cell(row=row, column=3).value  # Column C
    occupation_cls = ws.cell(row=row, column=4).value  # Column D
    sum_insured    = ws.cell(row=row, column=5).value  # Column E

    # Normalize product name — Excel has "PA shield", UI expects "PA Shield"
    product_map = {
        "pa shield":               "PA Shield",
        "personal accident safe":  "Personal Accident Safe",
        "personal accident shield": "PA Shield",
    }
    if pa_product:
        pa_product = product_map.get(pa_product.strip().lower(), pa_product.strip())

    # Normalize sum insured — ensure it's a string like "200,000"
    if isinstance(sum_insured, (int, float)):
        sum_insured = f"{int(sum_insured):,}"
    elif sum_insured:
        sum_insured = str(sum_insured).strip()

    return {
        "pa_product":     pa_product,
        "occupation_cls": occupation_cls.strip() if occupation_cls else None,
        "sum_insured":    sum_insured,
    }

# ==== Core Excel Writer (internal use only) ======
def _write_to_excel(policy_type, registration, coverage_label, quote_number, policy_number,
                    sum_insured=None, act_prem=None, basic_prem=None, ncd=None,
                    after_ncd=None, gross_premium=None, sst=None, stamp_duty=None, total=None):
    file_path = os.path.join(BASE_DIR, "UATStability.xlsx")

    wb = load_workbook(file_path) if os.path.exists(file_path) else Workbook()
    ws = wb.active

    # ---- Find next empty row based on Column C (NV/RV) ----
    row = 2
    while ws.cell(row=row, column=3).value:
        row += 1

    # ---- Serial Number in Column A ----
    prev_serial = ws.cell(row=row - 1, column=1).value if row > 2 else 0
    serial_no = (prev_serial or 0) + 1

    # ---- Write data ----
    ws.cell(row=row, column=1).value = serial_no
    ws.cell(row=row, column=3).value = registration
    ws.cell(row=row, column=4).value = policy_type
    ws.cell(row=row, column=5).value = coverage_label
    ws.cell(row=row, column=6).value = quote_number
    ws.cell(row=row, column=7).value = policy_number
    ws.cell(row=row, column=8).value = datetime.today().strftime("%d-%m-%Y")

    # ---- Premiums (I to Q) ----
    ws.cell(row=row, column=9).value = sum_insured    # I - Sum Insured
    ws.cell(row=row, column=10).value = act_prem      # J - Act Premium
    ws.cell(row=row, column=11).value = basic_prem    # K - Basic Premium
    ws.cell(row=row, column=12).value = ncd           # L - NCD
    ws.cell(row=row, column=13).value = after_ncd     # M - After NCD
    ws.cell(row=row, column=14).value = gross_premium # N - Gross Premium
    ws.cell(row=row, column=15).value = sst           # O - SST
    ws.cell(row=row, column=16).value = stamp_duty    # P - Stamp Duty
    ws.cell(row=row, column=17).value = total         # Q - Total Premium

    # ---- Auto-fill Column B, R & S from previous row ----
    if row > 2:
        for col in [2, 18, 19]:
            prev_val = ws.cell(row=row - 1, column=col).value
            if prev_val:
                ws.cell(row=row, column=col).value = prev_val

    wb.save(file_path)
    print("In Excel, Quote and Policy numbers captured successfully")


# ==== Output Functions (unchanged names) ======

def pa_excel(selected_title, quote_number, policy_number,sum_insured, 
            gross_premium, sst, stamp_duty, total):
    _write_to_excel("PA", "NV", selected_title, quote_number, policy_number,
                    sum_insured=sum_insured, act_prem="-", basic_prem="-", ncd="-", after_ncd="-",
                    gross_premium=gross_premium, sst=sst, stamp_duty=stamp_duty, total=total)

def dental(quote_number, policy_number):
    _write_to_excel("Dental", "NV", "Dental Shield", quote_number, policy_number)

def mc_excel(selected_coverage, quote_number, policy_number,
            sum_insured, act_prem, basic_prem, ncd,
            after_ncd, gross_premium, sst, stamp_duty, total):
    _write_to_excel("MC", "RV", selected_coverage, quote_number, policy_number,
                    sum_insured, act_prem, basic_prem, ncd,
                    after_ncd, gross_premium, sst, stamp_duty, total)

def pc_excel(selected_coverage, quote_number, policy_number,
            sum_insured, act_prem, basic_prem, ncd,
            after_ncd, gross_premium, sst, stamp_duty, total):
    _write_to_excel("PC", "RV", selected_coverage, quote_number, policy_number,
                    sum_insured, act_prem, basic_prem, ncd,
                    after_ncd, gross_premium, sst, stamp_duty, total)

def cv_excel(selected_coverage, quote_number, policy_number,
            sum_insured, act_prem, basic_prem, ncd,
            after_ncd, gross_premium, sst, stamp_duty, total):
    _write_to_excel("CV", "RV", selected_coverage, quote_number, policy_number,
                    sum_insured, act_prem, basic_prem, ncd,
                    after_ncd, gross_premium, sst, stamp_duty, total)
