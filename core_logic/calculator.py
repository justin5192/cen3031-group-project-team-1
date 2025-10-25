# core_logic/calculator.py
from .constants import TRANSPORT_FACTORS, FOOD_FACTORS

# PBI 4.3: Implement calculation logic to find footprint.

def calculate_footprint(activity_type, sub_category, value):
    """
    Calculates the carbon footprint based on activity (e.g., Transportation) 
    and value (e.g., miles traveled).
    """
    
    factor = 0.0
    
    if activity_type == "Transportation":
        factor = TRANSPORT_FACTORS.get(sub_category, 0.0)
    elif activity_type == "Food":
        factor = FOOD_FACTORS.get(sub_category, 0.0)
        
    # Footprint = Value * Conversion Factor
    footprint = factor * value
    
    return round(footprint, 2)