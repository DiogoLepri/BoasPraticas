"""
Authentication routes
"""
import sqlite3
from flask import Blueprint, request, render_template, redirect, url_for, session, flash

from app.db import get_db
from app.utils.helpers import hash_password
from app.auth.forms import LoginForm, RegisterForm

# Create blueprint
auth_bp = Blueprint('auth', __name__, url_prefix='/auth')


@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    """Handle user login"""
    error = None
    if request.method == 'POST':
        username = request.form['username']
        password = hash_password(request.form['password'])
        
        db = get_db()
        cursor = db.cursor()
        cursor.execute("SELECT * FROM users WHERE username = ? AND password = ?", 
                      (username, password))
        user = cursor.fetchone()
        
        if user:
            session['user_id'] = user['id']
            session['username'] = user['username']
            return redirect(url_for('tasks.index'))
        else:
            error = 'Invalid username or password'
    
    return render_template('auth/login.html', error=error)


@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    """Handle user registration"""
    error = None
    if request.method == 'POST':
        username = request.form['username']
        password = hash_password(request.form['password'])
        email = request.form['email']
        
        db = get_db()
        cursor = db.cursor()
        
        try:
            cursor.execute("INSERT INTO users (username, password, email) VALUES (?, ?, ?)", 
                          (username, password, email))
            db.commit()
            flash('Account created successfully. Please log in.', 'success')
            return redirect(url_for('auth.login'))
        except sqlite3.IntegrityError:
            error = 'Username or email already exists'
    
    return render_template('auth/register.html', error=error)


@auth_bp.route('/logout')
def logout():
    """Handle user logout"""
    session.clear()
    return redirect(url_for('auth.login'))