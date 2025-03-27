
"""
Custom decorators for the application
"""
from functools import wraps
from flask import redirect, url_for
from app.utils.helpers import is_logged_in


def login_required(f):
    """
    Decorator to ensure that a user is logged in before accessing a route.
    
    Args:
        f: The function to decorate
        
    Returns:
        function: The decorated function
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not is_logged_in():
            return redirect(url_for('auth.login'))
        return f(*args, **kwargs)
    return decorated_function