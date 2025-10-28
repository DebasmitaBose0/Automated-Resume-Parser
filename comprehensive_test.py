#!/usr/bin/env python
"""Create a comprehensive test resume for detailed extraction testing."""

import os
import sys

sys.path.insert(0, '/Resumeparser')

# Clean old database
db_path = '/Resumeparser/instance/app.db'
if os.path.exists(db_path):
    os.remove(db_path)
    print("✓ Cleaned database")

from app import create_app
from app.extensions import db
from app.models import Candidate, Education, Experience, Skill
from app.services.resume_extractor import ResumeExtractor

app = create_app()

comprehensive_resume = """JOHN MICHAEL ANDERSON
john.anderson@email.com | (555) 123-4567 | San Francisco, CA
LinkedIn: linkedin.com/in/johnanderson | GitHub: github.com/johnanderson

PROFESSIONAL SUMMARY
Results-driven Full Stack Developer with 8+ years of experience designing and implementing scalable web applications. 
Proven expertise in cloud architecture, microservices, and team leadership. Passionate about clean code and continuous improvement.

WORK EXPERIENCE

Senior Software Engineer
Tech Innovations Inc., San Francisco, CA
2021 - Present
Led development of microservices architecture serving 2M+ daily active users using Node.js and PostgreSQL.
Mentored team of 5 junior developers and conducted code reviews to ensure code quality standards.
Implemented automated testing suite increasing test coverage from 45% to 92%.
Optimized database queries reducing API response time by 40%.

Full Stack Developer
Digital Solutions Corp., San Jose, CA
2018 - 2021
Developed and maintained 15+ customer-facing web applications using React and Python Django.
Designed RESTful APIs consumed by mobile and web clients with 99.9% uptime.
Migrated legacy monolithic application to microservices architecture.
Collaborated with cross-functional teams to deliver projects 15% ahead of schedule.

Junior Developer
StartUp Innovations LLC., Palo Alto, CA
2016 - 2018
Built responsive web applications using HTML, CSS, JavaScript, and React.
Fixed critical production bugs and improved application stability.
Contributed to documentation and best practices for development team.

EDUCATION

Master of Science in Computer Science
Stanford University, Stanford, CA
2016 - 2018
GPA: 3.8/4.0
Specialization: Software Engineering and Distributed Systems

Bachelor of Science in Information Technology
University of California Berkeley, Berkeley, CA
2012 - 2016
GPA: 3.7/4.0
Dean's List: All Semesters

TECHNICAL SKILLS
Languages: Python, JavaScript, Java, SQL, HTML, CSS, TypeScript, Go
Frameworks: React, Django, Node.js, Express, Vue.js, Spring Boot
Databases: PostgreSQL, MongoDB, Redis, MySQL, Elasticsearch
Cloud & DevOps: AWS, Docker, Kubernetes, Jenkins, GitHub Actions, Terraform
Tools: Git, JIRA, Confluence, VS Code, IntelliJ IDEA, Postman

SOFT SKILLS
Leadership | Team Management | Problem Solving | Communication | Project Management
Critical Thinking | Mentoring | Agile Methodology | Adaptability | Time Management
"""

with app.app_context():
    db.create_all()
    print("✓ Database created")
    
    # Extract
    extractor = ResumeExtractor()
    extracted = extractor.extract_all(comprehensive_resume)
    
    print("\n" + "="*70)
    print("EXTRACTED DATA")
    print("="*70)
    
    print(f"\nName: {extracted['name']}")
    print(f"Email: {extracted['email']}")
    print(f"Phone: {extracted['phone']}")
    print(f"Location: {extracted['location']}")
    print(f"\nSummary: {extracted['summary'][:100] if extracted['summary'] else 'None'}...")
    
    # Store in database
    candidate = Candidate(
        name=extracted['name'],
        email=extracted['email'],
        phone=extracted['phone'],
        summary=extracted['summary'],
        location=extracted['location'],
        raw_text=comprehensive_resume,
        original_filename='john_anderson_resume.txt',
        file_type='txt'
    )
    
    db.session.add(candidate)
    db.session.commit()
    print(f"\n✓ Candidate created (ID: {candidate.id})")
    
    # Add education
    for edu in extracted['education']:
        education = Education(
            candidate_id=candidate.id,
            degree=edu['degree'],
            field_of_study=edu['field_of_study'],
            institution=edu['institution'],
            location=edu.get('location'),
            start_date=edu['start_date'],
            end_date=edu['end_date'],
            gpa=edu.get('gpa'),
            description=edu.get('description')
        )
        db.session.add(education)
    
    # Add experience
    for exp in extracted['experience']:
        experience = Experience(
            candidate_id=candidate.id,
            job_title=exp['job_title'],
            company=exp['company'],
            location=exp.get('location'),
            start_date=exp['start_date'],
            end_date=exp['end_date'],
            is_current=exp['is_current'],
            description=exp['description']
        )
        db.session.add(experience)
    
    # Add skills
    for skill in extracted['skills']:
        skill_obj = Skill(
            candidate_id=candidate.id,
            name=skill['name'],
            category=skill['category'],
            proficiency=skill.get('proficiency')
        )
        db.session.add(skill_obj)
    
    db.session.commit()
    print("✓ Education, experience, and skills saved")
    
    # Summary
    print("\n" + "="*70)
    print("SUMMARY")
    print("="*70)
    print(f"Education: {len(extracted['education'])} degree(s)")
    print(f"Experience: {len(extracted['experience'])} position(s)")
    print(f"Skills: {len(extracted['skills'])} skill(s)")
    print(f"\nCandidate ID: {candidate.id}")
    print("\nView at: http://localhost:5000/candidate/" + str(candidate.id))
    print("="*70)
