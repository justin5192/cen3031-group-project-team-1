# core_logic/constants.py

# PBI 4.1: Define and hardcode simple carbon conversion constants.
# Units: All output values are in kilograms of CO2 equivalent (kg CO2e)

# --- Transportation Factors (kg CO2e per mile) ---
TRANSPORT_FACTORS = {
    "car_gasoline_avg": 0.404,  # average US passenger vehicle
    "bus_local": 0.089,         
    "air_domestic": 0.22,       
}

# --- Food Factors (kg CO2e per serving) ---
FOOD_FACTORS = {
    "red_meat_serving": 7.0,   
    "poultry_serving": 2.0,    
    "vegetable_serving": 0.5,  
}

# Used to structure input forms in the Presentation Layer
ACTIVITY_CATEGORIES = {
    "Transportation": list(TRANSPORT_FACTORS.keys()),
    "Food": list(FOOD_FACTORS.keys())
}