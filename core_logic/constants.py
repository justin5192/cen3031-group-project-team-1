# ==============================================================================
# FILE 1: core_logic/constants.py
# ==============================================================================
"""
All constants and configuration values for the CarbonTracker application.
"""

# --- Emission Factors (kg CO2e per unit) ---
TRANSPORT_FACTORS = {
    "Car - Small Gasoline (Miles)": 0.350,
    "Car - SUV/Truck (Miles)": 0.550,
    "Air - Domestic (Miles)": 0.25,
    "Air - International (Miles)": 0.195,
    "Bus - Local (Miles)": 0.089,
    "Train - Commuter (Miles)": 0.040,
    "Taxi - Avg (Miles)": 0.404,
    "Motorcycle (Miles)": 0.210,
}

FOOD_FACTORS = {
    "Red Meat - Beef (Servings)": 7.0,
    "Red Meat - Lamb (Servings)": 5.5,
    "Poultry - Chicken (Servings)": 2.0,
    "Poultry - Turkey (Servings)": 2.5,
    "Fish - Farmed (Servings)": 3.0,
    "Fish - Wild Caught (Servings)": 1.5,
    "Plant Protein - Beans (Servings)": 0.4,
    "Plant Protein - Tofu (Servings)": 0.5,
    "Dairy - Milk (Servings)": 1.5,
    "Dairy - Cheese (Servings)": 2.0,
}

ENERGY_FACTORS = {
    "Electricity - US Avg (kWh)": 0.42,
    "Electricity - Coal Heavy (kWh)": 0.90,
    "Electricity - Renewable (kWh)": 0.05,
    "Natural Gas (Therms)": 5.31,
    "Heating Oil (Gallons)": 10.13,
    "Propane (Gallons)": 5.75,
}

WASTE_FACTORS = {
    "Trash - Landfill (Pounds)": 0.45,
    "Recycling - Mixed (Pounds)": 0.10,
    "Compost (Pounds)": 0.05,
}

# Main category labels for UI
MAIN_CATEGORIES = {
    "Transportation": TRANSPORT_FACTORS,
    "Food": FOOD_FACTORS,
    "Energy": ENERGY_FACTORS,
    "Waste": WASTE_FACTORS,
}

# Category mapping for tips
CATEGORY_MAPPING = {
    "Transportation": "Transportation",
    "Energy": "Home Energy",
    "Food": "Food",
    "Waste": "Waste"
}

# Default values
DEFAULT_WEEKLY_GOAL = 100.0  # kg CO2e per week
DEFAULT_DAILY_GOAL = 14.3    # kg CO2e per day (100/7)

