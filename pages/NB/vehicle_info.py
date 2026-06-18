VEHICLE_INFO = {
    "PC": {
        # ---- Vehicle Search ----
        "place_of_use": "Melaka",

        # ---- Make / Model / Year ----
        "change_vehicle": False,
        "make": "BMW",
        "model": "M4",
        "year": "2020",

        # ---- Capacities ----
        "engine_capacity": "1200",
        "seating_capacity": "2",

        # ---- Coverage ----
        "change_coverage": False,
        "coverage_type": "Comprehensive",  # "Comprehensive" or "TP, Fire & Theft"
    }
}


def get_vehicle_info(vehicle_type: str) -> dict:
    if vehicle_type not in VEHICLE_INFO:
        raise KeyError(
            f"Vehicle type '{vehicle_type}' not found. "
            f"Valid types: {list(VEHICLE_INFO.keys())}"
        )
    return VEHICLE_INFO[vehicle_type]