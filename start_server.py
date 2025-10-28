#!/usr/bin/env python
"""
Simple server starter that keeps the Flask app running
"""
import sys
import time
from app import create_app

def main():
    print("Initializing Resume Parser...")
    app = create_app()
    
    with app.app_context():
        from app.extensions import db
        from app.models import User
        
        # Create database tables
        db.create_all()
        print("✓ Database tables created successfully!")
        
        # Create default admin user if no users exist
        if User.query.count() == 0:
            admin_user = User(
                username='admin',
                email='admin@resumeparser.com',
                first_name='Admin',
                last_name='User',
                role='admin'
            )
            admin_user.set_password('admin123')
            db.session.add(admin_user)
            db.session.commit()
            print("✓ Default admin user created!")
            print("  Username: admin")
            print("  Password: admin123")
    
    print("\n" + "="*60)
    print("Starting Resume Parser")
    print("="*60)
    print("Server running on:")
    print("  - http://localhost:5000")
    print("  - http://127.0.0.1:5000")
    print("  - http://192.168.1.33:5000")
    print("\nPress Ctrl+C to stop the server")
    print("="*60 + "\n")
    
    try:
        app.run(
            debug=False,
            host='0.0.0.0',
            port=5000,
            use_reloader=False,
            threaded=True
        )
    except KeyboardInterrupt:
        print("\nServer stopped by user")
        sys.exit(0)
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

if __name__ == '__main__':
    main()
