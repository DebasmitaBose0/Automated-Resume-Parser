#!/usr/bin/env python
"""Debug extraction."""

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
print("DEBUG: Checking section split")
print("=" * 70)

extractor = ResumeExtractor()
sections = extractor._split_into_sections(sample_resume)

for i, section in enumerate(sections):
    print(f"\n--- SECTION {i} ---")
    print(section[:200])
    print("---")

print("\n" + "=" * 70)
print("DEBUG: Checking experience extraction")
print("=" * 70)

experience = extractor.extract_experience(sample_resume)
for i, exp in enumerate(experience):
    print(f"\nEntry {i}:")
    print(f"  Job Title: {exp.get('job_title')}")
    print(f"  Company: {exp.get('company')}")
    print(f"  Dates: {exp.get('start_date')} - {exp.get('end_date')}")
    print(f"  Description: {exp.get('description')[:100] if exp.get('description') else 'None'}")
