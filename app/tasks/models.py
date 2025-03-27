"""
Task data models and database operations
"""
from app.db import get_db


def get_user_tasks(user_id):
    """
    Get all tasks for a specific user
    
    Args:
        user_id (int): The user ID
        
    Returns:
        list: List of task dictionaries
    """
    db = get_db()
    cursor = db.cursor()
    cursor.execute("SELECT * FROM tasks WHERE user_id = ? ORDER BY due_date", (user_id,))
    tasks = cursor.fetchall()
    return tasks


def get_task(task_id, user_id):
    """
    Get a specific task
    
    Args:
        task_id (int): The task ID
        user_id (int): The user ID (for security)
        
    Returns:
        dict: Task details or None if not found
    """
    db = get_db()
    cursor = db.cursor()
    cursor.execute("SELECT * FROM tasks WHERE id = ? AND user_id = ?", (task_id, user_id))
    return cursor.fetchone()


def create_task(title, description, status, priority, due_date, user_id):
    """
    Create a new task
    
    Args:
        title (str): Task title
        description (str): Task description
        status (str): Task status
        priority (str): Task priority
        due_date (str): Task due date
        user_id (int): User ID
        
    Returns:
        int: ID of the created task
    """
    db = get_db()
    cursor = db.cursor()
    cursor.execute(
        "INSERT INTO tasks (title, description, status, priority, due_date, user_id) VALUES (?, ?, ?, ?, ?, ?)",
        (title, description, status, priority, due_date, user_id)
    )
    task_id = cursor.lastrowid
    db.commit()
    return task_id


def update_task(task_id, title, description, status, priority, due_date, user_id):
    """
    Update an existing task
    
    Args:
        task_id (int): Task ID
        title (str): Task title
        description (str): Task description
        status (str): Task status
        priority (str): Task priority
        due_date (str): Task due date
        user_id (int): User ID
        
    Returns:
        bool: True if successful, False otherwise
    """
    db = get_db()
    cursor = db.cursor()
    cursor.execute(
        "UPDATE tasks SET title = ?, description = ?, status = ?, priority = ?, due_date = ? WHERE id = ? AND user_id = ?",
        (title, description, status, priority, due_date, task_id, user_id)
    )
    db.commit()
    return cursor.rowcount > 0


def delete_task(task_id, user_id):
    """
    Delete a task
    
    Args:
        task_id (int): Task ID
        user_id (int): User ID
        
    Returns:
        bool: True if successful, False otherwise
    """
    db = get_db()
    cursor = db.cursor()
    cursor.execute("DELETE FROM tasks WHERE id = ? AND user_id = ?", (task_id, user_id))
    db.commit()
    return cursor.rowcount > 0