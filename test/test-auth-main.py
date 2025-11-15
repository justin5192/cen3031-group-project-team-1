# main.py 
# Final Verification Test for Core Logic (Phase 1 & 2)

from core_logic.auth import register_user, authenticate_user
from core_logic.calculator import calculate_footprint
from data_persistence.data_manager import save_activity_log, load_activity_logs

print("--- Authentication and Logic Verification Test ---")
test_user = "BlakeTest"
test_pass = "SecurePass1"

# 1. Test Registration (PBI 1.2)
print(f"\n[1. Testing Registration for {test_user}]")
# Ensure we start fresh by attempting to register, which might return True or an 'already taken' error
register_user(test_user, test_pass)
print("Registration attempt complete (check users.json file).")

# 2. Test Login (PBI 2.1)
print("\n[2. Testing Login]")
if authenticate_user(test_user, test_pass):
    print("SUCCESS: Login passed with correct credentials.")
else:
    print("FAILED: Login failed with correct credentials.")

if not authenticate_user(test_user, "wrongpass"):
    print("SUCCESS: Login with incorrect password failed (as expected).")
else:
    print("FAILED: Login passed with incorrect password.")


# 3. Test Activity Logging (Final Check)
# Note: Log count may be higher than 1 if you ran previous tests.
print("\n[3. Final Check: Data Integrity]")
logs = load_activity_logs()
log_count = len(logs.get(f"{test_user}_logs", []))
print(f"Log data loaded successfully. Logs for '{test_user}': {log_count}")