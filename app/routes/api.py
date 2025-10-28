from flask import Blueprint, request, jsonify, current_app
from flask_login import login_required, current_user
from werkzeug.utils import secure_filename
import os
import logging
from app.extensions import db
from app.models.models import Candidate, Education, Experience, Skill
from ..services import DocumentParser, ResumeExtractor

logger = logging.getLogger(__name__)

api_bp = Blueprint('api', __name__, url_prefix='/api')

def allowed_file(filename):
    """Check if the uploaded file has an allowed extension."""
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in current_app.config['ALLOWED_EXTENSIONS']

@api_bp.route('/upload', methods=['POST'])
@login_required
def upload_resume():
    """Upload and process a resume file."""
    try:
        # Check if file is in request
        if 'file' not in request.files:
            return jsonify({'error': 'No file provided'}), 400
        
        file = request.files['file']
        
        # Check if file is selected
        if file.filename == '':
            return jsonify({'error': 'No file selected'}), 400
        
        # Check file type
        if not allowed_file(file.filename):
            return jsonify({'error': 'File type not supported. Please upload PDF, DOC, or DOCX files.'}), 400
        
        # Secure filename and save file
        filename = secure_filename(file.filename)
        file_path = os.path.join(current_app.config['UPLOAD_FOLDER'], filename)
        file.save(file_path)
        
        try:
            # Extract text from document
            parser = DocumentParser()
            raw_text = parser.extract_text(file_path)
            cleaned_text = parser.clean_text(raw_text)
            
            if not cleaned_text:
                return jsonify({'error': 'Could not extract text from the document'}), 400
            
            # Extract structured information
            extractor = ResumeExtractor()
            extracted_data = extractor.extract_all(cleaned_text)
            
            # Create candidate record
            candidate = Candidate(
                name=extracted_data.get('name') or 'Unknown',
                email=extracted_data.get('email'),
                phone=extracted_data.get('phone'),
                location=extracted_data.get('location'),
                summary=extracted_data.get('summary'),
                original_filename=filename,
                file_type=filename.rsplit('.', 1)[1].lower(),
                raw_text=cleaned_text
            )
            
            db.session.add(candidate)
            db.session.flush()  # Get the candidate ID
            
            # Add education records (skip if incomplete)
            for edu_data in extracted_data.get('education', []):
                # Only add education if it has at least degree or institution with actual content
                if (edu_data.get('degree') and edu_data.get('degree').strip()) or \
                   (edu_data.get('institution') and edu_data.get('institution').strip()):
                    education = Education(
                        candidate_id=candidate.id,
                        degree=edu_data.get('degree') or '',
                        field_of_study=edu_data.get('field_of_study') or '',
                        institution=edu_data.get('institution') or '',
                        location=edu_data.get('location') or '',
                        start_date=edu_data.get('start_date') or '',
                        end_date=edu_data.get('end_date') or '',
                        gpa=edu_data.get('gpa') or '',
                        description=edu_data.get('description') or ''
                    )
                    db.session.add(education)
            
            # Add experience records (skip if incomplete)
            for exp_data in extracted_data.get('experience', []):
                # Only add experience if it has at least job_title or company with actual content
                if (exp_data.get('job_title') and exp_data.get('job_title').strip()) or \
                   (exp_data.get('company') and exp_data.get('company').strip()):
                    experience = Experience(
                        candidate_id=candidate.id,
                        job_title=exp_data.get('job_title') or '',
                        company=exp_data.get('company') or '',
                        location=exp_data.get('location') or '',
                        start_date=exp_data.get('start_date') or '',
                        end_date=exp_data.get('end_date') or '',
                        is_current=exp_data.get('is_current', False),
                        description=exp_data.get('description') or ''
                    )
                    db.session.add(experience)
            
            # Add skill records (skip if empty)
            for skill_data in extracted_data.get('skills', []):
                # Only add skill if it has a name with actual content
                if skill_data.get('name') and skill_data.get('name').strip():
                    skill = Skill(
                        candidate_id=candidate.id,
                        name=skill_data.get('name'),
                        category=skill_data.get('category') or '',
                        proficiency=skill_data.get('proficiency') or ''
                    )
                    db.session.add(skill)
            
            db.session.commit()
            
            # Clean up uploaded file
            os.remove(file_path)
            
            return jsonify({
                'message': 'Resume processed successfully',
                'candidate_id': candidate.id,
                'candidate': candidate.to_dict()
            }), 201
            
        except Exception as e:
            logger.error(f"Error processing resume: {str(e)}")
            # Clean up uploaded file on error
            if os.path.exists(file_path):
                os.remove(file_path)
            db.session.rollback()
            return jsonify({'error': f'Error processing resume: {str(e)}'}), 500
    
    except Exception as e:
        logger.error(f"Error in upload endpoint: {str(e)}")
        return jsonify({'error': 'Internal server error'}), 500

