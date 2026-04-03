"""
Smart Resume Analyzer - Model Training Script
Trains TF-IDF vectorizer and SVM classifier for resume analysis
"""

import pandas as pd
import numpy as np
import pickle
import os
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.svm import SVC
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics.pairwise import cosine_similarity
import re
import warnings
warnings.filterwarnings('ignore')

# Dataset path - user must place CSV here
DATA_PATH = 'data/resume_dataset.csv'
MODEL_DIR = 'models'

# Ensure models directory exists
os.makedirs(MODEL_DIR, exist_ok=True)


def preprocess_text(text):
    """Clean and preprocess text"""
    if pd.isna(text):
        return ""
    
    text = str(text).lower()
    # Remove special characters but keep spaces
    text = re.sub(r'[^a-z0-9\s]', ' ', text)
    # Remove extra whitespace
    text = ' '.join(text.split())
    return text


def generate_job_description(category):
    """
    Generate realistic job descriptions based on category
    These simulate real JDs (1-2 sentences) for training
    """
    jd_templates = {
        'data science': 'Seeking experienced data scientist with strong background in machine learning statistical analysis and data visualization. Must have expertise in Python R SQL and experience with predictive modeling and big data technologies.',
        
        'web development': 'Looking for full stack web developer proficient in modern frameworks and technologies. Required skills include JavaScript React Node.js database management and responsive design implementation.',
        
        'software engineer': 'Software engineer position requiring strong programming skills in object oriented design and software development lifecycle. Experience with agile methodologies version control and collaborative development essential.',
        
        'mobile development': 'Mobile application developer needed with expertise in iOS Android development and cross platform frameworks. Must have strong understanding of mobile UI UX principles and API integration.',
        
        'devops': 'DevOps engineer role focusing on CI CD automation cloud infrastructure and container orchestration. Proficiency in Docker Kubernetes AWS and infrastructure as code required.',
        
        'business analyst': 'Business analyst position requiring strong analytical skills stakeholder management and requirements gathering. Experience with data analysis process improvement and business intelligence tools preferred.',
        
        'network engineer': 'Network engineer needed with expertise in network architecture security and infrastructure management. Strong knowledge of routing switching firewalls and network protocols essential.',
        
        'database administrator': 'Database administrator role managing large scale database systems and ensuring data integrity. Experience with SQL database optimization backup recovery and performance tuning required.',
        
        'cyber security': 'Cybersecurity specialist position focusing on threat detection vulnerability assessment and security architecture. Required expertise in penetration testing security frameworks and incident response.',
        
        'cloud architect': 'Cloud architect role designing and implementing scalable cloud solutions. Strong experience with AWS Azure or GCP cloud native architectures and migration strategies essential.',
        
        'machine learning': 'Machine learning engineer position developing and deploying ML models and algorithms. Expertise in deep learning neural networks TensorFlow PyTorch and model optimization required.',
        
        'project manager': 'Project manager needed with strong leadership communication and organizational skills. Experience managing cross functional teams budgets timelines and stakeholder expectations essential.',
        
        'qa engineer': 'Quality assurance engineer role focusing on test automation and quality processes. Required skills include test framework development bug tracking and continuous integration testing.',
        
        'ui ux designer': 'UI UX designer position creating intuitive user experiences and interfaces. Strong portfolio demonstrating user research wireframing prototyping and visual design skills required.',
        
        'technical support': 'Technical support specialist providing troubleshooting and customer assistance. Strong communication skills technical knowledge and problem solving abilities essential for success.',
    }
    
    category_lower = category.lower() if isinstance(category, str) else ''
    
    # Try exact match first
    if category_lower in jd_templates:
        return jd_templates[category_lower]
    
    # Try partial match
    for key, desc in jd_templates.items():
        if key in category_lower or category_lower in key:
            return jd_templates[key]
    
    # Default JD for unknown categories
    return f'Seeking qualified professional with expertise in {category}. Strong technical skills problem solving abilities and communication skills required. Experience with relevant technologies and industry best practices essential.'


