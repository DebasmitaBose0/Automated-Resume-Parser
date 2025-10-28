from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify
from werkzeug.utils import secure_filename
from flask_login import login_required, current_user
import os
from app.services.document_parser import DocumentParser
from app.services.resume_extractor import ResumeExtractor
from app.models.models import Candidate
from app.extensions import db
import requests
import logging

logger = logging.getLogger(__name__)

main_bp = Blueprint('main', __name__)

@main_bp.route('/')
def index():
    """Main landing page - redirects based on authentication status."""
    if current_user.is_authenticated:
        return render_template('index.html')
    else:
        return render_template('landing.html')

@main_bp.route('/dashboard')
@login_required
def dashboard():
    """Main dashboard page with upload form and candidate list."""
    return render_template('index.html')

@main_bp.route('/upload', methods=['GET', 'POST'])
@login_required
def upload_page():
    """Upload page for resumes."""
    if request.method == 'POST':
        # This will be handled by the API endpoint
        return redirect(url_for('api.upload_resume'))
    return render_template('upload.html')

@main_bp.route('/candidates')
@login_required
def candidates_page():
    """Page showing all candidates."""
    return render_template('candidates.html')

@main_bp.route('/candidate/<int:candidate_id>')
@login_required
def candidate_detail(candidate_id):
    """Page showing detailed candidate information."""
    return render_template('candidate_detail.html', candidate_id=candidate_id)

# Footer Page Routes
@main_bp.route('/pricing')
def pricing():
    """Pricing page."""
    return render_template('pages/pricing.html')

@main_bp.route('/api-docs')
def api_docs():
    """API Documentation page."""
    return render_template('pages/api_docs.html')

@main_bp.route('/integrations')
def integrations():
    """Integrations page."""
    return render_template('pages/integrations.html')

@main_bp.route('/changelog')
def changelog():
    """Changelog page."""
    return render_template('pages/changelog.html')

@main_bp.route('/about')
def about():
    """About Us page."""
    return render_template('pages/about.html')

@main_bp.route('/careers')
def careers():
    """Careers page."""
    return render_template('pages/careers.html')

@main_bp.route('/blog')
def blog():
    """Blog page."""
    return render_template('pages/blog.html')

@main_bp.route('/press')
def press():
    """Press Kit page."""
    return render_template('pages/press.html')

@main_bp.route('/contact')
def contact():
    """Contact page."""
    return render_template('pages/contact.html')

@main_bp.route('/help')
def help():
    """Help Center page."""
    return render_template('pages/help.html')

@main_bp.route('/faq')
def faq():
    """FAQ page."""
    return render_template('pages/faq.html')

@main_bp.route('/status')
def status():
    """System Status page."""
    return render_template('pages/status.html')

@main_bp.route('/roadmap')
def roadmap():
    """Product Roadmap page."""
    return render_template('pages/roadmap.html')

@main_bp.route('/privacy')
def privacy():
    """Privacy Policy page."""
    return render_template('pages/privacy.html')

@main_bp.route('/terms')
def terms():
    """Terms of Service page."""
    return render_template('pages/terms.html')

@main_bp.route('/cookies')
def cookies():
    """Cookie Policy page."""
    return render_template('pages/cookies.html')

@main_bp.route('/security')
def security():
    """Security page."""
    return render_template('pages/security.html')

@main_bp.route('/licenses')
def licenses():
    """Open Licenses page."""
    return render_template('pages/licenses.html')@main_bp.route('/search')
@login_required
def search_page():
    """Search page for candidates."""
    return render_template('search.html')