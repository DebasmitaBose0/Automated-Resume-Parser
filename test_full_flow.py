#!/usr/bin/env python
"""Test full extraction and database storage."""

import os
import sys
import shutil

sys.path.insert(0, '/Resumeparser')

# Clean up old database
db_path = '/Resumeparser/instance/app.db'
if os.path.exists(db_path):
    os.remove(db_path)
    print("✓ Removed old database")

# Import after cleanup
from app import create_app
from app.models import Candidate, Education, Experience, Skill
from app.services.resume_extractor import ResumeExtractor

# Create app
app = create_app()

# Create database
with app.app_context():
    from app.extensions import db
    db.create_all()
    print("✓ Database created")
    
    # Sample resume with work experience
    sample_resume = """Babin Bid
babinbid05@gmail.com
(912) 377-7679

WORK EXPERIENCE
Senior Developer
Tech Solutions Inc.
2021 - 2023
Led development of microservices architecture.

Junior Developer
StartUp Co.
2019 - 2021
Developed web applications using Python.

EDUCATION
B.Tech in Computer Science Engineering
Adamas University, Hyderabad
2023 - 2027

SKILLS
Python, Java, JavaScript, Leadership
"""

    # Extract
    extractor = ResumeExtractor()
    extracted = extractor.extract_all(sample_resume)
    
    print("\n✓ Extracted data:")
    print(f"  Name: {extracted['name']}")
    print(f"  Email: {extracted['email']}")
    print(f"  Skills: {len(extracted['skills'])} found")
    print(f"  Education: {len(extracted['education'])} found")
    print(f"  Experience: {len(extracted['experience'])} found")
    
    # Store in database
    candidate = Candidate(
        name=extracted['name'],
        email=extracted['email'],
        phone=extracted['phone'],
        summary=extracted['summary'],
        location=extracted['location'],
        raw_text=sample_resume,
        original_filename='test_resume.txt',
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
            start_date=edu['start_date'],
            end_date=edu['end_date']
        )
        db.session.add(education)
    
    # Add experience
    for exp in extracted['experience']:
        experience = Experience(
            candidate_id=candidate.id,
            job_title=exp['job_title'],
            company=exp['company'],
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
            category=skill['category']
        )
        db.session.add(skill_obj)
    
    db.session.commit()
    print("✓ Education, experience, and skills saved")
    
    # Query back
    candidate = Candidate.query.filter_by(name='Babin Bid').first()
    print(f"\n✓ Retrieved candidate: {candidate.name}")
    print(f"  Education entries: {len(candidate.educations)}")
    for edu in candidate.educations:
        print(f"    - {edu.degree} in {edu.field_of_study} ({edu.start_date}-{edu.end_date})")
    
    print(f"  Experience entries: {len(candidate.experiences)}")
    for exp in candidate.experiences:
        print(f"    - {exp.job_title} at {exp.company} ({exp.start_date}-{exp.end_date})")
        if exp.description:
            print(f"      {exp.description[:50]}")
    
    print(f"  Skills: {len(candidate.skills)}")
    for skill in candidate.skills:
        print(f"    - {skill.name} ({skill.category})")
