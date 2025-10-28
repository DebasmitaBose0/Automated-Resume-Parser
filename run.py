from app import create_app

app = create_app()

if __name__ == '__main__':
    try:
        with app.app_context():
            # Import models and db after app context is available
            from app.extensions import db
            from app.models import User
            
            # Create database tables
            db.create_all()
            print("Database tables created successfully!")
            
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
                print("Default admin user created!")
                print("Username: admin")
                print("Password: admin123")
        
        print("Starting Resume Parser on http://localhost:5000")
        print("Press Ctrl+C to stop the server")
        app.run(debug=False, host='0.0.0.0', port=5000, use_reloader=False, threaded=True)
    except Exception as e:
        print(f"Error starting app: {e}")
        import traceback
        traceback.print_exc()