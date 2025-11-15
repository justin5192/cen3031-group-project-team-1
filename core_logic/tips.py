# ==============================================================================
# FILE 2: core_logic/tips.py
# ==============================================================================
"""
Reduction tips for users based on their carbon footprint patterns.
"""
import random
from typing import Optional

GENERAL_TIPS = [
    "Switch to a renewable energy supplier for your home to reduce your energy footprint.",
    "Try to buy local and seasonal produce to minimize transportation emissions.",
    "Unplug electronics that aren't in use to avoid phantom energy drain.",
    "Reduce, reuse, recycle! Focus on durable goods to lower your overall footprint.",
    "Carpool or take public transport a few times a week to cut emissions.",
    "Take shorter showers and switch off lights when leaving a room.",
]

CONTEXTUAL_TIPS = {
    "Transportation": [
        "Your largest contribution is Transportation. Try cycling or walking for short trips!",
        "Consider consolidating multiple trips into one to reduce driving mileage.",
        "Check your tire pressure - properly inflated tires improve fuel efficiency by up to 3%.",
        "Explore public transit options instead of driving solo.",
        "Try carpooling with coworkers or friends to cut your commute emissions in half.",
    ],
    "Food": [
        "Your largest contribution is Food. Try a vegetarian meal one day this week!",
        "Focus on reducing food waste - wasted food means wasted emissions.",
        "Buy locally sourced products or try plant-based alternatives.",
        "Brew your own coffee instead of buying to-go cups.",
        "Choose seasonal produce to reduce the carbon cost of transportation and storage.",
    ],
    "Home Energy": [
        "Your largest contribution is Home Energy. Lower your thermostat by a few degrees.",
        "Use energy-saving LED light bulbs throughout your home.",
        "Wash clothes in cold water - heating water uses significant energy.",
        "Seal air leaks around windows and doors for better efficiency.",
        "Unplug devices when not in use to eliminate phantom power drain.",
    ],
    "Waste": [
        "Your largest contribution is Waste. Focus on reducing single-use items.",
        "Start composting food scraps to reduce methane from landfills.",
        "Choose products with minimal packaging when shopping.",
        "Repair items instead of replacing them when possible.",
        "Bring reusable bags, bottles, and containers to reduce waste.",
    ],
    "General": GENERAL_TIPS
}


def get_random_tip() -> str:
    """Returns a random general reduction tip."""
    return random.choice(GENERAL_TIPS)


def get_contextual_tip(category: str) -> str:
    """
    Returns a tip specific to the user's highest footprint category.
    
    Args:
        category: The user's highest footprint category
        
    Returns:
        A relevant reduction tip string
    """
    # Map UI category to tip category
    normalized_category = category.strip()
    
    # Check if it's a main category or needs mapping
    if normalized_category in CONTEXTUAL_TIPS:
        return random.choice(CONTEXTUAL_TIPS[normalized_category])
    
    # Try to extract the main category (e.g., "Transportation" from "Transportation (Car, Bus...)")
    for key in CONTEXTUAL_TIPS.keys():
        if key in normalized_category:
            return random.choice(CONTEXTUAL_TIPS[key])
    
    return get_random_tip()
