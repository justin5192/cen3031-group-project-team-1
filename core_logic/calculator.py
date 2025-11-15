# ==============================================================================
# FILE 3: core_logic/calculator.py
# ==============================================================================
"""
Handles all carbon footprint calculations and aggregations.
"""
from datetime import datetime, timedelta
from collections import defaultdict, OrderedDict
from typing import List, Dict, Tuple
from .constants import MAIN_CATEGORIES


class CarbonFootprintCalculator:
    """Handles all carbon footprint calculation logic."""
    
    def __init__(self):
        """Initialize the calculator with all emission factors."""
        self.factors = {}
        for category_factors in MAIN_CATEGORIES.values():
            self.factors.update(category_factors)

    def get_activity_factor(self, activity_name: str) -> float:
        """
        Get the emission factor for a specific activity.
        
        Args:
            activity_name: Full name of the activity
            
        Returns:
            Emission factor or 0 if not found
        """
        return self.factors.get(activity_name, 0.0)

    def calculate_footprint(self, activity_name: str, value: float) -> float:
        """
        Calculate carbon footprint for a single activity.
        
        Args:
            activity_name: Full activity name (e.g., "Car - Small Gasoline (Miles)")
            value: Activity value (distance, servings, kWh, etc.)
            
        Returns:
            Carbon footprint in kg CO2e
        """
        if value < 0:
            value = 0
        factor = self.get_activity_factor(activity_name)
        return round(value * factor, 2)

    def calculate_weekly_total(self, all_activity_logs: List[dict]) -> float:
        """
        Calculate total footprint for the last 7 days.
        
        Args:
            all_activity_logs: List of activity log dictionaries
            
        Returns:
            Total weekly footprint in kg CO2e
        """
        seven_days_ago = datetime.now() - timedelta(days=7)
        weekly_footprint = 0.0
        
        for log in all_activity_logs:
            try:
                log_date = datetime.fromisoformat(log.get('timestamp'))
                if log_date >= seven_days_ago:
                    weekly_footprint += log.get('footprint', 0.0)
            except (ValueError, TypeError):
                continue
                
        return round(weekly_footprint, 2)

    def calculate_footprint_by_category(self, all_activity_logs: List[dict]) -> Dict[str, float]:
        """
        Aggregate footprint by main category for the last 7 days.
        
        Args:
            all_activity_logs: List of activity log dictionaries
            
        Returns:
            Dictionary mapping categories to total footprints
        """
        seven_days_ago = datetime.now() - timedelta(days=7)
        category_totals = defaultdict(float)
        
        for log in all_activity_logs:
            try:
                log_date = datetime.fromisoformat(log.get('timestamp'))
                if log_date < seven_days_ago:
                    continue
            except (ValueError, TypeError):
                continue

            category = log.get('category', 'Other')
            footprint = log.get('footprint', 0.0)
            category_totals[category] += footprint
            
        return {cat: round(total, 2) for cat, total in category_totals.items()}

    def calculate_footprint_over_last_n_days(self, all_activity_logs: List[dict], days: int = 7) -> List[dict]:
        """
        Calculate daily footprint totals for the last N days.
        
        Args:
            all_activity_logs: List of activity log dictionaries
            days: Number of days to include
            
        Returns:
            List of dictionaries with 'date' and 'footprint' keys
        """
        today = datetime.now().date()
        daily_footprint = OrderedDict()

        # Initialize all dates with 0.0
        for i in range(days - 1, -1, -1):
            date_obj = today - timedelta(days=i)
            date_str = date_obj.strftime('%Y-%m-%d')
            daily_footprint[date_str] = 0.0
            
        # Aggregate logs by date
        for log in all_activity_logs:
            try:
                log_date_str = datetime.fromisoformat(log['timestamp']).strftime('%Y-%m-%d')
                footprint = log.get('footprint', 0.0)
                
                if log_date_str in daily_footprint:
                    daily_footprint[log_date_str] += footprint
            except (KeyError, ValueError, TypeError):
                continue

        # Convert to list format
        return [
            {'date': date_str, 'footprint': round(total, 2)}
            for date_str, total in daily_footprint.items()
        ]

    def get_top_contributing_category(self, all_activity_logs: List[dict]) -> str:
        """
        Determine the category with the highest footprint.
        
        Args:
            all_activity_logs: List of activity log dictionaries
            
        Returns:
            Name of the top contributing category
        """
        category_breakdown = self.calculate_footprint_by_category(all_activity_logs)
        
        if not category_breakdown:
            return "General"
        
        return max(category_breakdown, key=category_breakdown.get)

    def calculate_system_average_weekly_footprint(self, all_user_weekly_totals: List[float]) -> float:
        """
        Calculate average weekly footprint across all users.
        
        Args:
            all_user_weekly_totals: List of weekly totals for each user
            
        Returns:
            Average weekly footprint in kg CO2e
        """
        if not all_user_weekly_totals:
            return 0.0
        
        average = sum(all_user_weekly_totals) / len(all_user_weekly_totals)
        return round(average, 2)
