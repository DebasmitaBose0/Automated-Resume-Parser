#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Simple Flask server starter with proper error handling and keeping process alive
"""
import os
import sys
import time

def main():
    try:
        print("Initializing Resume Parser...", flush=True)
        
        from app import create_app
        app = create_app()
        
        print("[OK] App created successfully", flush=True)
        
        with app.app_context():
            from app.extensions import db
            from app.models import User
            
            # Create database tables
            db.create_all()
            print("[OK] Database tables created successfully!", flush=True)
            
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
                print("[OK] Default admin user created!", flush=True)
                print("     Username: admin", flush=True)
                print("     Password: admin123", flush=True)
        
        print("\n" + "="*70, flush=True)
        print("Resume Parser Server", flush=True)
        print("="*70, flush=True)
        print("Server ready at:", flush=True)
        print("  -> http://localhost:5000", flush=True)
        print("  -> http://127.0.0.1:5000", flush=True)
        print("\nPress Ctrl+C to stop", flush=True)
        print("="*70 + "\n", flush=True)
        
        # Run the Flask app
        print(" * Starting Flask development server...", flush=True)
        app.run(
            host='0.0.0.0',
            port=5000,
            debug=False,
            use_reloader=False,
            threaded=True
        )
        
    except KeyboardInterrupt:
        print("\n\nServer stopped by user.", flush=True)
        sys.exit(0)
    except Exception as e:
        print(f"\n[ERROR] {e}", flush=True)
        import traceback
        traceback.print_exc()
        sys.exit(1)

if __name__ == '__main__':
    main()
