import json
import os

# Define file paths relative to the project structure
# Navigate up to the project root and then down into data_storage
BASE_DIR = os.path.join(os.path.dirname(__file__), '..', 'data_storage')
USERS_FILE = os.path.join(BASE_DIR, 'users.json')
LOGS_FILE = os.path.join(BASE_DIR, 'activity_logs.json')

# PBI 1.1: Design simple file-based storage/structure for user data.

def _load_json_data(filepath):
    """Internal helper to safely load data from a JSON file."""
    if not os.path.exists(filepath):
        # Ensure the data_storage directory exists
        os.makedirs(os.path.dirname(filepath), exist_ok=True)
        # Create an empty file if it doesn't exist
        with open(filepath, 'w') as f:
            json.dump({}, f)
        return {}
    
    with open(filepath, 'r') as f:
        try:
            # Handle empty files gracefully
            content = f.read()
            if not content:
                return {}
            f.seek(0) # Rewind for json.load
            return json.loads(content)
        except json.JSONDecodeError:
            # If the file is corrupted or not valid JSON
            return {}

def _save_json_data(data, filepath):
    """Internal helper to save data to a JSON file."""
    os.makedirs(os.path.dirname(filepath), exist_ok=True)
    with open(filepath, 'w') as f:
        json.dump(data, f, indent=4)

# --- Public Functions for Data Access ---

def load_user_data():
    """Loads all user accounts and credentials."""
    return _load_json_data(USERS_FILE)

def save_user_data(user_data):
    """Saves all user accounts and credentials."""
    _save_json_data(user_data, USERS_FILE)

def load_activity_logs():
    """Loads all user activity logs."""
    return _load_json_data(LOGS_FILE)

def save_activity_log(username, new_log_entry):
    """PBI 4.4: Appends a new log entry to a specific user's log list."""
    logs = load_activity_logs()
    
    log_key = f"{username}_logs"
    
    if log_key not in logs:
        logs[log_key] = []
        
    logs[log_key].append(new_log_entry)
    
    _save_json_data(logs, LOGS_FILE)

def get_cumulative_footprint(username):
    """
    PBI 6.1: Calculates the sum of all logged footprints for a user.
    This function is now available for the UI to call.
    """
    logs = load_activity_logs()
    log_key = f"{username}_logs"
    
    user_logs = logs.get(log_key, [])
    
    total_footprint = 0.0
    for entry in user_logs:
        # Safely read the footprint value
        total_footprint += entry.get('footprint', 0.0)
        
    return round(total_footprint, 2)

import csv
import os

def export_logs_to_csv(username, filepath="carbon_export.csv"):
    """
    Exports the user's logged activities to a CSV file.
    """
    logs = load_activity_logs()
    user_key = f"{username}_logs"
    user_logs = logs.get(user_key, [])

    if not user_logs:
        raise ValueError("No logs available to export.")

    # Ensure folder exists (if user gives path)
    os.makedirs(os.path.dirname(filepath) or ".", exist_ok=True)

    with open(filepath, "w", newline="") as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=user_logs[0].keys())
        writer.writeheader()
        writer.writerows(user_logs)

    return filepath



