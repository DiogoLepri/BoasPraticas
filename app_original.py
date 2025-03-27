from flask import Flask, request, jsonify, render_template, redirect, url_for, session
import sqlite3
import os
from datetime import datetime
import hashlib
import secrets
import json


app = Flask(__name__)
app.secret_key = "very-secret-key-should-be-changed"
DATABASE = "tasks.db"

def init_db():
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE NOT NULL,
        password TEXT NOT NULL,
        email TEXT UNIQUE NOT NULL,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    ''')
    
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


init_db()


def get_db():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn

# Authentication helper functions
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def is_logged_in():
    return 'user_id' in session

def login_required(f):
    def decorated_function(*args, **kwargs):
        if not is_logged_in():
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    decorated_function.__name__ = f.__name__
    return decorated_function


@app.route('/')
def home():
    if not is_logged_in():
        return redirect(url_for('login'))
    
    db = get_db()
    cursor = db.cursor()
    cursor.execute("SELECT * FROM tasks WHERE user_id = ? ORDER BY due_date", (session['user_id'],))
    tasks = cursor.fetchall()
    db.close()
    
    return render_template('index.html', tasks=tasks)

@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        username = request.form['username']
        password = hash_password(request.form['password'])
        
        db = get_db()
        cursor = db.cursor()
        cursor.execute("SELECT * FROM users WHERE username = ? AND password = ?", (username, password))
        user = cursor.fetchone()
        db.close()
        
        if user:
            session['user_id'] = user['id']
            session['username'] = user['username']
            return redirect(url_for('home'))
        else:
            error = 'Invalid username or password'
    
    return render_template('login.html', error=error)

@app.route('/register', methods=['GET', 'POST'])
def register():
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
            db.close()
            return redirect(url_for('login'))
        except sqlite3.IntegrityError:
            error = 'Username or email already exists'
            db.close()
    
    return render_template('register.html', error=error)

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

@app.route('/add_task', methods=['GET', 'POST'])
@login_required
def add_task():
    if request.method == 'POST':
        title = request.form['title']
        description = request.form['description']
        priority = request.form['priority']
        due_date = request.form['due_date']
        status = request.form['status']
        
        db = get_db()
        cursor = db.cursor()
        cursor.execute(
            "INSERT INTO tasks (title, description, status, priority, due_date, user_id) VALUES (?, ?, ?, ?, ?, ?)",
            (title, description, status, priority, due_date, session['user_id'])
        )
        db.commit()
        db.close()
        
        return redirect(url_for('home'))
    
    return render_template('add_task.html')

@app.route('/edit_task/<int:task_id>', methods=['GET', 'POST'])
@login_required
def edit_task(task_id):
    db = get_db()
    cursor = db.cursor()
    
    if request.method == 'POST':
        title = request.form['title']
        description = request.form['description']
        priority = request.form['priority']
        due_date = request.form['due_date']
        status = request.form['status']
        
        cursor.execute(
            "UPDATE tasks SET title = ?, description = ?, status = ?, priority = ?, due_date = ? WHERE id = ? AND user_id = ?",
            (title, description, status, priority, due_date, task_id, session['user_id'])
        )
        db.commit()
        db.close()
        
        return redirect(url_for('home'))
    
    cursor.execute("SELECT * FROM tasks WHERE id = ? AND user_id = ?", (task_id, session['user_id']))
    task = cursor.fetchone()
    db.close()
    
    if not task:
        return redirect(url_for('home'))
    
    return render_template('edit_task.html', task=task)

@app.route('/delete_task/<int:task_id>')
@login_required
def delete_task(task_id):
    db = get_db()
    cursor = db.cursor()
    cursor.execute("DELETE FROM tasks WHERE id = ? AND user_id = ?", (task_id, session['user_id']))
    db.commit()
    db.close()
    
    return redirect(url_for('home'))

# API Routes for potential future use
@app.route('/api/tasks', methods=['GET'])
def api_get_tasks():
    if not is_logged_in():
        return jsonify({"error": "Authentication required"}), 401
    
    db = get_db()
    cursor = db.cursor()
    cursor.execute("SELECT * FROM tasks WHERE user_id = ?", (session['user_id'],))
    tasks = cursor.fetchall()
    db.close()
    
    tasks_list = []
    for task in tasks:
        tasks_list.append({
            'id': task['id'],
            'title': task['title'],
            'description': task['description'],
            'status': task['status'],
            'priority': task['priority'],
            'due_date': task['due_date'],
            'created_at': task['created_at']
        })
    
    return jsonify(tasks_list)

@app.route('/api/tasks', methods=['POST'])
def api_add_task():
    if not is_logged_in():
        return jsonify({"error": "Authentication required"}), 401
    
    data = request.get_json()
    
    if not data or 'title' not in data:
        return jsonify({"error": "Title is required"}), 400
    
    title = data.get('title')
    description = data.get('description', '')
    status = data.get('status', 'todo')
    priority = data.get('priority', 'medium')
    due_date = data.get('due_date', '')
    
    db = get_db()
    cursor = db.cursor()
    cursor.execute(
        "INSERT INTO tasks (title, description, status, priority, due_date, user_id) VALUES (?, ?, ?, ?, ?, ?)",
        (title, description, status, priority, due_date, session['user_id'])
    )
    task_id = cursor.lastrowid
    db.commit()
    db.close()
    
    return jsonify({
        'id': task_id,
        'title': title,
        'description': description,
        'status': status,
        'priority': priority,
        'due_date': due_date,
        'user_id': session['user_id']
    }), 201

if __name__ == '__main__':
    app.run(debug=True)