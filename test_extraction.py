#!/usr/bin/env python
"""Test script to verify resume extraction improvements."""

from app.services.resume_extractor import ResumeExtractor

# Sample resume text similar to what was showing as "Unknown"
sample_resume = """
Babin Bid
babin.bid@example.com
+1-555-0123

EDUCATION
B.Tech in Computer Science Engineering
Bit Institute of Technology, Hyderabad
2018 - 2022
GPA: 3.8/4.0

ABOUT ME
Innovative software engineer with passion for building scalable applications.
Experienced in full-stack development and cloud technologies.

TECHNICAL SKILLS
Python, Java, JavaScript, React, Django, Flask, AWS, Docker, Kubernetes

WORK EXPERIENCE
Senior Developer
Tech Corp Solutions
2022 - Present
Led development of microservices architecture and managed team of 5 developers.
"""

print("=" * 60)
print("Testing Resume Extraction")
print("=" * 60)

extractor = ResumeExtractor()
results = extractor.extract_all(sample_resume)

print("\n✓ NAME EXTRACTION:")
print(f"  Extracted: {results.get('name')}")

print("\n✓ CONTACT INFO:")
print(f"  Email: {results.get('email')}")
print(f"  Phone: {results.get('phone')}")

print("\n✓ EDUCATION:")
for edu in results.get('education', []):
    print(f"  Degree: {edu.get('degree')}")
    print(f"  Field: {edu.get('field_of_study')}")
    print(f"  Institution: {edu.get('institution')}")
    print(f"  Years: {edu.get('start_date')} - {edu.get('end_date')}")

print("\n✓ SUMMARY:")
print(f"  {results.get('summary')}")

print("\n✓ SKILLS (first 5):")
for skill in results.get('skills', [])[:5]:
    print(f"  - {skill['name']} ({skill['category']})")

print("\n✓ EXPERIENCE:")
for exp in results.get('experience', []):
    print(f"  Position: {exp.get('job_title')}")
    print(f"  Company: {exp.get('company')}")
    print(f"  Years: {exp.get('start_date')} - {exp.get('end_date')}")

print("\n" + "=" * 60)
print("✅ Extraction Test Complete")
print("=" * 60)