def load_and_prepare_data():
    """Load dataset and prepare for training"""
    print("📂 Loading dataset...")
    
    if not os.path.exists(DATA_PATH):
        print(f"❌ ERROR: Dataset not found at {DATA_PATH}")
        print(f"Please place your resume dataset CSV in the data/ folder")
        print(f"Required columns: Resume_str, Category")
        exit(1)
    
    try:
        df = pd.read_csv(DATA_PATH)
    except Exception as e:
        print(f"❌ ERROR reading CSV: {e}")
        exit(1)
    
    # Validate required columns
    if 'Resume_str' not in df.columns or 'Category' not in df.columns:
        print(f"❌ ERROR: CSV must contain 'Resume_str' and 'Category' columns")
        print(f"Found columns: {list(df.columns)}")
        exit(1)
    
    print(f"✅ Loaded {len(df)} resumes")
    print(f"📊 Categories: {df['Category'].nunique()}")
    
    # Handle missing values
    df['Resume_str'] = df['Resume_str'].fillna('')
    df['Category'] = df['Category'].fillna('unknown')
    
    # Remove empty resumes
    df = df[df['Resume_str'].str.strip() != '']
    
    print(f"✅ After cleaning: {len(df)} resumes")
    
    return df


def train_model():
    """Main training function"""
    print("\n🚀 Starting Model Training...\n")
    
    # Load data
    df = load_and_prepare_data()
    
    # Preprocess resumes
    print("🔧 Preprocessing text...")
    df['processed_resume'] = df['Resume_str'].apply(preprocess_text)
    
    # Generate job descriptions
    print("📝 Generating job descriptions...")
    df['job_description'] = df['Category'].apply(generate_job_description)
    df['processed_jd'] = df['job_description'].apply(preprocess_text)
    
    # Initialize TF-IDF vectorizer
    print("🔍 Training TF-IDF vectorizer...")
    vectorizer = TfidfVectorizer(
        max_features=1000,
        ngram_range=(1, 2),
        min_df=2,
        max_df=0.8,
        stop_words='english'
    )
    
    # Fit on all text (resumes + JDs)
    all_text = pd.concat([df['processed_resume'], df['processed_jd']])
    vectorizer.fit(all_text)
    
    # Transform resumes and JDs
    print("⚙️ Vectorizing data...")
    resume_vectors = vectorizer.transform(df['processed_resume'])
    jd_vectors = vectorizer.transform(df['processed_jd'])
    
    # Calculate cosine similarity for each pair
    print("📐 Computing similarities...")
    similarities = []
    for i in range(len(df)):
        sim = cosine_similarity(
            resume_vectors[i:i+1],
            jd_vectors[i:i+1]
        )[0][0]
        similarities.append(sim)
    
    df['similarity'] = similarities
    
    # Create labels based on similarity threshold
    threshold = 0.65
    df['label'] = (df['similarity'] > threshold).astype(int)
    
    print(f"✅ Similarity threshold: {threshold}")
    print(f"   Selected (1): {df['label'].sum()} resumes")
    print(f"   Not Selected (0): {(1 - df['label']).sum()} resumes")
    
    # Train SVM classifier
    print("🤖 Training SVM classifier...")
    svm_model = SVC(
        kernel='rbf',
        probability=True,
        random_state=42,
        C=1.0,
        gamma='scale'
    )
    
    svm_model.fit(resume_vectors, df['label'])
    
    # Calculate training accuracy
    train_accuracy = svm_model.score(resume_vectors, df['label'])
    print(f"✅ Training accuracy: {train_accuracy * 100:.2f}%")
    
    # Encode categories
    label_encoder = LabelEncoder()
    label_encoder.fit(df['Category'])
    
    # Save models
    print("\n💾 Saving models...")
    
    with open(os.path.join(MODEL_DIR, 'tfidf_vectorizer.pkl'), 'wb') as f:
        pickle.dump(vectorizer, f)
    print(f"   ✓ TF-IDF vectorizer saved")
    
    with open(os.path.join(MODEL_DIR, 'svm_model.pkl'), 'wb') as f:
        pickle.dump(svm_model, f)
    print(f"   ✓ SVM model saved")
    
    with open(os.path.join(MODEL_DIR, 'label_encoder.pkl'), 'wb') as f:
        pickle.dump(label_encoder, f)
    print(f"   ✓ Label encoder saved")
    
    # Save sample categories for reference
    categories = sorted(df['Category'].unique().tolist())
    with open(os.path.join(MODEL_DIR, 'categories.txt'), 'w') as f:
        f.write('\n'.join(categories))
    print(f"   ✓ Categories list saved")
    
    print("\n✨ Training complete!")
    print(f"📁 Models saved in: {MODEL_DIR}/")
    print("\n🎯 Next steps:")
    print("   1. Add API keys to .env file")
    print("   2. Run backend: cd backend && python app.py")
    print("   3. Run ML service: cd ml_service && python ml_api.py")
    print("   4. Run frontend: cd frontend && npm start")


if __name__ == "__main__":
    train_model()
