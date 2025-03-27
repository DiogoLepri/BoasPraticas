"""
Application configuration settings
"""
import os
from datetime import timedelta

class Config:
    """Base configuration class for the application"""
    # Flask settings
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'very-secret-key-should-be-changed'
    
    # Database settings
    DATABASE = os.path.join(os.getcwd(), 'instance', 'tasks.db')
    
    # Session settings
    PERMANENT_SESSION_LIFETIME = timedelta(days=1)
    
    # Application settings
    TASK_STATUSES = ['todo', 'in-progress', 'done']
    TASK_PRIORITIES = ['low', 'medium', 'high']


class DevelopmentConfig(Config):
    """Development configuration"""
    DEBUG = True


class TestingConfig(Config):
    """Testing configuration"""
    TESTING = True
    DATABASE = os.path.join(os.getcwd(), 'instance', 'test_tasks.db')


class ProductionConfig(Config):
    """Production configuration"""
    DEBUG = False
    TESTING = False
    SECRET_KEY = os.environ.get('SECRET_KEY')  # Must be set in production