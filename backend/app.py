"""
Smart Resume Analyzer - Backend API
Handles file uploads and coordinates analysis
"""

from flask import Flask, request, jsonify
from flask_cors import CORS
from werkzeug.utils import secure_filename
import os
import requests
from dotenv import load_dotenv
from utils.text_extractor import extract_text_from_pdf, extract_text_from_docx

load_dotenv()

app = Flask(__name__)
CORS(app)

# Configuration
UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'pdf', 'docx'}
MAX_FILE_SIZE = 10 * 1024 * 1024  # 10MB

os.makedirs(UPLOAD_FOLDER, exist_ok=True)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = MAX_FILE_SIZE

# ML Service URL configurable via environment variable with localhost fallback
ML_SERVICE_URL = os.getenv('ML_SERVICE_URL', 'http://localhost:5001')


def allowed_file(filename):
    """Check if file extension is allowed"""
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({'status': 'healthy', 'service': 'backend'})


@app.route('/upload', methods=['POST'])
def upload_resume():
    """
    Handle resume upload and analysis
    Expects: resume file + job_description text
    """
    try:
        # Validate file
        if 'resume' not in request.files:
            return jsonify({'error': 'No resume file provided'}), 400
        
        file = request.files['resume']
        
        if file.filename == '':
            return jsonify({'error': 'No file selected'}), 400
        
        if not allowed_file(file.filename):
            return jsonify({'error': 'Invalid file type. Only PDF and DOCX allowed'}), 400
        
        # Get job description
        job_description = request.form.get('job_description', '')
        
        if not job_description or len(job_description.strip()) < 10:
            return jsonify({'error': 'Please provide a valid job description (min 10 characters)'}), 400
        
        # Save file temporarily
        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)
        
        # Extract text based on file type
        file_ext = filename.rsplit('.', 1)[1].lower()
        
        try:
            if file_ext == 'pdf':
                resume_text = extract_text_from_pdf(filepath)
            elif file_ext == 'docx':
                resume_text = extract_text_from_docx(filepath)
            else:
                return jsonify({'error': 'Unsupported file type'}), 400
        except Exception as e:
            os.remove(filepath)
            return jsonify({'error': f'Failed to extract text: {str(e)}'}), 500
        
        # Clean up file
        os.remove(filepath)
        
        # Validate extracted text
        if not resume_text or len(resume_text.strip()) < 50:
            return jsonify({'error': 'Could not extract sufficient text from resume'}), 400
        
        # Send to ML service for analysis
        try:
            ml_response = requests.post(
                f"{ML_SERVICE_URL}/analyze",
                json={
                    'resume_text': resume_text,
                    'job_description': job_description
                },
                timeout=30
            )
            
            if ml_response.status_code != 200:
                return jsonify({'error': 'ML service analysis failed'}), 500
            
            print("LanguageTool Raw Response:", ml_response.json())
            
            analysis_result = ml_response.json()
            
            # Add original text for frontend preview
            analysis_result['resume_text_preview'] = resume_text[:1000]  # First 1000 chars
            
            return jsonify(analysis_result), 200
            
        except requests.exceptions.RequestException as e:
            return jsonify({
                'error': 'Could not connect to ML service',
                'details': str(e)
            }), 503
    
    except Exception as e:
        return jsonify({'error': f'Server error: {str(e)}'}), 500


@app.route('/test', methods=['GET'])
def test_endpoint():
    """Test endpoint to verify backend is running"""
    return jsonify({
        'message': 'Backend is running',
        'ml_service_url': ML_SERVICE_URL,
        'allowed_extensions': list(ALLOWED_EXTENSIONS)
    })


if __name__ == '__main__':
    port = int(os.getenv('BACKEND_PORT', 5000))
    print(f"\n🚀 Backend server starting on port {port}...")
    print(f"📡 ML Service URL: {ML_SERVICE_URL}")
    print(f"📁 Upload folder: {UPLOAD_FOLDER}")
    print(f"✅ Allowed file types: {', '.join(ALLOWED_EXTENSIONS)}\n")
    
    app.run(debug=True, host='0.0.0.0', port=port)
