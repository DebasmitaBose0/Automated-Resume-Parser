#!/usr/bin/env python
"""Test extraction with the actual resume format."""

from app.services.resume_extractor import ResumeExtractor

# This matches what's shown in the screenshot
sample_resume = """Babin Bid
babinbid05@gmail.com
(912) 377-7679

EDUCATION
B.Tech in Computer Science Engineering
Adamas University, Hyderabad
2023 - 2027
GPA: 3.8/4.0

About Me:
Passionate about leveraging technology to solve real-world problems.

TECHNICAL SKILLS
Python, Java, JavaScript, Go, Html, Css, React, Sql, Oracle, Aws, Pandas, Numpy, R, Git

SOFT SKILLS
Leadership, Communication, Problem Solving, Creative, Time Management, Adaptability, Collaboration
"""

print("=" * 70)
print("Testing Resume Extraction")
print("=" * 70)

extractor = ResumeExtractor()
results = extractor.extract_all(sample_resume)

print("\n✓ NAME:")
print(f"  {results.get('name') or 'NOT EXTRACTED'}")

print("\n✓ CONTACT:")
print(f"  Email: {results.get('email')}")
print(f"  Phone: {results.get('phone')}")

print("\n✓ EDUCATION:")
for edu in results.get('education', []):
    print(f"  Degree: {edu.get('degree')}")
    print(f"  Field: {edu.get('field_of_study') or 'N/A'}")
    print(f"  Institution: {edu.get('institution')}")
    print(f"  Years: {edu.get('start_date')} - {edu.get('end_date')}")
    print()

print("\n✓ SKILLS (Technical):")
tech_skills = [s for s in results.get('skills', []) if s['category'] == 'technical']
for skill in tech_skills[:10]:
    print(f"  - {skill['name']}")

print("\n✓ SKILLS (Soft):")
soft_skills = [s for s in results.get('skills', []) if s['category'] == 'soft']
for skill in soft_skills[:10]:
    print(f"  - {skill['name']}")

print("\n" + "=" * 70)
