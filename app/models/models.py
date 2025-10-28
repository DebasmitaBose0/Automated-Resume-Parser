from datetime import datetime
import json
from app.extensions import db

class Candidate(db.Model):
    __tablename__ = 'candidates'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), nullable=True)
    phone = db.Column(db.String(20), nullable=True)
    location = db.Column(db.String(200), nullable=True)
    summary = db.Column(db.Text, nullable=True)
    
    # Raw resume text and metadata
    original_filename = db.Column(db.String(255), nullable=False)
    file_type = db.Column(db.String(10), nullable=False)  # pdf, doc, docx
    raw_text = db.Column(db.Text, nullable=False)
    
    # Timestamps
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    educations = db.relationship('Education', backref='candidate', lazy=True, cascade='all, delete-orphan')
    experiences = db.relationship('Experience', backref='candidate', lazy=True, cascade='all, delete-orphan')
    skills = db.relationship('Skill', backref='candidate', lazy=True, cascade='all, delete-orphan')
    
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'email': self.email,
            'phone': self.phone,
            'location': self.location,
            'summary': self.summary,
            'original_filename': self.original_filename,
            'file_type': self.file_type,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None,
            'educations': [edu.to_dict() for edu in self.educations],
            'experiences': [exp.to_dict() for exp in self.experiences],
            'skills': [skill.to_dict() for skill in self.skills]
        }

class Education(db.Model):
    __tablename__ = 'educations'
    
    id = db.Column(db.Integer, primary_key=True)
    candidate_id = db.Column(db.Integer, db.ForeignKey('candidates.id'), nullable=False)
    degree = db.Column(db.String(100), nullable=True, default='')
    field_of_study = db.Column(db.String(100), nullable=True, default='')
    institution = db.Column(db.String(200), nullable=True, default='')
    location = db.Column(db.String(200), nullable=True, default='')
    start_date = db.Column(db.String(20), nullable=True, default='')  # Store as string for flexibility
    end_date = db.Column(db.String(20), nullable=True, default='')
    gpa = db.Column(db.String(10), nullable=True, default='')
    description = db.Column(db.Text, nullable=True, default='')
    
    def to_dict(self):
        return {
            'id': self.id,
            'degree': self.degree or '',
            'field_of_study': self.field_of_study or '',
            'institution': self.institution or '',
            'location': self.location or '',
            'start_date': self.start_date or '',
            'end_date': self.end_date or '',
            'gpa': self.gpa or '',
            'description': self.description or ''
        }

class Experience(db.Model):
    __tablename__ = 'experiences'
    
    id = db.Column(db.Integer, primary_key=True)
    candidate_id = db.Column(db.Integer, db.ForeignKey('candidates.id'), nullable=False)
    job_title = db.Column(db.String(100), nullable=True, default='')
    company = db.Column(db.String(200), nullable=True, default='')
    location = db.Column(db.String(200), nullable=True, default='')
    start_date = db.Column(db.String(20), nullable=True, default='')
    end_date = db.Column(db.String(20), nullable=True, default='')
    is_current = db.Column(db.Boolean, default=False)
    description = db.Column(db.Text, nullable=True, default='')
    
    def to_dict(self):
        return {
            'id': self.id,
            'job_title': self.job_title or '',
            'company': self.company or '',
            'location': self.location or '',
            'start_date': self.start_date or '',
            'end_date': self.end_date or '',
            'is_current': self.is_current,
            'description': self.description or ''
        }

class Skill(db.Model):
    __tablename__ = 'skills'
    
    id = db.Column(db.Integer, primary_key=True)
    candidate_id = db.Column(db.Integer, db.ForeignKey('candidates.id'), nullable=False)
    name = db.Column(db.String(100), nullable=True, default='')
    category = db.Column(db.String(50), nullable=True, default='')  # technical, soft, language, etc.
    proficiency = db.Column(db.String(20), nullable=True, default='')  # beginner, intermediate, advanced, expert
    
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name or '',
            'category': self.category or '',
            'proficiency': self.proficiency or ''
        }

# Create indexes for better search performance
db.Index('idx_candidate_name', Candidate.name)
db.Index('idx_candidate_email', Candidate.email)
db.Index('idx_skill_name', Skill.name)
db.Index('idx_experience_title', Experience.job_title)
db.Index('idx_experience_company', Experience.company)
db.Index('idx_education_institution', Education.institution)
db.Index('idx_education_degree', Education.degree)