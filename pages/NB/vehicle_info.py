VEHICLE_INFO = {
    "PC": {
        # ---- Vehicle Search ----
        "place_of_use": "Melaka",

        # ---- Make / Model / Year ----
        "change_vehicle": True,
        "make": "BMW",
        "model": "M4",
        "year": "2020",

        # ---- Capacities ----
        "engine_capacity": "1200",
        "seating_capacity": "2",

        # ---- Coverage ----
        "change_coverage": True,
        "coverage_type": "TP, Fire & Theft",  # "Comprehensive" or "TP, Fire & Theft"
    },
    "MC": {
        # ---- Vehicle Search ----
        "place_of_use": "Melaka",

        # ---- Make / Model / Year ----
        "change_vehicle": True,
        "make": "HONDA",
        "model": "SL",
        "year": "2020",

        # ---- Capacities ----
        "engine_capacity": "125",
        "seating_capacity": "2",

        # ---- Coverage ----
        "change_coverage": False,
        "coverage_type": "Comprehensive",  # "Comprehensive" or "TP, Fire & Theft"
    },
    "CV": {
        # ---- Vehicle Search ----
        "place_of_use": "Melaka",

        # ---- Vehicle Class / Use ----
        "vehicle_class": "Commercial Vehicle",
        "vehicle_use": "C permit",

        # ---- Engine / Chassis ----
        "engine_no": "63547",
        "chassis_no": "34576657",

        # ---- Make / Model / Year ----
        "make": "VOLVO",
        "model": "F16",
        "year": "2015",
        "variant": "NA",

        # ---- Capacities ----
        "engine_capacity": "1200",
        "seating_capacity": "5",
        "carrying_capacity": "20",
        "carrying_capacity_unit": "Tonnes",  # "Tonnes" or "Kg"

        # ---- Carriage Goods ----
        "carriage_goods": "Beverages Bottles",

        # ---- Coverage ----
        "change_coverage": True,
        "coverage_type": "TP, Fire & Theft",  # "Comprehensive" or "TP, Fire & Theft"

        # --- Sum Insured ---
        "sum_insured": "25000"
    }
}


def get_vehicle_info(vehicle_type: str) -> dict:
    if vehicle_type not in VEHICLE_INFO:
        raise KeyError(
            f"Vehicle type '{vehicle_type}' not found. "
            f"Valid types: {list(VEHICLE_INFO.keys())}"
        )
    return VEHICLE_INFO[vehicle_type]


AUTOMATION_FLAGS = {

    "MC": {
        "explore_extensions":   True,   # Click on Extension Coverage button?
        "select_autobuddy":     False,   # Select Motorcyclist PA Contract?
        "select_extensions":    False,   # Select individual extensions?
    },

    "PC": {
        "explore_extensions":   True,   # Click on Extension Coverage button?
        "select_autobuddy":     False,  # Select Autobuddy package?
        "select_extensions":    False,   # Select individual extensions?
    },

    "CV": {
        "explore_extensions":   True,  # Click on Extension Coverage button?
        "select_autobuddy":     False,  # Select Motorist PA package?
        "select_extensions":    False,  # Select individual extensions?
    },
}