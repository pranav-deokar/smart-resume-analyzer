"""
Suggestions Engine
Generates actionable improvement suggestions and identifies strengths
Uses rule-based logic and optional AI enhancement
"""

import os
import re
import requests
from dotenv import load_dotenv

load_dotenv()


def generate_suggestions(resume_text, job_description, ats_score, jd_match, 
                        skills_analysis, sections, grammar_errors):
    """
    Generate structured suggestions
    Returns: {improvements: [...], strengths: [...]}
    """
    
    improvements = []
    strengths = []
    
    # Rule-based improvements
    improvements.extend(get_rule_based_improvements(
        resume_text, job_description, ats_score, jd_match,
        skills_analysis, sections, grammar_errors
    ))
    
    # Rule-based strengths
    strengths.extend(get_rule_based_strengths(
        resume_text, ats_score, jd_match, skills_analysis, sections
    ))
    
    # Optional: AI-enhanced suggestions
    if os.getenv('OPENROUTER_API_KEY'):
        try:
            ai_suggestions = get_ai_suggestions(
                resume_text, job_description, ats_score, jd_match
            )
            if ai_suggestions:
                improvements.extend(ai_suggestions.get('improvements', [])[:3])
                strengths.extend(ai_suggestions.get('strengths', [])[:2])
                print("OpenRouter Raw Response:", ai_suggestions)
        except Exception as e:
            print(f"AI suggestions error: {e}")
    
    # Remove duplicates and limit
    improvements = list(dict.fromkeys(improvements))[:8]
    strengths = list(dict.fromkeys(strengths))[:6]
    
    return {
        'improvements': improvements,
        'strengths': strengths
    }


def get_rule_based_improvements(resume_text, job_description, ats_score, jd_match,
                                skills_analysis, sections, grammar_errors):
    """Generate rule-based improvement suggestions"""
    
    improvements = []
    
    # JD Match Score
    if jd_match < 50:
        improvements.append("Incorporate more keywords from the job description throughout your resume")
        improvements.append("Align your experience descriptions with the job requirements")
    elif jd_match < 70:
        improvements.append("Strengthen alignment with job description by emphasizing relevant skills")
    
    # Missing Skills
    if len(skills_analysis['missing']) > 5:
        improvements.append(f"Consider adding or highlighting these skills: {', '.join(skills_analysis['missing'][:5])}")
    
    # Grammar
    if grammar_errors > 5:
        improvements.append("Review and fix grammar errors to ensure professional presentation")
    elif grammar_errors > 0:
        improvements.append("Polish your resume by addressing minor grammar issues")
    
    # Sections
    if not sections.get('summary'):
        improvements.append("Add a professional summary or objective statement at the top")
    
    if not sections.get('contact'):
        improvements.append("Ensure contact information (email, phone, LinkedIn) is clearly visible")
    
    if not sections.get('projects') and jd_match < 70:
        improvements.append("Include a projects section to showcase practical experience")
    
    # Quantifiable achievements
    numbers = re.findall(r'\b\d+%?\b', resume_text)
    if len(numbers) < 3:
        improvements.append("Add quantifiable achievements with specific numbers and percentages")
    
    # Action verbs
    action_verbs = ['developed', 'managed', 'led', 'created', 'implemented']
    verb_count = sum(1 for verb in action_verbs if verb in resume_text.lower())
    if verb_count < 3:
        improvements.append("Use stronger action verbs to describe your accomplishments")
    
    # Length
    word_count = len(resume_text.split())
    if word_count < 300:
        improvements.append("Expand your resume with more details about your experience and skills")
    elif word_count > 1200:
        improvements.append("Consider condensing your resume to 1-2 pages for better readability")
    
    # ATS Score
    if ats_score < 60:
        improvements.append("Optimize resume structure with clear section headers and bullet points")
    
    return improvements


def get_rule_based_strengths(resume_text, ats_score, jd_match, skills_analysis, sections):
    """Identify resume strengths"""
    
    strengths = []
    
    # High scores
    if ats_score >= 75:
        strengths.append("Excellent ATS compatibility with well-structured format")
    
    if jd_match >= 70:
        strengths.append("Strong alignment with job description requirements")
    
    # Skills match
    if len(skills_analysis['found']) >= 8:
        strengths.append("Comprehensive technical skill set matching job requirements")
    
    # Sections completeness
    section_count = sum(1 for v in sections.values() if v)
    if section_count >= 5:
        strengths.append("Complete resume structure with all essential sections")
    
    # Quantifiable achievements
    numbers = re.findall(r'\b\d+%?\b', resume_text)
    if len(numbers) >= 5:
        strengths.append("Effective use of metrics and quantifiable achievements")
    
    # Action verbs
    action_verbs = ['developed', 'managed', 'led', 'created', 'implemented', 
                    'designed', 'built', 'improved', 'increased', 'reduced']
    verb_count = sum(1 for verb in action_verbs if verb in resume_text.lower())
    if verb_count >= 5:
        strengths.append("Strong use of action verbs to demonstrate impact")
    
    # Professional keywords
    professional_terms = ['experience', 'project', 'team', 'development', 'analysis']
    term_count = sum(1 for term in professional_terms if term in resume_text.lower())
    if term_count >= 4:
        strengths.append("Professional terminology and industry-relevant language")
    
    return strengths


def get_ai_suggestions(resume_text, job_description, ats_score, jd_match):
    """
    Get AI-powered suggestions using OpenRouter API
    Optional enhancement - returns None if API fails
    """
    
    api_key = os.getenv('OPENROUTER_API_KEY')
    if not api_key:
        return None
    
    try:
        url = "https://openrouter.ai/api/v1/chat/completions"
        
        prompt = f"""Analyze this resume against the job description and provide brief, actionable suggestions.

Resume Summary: {resume_text[:500]}...
Job Description: {job_description[:300]}...
Current ATS Score: {ats_score}
JD Match: {jd_match}%

Provide exactly 3 improvements and 2 strengths as bullet points.
Keep each point to ONE sentence (15 words max).
Focus on specific, actionable advice.

Format as JSON:
{{
  "improvements": ["point 1", "point 2", "point 3"],
  "strengths": ["strength 1", "strength 2"]
}}"""

        headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        }
        
        payload = {
            "model": "openai/gpt-3.5-turbo",
            "messages": [
                {"role": "user", "content": prompt}
            ],
            "max_tokens": 300,
            "temperature": 0.7
        }
        
        response = requests.post(url, json=payload, headers=headers, timeout=15)
        
        if response.status_code == 200:
            result = response.json()
            content = result['choices'][0]['message']['content']
            
            # Try to parse JSON response
            import json
            suggestions = json.loads(content)
            return suggestions
        
        return None
    
    except Exception as e:
        print(f"AI suggestion error: {e}")
        return None
