#!/usr/bin/env python3
"""
Demo script for Resume Parser
This script demonstrates the key functionality of the resume parser.
"""

import os
import sys
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app.services.document_parser import DocumentParser
from app.services.resume_extractor import ResumeExtractor

def demo_text_extraction():
    """Demo text extraction from different file types."""
    print("=" * 60)
    print("DEMO: Document Text Extraction")
    print("=" * 60)
    
    parser = DocumentParser()
    
    # Demo with sample text (simulating a PDF extraction)
    sample_resume_text = """
    John Smith
    Software Engineer
    
    Email: john.smith@email.com
    Phone: (555) 123-4567
    Location: San Francisco, CA
    
    SUMMARY
    Experienced software engineer with 5+ years of experience in full-stack development.
    Passionate about creating scalable web applications and leading development teams.
    
    EXPERIENCE
    Senior Software Engineer
    Tech Solutions Inc. | San Francisco, CA
    January 2020 - Present
    
    • Lead development of microservices architecture using Python and Docker
    • Managed team of 4 junior developers
    • Improved application performance by 40%
    
    Software Engineer
    StartupCorp | San Francisco, CA
    June 2018 - December 2019
    
    • Developed web applications using React and Node.js
    • Implemented CI/CD pipelines using Jenkins
    • Collaborated with design team on user interface improvements
    
    EDUCATION
    Bachelor of Science in Computer Science
    Stanford University | Stanford, CA
    2014 - 2018
    GPA: 3.8
    
    SKILLS
    Programming Languages: Python, JavaScript, Java, C++
    Frameworks: React, Django, Flask, Node.js
    Databases: PostgreSQL, MongoDB, Redis
    Tools: Docker, Kubernetes, AWS, Git, Jenkins
    """
    
    print("Sample Resume Text (first 200 characters):")
    print("-" * 40)
    print(sample_resume_text[:200] + "...")
    
    # Clean the text
    cleaned_text = parser.clean_text(sample_resume_text)
    print(f"\nCleaned text length: {len(cleaned_text)} characters")
    
    return cleaned_text

def demo_information_extraction(text):
    """Demo information extraction using NLP."""
    print("\n" + "=" * 60)
    print("DEMO: Information Extraction")
    print("=" * 60)
    
    extractor = ResumeExtractor()
    
    # Extract all information
    print("Extracting information from resume text...")
    extracted_data = extractor.extract_all(text)
    
    # Display results
    print("\n📋 EXTRACTED INFORMATION:")
    print("-" * 40)
    
    print(f"👤 Name: {extracted_data.get('name', 'Not detected')}")
    print(f"📧 Email: {extracted_data.get('email', 'Not detected')}")
    print(f"📞 Phone: {extracted_data.get('phone', 'Not detected')}")
    print(f"📍 Location: {extracted_data.get('location', 'Not detected')}")
    
    if extracted_data.get('summary'):
        print(f"\n📝 Summary:")
        print(f"   {extracted_data['summary'][:100]}...")
    
    # Skills
    skills = extracted_data.get('skills', [])
    if skills:
        print(f"\n🛠️  Skills ({len(skills)} found):")
        for skill in skills[:10]:  # Show first 10 skills
            print(f"   • {skill['name']} ({skill['category']})")
        if len(skills) > 10:
            print(f"   ... and {len(skills) - 10} more")
    
    # Experience
    experiences = extracted_data.get('experience', [])
    if experiences:
        print(f"\n💼 Work Experience ({len(experiences)} positions):")
        for i, exp in enumerate(experiences, 1):
            print(f"   {i}. {exp.get('job_title', 'Position')} at {exp.get('company', 'Company')}")
            if exp.get('start_date') or exp.get('end_date'):
                start = exp.get('start_date', 'Start')
                end = 'Present' if exp.get('is_current') else exp.get('end_date', 'End')
                print(f"      ({start} - {end})")
    
    # Education
    educations = extracted_data.get('education', [])
    if educations:
        print(f"\n🎓 Education ({len(educations)} entries):")
        for i, edu in enumerate(educations, 1):
            degree = edu.get('degree', 'Degree')
            institution = edu.get('institution', 'Institution')
            print(f"   {i}. {degree} from {institution}")
            if edu.get('start_date') or edu.get('end_date'):
                start = edu.get('start_date', 'Start')
                end = edu.get('end_date', 'End')
                print(f"      ({start} - {end})")
    
    return extracted_data

