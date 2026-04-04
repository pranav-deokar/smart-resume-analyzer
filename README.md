# 🎯 Smart Resume Analyzer

A production-ready AI-powered resume analysis system with ATS scoring, ML-based predictions, and intelligent feedback.
LIVE DEMO:
BACKEND:https://resume-backend-d6i6.onrender.com/health
ML SERVICE:https://resume-ml-service-6mo8.onrender.com/health
RUN BACKEND URL FIRST TO TRIGGER IT BECAUSE IT IS HOSTED ON FREE TIER PLATFORM 
USE APPLICATION WHEN BACKEND RETURNS SOMETHING LIKE:: {"service":"backend","status":"healthy"}
FRONTEND:https://smart-resume-analyzer-topaz.vercel.app

## ✨ Features

- **PDF/DOCX Resume Upload**: Automatic text extraction
- **ATS Score Calculation**: Multi-metric scoring system
- **ML-Powered Analysis**: TF-IDF + SVM classifier
- **Job Description Matching**: Cosine similarity scoring
- **Grammar Checking**: Integrated LanguageTool API
- **Skills Analysis**: Found vs Missing skills detection
- **Intelligent Suggestions**: Rule-based + AI-powered feedback
- **Futuristic UI**: Brown-beige theme with smooth animations
- **Fully Responsive**: Mobile, tablet, and desktop support

## 🚀 Quick Start

### Prerequisites

- Python 3.8+
- Node.js 16+
- npm or yarn

### Step 1: Dataset Preparation

1. Download or prepare your resume dataset CSV file with these columns:
   - `Resume_str` (resume text)
   - `Category` (job category/domain)

2. Place the CSV file in the `data/` folder:
   ```
   data/resume_dataset.csv
   ```

### Step 2: Train the ML Model

```bash
# Install Python dependencies
pip install -r requirements.txt

# Train the model (one-time setup)
python train_model.py
```

This will:
- Load the dataset from `data/resume_dataset.csv`
- Preprocess the text
- Train TF-IDF vectorizer and SVM classifier
- Save models to `models/` folder

### Step 3: Configure Environment

Create a `.env` file in the root directory:

```env
# OpenRouter API (optional - for AI suggestions)
OPENROUTER_API_KEY=your_openrouter_api_key_here

# LanguageTool API (optional - for grammar checking)
LANGUAGETOOL_API_KEY=your_languagetool_key_or_leave_empty

# Server Configuration
BACKEND_PORT=5000
FRONTEND_PORT=3000
ML_SERVICE_PORT=5001
```

### Step 4: Run the Application

#### Terminal 1 - Backend Server
```bash
cd backend
pip install -r requirements.txt
python app.py
```

#### Terminal 2 - ML Service
```bash
cd ml_service
pip install -r requirements.txt
python ml_api.py
```

#### Terminal 3 - Frontend
```bash
cd frontend
npm install
npm start
```

### Step 5: Access the Application

Open your browser and navigate to:
```
http://localhost:3000
```

## 📁 Project Structure

```
smart-resume-analyzer/
├── README.md
├── train_model.py          # Model training script
├── requirements.txt        # Python dependencies
├── .env                    # Environment variables
├── data/
│   └── resume_dataset.csv  # Your training dataset (add manually)
├── models/
│   ├── tfidf_vectorizer.pkl
│   ├── svm_model.pkl
│   └── label_encoder.pkl
├── backend/
│   ├── app.py              # Flask backend
│   ├── requirements.txt
│   └── utils/
│       └── text_extractor.py
├── ml_service/
│   ├── ml_api.py           # ML inference API
│   ├── requirements.txt
│   └── analyzers/
│       ├── ats_scorer.py
│       ├── skills_analyzer.py
│       └── suggestions_engine.py
└── frontend/
    ├── package.json
    ├── public/
    └── src/
        ├── App.js
        ├── pages/
        ├── components/
        └── styles/
```

## 🎯 How It Works

### Training Phase
1. Load resume dataset from CSV
2. Generate realistic job descriptions for each category
3. Compute TF-IDF vectors
4. Calculate cosine similarity (resume vs JD)
5. Label data: similarity > 0.65 = Selected (1), else Not Selected (0)
6. Train SVM classifier
7. Save models

### Inference Phase
1. User uploads resume + provides job description
2. Extract text from PDF/DOCX
3. Transform using trained TF-IDF vectorizer
4. Compute JD Match Score (cosine similarity)
5. Predict using SVM (Selected/Not Selected + confidence)
6. Calculate ATS score using multiple metrics
7. Analyze skills, grammar, sections
8. Generate structured suggestions
9. Return comprehensive JSON response

## 📊 Output Format

```json
{
  "ats_score": 75,
  "jd_match": 68,
  "svm_prediction": "Selected",
  "confidence": 82,
  "skills": {
    "found": ["Python", "Machine Learning", "TensorFlow"],
    "missing": ["Docker", "Kubernetes"]
  },
  "sections": {
    "contact": true,
    "summary": true,
    "experience": true,
    "education": true,
    "skills": true
  },
  "grammar_errors": 3,
  "suggestions": {
    "improvements": [
      "Add quantifiable achievements in experience section",
      "Include more technical keywords from job description",
      "Optimize resume length to 1-2 pages"
    ],
    "strengths": [
      "Strong technical skills alignment",
      "Clear project descriptions",
      "Well-structured format"
    ]
  }
}
```

## 🛠️ Technology Stack

### Backend
- Flask (Python web framework)
- PyPDF2 / pdfplumber (PDF extraction)
- python-docx (DOCX extraction)
- scikit-learn (ML)
- pandas, numpy

### ML Service
- TF-IDF Vectorization
- SVM Classifier
- LanguageTool API
- OpenRouter API (optional)

### Frontend
- React.js
- Axios (HTTP client)
- Framer Motion (animations)
- React Router
- CSS3 with animations

## 🔧 API Endpoints

### Backend (`http://localhost:5000`)
- `POST /upload` - Upload resume and job description

### ML Service (`http://localhost:5001`)
- `POST /analyze` - Analyze resume text

## 📝 Notes

- The system works completely offline after training (except grammar and AI suggestions)
- Grammar checking uses free LanguageTool API
- AI suggestions are optional (works with rule-based only if no API key)
- All suggestions are returned as bullet points (no paragraphs)
- Dataset must be placed manually in `data/` folder before training
- Training is required only once (unless you update the dataset)

## 🎨 UI Theme

- **Colors**: Beige, Brown, Gold tones
- **Style**: Futuristic with smooth animations
- **Layout**: Clean, modern, non-generic
- **Responsive**: Mobile-first design

## 🐛 Troubleshooting

**Model not found error:**
- Ensure you ran `python train_model.py` successfully
- Check that `models/` folder contains .pkl files

**Port already in use:**
- Change ports in `.env` file
- Kill existing processes on those ports

**Import errors:**
- Ensure all requirements are installed
- Use virtual environment for isolation

## 📜 License

MIT License - feel free to use and modify for your needs.

## 🤝 Contributing

This is a production-ready template. Customize as needed for your specific use case.
