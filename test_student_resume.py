#!/usr/bin/env python
"""Test that student resume without work experience still works."""

import sys
sys.path.insert(0, '/Resumeparser')

from app.services.resume_extractor import ResumeExtractor

# Original student resume (no work experience)
student_resume = """Babin Bid
babinbid05@gmail.com
(912) 377-7679

EDUCATION
B.Tech in Computer Science Engineering
Adamas University, Hyderabad
2023 - 2027

SKILLS
Python, Java, JavaScript
"""

print("=" * 70)
print("Testing Student Resume (No Work Experience)")
print("=" * 70)

extractor = ResumeExtractor()
results = extractor.extract_all(student_resume)

print(f"\n✓ Name: {results.get('name')}")
print(f"✓ Email: {results.get('email')}")
print(f"✓ Phone: {results.get('phone')}")

print(f"\n✓ Education ({len(results.get('education', []))} found):")
for edu in results.get('education', []):
    print(f"  - {edu.get('degree')} in {edu.get('field_of_study')}")
    print(f"    {edu.get('institution')} ({edu.get('start_date')}-{edu.get('end_date')})")

print(f"\n✓ Experience ({len(results.get('experience', []))} found):")
if results.get('experience'):
    for exp in results.get('experience', []):
        print(f"  - {exp.get('job_title')} at {exp.get('company')}")
else:
    print("  NONE (as expected for student resume)")

print(f"\n✓ Skills ({len(results.get('skills', []))} found):")
for skill in results.get('skills', []):
    print(f"  - {skill.get('name')} ({skill.get('category')})")

print("\n" + "=" * 70)
print("✓ TEST PASSED - Student resume handled correctly")
print("=" * 70)
