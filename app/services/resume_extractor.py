import re
import email_validator
import phonenumbers
import nltk
from typing import Dict, List, Tuple, Optional
import logging

logger = logging.getLogger(__name__)

class ResumeExtractor:
    """Service for extracting structured information from resume text using basic NLP."""
    
    def __init__(self):
        """Initialize the extractor with patterns and keywords."""
        # Download required NLTK data
        try:
            nltk.download('punkt', quiet=True)
            nltk.download('stopwords', quiet=True)
            nltk.download('averaged_perceptron_tagger', quiet=True)
        except:
            logger.warning("Could not download NLTK data")
        
        # Common skill keywords (can be expanded)
        self.technical_skills = {
            'programming': ['python', 'java', 'javascript', 'c++', 'c#', 'php', 'ruby', 'go', 'rust', 'swift'],
            'web': ['html', 'css', 'react', 'angular', 'vue', 'node.js', 'express', 'django', 'flask'],
            'database': ['sql', 'mysql', 'postgresql', 'mongodb', 'sqlite', 'oracle', 'redis'],
            'cloud': ['aws', 'azure', 'gcp', 'docker', 'kubernetes', 'terraform'],
            'data': ['pandas', 'numpy', 'scikit-learn', 'tensorflow', 'pytorch', 'r', 'matlab'],
            'tools': ['git', 'jenkins', 'jira', 'confluence', 'slack', 'trello']
        }
        
        self.soft_skills = [
            'leadership', 'communication', 'teamwork', 'problem solving', 'analytical',
            'creative', 'detail oriented', 'time management', 'project management',
            'critical thinking', 'adaptability', 'collaboration'
        ]
        
        # Education patterns
        self.degree_patterns = [
            r'bachelor[\'s]?\s+(?:of\s+)?(?:science|arts|engineering|business)',
            r'master[\'s]?\s+(?:of\s+)?(?:science|arts|engineering|business)',
            r'ph\.?d\.?|doctorate|doctoral',
            r'associate[\'s]?\s+degree',
            r'b\.?s\.?|b\.?a\.?|m\.?s\.?|m\.?a\.?|m\.?b\.?a\.?'
        ]
        
    def extract_contact_info(self, text: str) -> Dict[str, Optional[str]]:
        """Extract contact information from resume text."""
        contact_info = {
            'email': None,
            'phone': None
        }
        
        # Extract email
        email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
        emails = re.findall(email_pattern, text)
        if emails:
            # Validate the first email found
            try:
                email_validator.validate_email(emails[0])
                contact_info['email'] = emails[0]
            except email_validator.EmailNotValidError:
                pass
        
        # Extract phone number
        phone_patterns = [
            r'\+?1?[-.\s]?\(?([0-9]{3})\)?[-.\s]?([0-9]{3})[-.\s]?([0-9]{4})',
            r'\b\d{3}[-.]?\d{3}[-.]?\d{4}\b'
        ]
        
        for pattern in phone_patterns:
            matches = re.findall(pattern, text)
            if matches:
                if isinstance(matches[0], tuple):
                    phone = ''.join(matches[0])
                else:
                    phone = matches[0]
                
                # Try to parse and format phone number
                try:
                    parsed_phone = phonenumbers.parse(phone, "US")
                    if phonenumbers.is_valid_number(parsed_phone):
                        contact_info['phone'] = phonenumbers.format_number(
                            parsed_phone, phonenumbers.PhoneNumberFormat.NATIONAL
                        )
                        break
                except:
                    continue
        
        return contact_info
    
    def extract_name(self, text: str) -> Optional[str]:
        """Extract candidate name from resume text using basic patterns."""
        lines = text.split('\n')[:15]  # Check first 15 lines
        
        # Keywords that indicate we've passed the name section
        section_keywords = ['email', 'phone', 'linkedin', 'github', 'education', 'experience', 
                           'skills', 'summary', 'objective', 'about', 'b.tech', 'b.sc', 'mba',
                           'contact', 'address', 'date', 'dob', 'male', 'female']
        
        for line in lines:
            line = line.strip()
            
            # Skip empty lines
            if not line:
                continue
            
            # Skip lines with section keywords
            if any(keyword in line.lower() for keyword in section_keywords):
                continue
            
            # Skip lines that are too long (likely not a name)
            if len(line) > 50:
                continue
            
            # Skip lines with email or special characters
            if '@' in line or any(char in line for char in ['http', 'www', '+', ':', '=']):
                continue
            
            # Check if line looks like a name (mostly alphabetic with spaces and hyphens)
            words = line.split()
            
            # Should have 1-4 words
            if len(words) == 0 or len(words) > 4:
                continue
            
            # Each word should be mostly alphabetic
            is_valid_name = True
            for word in words:
                # Remove common punctuation
                clean_word = word.replace('.', '').replace(',', '')
                # Must be at least 2 characters and mostly letters
                if len(clean_word) < 2:
                    is_valid_name = False
                    break
                # Should be all alphabetic (no digits or special chars except hyphen)
                if not all(c.isalpha() or c == '-' for c in clean_word):
                    is_valid_name = False
                    break
            
            # If valid, return it
            if is_valid_name and len(words) >= 1:
                # Ensure first letter is capital
                if line[0].isupper():
                    return line
        
        return None
    
    def extract_skills(self, text: str) -> List[Dict[str, str]]:
        """Extract skills from resume text."""
        skills = []
        text_lower = text.lower()
        
        # Extract technical skills
        for category, skill_list in self.technical_skills.items():
            for skill in skill_list:
                if skill in text_lower:
                    skills.append({
                        'name': skill.title(),
                        'category': 'technical',
                        'proficiency': None
                    })
        
        # Extract soft skills
        for skill in self.soft_skills:
            if skill in text_lower:
                skills.append({
                    'name': skill.title(),
                    'category': 'soft',
                    'proficiency': None
                })
        
        # Remove duplicates
        unique_skills = []
        seen_skills = set()
        for skill in skills:
            if skill['name'] not in seen_skills:
                unique_skills.append(skill)
                seen_skills.add(skill['name'])
        
        return unique_skills
    
    def extract_education(self, text: str) -> List[Dict[str, Optional[str]]]:
        """Extract education information from resume text using line-by-line parsing."""
        education_entries = []
        lines = text.split('\n')
        
        # Degree pattern mappings
        degree_patterns = {
            r'\bb\.?\s*tech\b|\bbtec?h\b': 'B.Tech',
            r'\bb\.?\s*e(?:ngineering)?\b': 'B.E',
            r'\bb\.?\s*sc\b|\bb\.?\s*s(?:cience)?\b': 'B.Sc',
            r'\bb\.?\s*a(?:rts)?\b': 'B.A',
            r'\bb\.?\s*com(?:merce)?\b': 'B.Com',
            r'\bm\.?\s*tech(?:nology)?\b': 'M.Tech',
            r'\bm\.?\s*sc\b|\bm\.?\s*s(?:cience)?\b': 'M.Sc',
            r'\bm\.?\s*a(?:rts)?\b': 'M.A',
            r'\bm\.?\s*b\.?\s*a\b|\bmba\b': 'MBA',
            r'\bph\.?\s*d\.?\b|\bdoctorate\b': 'Ph.D',
            r'\bdiploma\b': 'Diploma',
        }
        
        found_degrees = set()
        i = 0
        
        while i < len(lines):
            line = lines[i].strip()
            
            # Skip empty lines
            if not line:
                i += 1
                continue
            
            # Check if this line contains a degree
            degree_found = None
            degree_match_obj = None
            
            for pattern, degree_name in degree_patterns.items():
                if degree_name not in found_degrees:
                    match = re.search(pattern, line, re.IGNORECASE)
                    if match:
                        degree_found = degree_name
                        degree_match_obj = match
                        break
            
            if degree_found:
                # Extract field of study from the same line (after degree)
                field_of_study = None
                after_degree = line[degree_match_obj.end():].strip()
                
                # Look for "in <field>" pattern
                field_match = re.search(r'in\s+([A-Za-z\s&]+?)(?:,|$)', after_degree, re.IGNORECASE)
                if field_match:
                    potential_field = field_match.group(1).strip()
                    # Remove trailing words that are not fields
                    words = potential_field.split()
                    if len(words) > 0 and words[0].lower() not in ['the', 'a', 'an']:
                        field_of_study = potential_field
                
                # Extract institution from the same or next line
                institution = None
                
                # First, check if institution is in the same line after the degree
                inst_search_line = after_degree
                
                # Also check next line if it starts with capital letters (likely institution name)
                next_line = lines[i + 1].strip() if i + 1 < len(lines) else ""
                
                # Pattern 1: "Name University/College/Institute"
                uni_patterns = [
                    r'(?:from|at)?\s*([A-Z][A-Za-z\s&,]*(?:University|College|Institute|School))',
                    r'([A-Z][A-Za-z\s&]*)\s+(?:University|College|Institute|School|University|IIT|NIT)',
                ]
                
                for uni_pattern in uni_patterns:
                    # Try in current line first
                    inst_match = re.search(uni_pattern, inst_search_line, re.IGNORECASE)
                    if not inst_match and next_line:
                        # Try in next line
                        inst_match = re.search(uni_pattern, next_line, re.IGNORECASE)
                    
                    if inst_match:
                        potential_inst = inst_match.group(0).strip()
                        # Clean up - remove leading "from" or "at"
                        potential_inst = re.sub(r'^(?:from|at)\s+', '', potential_inst, flags=re.IGNORECASE).strip()
                        # Limit to reasonable length and word count
                        if 3 < len(potential_inst) < 100 and len(potential_inst.split()) <= 6:
                            institution = potential_inst
                            break
                
                # Fallback: if next line looks like institution (all caps or title case)
                if not institution and next_line:
                    if (len(next_line) > 3 and 
                        (next_line[0].isupper() or next_line.isupper()) and
                        any(word.lower() in next_line.lower() for word in ['university', 'college', 'institute', 'school', 'iit', 'nit'])):
                        institution = next_line
                
                # Extract years - check current line and next 2 lines
                years_search = line
                if i + 1 < len(lines):
                    years_search += ' ' + lines[i + 1]
                if i + 2 < len(lines):
                    years_search += ' ' + lines[i + 2]
                
                years = re.findall(r'\b(20\d{2}|19\d{2})\b', years_search)
                start_date = years[0] if len(years) > 0 else None
                end_date = years[1] if len(years) > 1 else None
                
                # Add entry if we have degree and institution
                if institution:
                    education_entries.append({
                        'degree': degree_found,
                        'field_of_study': field_of_study,
                        'institution': institution,
                        'location': None,
                        'start_date': start_date,
                        'end_date': end_date,
                        'gpa': None,
                        'description': None
                    })
                    found_degrees.add(degree_found)
            
            i += 1
        
        return education_entries
    
    def extract_experience(self, text: str) -> List[Dict[str, Optional[str]]]:
        """Extract work experience from resume text using improved pattern recognition."""
        experience_entries = []
        
        # Split text into sections
        sections = self._split_into_sections(text)
        experience_section = ""
        
        # Find experience section explicitly
        for section in sections:
            if any(keyword in section.lower() for keyword in ['experience', 'work', 'employment', 'career']):
                experience_section = section
                break
        
        # If no experience section found, return empty
        if not experience_section:
            return experience_entries
        
        # Keywords to skip
        education_keywords = ['university', 'college', 'institute', 'school', 'degree', 'b.tech', 'b.sc', 'mba', 'phd', 'education', 'diploma']
        section_headers = ['experience', 'work', 'employment', 'career', 'education', 'skills', 'projects', 'certifications']
        
        lines = experience_section.split('\n')
        
        # Skip section header line
        start_idx = 0
        for i, line in enumerate(lines):
            if any(header in line.lower() for header in section_headers):
                start_idx = i + 1
                break
        
        # Process remaining lines
        lines = lines[start_idx:]
        i = 0
        
        while i < len(lines):
            line = lines[i].strip()
            i += 1
            
            if not line or any(keyword in line.lower() for keyword in education_keywords):
                continue
            
            # Start of a new job entry
            # Typical patterns:
            # 1. Job Title\n Company \n Dates or just dates on same line
            # 2. Job Title - Company, Year - Year
            # 3. Job Title\n Year - Year\n Company
            
            job_title = None
            company = None
            start_date = None
            end_date = None
            is_current = False
            description_lines = []
            
            # Check if this line has both title and company (e.g., "Senior Developer - Tech Solutions")
            if ' - ' in line and not re.search(r'\b(?:19|20)\d{2}\b', line):
                # Might be "Job Title - Company" format
                parts = line.split(' - ')
                if len(parts) == 2:
                    job_title = parts[0].strip()
                    company = parts[1].strip()
                else:
                    job_title = line
            else:
                job_title = line
            
            # Look ahead for company, dates, and description
            while i < len(lines):
                next_line = lines[i].strip()
                
                if not next_line:
                    i += 1
                    continue
                
                # Skip education keywords
                if any(keyword in next_line.lower() for keyword in education_keywords):
                    i += 1
                    continue
                
                # Check if this is a date line
                date_pattern = r'\b(?:19|20)\d{2}\b'
                has_dates = re.search(date_pattern, next_line, re.IGNORECASE)
                
                if has_dates:
                    # Extract dates - use non-capturing group for the century
                    dates = re.findall(r'\b(?:19|20)\d{2}\b', next_line)
                    start_date = dates[0] if len(dates) > 0 else None
                    end_date = dates[1] if len(dates) > 1 else None
                    
                    # Check for "present" or "current"
                    is_current = bool(re.search(r'\b(present|current)\b', next_line, re.IGNORECASE))
                    
                    # Extract company if on same line as dates (e.g., "Tech Solutions Inc. 2021 - 2023")
                    company_part = re.sub(date_pattern, '', next_line).strip()
                    if company_part and company_part not in ['present', 'current'] and not company:
                        company = company_part
                    
                    i += 1
                    # Now continue looking for description lines
                    break
                else:
                    # Non-date line - could be company if we don't have it yet
                    if not company and job_title and next_line.lower() not in [job_title.lower(), 'present', 'current']:
                        company = next_line
                        i += 1
                    else:
                        # This and remaining lines until next job are description
                        break
            
            # Collect description lines until we hit another job or end
            while i < len(lines):
                next_line = lines[i].strip()
                
                if not next_line:
                    i += 1
                    continue
                
                # Skip education keywords
                if any(keyword in next_line.lower() for keyword in education_keywords):
                    i += 1
                    continue
                
                # Check if this looks like a new job entry (title without being description)
                # A new job typically: doesn't look like description, OR has dates
                if re.search(r'\b(?:19|20)\d{2}\b', next_line):
                    # Likely start of next job
                    break
                
                # Check if it looks like a job title (short line, no obvious description words)
                is_likely_title = (
                    len(next_line) < 80 and 
                    not any(desc_word in next_line.lower() for desc_word in ['responsible', 'developed', 'led', 'managed', 'worked', 'designed', 'implemented', 'achieved', 'created'])
                )
                
                # If we have company and start_date, this is probably next job
                if company and start_date and is_likely_title:
                    break
                
                # Otherwise it's description
                description_lines.append(next_line)
                i += 1
            
            # Only add if we have meaningful data
            if job_title or company:
                experience_entries.append({
                    'job_title': job_title,
                    'company': company,
                    'location': None,
                    'start_date': start_date,
                    'end_date': end_date,
                    'is_current': is_current,
                    'description': '\n'.join(description_lines) if description_lines else None
                })
        
        return experience_entries
    
    def _split_into_sections(self, text: str) -> List[str]:
        """Split resume text into logical sections."""
        # Common section headers
        section_headers = [
            'education', 'experience', 'work experience', 'employment',
            'skills', 'technical skills', 'projects', 'certifications',
            'summary', 'objective', 'profile'
        ]
        
        sections = []
        current_section = []
        
        lines = text.split('\n')
        for line in lines:
            line_lower = line.lower().strip()
            
            # Check if this line is a section header
            is_header = any(header in line_lower for header in section_headers)
            
            if is_header and current_section:
                # Start new section
                sections.append('\n'.join(current_section))
                current_section = [line]
            else:
                current_section.append(line)
        
        # Add the last section
        if current_section:
            sections.append('\n'.join(current_section))
        
        return sections
    
    def extract_all(self, text: str) -> Dict:
        """Extract all information from resume text."""
        try:
            # Do NOT clean the text yet - preserve newlines for line-by-line parsing
            # text = self._clean_text(text)  # This breaks line-by-line parsing
            
            # Extract all components
            contact_info = self.extract_contact_info(text)
            name = self.extract_name(text)
            skills = self.extract_skills(text)
            education = self.extract_education(text)
            experience = self.extract_experience(text)
            
            return {
                'name': name,
                'email': contact_info.get('email'),
                'phone': contact_info.get('phone'),
                'skills': skills,
                'education': education,
                'experience': experience,
                'summary': self._extract_summary(text),
                'location': self._extract_location(text)
            }
        except Exception as e:
            logger.error(f"Error during extraction: {str(e)}")
            raise
    
    def _clean_text(self, text: str) -> str:
        """Clean and normalize text for processing."""
        # Remove excessive whitespace
        text = re.sub(r'\s+', ' ', text)
        # Remove special characters that might interfere
        text = re.sub(r'[^\w\s@.-]', ' ', text)
        return text.strip()
    
    def _extract_summary(self, text: str) -> Optional[str]:
        """Extract summary/objective section."""
        lines = text.split('\n')
        summary_lines = []
        in_summary = False
        
        for line in lines:
            line_lower = line.lower().strip()
            if any(keyword in line_lower for keyword in ['summary', 'objective', 'profile']):
                in_summary = True
                continue
            elif in_summary:
                if any(keyword in line_lower for keyword in ['experience', 'education', 'skills']):
                    break
                if line.strip():
                    summary_lines.append(line.strip())
        
        return ' '.join(summary_lines) if summary_lines else None
    
    def _extract_location(self, text: str) -> Optional[str]:
        """Extract location information using basic patterns."""
        # Common location patterns
        location_patterns = [
            r'\b([A-Z][a-z]+,\s*[A-Z]{2})\b',  # City, State
            r'\b([A-Z][a-z]+\s+[A-Z][a-z]+,\s*[A-Z]{2})\b',  # City Name, State
            r'\b(New York|Los Angeles|Chicago|Houston|Phoenix|Philadelphia|San Antonio|San Diego|Dallas|San Jose|Austin|Jacksonville|Fort Worth|Columbus|Charlotte|San Francisco|Indianapolis|Seattle|Denver|Washington|Boston|El Paso|Nashville|Detroit|Oklahoma City|Portland|Las Vegas|Memphis|Louisville|Baltimore|Milwaukee|Albuquerque|Tucson|Fresno|Sacramento|Kansas City|Long Beach|Mesa|Atlanta|Colorado Springs|Virginia Beach|Raleigh|Omaha|Miami|Oakland|Minneapolis|Tulsa|Wichita|New Orleans|Arlington)\b',
        ]
        
        for pattern in location_patterns:
            matches = re.findall(pattern, text[:1000], re.IGNORECASE)  # Check first 1000 chars
            if matches:
                return matches[0]
        
        return None