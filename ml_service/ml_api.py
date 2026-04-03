"""
Smart Resume Analyzer - ML Service API
Handles ML inference and analysis
"""

from flask import Flask, request, jsonify
from flask_cors import CORS
import os
import pickle
import re
from dotenv import load_dotenv
from sklearn.metrics.pairwise import cosine_similarity
from analyzers.ats_scorer import calculate_ats_score
from analyzers.skills_analyzer import analyze_skills
from analyzers.suggestions_engine import generate_suggestions
import requests

load_dotenv()

app = Flask(__name__)
CORS(app)

# Load ML models
MODEL_DIR = '../models'

print("📦 Loading ML models...")
try:
    with open(os.path.join(MODEL_DIR, 'tfidf_vectorizer.pkl'), 'rb') as f:
        vectorizer = pickle.load(f)
    print("   ✓ TF-IDF vectorizer loaded")
    
    with open(os.path.join(MODEL_DIR, 'svm_model.pkl'), 'rb') as f:
        svm_model = pickle.load(f)
    print("   ✓ SVM model loaded")
    
    print("✅ Models loaded successfully\n")
except Exception as e:
    print(f"❌ Error loading models: {e}")
    print("Please run train_model.py first!")
    exit(1)


def preprocess_text(text):
    """Clean and preprocess text"""
    if not text:
        return ""
    
    text = str(text).lower()
    text = re.sub(r'[^a-z0-9\s]', ' ', text)
    text = ' '.join(text.split())
    return text


def check_grammar(text):
    """
    Check grammar using LanguageTool API
    Returns number of errors and corrections
    """
    try:
        # Use free public LanguageTool API
        url = "https://api.languagetool.org/v2/check"
        
        # Limit text to first 10000 characters for API
        text_sample = text[:10000]
        
        data = {
            'text': text_sample,
            'language': 'en-US'
        }
        
        response = requests.post(url, data=data, timeout=10)
        print("\n🔍 LanguageTool FULL RESPONSE:\n", response.json())
        if response.status_code == 200:
            result = response.json()
            matches = result.get('matches', [])
            
            # Count errors
            error_count = len(matches)
            
            # Get top corrections (limit to 5)
            corrections = []
            for match in matches[:5]:
                if match.get('message'):
                    corrections.append(match['message'])
            
            return {
                'error_count': error_count,
                'corrections': corrections
            }
        else:
            return {'error_count': 0, 'corrections': []}
    
    except Exception as e:
        print(f"Grammar check error: {e}")
        return {'error_count': 0, 'corrections': []}


def analyze_sections(text):
    """
    Detect presence of key resume sections
    """
    text_lower = text.lower()
    
    sections = {
        'contact': bool(re.search(r'(email|phone|linkedin|github|portfolio)', text_lower)),
        'summary': bool(re.search(r'(summary|objective|profile|about)', text_lower)),
        'experience': bool(re.search(r'(experience|work history|employment|worked)', text_lower)),
        'education': bool(re.search(r'(education|degree|university|college|bachelor|master)', text_lower)),
        'skills': bool(re.search(r'(skills|technologies|tools|proficient)', text_lower)),
        'projects': bool(re.search(r'(project|portfolio|built|developed)', text_lower)),
        'certifications': bool(re.search(r'(certification|certified|certificate)', text_lower))
    }
    
    return sections


@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({'status': 'healthy', 'service': 'ml_service'})


@app.route('/analyze', methods=['POST'])
def analyze_resume():
    """
    Main analysis endpoint
    Expects: resume_text, job_description
    Returns: comprehensive analysis JSON
    """
    try:
        data = request.json
        
        resume_text = data.get('resume_text', '')
        job_description = data.get('job_description', '')
        
        if not resume_text or not job_description:
            return jsonify({'error': 'Missing resume_text or job_description'}), 400
        
        # Preprocess texts
        processed_resume = preprocess_text(resume_text)
        processed_jd = preprocess_text(job_description)
        
        # Transform using TF-IDF
        resume_vector = vectorizer.transform([processed_resume])
        jd_vector = vectorizer.transform([processed_jd])
        
        # Calculate JD match score (cosine similarity)
        jd_match_score = cosine_similarity(resume_vector, jd_vector)[0][0]
        jd_match_percentage = round(jd_match_score * 100, 2)
        
        # SVM prediction
        svm_prediction_label = svm_model.predict(resume_vector)[0]
        svm_probabilities = svm_model.predict_proba(resume_vector)[0]
        
        svm_prediction = "Selected" if svm_prediction_label == 1 else "Not Selected"
        confidence = round(max(svm_probabilities) * 100, 2)
        
        # Calculate ATS score
        ats_score = calculate_ats_score(
            resume_text=resume_text,
            job_description=job_description,
            jd_match=jd_match_percentage
        )
        
        # Analyze skills
        skills_analysis = analyze_skills(resume_text, job_description)
        
        # Detect sections
        sections = analyze_sections(resume_text)
        
        # Grammar check
        grammar_result = check_grammar(resume_text)
        
        # Generate suggestions
        suggestions = generate_suggestions(
            resume_text=resume_text,
            job_description=job_description,
            ats_score=ats_score,
            jd_match=jd_match_percentage,
            skills_analysis=skills_analysis,
            sections=sections,
            grammar_errors=grammar_result['error_count']
        )
        
        # Compile final response
        response = {
            'ats_score': ats_score,
            'jd_match': jd_match_percentage,
            'svm_prediction': svm_prediction,
            'confidence': confidence,
            'skills': skills_analysis,
            'sections': sections,
            'grammar_errors': grammar_result['error_count'],
            'grammar_corrections': grammar_result['corrections'],
            'suggestions': suggestions
        }
        print("\n📊 Analysis Result:\n", response)
        return jsonify(response), 200
    
    except Exception as e:
        print(f"Analysis error: {e}")
        return jsonify({'error': f'Analysis failed: {str(e)}'}), 500


if __name__ == '__main__':
    port = int(os.getenv('ML_SERVICE_PORT', 5001))
    print(f"\n🤖 ML Service starting on port {port}...")
    print(f"📁 Model directory: {MODEL_DIR}\n")
    
    app.run(debug=True, host='0.0.0.0', port=port)
