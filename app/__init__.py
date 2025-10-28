from flask import Flask
from config import Config
import logging
import os

def create_app(config_class=Config):
    """Application factory pattern."""
    # Get the absolute path to the project root
    basedir = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
    
    app = Flask(__name__, 
                template_folder=os.path.join(basedir, 'templates'),
                static_folder=os.path.join(basedir, 'static'))
    app.config.from_object(config_class)
    
    # Initialize extensions with app
    from app.extensions import db, migrate, login_manager
    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)
    
    # Configure Flask-Login
    login_manager.login_view = 'auth.login'
    login_manager.login_message = 'Please log in to access this page.'
    login_manager.login_message_category = 'info'
    
    # User loader for Flask-Login
    @login_manager.user_loader
    def load_user(user_id):
        from app.models.user import User
        return User.query.get(int(user_id))
    
    # Configure logging
    logging.basicConfig(level=logging.INFO)
    
    # Import models to ensure they are registered with SQLAlchemy
    from app.models import models
    
    # Register blueprints
    from app.routes import api_bp, main_bp, auth_bp
    app.register_blueprint(api_bp)
    app.register_blueprint(main_bp)
    app.register_blueprint(auth_bp)
    
    return app