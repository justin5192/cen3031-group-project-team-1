# ==============================================================================
# FILE 4: core_logic/data_persistence.py  
# ==============================================================================
"""
Handles all data persistence operations using JSON file storage.
"""
import os
import json
import hashlib
import csv
from datetime import datetime
from typing import Tuple, Dict, List, Optional


class DataPersistence:
    """Manages user data storage and retrieval."""
    
    def __init__(self, storage_dir: str = 'user_data'):
        """
        Initialize data persistence layer.
        
        Args:
            storage_dir: Directory for storing user data files
        """
        self.storage_dir = storage_dir
        self.dummy_users_file = os.path.join(storage_dir, 'dummy_users.json')
        
        if not os.path.exists(self.storage_dir):
            try:
                os.makedirs(self.storage_dir)
            except Exception as e:
                print(f"FATAL ERROR: Could not create storage directory '{self.storage_dir}'. {e}")
        
        # Initialize dummy users if they don't exist
        self._initialize_dummy_users()

    def _get_user_file_path(self, username: str) -> str:
        """Generate secure filename using username hash."""
        safe_name = hashlib.sha256(username.encode()).hexdigest()
        return os.path.join(self.storage_dir, f'{safe_name}.json')

    def _hash_password(self, password: str) -> str:
        """Hash password for secure storage."""
        return hashlib.sha256(password.encode()).hexdigest()

    def load_user_data(self, username: str) -> Dict:
        """
        Load user data from file.
        
        Args:
            username: Username to load data for
            
        Returns:
            User data dictionary with default values if file doesn't exist
        """
        filepath = self._get_user_file_path(username)
        
        if os.path.exists(filepath):
            try:
                with open(filepath, 'r') as f:
                    data = json.load(f)
                    # Ensure required keys exist
                    data.setdefault('logs', [])
                    data.setdefault('goal', 100.0)
                    data.setdefault('goal_type', 'weekly')
                    data.setdefault('needs_initial_goal', False)
                    return data
            except json.JSONDecodeError:
                print(f"Error reading {filepath}. Returning default data.")
        
        # Return default structure
        return {
            'goal': 100.0,
            'goal_type': 'weekly',
            'logs': [],
            'password_hash': None,
            'needs_initial_goal': True
        }

    def save_user_data(self, username: str, data: Dict) -> None:
        """
        Save user data to file.
        
        Args:
            username: Username to save data for
            data: User data dictionary
        """
        filepath = self._get_user_file_path(username)
        with open(filepath, 'w') as f:
            json.dump(data, f, indent=4)

    # --- Authentication ---
    
    def register_user(self, username: str, password: str) -> Tuple[bool, str]:
        """
        Register a new user.
        
        Args:
            username: Desired username
            password: User password
            
        Returns:
            Tuple of (success boolean, message string)
        """
        if not username or not password:
            return False, "Username and password cannot be empty."

        if len(password) < 6:
            return False, "Password must be at least 6 characters long."

        filepath = self._get_user_file_path(username)
        if os.path.exists(filepath):
            return False, "Username already exists. Please choose a different username."

        initial_data = {
            'goal': 100.0,
            'goal_type': 'weekly',
            'logs': [],
            'password_hash': self._hash_password(password),
            'needs_initial_goal': True  # Flag for redirect to goal setting
        }
        
        try:
            self.save_user_data(username, initial_data)
            return True, "User registered successfully."
        except Exception as e:
            return False, f"System Error: Failed to save data. Check folder permissions: {e}"

    def authenticate_user(self, username: str, password: str) -> Tuple[bool, str]:
        """
        Authenticate user credentials.
        
        Args:
            username: Username to authenticate
            password: Password to verify
            
        Returns:
            Tuple of (success boolean, message string)
        """
        data = self.load_user_data(username)
        
        if 'password_hash' not in data or data['password_hash'] is None:
            filepath = self._get_user_file_path(username)
            if not os.path.exists(filepath):
                return False, "User not found."
            return False, "Authentication failed. User data is incomplete."

        if data['password_hash'] == self._hash_password(password):
            return True, "Authentication successful."
        
        return False, "Invalid username or password."
            
    # --- Activity Log Management ---
    
    def get_all_activity_logs(self, username: str) -> List[Dict]:
        """Get all activity logs for a user."""
        data = self.load_user_data(username)
        return data.get('logs', [])

    def add_activity_log(self, username: str, log_data: Dict) -> bool:
        """
        Add new activity log entry.
        
        Args:
            username: Username to add log for
            log_data: Log entry dictionary
            
        Returns:
            True if successful
        """
        data = self.load_user_data(username)
        log_data['timestamp'] = datetime.now().isoformat()
        data['logs'].append(log_data)
        self.save_user_data(username, data)
        return True

    def update_activity_log(self, username: str, index: int, new_log_data: Dict) -> bool:
        """
        Update existing activity log.
        
        Args:
            username: Username
            index: Index of log to update
            new_log_data: Updated log data
            
        Returns:
            True if successful, False if index invalid
        """
        data = self.load_user_data(username)
        
        if 0 <= index < len(data['logs']):
            original_timestamp = data['logs'][index].get('timestamp')
            data['logs'][index].update(new_log_data)
            
            # Preserve original timestamp if not provided
            if 'timestamp' not in data['logs'][index]:
                data['logs'][index]['timestamp'] = original_timestamp or datetime.now().isoformat()
            
            try:
                self.save_user_data(username, data)
                return True
            except Exception as e:
                print(f"Error saving data: {e}")
        
        return False

    def delete_activity_log(self, username: str, index: int) -> bool:
        """
        Delete activity log entry.
        
        Args:
            username: Username
            index: Index of log to delete
            
        Returns:
            True if successful, False if index invalid
        """
        data = self.load_user_data(username)
        
        if 0 <= index < len(data['logs']):
            del data['logs'][index]
            try:
                self.save_user_data(username, data)
                return True
            except Exception as e:
                print(f"Error saving data: {e}")
        
        return False

    # --- Goal Management ---
    
    def get_current_goal(self, username: str) -> Tuple[float, str]:
        """
        Get user's current goal and type.
        
        Returns:
            Tuple of (goal value, goal type)
        """
        data = self.load_user_data(username)
        return data.get('goal', 100.0), data.get('goal_type', 'weekly')

    def set_current_goal(self, username: str, new_goal: float, goal_type: str = 'weekly') -> bool:
        """
        Set user's goal.
        
        Args:
            username: Username
            new_goal: New goal value in kg CO2e
            goal_type: 'daily' or 'weekly'
            
        Returns:
            True if successful
        """
        data = self.load_user_data(username)
        data['goal'] = new_goal
        data['goal_type'] = goal_type
        data['needs_initial_goal'] = False  # Clear the flag
        self.save_user_data(username, data)
        return True
    
    def needs_initial_goal_setting(self, username: str) -> bool:
        """Check if user needs to set initial goal."""
        data = self.load_user_data(username)
        return data.get('needs_initial_goal', False)

    # --- Data Export (PBI 13.1) ---
    
    def export_logs_to_csv(self, username: str, filepath: str, start_date: str = None, end_date: str = None) -> bool:
        """
        Export user's activity logs to CSV file.
        
        Args:
            username: Username
            filepath: Path to save CSV file
            start_date: Optional start date (ISO format)
            end_date: Optional end date (ISO format)
            
        Returns:
            True if successful
        """
        logs = self.get_all_activity_logs(username)
        
        # Filter by date range if provided
        if start_date or end_date:
            filtered_logs = []
            for log in logs:
                try:
                    log_date = datetime.fromisoformat(log['timestamp']).date()
                    if start_date and log_date < datetime.fromisoformat(start_date).date():
                        continue
                    if end_date and log_date > datetime.fromisoformat(end_date).date():
                        continue
                    filtered_logs.append(log)
                except (ValueError, KeyError):
                    continue
            logs = filtered_logs
        
        try:
            with open(filepath, 'w', newline='') as csvfile:
                if not logs:
                    csvfile.write("No data to export\n")
                    return True
                
                fieldnames = ['timestamp', 'category', 'activity', 'value', 'footprint', 'description']
                writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                
                writer.writeheader()
                for log in logs:
                    writer.writerow({
                        'timestamp': log.get('timestamp', ''),
                        'category': log.get('category', ''),
                        'activity': log.get('activity', ''),
                        'value': log.get('value', ''),
                        'footprint': log.get('footprint', ''),
                        'description': log.get('description', '')
                    })
            return True
        except Exception as e:
            print(f"Error exporting to CSV: {e}")
            return False

    # --- Dummy Users for Comparison (PBI 10.1) ---
    
    def _initialize_dummy_users(self):
        """Create dummy user data if it doesn't exist."""
        if os.path.exists(self.dummy_users_file):
            return
        
        import random
        from datetime import timedelta
        
        dummy_data = []
        
        # Generate 100 dummy users with realistic weekly totals
        for i in range(100):
            # Weekly totals range from 50 to 200 kg CO2e with normal distribution
            weekly_total = random.gauss(120, 30)  # mean=120, std=30
            weekly_total = max(50, min(200, weekly_total))  # Clamp between 50-200
            
            dummy_data.append({
                'user_id': f'dummy_{i}',
                'weekly_total': round(weekly_total, 2)
            })
        
        try:
            with open(self.dummy_users_file, 'w') as f:
                json.dump(dummy_data, f, indent=4)
        except Exception as e:
            print(f"Error creating dummy users: {e}")
    
    def get_all_weekly_totals_for_comparison(self, current_username: str, calculator) -> Tuple[float, float, float]:
        """
        Get user's weekly total, system average, and percentage difference.
        
        Args:
            current_username: Current user's username
            calculator: CarbonFootprintCalculator instance
            
        Returns:
            Tuple of (user_total, system_average, percentage_difference)
        """
        # Get current user's weekly total
        user_logs = self.get_all_activity_logs(current_username)
        user_total = calculator.calculate_weekly_total(user_logs)
        
        # Load dummy users
        try:
            with open(self.dummy_users_file, 'r') as f:
                dummy_data = json.load(f)
                dummy_totals = [d['weekly_total'] for d in dummy_data]
        except:
            dummy_totals = []
        
        # Get all real users (scan directory)
        real_user_totals = []
        for filename in os.listdir(self.storage_dir):
            if filename.endswith('.json') and filename != 'dummy_users.json':
                try:
                    filepath = os.path.join(self.storage_dir, filename)
                    with open(filepath, 'r') as f:
                        user_data = json.load(f)
                        logs = user_data.get('logs', [])
                        total = calculator.calculate_weekly_total(logs)
                        if total > 0:  # Only include users with activity
                            real_user_totals.append(total)
                except:
                    continue
        
        # Combine all totals
        all_totals = dummy_totals + real_user_totals
        
        if not all_totals:
            return user_total, 0.0, 0.0
        
        system_average = sum(all_totals) / len(all_totals)
        
        # Calculate percentage difference
        if system_average > 0:
            percentage_diff = ((user_total - system_average) / system_average) * 100
        else:
            percentage_diff = 0.0
        
        return user_total, round(system_average, 2), round(percentage_diff, 1)

