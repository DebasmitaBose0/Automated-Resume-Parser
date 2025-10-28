# Automated Resume Parser

A sophisticated web application that extracts and categorizes information from resumes using AI and Natural Language Processing (NLP). Built with Python, Flask, spaCy, and PostgreSQL.

## Features

- **Document Processing**: Extract text from PDF, DOC, and DOCX files
- **AI-Powered Extraction**: Use spaCy NLP to automatically extract:
  - Candidate names and contact information
  - Skills (technical and soft skills)
  - Work experience with job titles, companies, and dates
  - Education with degrees, institutions, and dates
  - Professional summaries
- **RESTful API**: Complete REST API for programmatic access
- **Web Interface**: User-friendly web interface for uploading and viewing resumes
- **Advanced Search**: Search candidates by name, skills, companies, education, etc.
- **Database Storage**: Structured storage in PostgreSQL for fast querying
- **Responsive Design**: Mobile-friendly Bootstrap interface

## Technology Stack

- **Backend**: Python 3.8+, Flask
- **Database**: PostgreSQL with SQLAlchemy ORM
- **NLP**: spaCy for named entity recognition and text processing
- **Document Processing**: PDFPlumber for PDFs, python-docx for Word documents
- **Frontend**: HTML5, CSS3, JavaScript, Bootstrap 5
- **Additional Libraries**: NLTK, pandas, scikit-learn for enhanced text processing

## Project Structure

```
Resumeparser/
├── app/
│   ├── __init__.py              # Flask app factory
│   ├── models/
│   │   ├── __init__.py
│   │   └── models.py            # Database models
│   ├── routes/
│   │   ├── __init__.py
│   │   ├── api.py               # REST API endpoints
│   │   └── main.py              # Web interface routes
│   └── services/
│       ├── __init__.py
│       ├── document_parser.py   # Document text extraction
│       └── resume_extractor.py  # NLP-based information extraction
├── templates/                   # HTML templates
│   ├── base.html
│   ├── index.html
│   ├── upload.html
│   ├── candidates.html
│   ├── search.html
│   └── candidate_detail.html
├── static/                      # Static files (CSS, JS, images)
├── uploads/                     # Temporary file storage
├── config.py                    # Application configuration
├── requirements.txt             # Python dependencies
├── setup.py                     # Setup script
├── run.py                       # Application entry point
├── .env                         # Environment variables
└── README.md                    # This file
```

## Installation & Setup

### Prerequisites

- Python 3.8 or higher
- PostgreSQL 12 or higher
- pip (Python package manager)

### Quick Setup

1. **Clone the repository:**
   ```bash
   git clone <repository-url>
   cd Resumeparser
   ```

2. **Create and activate virtual environment (recommended):**
   ```bash
   python -m venv venv
   
   # On Windows:
   venv\Scripts\activate
   
   # On macOS/Linux:
   source venv/bin/activate
   ```

3. **Run the setup script:**
   ```bash
   python setup.py
   ```

4. **Configure the database:**
   - Create a PostgreSQL database
   - Update the `DATABASE_URL` in `.env` file:
     ```
     DATABASE_URL=postgresql://username:password@localhost:5432/resume_parser_db
     ```

5. **Update the secret key:**
   - Generate a secure secret key and update it in `.env`:
     ```
     SECRET_KEY=your-secure-secret-key-here
     ```

6. **Run the application:**
   ```bash
   python run.py
   ```

The application will be available at `http://localhost:5000`

### Manual Setup (Alternative)

If you prefer manual setup:

1. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Download spaCy model:**
   ```bash
   python -m spacy download en_core_web_sm
   ```

3. **Download NLTK data:**
   ```python
   import nltk
   nltk.download('punkt')
   nltk.download('stopwords')
   nltk.download('averaged_perceptron_tagger')
   nltk.download('wordnet')
   ```

## Configuration

### Environment Variables

Create a `.env` file in the project root with the following variables:

```env
# Database connection
DATABASE_URL=postgresql://username:password@localhost:5432/resume_parser_db

# Security
SECRET_KEY=your-secret-key-here

# File upload settings
UPLOAD_FOLDER=uploads
MAX_CONTENT_LENGTH=16777216  # 16MB
ALLOWED_EXTENSIONS=pdf,doc,docx
```

### Database Setup

The application uses PostgreSQL as the database. Make sure to:

