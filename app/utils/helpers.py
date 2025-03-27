"""
Helper functions for the application
"""
import hashlib
from flask import session


def hash_password(password):
    """
    Hash a password using SHA-256.
    
    Args:
        password (str): The password to hash
        
    Returns:
        str: The hashed password
    """
    return hashlib.sha256(password.encode()).hexdigest()


def is_logged_in():
    """
    Check if the user is logged in.
    
    Returns:
        bool: True if the user is logged in, False otherwise
    """
    return 'user_id' in session