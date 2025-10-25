# data_persistence/data_manager.py
import json
import os

# Define file paths relative to the project structure
BASE_DIR = os.path.join(os.path.dirname(__file__), '..', 'data_storage')
USERS_FILE = os.path.join(BASE_DIR, 'users.json')
LOGS_FILE = os.path.join(BASE_DIR, 'activity_logs.json')

# PBI 1.1: Design simple file-based storage/structure for user data.

def _load_json_data(filepath):
    """Internal helper to safely load data from a JSON file."""
    if not os.path.exists(filepath):
        os.makedirs(os.path.dirname(filepath), exist_ok=True)
        with open(filepath, 'w') as f:
            json.dump({}, f)
        return {}
    
    with open(filepath, 'r') as f:
        try:
            return json.load(f)
        except json.JSONDecodeError:
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