1. Install PostgreSQL on your system
2. Create a database for the application
3. Update the `DATABASE_URL` in your `.env` file
4. The application will automatically create the required tables on first run

## API Documentation

### Upload Resume
- **POST** `/api/upload`
- Upload and process a resume file
- **Body**: Form data with `file` field
- **Response**: Extracted candidate information

### Get All Candidates
- **GET** `/api/candidates`
- Retrieve all candidates with pagination
- **Query Parameters**:
  - `page`: Page number (default: 1)
  - `per_page`: Items per page (default: 10)
  - `skill`: Filter by skill
  - `company`: Filter by company
  - `education`: Filter by education

### Get Candidate Details
- **GET** `/api/candidates/{id}`
- Get detailed information for a specific candidate

### Search Candidates
- **GET** `/api/search?q={query}`
- Search candidates by various criteria
- Searches in names, emails, skills, companies, education, etc.

### Delete Candidate
- **DELETE** `/api/candidates/{id}`
- Delete a candidate and all associated records

### Get Statistics
- **GET** `/api/stats`
- Get database statistics including top skills and companies

## Usage

### Web Interface

1. **Home Page**: Overview and statistics
2. **Upload**: Upload new resumes for processing
3. **Candidates**: Browse all candidates with filtering options
4. **Search**: Advanced search functionality
5. **Candidate Details**: Detailed view of individual candidates

### Uploading Resumes

1. Navigate to the Upload page
2. Select a PDF, DOC, or DOCX file
3. Click "Upload and Process"
4. The system will:
   - Extract text from the document
   - Apply NLP processing to identify key information
   - Store structured data in the database
   - Display extracted information

### Searching Candidates

The search functionality supports:
- **Name searches**: Find candidates by name
- **Skill searches**: Find candidates with specific skills (e.g., "Python", "React")
- **Company searches**: Find candidates who worked at specific companies
- **Education searches**: Find candidates from specific institutions
- **General text search**: Search in all text fields

## Data Extraction Capabilities

### Contact Information
- Full names
- Email addresses
- Phone numbers
- Location/address information

### Skills
- Technical skills (programming languages, frameworks, tools)
- Soft skills (leadership, communication, etc.)
- Categorization of skills by type

### Work Experience
- Job titles and positions
- Company names
- Employment dates (start/end dates)
- Current position detection
- Job descriptions

### Education
- Degree types and levels
- Fields of study
- Institution names
- Graduation dates
- GPA (when available)

## Customization

### Adding New Skills

Edit the `technical_skills` and `soft_skills` dictionaries in `app/services/resume_extractor.py`:

```python
self.technical_skills = {
    'programming': ['python', 'java', 'your-new-skill'],
    # ... add more categories and skills
}
```

### Improving Extraction

The NLP extraction can be enhanced by:
- Training custom spaCy models
- Adding more keyword patterns
- Implementing machine learning classifiers
- Adding industry-specific vocabularies

### Database Schema Modifications

To add new fields, update the models in `app/models/models.py` and create database migrations.

## Troubleshooting

### Common Issues

1. **spaCy model not found**:
   ```bash
   python -m spacy download en_core_web_sm
   ```

2. **Database connection errors**:
   - Verify PostgreSQL is running
   - Check database credentials in `.env`
   - Ensure database exists

3. **File upload errors**:
   - Check file size (max 16MB)
   - Verify file format (PDF, DOC, DOCX only)
   - Ensure uploads directory exists and is writable

4. **Text extraction issues**:
   - Some PDF files may have text as images (OCR not implemented)
   - Encrypted PDFs may not be readable
   - Very old DOC formats may not be supported

### Performance Optimization

For better performance with large datasets:
- Add database indexes for frequently searched fields
- Implement caching for search results
- Use database connection pooling
- Consider implementing background job processing for file uploads

## Security Considerations

- Files are automatically deleted after processing
- Input validation on all file uploads
- SQL injection protection through SQLAlchemy ORM
- XSS protection in web interface
- Secure file handling with filename sanitization

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Support

For support and questions:
- Check the troubleshooting section above
- Review the API documentation
- Open an issue on the project repository

## Future Enhancements

Potential improvements for future versions:
- OCR support for scanned PDFs
- Machine learning models for better extraction accuracy
- Support for additional file formats
- Resume scoring and ranking
- Integration with job boards and ATS systems
- Advanced analytics and reporting
- Multi-language support
- Resume template generation