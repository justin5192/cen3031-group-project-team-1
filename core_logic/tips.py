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
    "Opt for energy-efficient appliances when replacing old ones (look for Energy Star ratings).",
    "Bring your own reusable coffee cup and water bottle everywhere you go.",
    "Adjust your thermostat instead of using portable heaters or AC units.",
    "Buy second-hand clothing and furniture to reduce the demand for new production.",
    "Support companies with strong, verifiable sustainability practices.",
    "Switch to paperless billing and digital documents to save paper.",
    "Reduce your reliance on fast fashion by choosing quality over quantity.",
    "Offset the emissions from unavoidable travel, though reduction is always better.",
    "Plant a tree or support local reforestation efforts.",
    "Use cold water for laundry whenever possible, as heating water is energy-intensive.",
    "Install a low-flow showerhead to significantly reduce water usage.",
    "Insulate your hot water heater and pipes to retain heat.",
    "Learn to mend clothing instead of throwing it away.",
    "Cancel junk mail and unwanted catalogs to save paper and resources.",
    "Use rechargeable batteries instead of disposable ones.",
    "Choose products made from recycled materials.",
    "Support local farmers' markets to reduce the food miles of your purchases.",
    "Educate yourself and others about climate change and sustainable living.",
    "Invest in a home energy audit to identify areas for improvement.",
    "Switch to greener cleaning products to reduce chemical pollutants.",
]

