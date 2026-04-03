import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { motion } from 'framer-motion';
import axios from 'axios';
import { API_ENDPOINTS } from '../config/api';
import '../styles/Upload.css';

const Upload = () => {
  const navigate = useNavigate();
  const [file, setFile] = useState(null);
  const [jobDescription, setJobDescription] = useState('');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const [dragActive, setDragActive] = useState(false);

  const handleDrag = (e) => {
    e.preventDefault();
    e.stopPropagation();
    if (e.type === "dragenter" || e.type === "dragover") {
      setDragActive(true);
    } else if (e.type === "dragleave") {
      setDragActive(false);
    }
  };

  const handleDrop = (e) => {
    e.preventDefault();
    e.stopPropagation();
    setDragActive(false);
    
    if (e.dataTransfer.files && e.dataTransfer.files[0]) {
      handleFileChange(e.dataTransfer.files[0]);
    }
  };

  const handleFileChange = (selectedFile) => {
    const validTypes = ['application/pdf', 'application/vnd.openxmlformats-officedocument.wordprocessingml.document'];
    
    if (selectedFile && validTypes.includes(selectedFile.type)) {
      setFile(selectedFile);
      setError('');
    } else {
      setError('Please upload a valid PDF or DOCX file');
      setFile(null);
    }
  };

  const handleFileInput = (e) => {
    if (e.target.files && e.target.files[0]) {
      handleFileChange(e.target.files[0]);
    }
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    
    if (!file) {
      setError('Please upload a resume');
      return;
    }
    
    if (!jobDescription || jobDescription.trim().length < 10) {
      setError('Please enter a job description (minimum 10 characters)');
      return;
    }

    setLoading(true);
    setError('');

    const formData = new FormData();
    formData.append('resume', file);
    formData.append('job_description', jobDescription);

    try {
      const response = await axios.post(API_ENDPOINTS.UPLOAD, formData, {
        headers: {
          'Content-Type': 'multipart/form-data',
        },
      });

      // Navigate to dashboard with results
      navigate('/dashboard', { state: { results: response.data } });
    } catch (err) {
      setError(err.response?.data?.error || 'An error occurred. Please try again.');
      setLoading(false);
    }
  };

  return (
    <div className="upload-page">
      <div className="upload-header">
        <motion.button
          className="back-btn"
          onClick={() => navigate('/')}
          whileHover={{ x: -5 }}
          whileTap={{ scale: 0.95 }}
        >
          ← Back to Home
        </motion.button>
      </div>

      <div className="upload-container">
        <motion.div
          className="upload-content"
          initial={{ opacity: 0, y: 30 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.6 }}
        >
          <h1 className="upload-title">
            Analyze Your Resume
          </h1>
          <p className="upload-subtitle">
            Upload your resume and paste the job description to get instant AI-powered insights
          </p>

          <form onSubmit={handleSubmit} className="upload-form">
            {/* File Upload */}
            <div className="form-section">
              <label className="form-label">Resume Upload</label>
              <div
                className={`dropzone ${dragActive ? 'active' : ''} ${file ? 'has-file' : ''}`}
                onDragEnter={handleDrag}
                onDragLeave={handleDrag}
                onDragOver={handleDrag}
                onDrop={handleDrop}
              >
                {file ? (
                  <div className="file-info">
                    <div className="file-icon">📄</div>
                    <div className="file-details">
                      <p className="file-name">{file.name}</p>
                      <p className="file-size">{(file.size / 1024).toFixed(2)} KB</p>
                    </div>
                    <button
                      type="button"
                      className="remove-file"
                      onClick={() => setFile(null)}
                    >
                      ✕
                    </button>
                  </div>
                ) : (
                  <div className="dropzone-content">
                    <div className="upload-icon">📁</div>
                    <p className="dropzone-text">
                      Drag & drop your resume here
                    </p>
                    <p className="dropzone-subtext">or</p>
                    <label className="file-input-label">
                      <input
                        type="file"
                        className="file-input"
                        accept=".pdf,.docx"
                        onChange={handleFileInput}
                      />
                      Browse Files
                    </label>
                    <p className="file-types">Supports PDF and DOCX (Max 10MB)</p>
                  </div>
                )}
              </div>
            </div>

            {/* Job Description */}
            <div className="form-section">
              <label className="form-label">Job Description</label>
              <textarea
                className="job-description-input"
                placeholder="Paste the complete job description here including requirements, responsibilities, and qualifications..."
                value={jobDescription}
                onChange={(e) => setJobDescription(e.target.value)}
                rows={12}
              />
              <div className="char-counter">
                {jobDescription.length} characters
              </div>
            </div>

            {/* Error Message */}
            {error && (
              <motion.div
                className="error-message"
                initial={{ opacity: 0, y: -10 }}
                animate={{ opacity: 1, y: 0 }}
              >
                ⚠️ {error}
              </motion.div>
            )}

            {/* Submit Button */}
            <motion.button
              type="submit"
              className="btn btn-primary submit-btn"
              disabled={loading}
              whileHover={{ scale: loading ? 1 : 1.02 }}
              whileTap={{ scale: loading ? 1 : 0.98 }}
            >
              {loading ? (
                <>
                  <div className="spinner-small"></div>
                  Analyzing...
                </>
              ) : (
                'Analyze Resume'
              )}
            </motion.button>
          </form>

          {/* Info Cards */}
          <div className="info-cards">
            <div className="info-card">
              <span className="info-icon">⚡</span>
              <p>Fast analysis in under 30 seconds</p>
            </div>
            <div className="info-card">
              <span className="info-icon">🔒</span>
              <p>Your data is secure and private</p>
            </div>
            <div className="info-card">
              <span className="info-icon">🎯</span>
              <p>95% accuracy with ML predictions</p>
            </div>
          </div>
        </motion.div>
      </div>
    </div>
  );
};

export default Upload;
