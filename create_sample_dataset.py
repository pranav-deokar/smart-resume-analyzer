"""
Sample Dataset Generator
Creates a small sample dataset for testing the system
Run this if you don't have a real dataset
"""

import pandas as pd
import os

# Sample resumes (shortened for demo purposes)
sample_data = [
    {
        "Resume_str": """John Smith
Email: john.smith@email.com | Phone: 555-0123 | LinkedIn: linkedin.com/in/johnsmith

PROFESSIONAL SUMMARY
Data Scientist with 5+ years of experience in machine learning, statistical analysis, and data visualization. 
Expert in Python, R, and SQL with proven track record of delivering actionable insights.

EXPERIENCE
Senior Data Scientist | Tech Corp | 2020-Present
- Developed predictive models using Python and TensorFlow achieving 92% accuracy
- Led team of 4 data analysts in customer churn prediction project
- Implemented automated data pipelines processing 10M+ records daily
- Reduced analysis time by 40% through process optimization

Data Analyst | Analytics Inc | 2018-2020
- Created dashboards using Tableau and Power BI for C-level executives
- Performed statistical analysis on customer behavior data
- Collaborated with product team on A/B testing initiatives

EDUCATION
Master of Science in Data Science | University of California | 2018
Bachelor of Science in Statistics | State University | 2016

SKILLS
Programming: Python, R, SQL, Java
Machine Learning: TensorFlow, PyTorch, Scikit-learn, Keras
Data Visualization: Tableau, Power BI, Matplotlib, Seaborn
Databases: PostgreSQL, MongoDB, MySQL
Tools: Git, Docker, AWS, Jupyter""",
        "Category": "Data Science"
    },
    {
        "Resume_str": """Sarah Johnson
sarah.j@email.com | 555-0124 | github.com/sarahj | Portfolio: sarahj.dev

SUMMARY
Full Stack Web Developer specializing in React, Node.js, and cloud technologies. 
Passionate about building scalable web applications with clean, maintainable code.

WORK EXPERIENCE
Full Stack Developer | WebSolutions LLC | 2019-Present
- Built responsive web applications using React, Redux, and Material-UI
- Developed RESTful APIs with Node.js and Express serving 100k+ daily users
- Implemented CI/CD pipelines using Jenkins and Docker
- Optimized database queries reducing response time by 60%

Junior Developer | StartupXYZ | 2017-2019
- Created dynamic websites using HTML, CSS, JavaScript, and PHP
- Integrated third-party APIs including Stripe, SendGrid, and Google Maps
- Participated in code reviews and agile sprint planning

EDUCATION
Bachelor of Computer Science | Tech University | 2017

TECHNICAL SKILLS
Frontend: React, Vue.js, Angular, HTML5, CSS3, JavaScript, TypeScript
Backend: Node.js, Express, Django, PHP
Databases: MongoDB, PostgreSQL, MySQL, Redis
DevOps: Docker, Kubernetes, AWS, Jenkins, Git
Testing: Jest, Mocha, Cypress

PROJECTS
E-commerce Platform - Built full-stack application handling 50k transactions/month
Real-time Chat App - Developed using WebSocket and React with 1000+ concurrent users""",
        "Category": "Web Development"
    },
    {
        "Resume_str": """Michael Chen
m.chen@email.com | 555-0125 | LinkedIn: linkedin.com/in/michaelchen

OBJECTIVE
Software Engineer with expertise in Java, C++, and system design seeking challenging role 
in enterprise software development.

PROFESSIONAL EXPERIENCE
Software Engineer II | Enterprise Systems Inc | 2019-Present
- Designed and implemented microservices architecture using Spring Boot
- Developed high-performance algorithms processing 5M transactions/day
- Led code refactoring initiative improving system performance by 35%
- Mentored 3 junior developers on best practices and design patterns

Software Developer | Tech Solutions | 2017-2019
- Built enterprise applications using Java, Spring Framework, and Hibernate
- Implemented authentication and authorization using OAuth2 and JWT
- Created unit and integration tests achieving 90% code coverage

EDUCATION
Bachelor of Science in Computer Engineering | Engineering College | 2017
Relevant Coursework: Data Structures, Algorithms, Operating Systems, Database Systems

SKILLS
Languages: Java, C++, Python, JavaScript, SQL
Frameworks: Spring Boot, Spring MVC, Hibernate, JUnit
Tools: Maven, Gradle, Jenkins, Git, IntelliJ IDEA
Databases: Oracle, MySQL, PostgreSQL
Cloud: AWS (EC2, S3, RDS), Azure
Methodologies: Agile, Scrum, TDD, Object-Oriented Design

CERTIFICATIONS
Oracle Certified Professional Java SE 11 Developer
AWS Certified Solutions Architect - Associate""",
        "Category": "Software Engineer"
    },
    {
        "Resume_str": """Emily Rodriguez
emily.r@email.com | 555-0126 | github.com/emilyrodriguez

PROFESSIONAL SUMMARY
DevOps Engineer with 4+ years experience automating infrastructure, implementing CI/CD pipelines, 
and managing cloud environments at scale.

EXPERIENCE
DevOps Engineer | CloudFirst Inc | 2020-Present
- Managed AWS infrastructure serving 500k+ users with 99.9% uptime
- Automated deployment pipelines using Jenkins, GitLab CI, and GitHub Actions
- Implemented Infrastructure as Code using Terraform and Ansible
- Reduced deployment time by 70% through automation initiatives
- Set up monitoring and alerting using Prometheus and Grafana

Junior DevOps Engineer | TechStart | 2018-2020
- Containerized applications using Docker and orchestrated with Kubernetes
- Created automated backup and disaster recovery procedures
- Managed Linux servers and performed system administration tasks

EDUCATION
Bachelor of Science in Information Technology | State University | 2018

TECHNICAL SKILLS
Cloud Platforms: AWS (EC2, S3, RDS, Lambda, ECS), Azure, GCP
Containers & Orchestration: Docker, Kubernetes, Docker Compose
CI/CD: Jenkins, GitLab CI, GitHub Actions, CircleCI
Infrastructure as Code: Terraform, Ansible, CloudFormation
Monitoring: Prometheus, Grafana, ELK Stack, Datadog
Scripting: Bash, Python, PowerShell
Version Control: Git, GitHub, GitLab
Operating Systems: Linux (Ubuntu, CentOS), Windows Server

CERTIFICATIONS
AWS Certified DevOps Engineer - Professional
Certified Kubernetes Administrator (CKA)""",
        "Category": "DevOps"
    },
    {
        "Resume_str": """David Park
david.park@email.com | 555-0127

SUMMARY
Business Analyst with strong analytical skills and experience translating business 
requirements into technical specifications. Proven ability to drive process improvements.

WORK HISTORY
Senior Business Analyst | Finance Corp | 2019-Present
- Gathered and documented business requirements for 15+ projects
- Created process flow diagrams and technical specifications
- Facilitated meetings with stakeholders to define project scope
- Analyzed data to identify trends and recommend solutions
- Reduced operational costs by 25% through process optimization

Business Analyst | Consulting Group | 2017-2019
- Conducted gap analysis and recommended system improvements
- Created user stories and acceptance criteria for development teams
- Performed UAT and validated deliverables against requirements
- Developed reports and dashboards for executive leadership

EDUCATION
MBA in Business Analytics | Business School | 2017
Bachelor of Business Administration | University | 2015

SKILLS
Analysis: Requirements Gathering, Process Mapping, Gap Analysis, Data Analysis
Tools: JIRA, Confluence, Visio, Lucidchart, SQL, Excel, Tableau
Methodologies: Agile, Scrum, Waterfall, Six Sigma
Technical: SQL, Python, Power BI, Salesforce
Soft Skills: Stakeholder Management, Communication, Problem Solving, Critical Thinking

CERTIFICATIONS
Certified Business Analysis Professional (CBAP)
PMI Professional in Business Analysis (PMI-PBA)""",
        "Category": "Business Analyst"
    }
]

# Create DataFrame
df = pd.DataFrame(sample_data)

# Ensure data directory exists
os.makedirs('data', exist_ok=True)

# Save to CSV
output_path = 'data/resume_dataset.csv'
df.to_csv(output_path, index=False)

print(f"✅ Sample dataset created successfully!")
print(f"📁 Location: {output_path}")
print(f"📊 Number of samples: {len(df)}")
print(f"📋 Categories: {', '.join(df['Category'].unique())}")
print(f"\n⚠️  NOTE: This is a SMALL sample dataset for testing only.")
print(f"For production use, you should use a larger dataset (100+ resumes).")
print(f"\nNext steps:")
print(f"1. Run: python train_model.py")
print(f"2. Add API keys to .env file")
print(f"3. Start the servers")
