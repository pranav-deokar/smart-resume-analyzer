"""
ATS Score Calculator
Calculates comprehensive ATS score based on multiple metrics
"""

import re


def calculate_ats_score(resume_text, job_description, jd_match):
    """
    Calculate ATS score using multiple weighted metrics
    
    Metrics:
    - JD Match Score (40%)
    - Keyword Density (25%)
    - Format & Structure (20%)
    - Length Optimization (15%)
    
    Returns: ATS score (0-100)
    """
    
    # Metric 1: JD Match (40% weight)
    jd_score = min(jd_match, 100)  # Cap at 100
    
    # Metric 2: Keyword Density (25% weight)
    keyword_score = calculate_keyword_density(resume_text, job_description)
    
    # Metric 3: Format & Structure (20% weight)
    format_score = calculate_format_score(resume_text)
    
    # Metric 4: Length Optimization (15% weight)
    length_score = calculate_length_score(resume_text)
    
    # Weighted average
    ats_score = (
        jd_score * 0.40 +
        keyword_score * 0.25 +
        format_score * 0.20 +
        length_score * 0.15
    )
    
    return round(ats_score, 2)


def calculate_keyword_density(resume_text, job_description):
    """
    Calculate keyword density score
    Measures how many important keywords from JD appear in resume
    """
    # Extract important words from JD (longer than 4 chars, not common words)
    jd_words = set(re.findall(r'\b[a-z]{5,}\b', job_description.lower()))
    
    # Common words to exclude
    common_words = {
        'experience', 'required', 'preferred', 'ability', 'skills',
        'knowledge', 'position', 'candidates', 'looking', 'seeking',
        'opportunity', 'excellent', 'strong', 'years', 'demonstrated'
    }
    
    jd_keywords = jd_words - common_words
    
    if not jd_keywords:
        return 50  # Neutral score if no keywords found
    
    # Count matching keywords in resume
    resume_lower = resume_text.lower()
    matches = sum(1 for keyword in jd_keywords if keyword in resume_lower)
    
    # Calculate percentage
    match_rate = (matches / len(jd_keywords)) * 100
    
    # Score: higher is better, cap at 100
    score = min(match_rate * 1.2, 100)
    
    return round(score, 2)


def calculate_format_score(resume_text):
    """
    Evaluate resume format and structure
    Checks for key sections and proper formatting
    """
    score = 0
    max_score = 100
    
    text_lower = resume_text.lower()
    
    # Check for key sections (60 points total)
    sections = {
        'contact': r'(email|phone|linkedin)',
        'summary': r'(summary|objective|profile)',
        'experience': r'(experience|work history|employment)',
        'education': r'(education|degree|university)',
        'skills': r'(skills|technologies|proficient)',
    }
    
    for section, pattern in sections.items():
        if re.search(pattern, text_lower):
            score += 12  # 12 points per section
    
    # Check for quantifiable achievements (20 points)
    numbers = re.findall(r'\b\d+%?\b', resume_text)
    if len(numbers) >= 5:
        score += 20
    elif len(numbers) >= 2:
        score += 10
    
    # Check for action verbs (20 points)
    action_verbs = [
        'developed', 'managed', 'led', 'created', 'implemented',
        'designed', 'built', 'improved', 'increased', 'reduced',
        'achieved', 'established', 'launched', 'optimized'
    ]
    
    verb_count = sum(1 for verb in action_verbs if verb in text_lower)
    if verb_count >= 5:
        score += 20
    elif verb_count >= 3:
        score += 10
    
    return min(score, max_score)


def calculate_length_score(resume_text):
    """
    Evaluate resume length (optimal: 400-1000 words)
    """
    word_count = len(resume_text.split())
    
    if 400 <= word_count <= 1000:
        # Optimal range
        score = 100
    elif 300 <= word_count < 400 or 1000 < word_count <= 1200:
        # Acceptable range
        score = 80
    elif 200 <= word_count < 300 or 1200 < word_count <= 1500:
        # Suboptimal range
        score = 60
    elif word_count < 200:
        # Too short
        score = 40
    else:
        # Too long
        score = 50
    
    return score
