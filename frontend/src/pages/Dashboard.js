import React, { useEffect, useState } from 'react';
import { useLocation, useNavigate } from 'react-router-dom';
import { motion } from 'framer-motion';
import '../styles/Dashboard.css';

const Dashboard = () => {
  const location = useLocation();
  const navigate = useNavigate();
  const [results, setResults] = useState(null);
  const [activeTab, setActiveTab] = useState('overview');

  useEffect(() => {
    if (!location.state?.results) {
      navigate('/upload');
    } else {
      setResults(location.state.results);
    }
  }, [location, navigate]);

  if (!results) {
    return null;
  }

  const getScoreColor = (score) => {
    if (score >= 75) return '#4CAF50';
    if (score >= 50) return '#FFA726';
    return '#EF5350';
  };

  const getScoreLabel = (score) => {
    if (score >= 75) return 'Excellent';
    if (score >= 60) return 'Good';
    if (score >= 40) return 'Average';
    return 'Needs Improvement';
  };

  return (
    <div className="dashboard">
      {/* Header */}
      <div className="dashboard-header">
        <div className="container">
          <div className="header-content">
            <motion.div
              initial={{ opacity: 0, x: -20 }}
              animate={{ opacity: 1, x: 0 }}
            >
              <h1 className="dashboard-title">Resume Analysis</h1>
              <p className="dashboard-subtitle">AI-Powered Insights & Recommendations</p>
            </motion.div>
            <motion.button
              className="btn btn-secondary"
              onClick={() => navigate('/upload')}
              whileHover={{ scale: 1.05 }}
              whileTap={{ scale: 0.95 }}
              initial={{ opacity: 0, x: 20 }}
              animate={{ opacity: 1, x: 0 }}
            >
              Analyze Another
            </motion.button>
          </div>
        </div>
      </div>

      <div className="container">
        {/* Main Score Card */}
        <motion.div
          className="main-score-card"
          initial={{ opacity: 0, y: 30 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.6 }}
        >
          <div className="score-primary">
            <div className="score-circle">
              <svg viewBox="0 0 200 200" className="score-svg">
                <circle
                  cx="100"
                  cy="100"
                  r="85"
                  fill="none"
                  stroke="var(--beige-light)"
                  strokeWidth="12"
                />
                <motion.circle
                  cx="100"
                  cy="100"
                  r="85"
                  fill="none"
                  stroke={getScoreColor(results.ats_score)}
                  strokeWidth="12"
                  strokeLinecap="round"
                  strokeDasharray={`${2 * Math.PI * 85}`}
                  initial={{ strokeDashoffset: 2 * Math.PI * 85 }}
                  animate={{
                    strokeDashoffset: 2 * Math.PI * 85 * (1 - results.ats_score / 100)
                  }}
                  transition={{ duration: 1.5, ease: "easeOut" }}
                  style={{ transform: 'rotate(-90deg)', transformOrigin: 'center' }}
                />
              </svg>
              <div className="score-value">
                <motion.span
                  className="score-number"
                  initial={{ opacity: 0 }}
                  animate={{ opacity: 1 }}
                  transition={{ delay: 0.5 }}
                >
                  {results.ats_score}
                </motion.span>
                <span className="score-label">ATS Score</span>
              </div>
            </div>
            <div className="score-status">
              <span className="status-badge" style={{ background: getScoreColor(results.ats_score) }}>
                {getScoreLabel(results.ats_score)}
              </span>
            </div>
          </div>

          <div className="score-breakdown">
            <div className="breakdown-item">
              <span className="breakdown-label">JD Match</span>
              <div className="breakdown-bar">
                <motion.div
                  className="breakdown-fill"
                  initial={{ width: 0 }}
                  animate={{ width: `${results.jd_match}%` }}
                  transition={{ duration: 1, delay: 0.3 }}
                  style={{ background: 'var(--gradient-gold)' }}
                />
                <span className="breakdown-value">{results.jd_match}%</span>
              </div>
            </div>

            <div className="breakdown-item">
              <span className="breakdown-label">ML Confidence</span>
              <div className="breakdown-bar">
                <motion.div
                  className="breakdown-fill"
                  initial={{ width: 0 }}
                  animate={{ width: `${results.confidence}%` }}
                  transition={{ duration: 1, delay: 0.5 }}
                  style={{ background: 'var(--gradient-primary)' }}
                />
                <span className="breakdown-value">{results.confidence}%</span>
              </div>
            </div>

            <div className="prediction-card">
              <span className="prediction-label">ML Prediction</span>
              <span className={`prediction-value ${results.svm_prediction === 'Selected' ? 'selected' : 'not-selected'}`}>
                {results.svm_prediction}
              </span>
            </div>
          </div>
        </motion.div>

        {/* Tabs */}
        <div className="tabs">
          {['overview', 'skills', 'suggestions'].map((tab) => (
            <button
              key={tab}
              className={`tab ${activeTab === tab ? 'active' : ''}`}
              onClick={() => setActiveTab(tab)}
            >
              {tab.charAt(0).toUpperCase() + tab.slice(1)}
            </button>
          ))}
        </div>

        {/* Tab Content */}
        <div className="tab-content">
          {activeTab === 'overview' && (
            <motion.div
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              className="overview-grid"
            >
              {/* Sections Checklist */}
              <div className="card sections-card">
                <h3 className="card-title">Resume Sections</h3>
                <div className="sections-list">
                  {Object.entries(results.sections).map(([section, present]) => (
                    <div key={section} className="section-item">
                      <span className={`section-icon ${present ? 'present' : 'missing'}`}>
                        {present ? '✓' : '✕'}
                      </span>
                      <span className="section-name">
                        {section.charAt(0).toUpperCase() + section.slice(1)}
                      </span>
                    </div>
                  ))}
                </div>
              </div>

              {/* Grammar */}
              <div className="card grammar-card">
                <h3 className="card-title">Grammar Check</h3>
                <div className="grammar-score">
                  <span className="grammar-icon">
                    {results.grammar_errors === 0 ? '✓' : '⚠'}
                  </span>
                  <div className="grammar-info">
                    <span className="grammar-count">{results.grammar_errors}</span>
                    <span className="grammar-label">
                      {results.grammar_errors === 1 ? 'Issue' : 'Issues'} Found
                    </span>
                  </div>
                </div>
                {results.grammar_corrections && results.grammar_corrections.length > 0 && (
                  <div className="grammar-corrections">
                    <p className="corrections-title">Top Corrections:</p>
                    <ul className="corrections-list">
                      {results.grammar_corrections.slice(0, 3).map((correction, idx) => (
                        <li key={idx}>{correction}</li>
                      ))}
                    </ul>
                  </div>
                )}
              </div>
            </motion.div>
          )}

          {activeTab === 'skills' && (
            <motion.div
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              className="skills-grid"
            >
              {/* Found Skills */}
              <div className="card skills-card">
                <h3 className="card-title">
                  <span className="title-icon">✓</span>
                  Found Skills ({results.skills.found.length})
                </h3>
                <div className="skills-tags">
                  {results.skills.found.map((skill, idx) => (
                    <motion.span
                      key={idx}
                      className="skill-tag found"
                      initial={{ opacity: 0, scale: 0.8 }}
                      animate={{ opacity: 1, scale: 1 }}
                      transition={{ delay: idx * 0.05 }}
                    >
                      {skill}
                    </motion.span>
                  ))}
                </div>
              </div>

              {/* Missing Skills */}
              <div className="card skills-card">
                <h3 className="card-title">
                  <span className="title-icon">+</span>
                  Missing Skills ({results.skills.missing.length})
                </h3>
                {results.skills.missing.length > 0 ? (
                  <div className="skills-tags">
                    {results.skills.missing.map((skill, idx) => (
                      <motion.span
                        key={idx}
                        className="skill-tag missing"
                        initial={{ opacity: 0, scale: 0.8 }}
                        animate={{ opacity: 1, scale: 1 }}
                        transition={{ delay: idx * 0.05 }}
                      >
                        {skill}
                      </motion.span>
                    ))}
                  </div>
                ) : (
                  <p className="no-missing">All required skills present!</p>
                )}
              </div>
            </motion.div>
          )}

          {activeTab === 'suggestions' && (
            <motion.div
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              className="suggestions-grid"
            >
              {/* Improvements */}
              <div className="card suggestions-card">
                <h3 className="card-title">
                  <span className="title-icon">💡</span>
                  Areas for Improvement
                </h3>
                <ul className="suggestions-list">
                  {results.suggestions.improvements.map((suggestion, idx) => (
                    <motion.li
                      key={idx}
                      initial={{ opacity: 0, x: -20 }}
                      animate={{ opacity: 1, x: 0 }}
                      transition={{ delay: idx * 0.1 }}
                    >
                      {suggestion}
                    </motion.li>
                  ))}
                </ul>
              </div>

              {/* Strengths */}
              <div className="card suggestions-card">
                <h3 className="card-title">
                  <span className="title-icon">⭐</span>
                  Resume Strengths
                </h3>
                <ul className="suggestions-list strengths">
                  {results.suggestions.strengths.map((strength, idx) => (
                    <motion.li
                      key={idx}
                      initial={{ opacity: 0, x: -20 }}
                      animate={{ opacity: 1, x: 0 }}
                      transition={{ delay: idx * 0.1 }}
                    >
                      {strength}
                    </motion.li>
                  ))}
                </ul>
              </div>
            </motion.div>
          )}
        </div>

        {/* Action Buttons */}
        <motion.div
          className="action-buttons"
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          transition={{ delay: 0.8 }}
        >
          <button className="btn btn-primary" onClick={() => navigate('/upload')}>
            Analyze Another Resume
          </button>
          <button className="btn btn-secondary" onClick={() => navigate('/')}>
            Back to Home
          </button>
        </motion.div>
      </div>
    </div>
  );
};

export default Dashboard;
