#!/usr/bin/env python
"""Test extraction directly without server."""

import sys
sys.path.insert(0, '/Resumeparser')

from app.services.resume_extractor import ResumeExtractor

# Test with a resume that has work experience
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
Python, Java, JavaScript
"""

print("=" * 70)
print("Testing Experience Extraction")
print("=" * 70)

extractor = ResumeExtractor()
results = extractor.extract_all(sample_resume)

print("\n✓ EXPERIENCE:")
if results.get('experience'):
    for exp in results.get('experience', []):
        print(f"\n  Job Title: {exp.get('job_title')}")
        print(f"  Company: {exp.get('company')}")
        print(f"  Years: {exp.get('start_date')} - {exp.get('end_date')}")
        print(f"  Current: {exp.get('is_current')}")
        if exp.get('description'):
            print(f"  Description: {exp.get('description')}")
else:
    print("  NO EXPERIENCE FOUND")

print("\n✓ EDUCATION:")
if results.get('education'):
    for edu in results.get('education', []):
        print(f"\n  Degree: {edu.get('degree')}")
        print(f"  Field: {edu.get('field_of_study')}")
        print(f"  Institution: {edu.get('institution')}")
else:
    print("  NO EDUCATION FOUND")

print("\n" + "=" * 70)
