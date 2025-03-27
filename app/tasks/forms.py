"""
Task-related forms
"""
from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SelectField, DateField, SubmitField
from wtforms.validators import DataRequired, Length, Optional
from flask import current_app


class TaskForm(FlaskForm):
    """Form for adding or editing a task"""
    title = StringField('Title', validators=[DataRequired(), Length(min=1, max=100)])
    description = TextAreaField('Description', validators=[Optional(), Length(max=500)])
    
    status = SelectField('Status', validators=[DataRequired()], 
                        choices=[('todo', 'To Do'), 
                                ('in-progress', 'In Progress'), 
                                ('done', 'Done')])
    
    priority = SelectField('Priority', validators=[DataRequired()],
                          choices=[('low', 'Low'), 
                                  ('medium', 'Medium'), 
                                  ('high', 'High')])
    
    due_date = DateField('Due Date', validators=[Optional()], format='%Y-%m-%d')
    
    submit = SubmitField('Save Task')