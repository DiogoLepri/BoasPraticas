from flask import Flask
from app_original import init_db
from app.db import init_db
from app.config import Config


def create_app(config_class=Config):
    """Create and configure the Flask application"""
    app = Flask(__name__)
    app.config.from_object(config_class)
    
    # Initialize database
    with app.app_context():  # Adicione esta linha
        init_db()           # Agora init_db() está dentro do contexto da aplicação
    
    # Register blueprints
    from app.auth.routes import auth_bp
    from app.tasks.routes import tasks_bp
    
    app.register_blueprint(auth_bp)
    app.register_blueprint(tasks_bp)
    
    return app