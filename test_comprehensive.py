#!/usr/bin/env python
"""Test comprehensive resume extraction with all details."""

import sys
sys.path.insert(0, '/Resumeparser')

from app.services.resume_extractor import ResumeExtractor

# Comprehensive resume with all details
comprehensive_resume = """John Michael Anderson
john.anderson@email.com
(555) 123-4567
New York, NY

PROFESSIONAL SUMMARY
Experienced Software Engineer with 8+ years of expertise in full-stack development, cloud architecture, and team leadership. Proven track record of delivering scalable solutions for Fortune 500 companies. Passionate about mentoring junior developers and implementing best practices.

WORK EXPERIENCE

Senior Software Engineer
Tech Innovations Corp
New York, NY
January 2021 - Present
Led development and architecture of microservices platform serving 10M+ users daily. Managed team of 5 engineers implementing CI/CD pipelines. Reduced deployment time by 70% through automation. Mentored 3 junior developers. Tech stack: Python, Kubernetes, AWS.

Senior Developer
CloudFirst Solutions
San Francisco, CA
June 2018 - December 2020
Architected cloud migration strategy for legacy systems. Implemented RESTful APIs handling 500K requests/day. Improved system performance by 45% through database optimization. Led code reviews and best practices workshops.

Full Stack Developer
WebDev Startup
Boston, MA
March 2016 - May 2018
Developed responsive web applications using React and Node.js. Built microservices in Python and Go. Implemented real-time data processing using Apache Kafka. Designed PostgreSQL database schemas.

Junior Developer
Digital Solutions Inc
Philadelphia, PA
July 2015 - February 2016
Contributed to web application development using JavaScript and jQuery. Learned agile methodologies and version control. Supported senior developers in bug fixes and feature implementation.

EDUCATION

Master of Science in Computer Science
Stanford University, Stanford, CA
Expected: May 2024
Specialization: Machine Learning and Artificial Intelligence
GPA: 3.8/4.0
Relevant Courses: Deep Learning, Natural Language Processing, Computer Vision

Bachelor of Science in Computer Engineering
MIT (Massachusetts Institute of Technology)
Graduated: May 2015
GPA: 3.9/4.0
Honors: Cum Laude, Dean's List all semesters
Relevant Coursework: Data Structures, Algorithms, Operating Systems, Computer Networks

TECHNICAL SKILLS
Programming Languages: Python, Java, JavaScript, C++, Go, Rust, SQL
Web Frameworks: Django, Flask, React, Angular, Vue.js, Node.js
Databases: PostgreSQL, MongoDB, MySQL, Redis, Elasticsearch
Cloud Platforms: AWS (EC2, S3, Lambda, RDS), Google Cloud Platform, Azure
DevOps Tools: Docker, Kubernetes, Jenkins, GitLab CI/CD, Terraform
Tools & Technologies: Git, Jira, Confluence, Slack, Linux, Nginx

SOFT SKILLS
Leadership: Team management, mentoring, code review guidance
Communication: Technical documentation, presentations, stakeholder management
Problem Solving: Analytical thinking, debugging complex systems, optimization
Teamwork: Agile/Scrum methodologies, cross-functional collaboration
Adaptability: Quick learner, stays updated with latest technologies

CERTIFICATIONS
AWS Certified Solutions Architect - Professional
Certified Kubernetes Administrator (CKA)
Google Cloud Certified - Professional Data Engineer
Certified Scrum Master (CSM)

PROJECTS
Real-time Analytics Platform
Designed and built scalable analytics platform processing 100M events/day. Implemented data pipeline using Kafka, Spark, and Elasticsearch. Results: 40% faster query processing.

AI-Powered Recommendation Engine
Developed machine learning model for product recommendations. Increased user engagement by 35%. Tech: Python, TensorFlow, PostgreSQL.

Open Source Contributions
Active contributor to Kubernetes and Docker projects. 50+ merged pull requests. Recognized as top contributor in 2023.

LANGUAGES
English: Native
Spanish: Fluent
Mandarin: Conversational

AWARDS & RECOGNITION
Employee of the Year - Tech Innovations Corp (2022)
Innovation Award - CloudFirst Solutions (2019)
"""

print("=" * 80)
print("COMPREHENSIVE RESUME EXTRACTION TEST")
print("=" * 80)

extractor = ResumeExtractor()
results = extractor.extract_all(comprehensive_resume)

print("\n" + "=" * 80)
print("CONTACT INFORMATION")
print("=" * 80)
print(f"Name: {results.get('name')}")
print(f"Email: {results.get('email')}")
print(f"Phone: {results.get('phone')}")
print(f"Location: {results.get('location')}")

print("\n" + "=" * 80)
print("PROFESSIONAL SUMMARY")
print("=" * 80)
if results.get('summary'):
    print(results.get('summary')[:200] + "...")
else:
    print("NOT EXTRACTED")

print("\n" + "=" * 80)
print(f"WORK EXPERIENCE ({len(results.get('experience', []))} positions)")
print("=" * 80)
for i, exp in enumerate(results.get('experience', []), 1):
    print(f"\n{i}. {exp.get('job_title')}")
    print(f"   Company: {exp.get('company')}")
    print(f"   Location: {exp.get('location', 'N/A')}")
    print(f"   Dates: {exp.get('start_date')} - {exp.get('end_date') or 'Present'}")
    print(f"   Current: {exp.get('is_current')}")
    if exp.get('description'):
        print(f"   Description: {exp.get('description')[:100]}...")

print("\n" + "=" * 80)
print(f"EDUCATION ({len(results.get('education', []))} degrees)")
print("=" * 80)
for i, edu in enumerate(results.get('education', []), 1):
    print(f"\n{i}. {edu.get('degree')} in {edu.get('field_of_study')}")
    print(f"   Institution: {edu.get('institution')}")
    print(f"   Duration: {edu.get('start_date')} - {edu.get('end_date')}")
    if edu.get('gpa'):
        print(f"   GPA: {edu.get('gpa')}")
    if edu.get('description'):
        print(f"   Details: {edu.get('description')}")

print("\n" + "=" * 80)
print(f"SKILLS ({len(results.get('skills', []))} total)")
print("=" * 80)

# Group by category
skills_by_cat = {}
for skill in results.get('skills', []):
    cat = skill.get('category', 'Other')
    if cat not in skills_by_cat:
        skills_by_cat[cat] = []
    skills_by_cat[cat].append(skill.get('name'))

for category, skills in sorted(skills_by_cat.items()):
    print(f"\n{category.upper()} ({len(skills)}):")
    print(f"  {', '.join(skills)}")

print("\n" + "=" * 80)
print("EXTRACTION SUMMARY")
print("=" * 80)
print(f"✓ Contact Info: Name, Email, Phone, Location")
print(f"✓ Professional Summary: {'YES' if results.get('summary') else 'NO'}")
print(f"✓ Work Experience: {len(results.get('experience', []))} positions")
print(f"✓ Education: {len(results.get('education', []))} degrees")
print(f"✓ Skills: {len(results.get('skills', []))} skills")
print(f"✓ Total Skill Categories: {len(skills_by_cat)}")
print("=" * 80)