def demo_api_usage():
    """Demo API usage examples."""
    print("\n" + "=" * 60)
    print("DEMO: API Usage Examples")
    print("=" * 60)
    
    print("""
🚀 REST API Endpoints:

1. Upload Resume:
   POST /api/upload
   Content-Type: multipart/form-data
   Body: file=resume.pdf
   
   Response: {
     "message": "Resume processed successfully",
     "candidate_id": 1,
     "candidate": { ... extracted data ... }
   }

2. Get All Candidates:
   GET /api/candidates?page=1&per_page=10
   
   Response: {
     "candidates": [...],
     "total": 50,
     "pages": 5,
     "current_page": 1
   }

3. Search Candidates:
   GET /api/search?q=python
   
   Response: {
     "candidates": [...],
     "total": 15,
     "query": "python"
   }

4. Get Candidate Details:
   GET /api/candidates/1
   
   Response: {
     "id": 1,
     "name": "John Smith",
     "email": "john.smith@email.com",
     ...
   }

5. Get Statistics:
   GET /api/stats
   
   Response: {
     "total_candidates": 100,
     "total_skills": 250,
     "top_skills": [...],
     "top_companies": [...]
   }
""")

def demo_web_interface():
    """Demo web interface features."""
    print("\n" + "=" * 60)
    print("DEMO: Web Interface Features")
    print("=" * 60)
    
    print("""
🌐 Web Interface Features:

1. 🏠 Home Page (/)
   • Overview and statistics dashboard
   • Quick access to all features
   • Real-time stats loading

2. 📤 Upload Page (/upload)
   • Drag & drop file upload
   • Real-time processing feedback
   • Immediate results display
   • Supported formats: PDF, DOC, DOCX

3. 👥 Candidates Page (/candidates)
   • Paginated candidate list
   • Advanced filtering options
   • Sortable columns
   • Quick actions (view, delete)

4. 🔍 Search Page (/search)
   • Full-text search across all fields
   • Highlighted search results
   • Advanced search capabilities
   • Search suggestions

5. 👤 Candidate Details (/candidate/<id>)
   • Complete candidate profile
   • Organized information display
   • Export options
   • Edit capabilities

Features:
✅ Responsive design (mobile-friendly)
✅ Real-time updates
✅ Error handling and validation
✅ Secure file handling
✅ Progress indicators
✅ Accessibility support
""")

def main():
    """Main demo function."""
    print("🤖 RESUME PARSER DEMONSTRATION")
    print("=" * 60)
    print("This demo shows the core functionality of the Resume Parser system.")
    print("The system extracts structured information from resumes using AI/NLP.")
    
    try:
        # Demo 1: Text extraction
        sample_text = demo_text_extraction()
        
        # Demo 2: Information extraction
        extracted_data = demo_information_extraction(sample_text)
        
        # Demo 3: API usage
        demo_api_usage()
        
        # Demo 4: Web interface
        demo_web_interface()
        
        print("\n" + "=" * 60)
        print("✅ DEMO COMPLETED SUCCESSFULLY!")
        print("=" * 60)
        print("""
🚀 Next Steps:

1. Start the application:
   python run.py

2. Open your browser:
   http://localhost:5000

3. Upload sample resumes and explore the features!

4. Check the API documentation in README.md

5. Customize the extraction logic in:
   app/services/resume_extractor.py
""")
        
    except Exception as e:
        print(f"\n❌ Demo failed: {str(e)}")
        print("Please check that all dependencies are installed correctly.")
        return 1
    
    return 0

if __name__ == "__main__":
    sys.exit(main())