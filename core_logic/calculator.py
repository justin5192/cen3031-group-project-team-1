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

from datetime import datetime, timedelta

def summarize_by_category(user_logs):
    """Return {category: total footprint}."""
    summary = {}
    for entry in user_logs:
        cat = entry.get("activity_type")
        fp = entry.get("footprint", 0)
        summary[cat] = summary.get(cat, 0) + fp
    return {k: round(v, 2) for k, v in summary.items()}

def last_7_days_timeseries(user_logs):
    """Return list of (date_str, total_fp) for last 7 days."""
    today = datetime.now().date()
    series = {today - timedelta(days=i): 0 for i in range(7)}

    for entry in user_logs:
        # Accept either 'timestamp' or 'date' keys depending on where the log was created
        ts = entry.get("timestamp") or entry.get("date")
        if not ts:
            continue
        try:
            d = datetime.strptime(ts, "%Y-%m-%d %H:%M:%S").date()
        except:
            continue
        if d in series:
            series[d] += entry.get("footprint", 0)

    # Convert to chart-friendly sorted list
    return [(d.strftime("%Y-%m-%d"), round(v, 2)) for d, v in sorted(series.items())]
