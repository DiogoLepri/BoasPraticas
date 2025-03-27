"""
Database connection and utilities
"""
import sqlite3
from flask import current_app, g
import os


def get_db():
    """
    Get a database connection.
    
    Returns:
        sqlite3.Connection: Database connection with row factory set to sqlite3.Row
    """
    if 'db' not in g:
        g.db = sqlite3.connect(current_app.config['DATABASE'])
        g.db.row_factory = sqlite3.Row
    return g.db


def close_db(e=None):
    """
    Close the database connection if it exists.
    
    Args:
        e: Exception that may have occurred
    """
    db = g.pop('db', None)
    if db is not None:
        db.close()


def init_db():
    """
    Initialize the database with the required tables.
    """
    from flask import current_app
    
    # Acesse o caminho do banco de dados diretamente do objeto Config se current_app não estiver disponível
    try:
        db_path = current_app.config['DATABASE']
    except RuntimeError:
        # Fallback para quando não estamos em um contexto de aplicação
        from app.config import Config
        db_path = Config.DATABASE
    
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # Create users table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE NOT NULL,
        password TEXT NOT NULL,
        email TEXT UNIQUE NOT NULL,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    ''')
    
    # Create tasks table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS tasks (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT NOT NULL,
        description TEXT,
        status TEXT DEFAULT 'todo',
        priority TEXT DEFAULT 'medium',
        due_date TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        user_id INTEGER,
        FOREIGN KEY (user_id) REFERENCES users (id)
    )
    ''')
    
    conn.commit()
    conn.close()