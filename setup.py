#!/usr/bin/env python3
"""
Setup script for Resume Parser
This script helps set up the environment and download required models.
"""

import subprocess
import sys
import os

def run_command(command, description):
    """Run a shell command and handle errors."""
    print(f"\n{description}...")
    try:
        result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
        print(f"✓ {description} completed successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"✗ Error during {description}:")
        print(f"  Command: {command}")
        print(f"  Error: {e.stderr}")
        return False

def main():
    """Main setup function."""
    print("Resume Parser Setup Script")
    print("=" * 40)
    
    # Check if we're in a virtual environment
    if not hasattr(sys, 'real_prefix') and not (hasattr(sys, 'base_prefix') and sys.base_prefix != sys.prefix):
        print("⚠️  It's recommended to run this in a virtual environment")
        response = input("Continue anyway? (y/N): ")
        if response.lower() != 'y':
            print("Setup cancelled. Please activate a virtual environment and try again.")
            return
    
    # Install requirements
    if not run_command("pip install -r requirements.txt", "Installing Python packages"):
        print("Failed to install requirements. Please check your internet connection and try again.")
        return
    
    # Download spaCy model
    print("\nDownloading spaCy English model...")
    if not run_command("python -m spacy download en_core_web_sm", "Downloading spaCy model"):
        print("Failed to download spaCy model. You may need to install it manually:")
        print("  python -m spacy download en_core_web_sm")
    
    # Download NLTK data
    print("\nDownloading NLTK data...")
    nltk_script = '''
import nltk
try:
    nltk.download('punkt')
    nltk.download('stopwords')
    nltk.download('averaged_perceptron_tagger')
    nltk.download('wordnet')
    print("NLTK data downloaded successfully")
except Exception as e:
    print(f"Error downloading NLTK data: {e}")
    '''
    
    try:
        subprocess.run([sys.executable, "-c", nltk_script], check=True)
        print("✓ NLTK data downloaded successfully")
    except subprocess.CalledProcessError:
        print("✗ Failed to download NLTK data")
    
    # Create environment file if it doesn't exist
    env_file = '.env'
    if not os.path.exists(env_file):
        print(f"\nCreating {env_file} file...")
        with open(env_file, 'w') as f:
            f.write('''# Resume Parser Configuration
DATABASE_URL=postgresql://username:password@localhost:5432/resume_parser_db
SECRET_KEY=your-secret-key-here-change-this-in-production
UPLOAD_FOLDER=uploads
MAX_CONTENT_LENGTH=16777216
ALLOWED_EXTENSIONS=pdf,doc,docx
''')
        print(f"✓ Created {env_file} file")
        print("⚠️  Please update the DATABASE_URL and SECRET_KEY in the .env file")
    
    # Create uploads directory
    uploads_dir = 'uploads'
    if not os.path.exists(uploads_dir):
        os.makedirs(uploads_dir)
        print(f"✓ Created {uploads_dir} directory")
    
    print("\n" + "=" * 40)
    print("Setup completed! Next steps:")
    print("1. Update the DATABASE_URL in .env file with your PostgreSQL credentials")
    print("2. Update the SECRET_KEY in .env file with a secure random string")
    print("3. Make sure PostgreSQL is running and the database exists")
    print("4. Run the application with: python run.py")
    print("\nThe application will be available at: http://localhost:5000")

if __name__ == "__main__":
    main()