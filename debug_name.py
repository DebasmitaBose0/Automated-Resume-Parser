#!/usr/bin/env python
"""Debug name extraction."""

from app.services.resume_extractor import ResumeExtractor

sample_resume = """Babin Bid
babin.bid@example.com
+1-555-0123

EDUCATION
B.Tech in Computer Science Engineering
Bit Institute of Technology, Hyderabad
2018 - 2022
GPA: 3.8/4.0"""

extractor = ResumeExtractor()
lines = sample_resume.split('\n')[:15]

print("First 15 lines:")
for i, line in enumerate(lines):
    print(f"{i}: '{line}'")

print("\n" + "="*60)
print("Checking name extraction logic:")

section_keywords = ['email', 'phone', 'linkedin', 'github', 'education', 'experience', 
                   'skills', 'summary', 'objective', 'about', 'b.tech', 'b.sc', 'mba',
                   'contact', 'address', 'date', 'dob', 'male', 'female']

for i, line in enumerate(lines):
    line_stripped = line.strip()
    if not line_stripped:
        print(f"Line {i}: SKIP (empty)")
        continue
    
    if any(keyword in line_stripped.lower() for keyword in section_keywords):
        print(f"Line {i}: SKIP (has section keyword: '{line_stripped}')")
        continue
    
    if len(line_stripped) > 50:
        print(f"Line {i}: SKIP (too long: '{line_stripped}')")
        continue
    
    if '@' in line_stripped or any(char in line_stripped for char in ['http', 'www', '+', ':', '=']):
        print(f"Line {i}: SKIP (has special chars: '{line_stripped}')")
        continue
    
    words = line_stripped.split()
    if len(words) == 0 or len(words) > 4:
        print(f"Line {i}: SKIP (word count {len(words)}: '{line_stripped}')")
        continue
    
    is_valid_name = True
    for word in words:
        clean_word = word.replace('.', '').replace(',', '')
        if len(clean_word) < 2:
            print(f"Line {i}: SKIP (word too short: '{word}')")
            is_valid_name = False
            break
        if not all(c.isalpha() or c == '-' for c in clean_word):
            print(f"Line {i}: SKIP (invalid chars in word: '{word}')")
            is_valid_name = False
            break
    
    if is_valid_name and len(words) >= 1:
        if line_stripped[0].isupper():
            print(f"Line {i}: MATCH! '{line_stripped}'")
        else:
            print(f"Line {i}: SKIP (doesn't start with capital)")
    else:
        print(f"Line {i}: SKIP (not valid name)")

print("\n" + "="*60)
name = extractor.extract_name(sample_resume)
print(f"Extracted name: {name}")
