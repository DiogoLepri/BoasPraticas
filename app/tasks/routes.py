"""
Task management routes
"""
from flask import Blueprint, render_template, request, redirect, url_for, session, flash, jsonify

from app.tasks.models import (
    get_user_tasks, get_task, create_task, update_task, delete_task
)
from app.utils.decorators import login_required
from app.utils.helpers import is_logged_in

# Create blueprint
tasks_bp = Blueprint('tasks', __name__)


@tasks_bp.route('/')
@login_required
def index():
    """Display user's tasks"""
    tasks = get_user_tasks(session['user_id'])
    return render_template('tasks/index.html', tasks=tasks)


@tasks_bp.route('/add', methods=['GET', 'POST'])
@login_required
def add_task():
    """Add a new task"""
    if request.method == 'POST':
        title = request.form['title']
        description = request.form['description']
        priority = request.form['priority']
        due_date = request.form['due_date']
        status = request.form['status']
        
        create_task(
            title=title,
            description=description,
            status=status,
            priority=priority,
            due_date=due_date,
            user_id=session['user_id']
        )
        
        flash('Task added successfully!', 'success')
        return redirect(url_for('tasks.index'))
    
    return render_template('tasks/add.html')


@tasks_bp.route('/edit/<int:task_id>', methods=['GET', 'POST'])
@login_required
def edit_task(task_id):
    """Edit an existing task"""
    task = get_task(task_id, session['user_id'])
    
    if not task:
        flash('Task not found or you do not have permission to edit it.', 'error')
        return redirect(url_for('tasks.index'))
    
    if request.method == 'POST':
        title = request.form['title']
        description = request.form['description']
        priority = request.form['priority']
        due_date = request.form['due_date']
        status = request.form['status']
        
        success = update_task(
            task_id=task_id,
            title=title,
            description=description,
            status=status,
            priority=priority,
            due_date=due_date,
            user_id=session['user_id']
        )
        
        if success:
            flash('Task updated successfully!', 'success')
        else:
            flash('Error updating task.', 'error')
        
        return redirect(url_for('tasks.index'))
    
    return render_template('tasks/edit.html', task=task)


@tasks_bp.route('/delete/<int:task_id>')
@login_required
def delete(task_id):
    """Delete a task"""
    success = delete_task(task_id, session['user_id'])
    
    if success:
        flash('Task deleted successfully!', 'success')
    else:
        flash('Error deleting task.', 'error')
    
    return redirect(url_for('tasks.index'))


# API Routes
@tasks_bp.route('/api/tasks', methods=['GET'])
def api_get_tasks():
    """API endpoint to get user tasks"""
    if not is_logged_in():
        return jsonify({"error": "Authentication required"}), 401
    
    tasks = get_user_tasks(session['user_id'])
    
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


@tasks_bp.route('/api/tasks', methods=['POST'])
def api_add_task():
    """API endpoint to add a task"""
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
    
    task_id = create_task(
        title=title,
        description=description,
        status=status,
        priority=priority,
        due_date=due_date,
        user_id=session['user_id']
    )
    
    return jsonify({
        'id': task_id,
        'title': title,
        'description': description,
        'status': status,
        'priority': priority,
        'due_date': due_date,
        'user_id': session['user_id']
    }), 201