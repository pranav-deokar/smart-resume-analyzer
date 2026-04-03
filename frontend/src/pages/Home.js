import React from 'react';
import { useNavigate } from 'react-router-dom';
import { motion } from 'framer-motion';
import '../styles/Home.css';

const Home = () => {
  const navigate = useNavigate();

  const features = [
    {
      title: "ATS Score",
      description: "Multi-metric scoring system analyzing format, keywords, and structure",
      icon: "📊"
    },
    {
      title: "ML Prediction",
      description: "SVM-based machine learning model predicts selection probability",
      icon: "🤖"
    },
    {
      title: "JD Matching",
      description: "Cosine similarity analysis between resume and job description",
      icon: "🎯"
    },
    {
      title: "Skills Analysis",
      description: "Identifies found and missing skills from job requirements",
      icon: "⚡"
    },
    {
      title: "Grammar Check",
      description: "Professional grammar analysis for polished presentation",
      icon: "✍️"
    },
    {
      title: "AI Suggestions",
      description: "Intelligent, actionable feedback to improve your resume",
      icon: "💡"
    }
  ];

  const tips = [
    "Optimize resume length between 400-1000 words for best ATS performance",
    "Use action verbs like 'developed', 'managed', 'led' to showcase achievements",
    "Include quantifiable metrics (percentages, numbers) to demonstrate impact",
    "Align technical keywords from job description throughout your resume",
    "Maintain clear section headers: Summary, Experience, Education, Skills"
  ];

  return (
    <div className="home">
      {/* Hero Section */}
      <section className="hero">
        <motion.div 
          className="hero-content"
          initial={{ opacity: 0, y: 30 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.8 }}
        >
          <motion.div
            className="hero-badge"
            initial={{ opacity: 0, scale: 0.8 }}
            animate={{ opacity: 1, scale: 1 }}
            transition={{ delay: 0.2, duration: 0.6 }}
          >
            AI-POWERED ANALYSIS
          </motion.div>
          
          <motion.h1 
            className="hero-title"
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: 0.4, duration: 0.8 }}
          >
            Smart Resume
            <span className="hero-title-accent"> Analyzer</span>
          </motion.h1>
          
          <motion.p 
            className="hero-subtitle"
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            transition={{ delay: 0.6, duration: 0.8 }}
          >
            Decode ATS systems with machine learning. Optimize your resume.
            <br />Land your dream job.
          </motion.p>
          
          <motion.div 
            className="hero-cta"
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: 0.8, duration: 0.8 }}
          >
            <button 
              className="btn btn-primary hero-btn"
              onClick={() => navigate('/upload')}
            >
              Analyze Resume
            </button>
            <div className="hero-stats">
              <div className="stat-item">
                <span className="stat-value">95%</span>
                <span className="stat-label">Accuracy</span>
              </div>
              <div className="stat-divider"></div>
              <div className="stat-item">
                <span className="stat-value">&lt;30s</span>
                <span className="stat-label">Analysis</span>
              </div>
            </div>
          </motion.div>
        </motion.div>

        <div className="hero-decoration">
          <div className="decoration-circle decoration-circle-1"></div>
          <div className="decoration-circle decoration-circle-2"></div>
          <div className="decoration-line decoration-line-1"></div>
          <div className="decoration-line decoration-line-2"></div>
        </div>
      </section>

      {/* Features Section */}
      <section className="features">
        <div className="container">
          <motion.h2 
            className="section-title"
            initial={{ opacity: 0, y: 20 }}
            whileInView={{ opacity: 1, y: 0 }}
            viewport={{ once: true }}
            transition={{ duration: 0.6 }}
          >
            Comprehensive Analysis
          </motion.h2>
          
          <div className="features-grid">
            {features.map((feature, index) => (
              <motion.div
                key={index}
                className="feature-card"
                initial={{ opacity: 0, y: 30 }}
                whileInView={{ opacity: 1, y: 0 }}
                viewport={{ once: true }}
                transition={{ delay: index * 0.1, duration: 0.6 }}
                whileHover={{ y: -5 }}
              >
                <div className="feature-icon">{feature.icon}</div>
                <h3 className="feature-title">{feature.title}</h3>
                <p className="feature-description">{feature.description}</p>
              </motion.div>
            ))}
          </div>
        </div>
      </section>

      {/* Tips Section */}
      <section className="tips">
        <div className="container">
          <motion.h2 
            className="section-title"
            initial={{ opacity: 0, y: 20 }}
            whileInView={{ opacity: 1, y: 0 }}
            viewport={{ once: true }}
            transition={{ duration: 0.6 }}
          >
            Resume Optimization Tips
          </motion.h2>
          
          <div className="tips-list">
            {tips.map((tip, index) => (
              <motion.div
                key={index}
                className="tip-item"
                initial={{ opacity: 0, x: -20 }}
                whileInView={{ opacity: 1, x: 0 }}
                viewport={{ once: true }}
                transition={{ delay: index * 0.1, duration: 0.6 }}
              >
                <div className="tip-number">{String(index + 1).padStart(2, '0')}</div>
                <p className="tip-text">{tip}</p>
              </motion.div>
            ))}
          </div>

          <motion.div 
            className="tips-cta"
            initial={{ opacity: 0 }}
            whileInView={{ opacity: 1 }}
            viewport={{ once: true }}
            transition={{ delay: 0.6, duration: 0.6 }}
          >
            <button 
              className="btn btn-primary"
              onClick={() => navigate('/upload')}
            >
              Get Started Now
            </button>
          </motion.div>
        </div>
      </section>

      {/* Footer */}
      <footer className="footer">
        <div className="container">
          <p className="footer-text">
            Smart Resume Analyzer &copy; 2024 | AI-Powered Career Tools
          </p>
        </div>
      </footer>
    </div>
  );
};

export default Home;
