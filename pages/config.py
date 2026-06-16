# ============================================================
#  config.py — D:\Automation\pages\config.py
#  Set True/False before each run
# ============================================================

AUTOMATION_FLAGS = {

    "MC": {
        "explore_extensions":   True,   # Click on Extension Coverage button?
        "select_autobuddy":     True,   # Select Motorcyclist PA Contract?
        "select_extensions":    True,   # Select individual extensions?
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