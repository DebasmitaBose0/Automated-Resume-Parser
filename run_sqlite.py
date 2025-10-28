#!/usr/bin/env python3
"""
Run the Resume Parser application with SQLite for testing
"""

from app import create_app
from app.models import db
from config_sqlite import Config

def create_test_app():
    """Create app with SQLite configuration for testing."""
    app = create_app(Config)
    return app

if __name__ == '__main__':
    app = create_test_app()
    
    with app.app_context():
        # Create database tables
        db.create_all()
        print("Database tables created successfully!")
    
    print("Starting Resume Parser on http://localhost:5000")
    print("Press Ctrl+C to stop the server")
    
    app.run(debug=True, host='0.0.0.0', port=5000)