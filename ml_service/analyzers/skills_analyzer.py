"""
Skills Analyzer
Identifies found and missing skills from job description
"""

import re


def analyze_skills(resume_text, job_description):
    """
    Analyze skills match between resume and job description
    Returns: {found: [...], missing: [...]}
    """
    
    # Extract skills from job description
    jd_skills = extract_skills_from_text(job_description)
    
    # Extract skills from resume
    resume_skills = extract_skills_from_text(resume_text)
    
    # Find matches (case-insensitive)
    resume_skills_lower = {skill.lower(): skill for skill in resume_skills}
    
    found_skills = []
    missing_skills = []
    
    for jd_skill in jd_skills:
        jd_skill_lower = jd_skill.lower()
        
        # Check for exact match or partial match
        if jd_skill_lower in resume_skills_lower:
            found_skills.append(jd_skill)
        else:
            # Check for partial matches (e.g., "JavaScript" matches "JS")
            found = False
            for resume_skill_lower in resume_skills_lower:
                if (jd_skill_lower in resume_skill_lower or 
                    resume_skill_lower in jd_skill_lower):
                    found_skills.append(jd_skill)
                    found = True
                    break
            
            if not found:
                missing_skills.append(jd_skill)
    
    # Limit to most important skills
    return {
        'found': found_skills[:15],  # Top 15 found
        'missing': missing_skills[:10]  # Top 10 missing
    }


def extract_skills_from_text(text):
    """
    Extract technical skills and keywords from text
    """
    
    # Comprehensive skill database
    skill_patterns = [
        # Programming Languages
        r'\b(Python|Java|JavaScript|TypeScript|C\+\+|C#|Ruby|Go|Rust|Swift|Kotlin|PHP|Scala|R|MATLAB)\b',
        
        # Web Technologies
        r'\b(HTML|CSS|React|Angular|Vue|Node\.js|Express|Django|Flask|FastAPI|Spring|ASP\.NET)\b',
        
        # Databases
        r'\b(SQL|MySQL|PostgreSQL|MongoDB|Oracle|Redis|Cassandra|DynamoDB|SQLite|MariaDB)\b',
        
        # Cloud & DevOps
        r'\b(AWS|Azure|GCP|Docker|Kubernetes|Jenkins|CI/CD|Terraform|Ansible|Git|GitHub|GitLab)\b',
        
        # Data Science & ML
        r'\b(Machine Learning|Deep Learning|TensorFlow|PyTorch|Scikit-learn|Pandas|NumPy|Keras|NLP|Computer Vision)\b',
        
        # Tools & Frameworks
        r'\b(Jira|Confluence|Slack|Tableau|Power BI|Excel|Figma|Sketch|Photoshop|Illustrator)\b',
        
        # Methodologies
        r'\b(Agile|Scrum|Kanban|DevOps|Microservices|REST API|GraphQL|TDD|CI/CD)\b',
        
        # Soft Skills
        r'\b(Leadership|Communication|Team Management|Problem Solving|Analytical|Critical Thinking)\b',
        
        # Certifications & Concepts
        r'\b(AWS Certified|Azure Certified|PMP|Certified|Security|Networking|API|ETL|Data Pipeline)\b'
    ]
    
    skills = set()
    
    for pattern in skill_patterns:
        matches = re.findall(pattern, text, re.IGNORECASE)
        skills.update(matches)
    
    # Also extract capitalized technical terms
    cap_words = re.findall(r'\b[A-Z][a-zA-Z]{2,}\b', text)
    
    # Filter technical-sounding capitalized words
    for word in cap_words:
        if (len(word) >= 3 and 
            not word.lower() in ['the', 'and', 'for', 'with', 'this', 'that']):
            skills.add(word)
    
    # Extract acronyms (2-5 uppercase letters)
    acronyms = re.findall(r'\b[A-Z]{2,5}\b', text)
    skills.update(acronyms)
    
    # Clean and return
    cleaned_skills = [skill.strip() for skill in skills if len(skill.strip()) >= 2]
    
    # Remove duplicates (case-insensitive)
    unique_skills = {}
    for skill in cleaned_skills:
        key = skill.lower()
        if key not in unique_skills:
            unique_skills[key] = skill
    
    return list(unique_skills.values())