CONTEXTUAL_TIPS = {
    "Transportation": [
        "Your largest contribution is Transportation. Try cycling or walking for short trips!",
        "Consider consolidating multiple trips into one to reduce driving mileage.",
        "Check your tire pressure - properly inflated tires improve fuel efficiency by up to 3%.",
        "Explore public transit options instead of driving solo.",
        "Try carpooling with coworkers or friends to cut your commute emissions in half.",
        "If buying a new car, prioritize hybrid or electric vehicles.",
        "Practice 'eco-driving' by avoiding rapid acceleration and hard braking.",
        "Use cruise control on highways to maintain a steady speed and conserve fuel.",
        "Remove unnecessary heavy items from your car trunk to improve mileage.",
        "Avoid idling your engine; turn it off if stopped for more than 10 seconds.",
        "Plan your routes efficiently using navigation apps to avoid traffic and wasted fuel.",
        "Consider train travel over flying for domestic or regional trips.",
        "When flying, choose direct flights to reduce take-off and landing emissions.",
        "Look for airlines that use more fuel-efficient aircraft or sustainable aviation fuels.",
        "Maintain your vehicle regularly; a well-tuned engine runs more efficiently.",
        "When renting a vehicle, choose the smallest, most fuel-efficient option you need.",
        "If you live close to work, ask your employer about flexible work-from-home options.",
        "Switch to a bike for your commute if feasible.",
        "Utilize ride-sharing services that focus on shared rides to reduce the number of cars on the road.",
        "Drive at or below the speed limit, as fuel efficiency drops significantly at higher speeds.",
        "Consider using a cargo bike for errands instead of the car.",
        "Avoid using roof racks or external carriers when not needed, as they increase drag and fuel use.",
        "Ask your local government to invest in better bicycle lanes and public transit.",
        "Take a 'staycation' to reduce the emissions from long-distance travel.",
        "When moving, hire a company that uses modern, fuel-efficient trucks.",
    ],
    "Food": [
        "Your largest contribution is Food. Try a vegetarian meal one day this week!",
        "Focus on reducing food waste - wasted food means wasted emissions.",
        "Buy locally sourced products or try plant-based alternatives.",
        "Brew your own coffee instead of buying to-go cups.",
        "Choose seasonal produce to reduce the carbon cost of transportation and storage.",
        "Significantly reduce your consumption of high-carbon meats like beef and lamb.",
        "Buy in bulk for pantry staples to reduce packaging waste.",
        "Plan your meals ahead of time to avoid impulse purchases and food waste.",
        "Store food properly to extend its shelf life.",
        "Learn to preserve food through methods like freezing or canning.",
        "Eat smaller portions of meat and make vegetables the focus of your plate.",
        "Try 'ugly' produce boxes or stores to save food that might otherwise be wasted.",
        "Grow your own herbs or vegetables in a small garden or window box.",
        "Avoid highly processed foods, which often have a larger production footprint.",
        "Drink tap water instead of bottled water to reduce plastic waste and transport costs.",
        "Choose sustainable and ethically sourced seafood (check guides like Monterey Bay Aquarium Seafood Watch).",
        "Use all edible parts of vegetables (e.g., broccoli stems, carrot tops).",
        "Donate unused, non-perishable food before it expires.",
        "Bring reusable containers for leftovers when dining out.",
        "Make stock from vegetable scraps and bone trimmings.",
        "Look for certifications that ensure sustainable farming practices.",
        "Reduce dairy consumption by trying plant-based milks and cheeses.",
        "Support companies that are committed to sustainable sourcing and fair trade.",
        "Read labels and choose products with fewer ingredients and less artificial content.",
        "Only buy the amount of food you can realistically consume.",
    ],
    "Home Energy": [
        "Your largest contribution is Home Energy. Lower your thermostat by a few degrees.",
        "Use energy-saving LED light bulbs throughout your home.",
        "Wash clothes in cold water - heating water uses significant energy.",
        "Seal air leaks around windows and doors for better efficiency.",
        "Unplug devices when not in use to eliminate phantom power drain.",
        "Install a smart thermostat to optimize heating and cooling schedules.",
        "Close blinds and curtains to keep heat out in the summer and in during the winter.",
        "Weatherize your home by adding insulation to attics and walls.",
        "Replace old, drafty windows with energy-efficient, double-paned ones.",
        "Use a drying rack or clothesline instead of a tumble dryer.",
        "Clean or replace air filters regularly in your HVAC system for optimal performance.",
        "Turn off the oven a few minutes early and let residual heat finish the cooking.",
        "Use smaller appliances (like microwaves or toasters) instead of the oven when possible.",
        "Run your dishwasher and washing machine only when fully loaded.",
        "Set your water heater to 120 Degrees F to save energy and prevent scalding.",
        "Consider installing solar panels on your roof to generate your own renewable energy.",
        "Use power strips for electronics and flip the switch off when leaving the room.",
        "Switch to a laptop or tablet, as they typically use less power than a desktop computer.",
        "Check your refrigerator seals to ensure cold air isn't escaping.",
        "Dress warmer indoors in winter to avoid turning up the heat.",
        "Use ceiling fans to circulate air and reduce the need for AC or heating.",
        "Insulate your electrical outlets and switch plates.",
        "Defrost your freezer regularly to improve its efficiency.",
        "Program your furnace or boiler to only run when you are home or awake.",
        "When remodeling, choose highly energy-efficient construction materials.",
    ],
    "Waste": [
        "Your largest contribution is Waste. Focus on reducing single-use items.",
        "Start composting food scraps to reduce methane from landfills.",
        "Choose products with minimal packaging when shopping.",
        "Repair items instead of replacing them when possible.",
        "Bring reusable bags, bottles, and containers to reduce waste.",
        "Avoid purchasing pre-cut or individually wrapped fruits and vegetables.",
        "Say 'no' to straws, plastic cutlery, and unnecessary receipts.",
        "Choose products in glass or metal containers over plastic where possible.",
        "Shop at bulk food stores using your own reusable containers.",
        "Properly clean all recyclables to ensure they can be processed.",
        "Check local guidelines for what can and cannot be recycled in your area.",
        "Avoid using paper towels by switching to reusable cloths or sponges.",
        "Donate unwanted items (clothes, books, electronics) instead of throwing them away.",
        "Buy products designed for durability and longevity.",
        "Upcycle or repurpose old items into something new and useful.",
        "Use reusable cloth diapers instead of disposables.",
        "Look for refillable options for cleaning products and personal care items.",
        "Cancel physical newspapers and magazines, opting for digital subscriptions.",
        "Use a fountain pen or mechanical pencil to reduce disposable plastic.",
        "Buy concentrated versions of cleaners to reduce packaging and shipping volume.",
        "Compost yard waste like leaves and grass clippings.",
        "Choose non-toxic, biodegradable products to reduce chemical waste in waterways.",
        "Return old electronics to manufacturers or designated recycling centers.",
        "Buy less! Evaluate if you truly need an item before purchasing it.",
        "Support companies with take-back programs for their products or packaging.",
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
