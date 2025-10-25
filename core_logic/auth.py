# core_logic/auth.py
import hashlib
import os
import binascii 
from data_persistence.data_manager import load_user_data, save_user_data

# Configuration for secure password hashing
HASH_ALGORITHM = 'sha256'
ITERATIONS = 100000 
SALT_SIZE = 16 # bytes

def _hash_password(password, salt=None):
    """
    Internal function to securely hash the password using PBKDF2.
    It returns the salt and the derived hashed password.
    """
    if salt is None:
        # Generate a new random salt for registration
        salt = os.urandom(SALT_SIZE)
        
    hashed_password = hashlib.pbkdf2_hmac(
        HASH_ALGORITHM,
        password.encode('utf-8'),
        salt,
        ITERATIONS
    )
    
    return salt, hashed_password

def register_user(username, password):
    """
    PBI 1.2: Implements user registration (username/password) with basic saving/hashing.
    
    Returns: True on success, or an error message string on failure.
    """
    user_data = load_user_data()
    
    # 1. Check for existing username (User Story 1 Conversation)
    if username in user_data:
        return f"Error: Username '{username}' is already taken."
    
    # 2. Basic password requirement check
    if len(password) < 6:
        return "Error: Password must be at least 6 characters long."
    
    # 3. Generate salt and hash
    salt, hashed_pw = _hash_password(password)
    
    # 4. Create and store the new user profile
    new_user_profile = {
        # Convert to hex strings for safe storage in JSON
        "salt": binascii.hexlify(salt).decode('utf-8'),
        "password_hash": binascii.hexlify(hashed_pw).decode('utf-8'),
        # Goal setting (PBI 3.1) is handled after registration
        "reduction_goal": None 
    }
    
    user_data[username] = new_user_profile
    save_user_data(user_data)
    
    return True

def authenticate_user(username, password):
    """
    PBI 2.1: Implements basic authentication check against saved credentials.
    
    Returns: True on successful login, False on failure.
    """
    user_data = load_user_data()
    
    # 1. Check if the username exists
    if username not in user_data:
        return False

    user_profile = user_data[username]
    
    try:
        # 2. Retrieve and convert the stored salt and hash back to bytes
        stored_salt = binascii.unhexlify(user_profile['salt'].encode('utf-8'))
        stored_hash = binascii.unhexlify(user_profile['password_hash'].encode('utf-8'))
    except binascii.Error:
        return False
    
    # 3. Hash the provided password using the stored salt
    _, provided_hash = _hash_password(password, salt=stored_salt)
    
    # 4. Compare hashes securely
    #return hashlib.compare_digest(provided_hash, stored_hash)
    return provided_hash == stored_hash