@api_bp.route('/candidates', methods=['GET'])
@login_required
def get_candidates():
    """Get all candidates with optional filtering."""
    try:
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 10, type=int)
        
        # Optional filters
        skill_filter = request.args.get('skill')
        company_filter = request.args.get('company')
        education_filter = request.args.get('education')
        
        query = Candidate.query
        
        # Apply filters if provided
        if skill_filter:
            query = query.join(Skill).filter(Skill.name.ilike(f'%{skill_filter}%'))
        
        if company_filter:
            query = query.join(Experience).filter(Experience.company.ilike(f'%{company_filter}%'))
        
        if education_filter:
            query = query.join(Education).filter(Education.institution.ilike(f'%{education_filter}%'))
        
        # Paginate results
        candidates = query.paginate(
            page=page, per_page=per_page, error_out=False
        )
        
        return jsonify({
            'candidates': [candidate.to_dict() for candidate in candidates.items],
            'total': candidates.total,
            'pages': candidates.pages,
            'current_page': page,
            'per_page': per_page
        })
    
    except Exception as e:
        logger.error(f"Error getting candidates: {str(e)}")
        return jsonify({'error': 'Internal server error'}), 500

@api_bp.route('/candidates/<int:candidate_id>', methods=['GET'])
@login_required
def get_candidate(candidate_id):
    """Get a specific candidate by ID."""
    try:
        candidate = Candidate.query.get_or_404(candidate_id)
        return jsonify(candidate.to_dict())
    
    except Exception as e:
        logger.error(f"Error getting candidate {candidate_id}: {str(e)}")
        return jsonify({'error': 'Internal server error'}), 500

@api_bp.route('/candidates/<int:candidate_id>', methods=['DELETE'])
@login_required
def delete_candidate(candidate_id):
    """Delete a candidate and all associated records."""
    try:
        candidate = Candidate.query.get_or_404(candidate_id)
        db.session.delete(candidate)
        db.session.commit()
        
        return jsonify({'message': 'Candidate deleted successfully'})
    
    except Exception as e:
        logger.error(f"Error deleting candidate {candidate_id}: {str(e)}")
        db.session.rollback()
        return jsonify({'error': 'Internal server error'}), 500

@api_bp.route('/search', methods=['GET'])
@login_required
def search_candidates():
    """Search candidates by various criteria."""
    try:
        query_text = request.args.get('q', '').strip()
        if not query_text:
            return jsonify({'error': 'Search query is required'}), 400
        
        # Search in multiple fields
        candidates = Candidate.query.filter(
            db.or_(
                Candidate.name.ilike(f'%{query_text}%'),
                Candidate.email.ilike(f'%{query_text}%'),
                Candidate.summary.ilike(f'%{query_text}%'),
                Candidate.raw_text.ilike(f'%{query_text}%')
            )
        ).all()
        
        # Also search in skills, experience, and education
        skill_candidates = Candidate.query.join(Skill).filter(
            Skill.name.ilike(f'%{query_text}%')
        ).all()
        
        exp_candidates = Candidate.query.join(Experience).filter(
            db.or_(
                Experience.job_title.ilike(f'%{query_text}%'),
                Experience.company.ilike(f'%{query_text}%')
            )
        ).all()
        
        edu_candidates = Candidate.query.join(Education).filter(
            db.or_(
                Education.institution.ilike(f'%{query_text}%'),
                Education.degree.ilike(f'%{query_text}%'),
                Education.field_of_study.ilike(f'%{query_text}%')
            )
        ).all()
        
        # Combine and deduplicate results
        all_candidates = candidates + skill_candidates + exp_candidates + edu_candidates
        unique_candidates = {c.id: c for c in all_candidates}.values()
        
        return jsonify({
            'candidates': [candidate.to_dict() for candidate in unique_candidates],
            'total': len(unique_candidates),
            'query': query_text
        })
    
    except Exception as e:
        logger.error(f"Error searching candidates: {str(e)}")
        return jsonify({'error': 'Internal server error'}), 500

@api_bp.route('/stats', methods=['GET'])
@login_required
def get_stats():
    """Get database statistics."""
    try:
        total_candidates = Candidate.query.count()
        total_skills = Skill.query.count()
        
        # Top skills
        top_skills = db.session.query(
            Skill.name, db.func.count(Skill.id).label('count')
        ).group_by(Skill.name).order_by(
            db.func.count(Skill.id).desc()
        ).limit(10).all()
        
        # Top companies
        top_companies = db.session.query(
            Experience.company, db.func.count(Experience.id).label('count')
        ).filter(Experience.company.isnot(None)).group_by(
            Experience.company
        ).order_by(db.func.count(Experience.id).desc()).limit(10).all()
        
        return jsonify({
            'total_candidates': total_candidates,
            'total_skills': total_skills,
            'top_skills': [{'name': skill[0], 'count': skill[1]} for skill in top_skills],
            'top_companies': [{'name': company[0], 'count': company[1]} for company in top_companies]
        })
    
    except Exception as e:
        logger.error(f"Error getting stats: {str(e)}")
        return jsonify({'error': 'Internal server error'}), 500