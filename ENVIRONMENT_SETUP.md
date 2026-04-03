# Environment Configuration Guide

This document explains how to configure the Smart Resume Analyzer for different deployment environments.

## Overview

The application has been updated to support both **local development** and **production deployment** without any breaking changes. The key is using environment variables with sensible fallback defaults.

### Architecture

- **Frontend**: React application (local: http://localhost:5000, production: via environment variable)
- **Backend**: Flask API (local: http://localhost:5000, production: configurable)
- **ML Service**: ML inference service (local: http://localhost:5001, production: configurable)

---

## Local Development Setup

### Quick Start (No Configuration Needed)

By default, all services work on localhost:

```bash
# Terminal 1: Frontend
cd frontend
npm install
npm start
# Opens on http://localhost:3000

# Terminal 2: Backend
cd backend
pip install -r requirements.txt
python app.py
# Runs on http://localhost:5000

# Terminal 3: ML Service
cd ml_service
pip install -r requirements.txt
python ml_api.py
# Runs on http://localhost:5001
```

The `.env` files in each directory contain default localhost values and will work immediately without modification.

### Optional: Custom Local Ports

If you want to run services on different ports:

**Backend** (`backend/.env`):
```
BACKEND_PORT=8000
ML_SERVICE_URL=http://localhost:5001
```

**ML Service** (`ml_service/.env`):
```
ML_SERVICE_PORT=5001
```

**Frontend** (`frontend/.env`):
```
REACT_APP_BACKEND_URL=http://localhost:8000
```

---

## Production Deployment

### Environment Variables to Set

#### Backend (Flask) - Deploy on Render, Railway, etc.

Set these environment variables on your hosting platform:

```
BACKEND_PORT=5000
ML_SERVICE_URL=https://your-ml-service-url.com
```

Example for Render:
- In your Render service settings, go to Environment
- Add: `ML_SERVICE_URL` = `https://your-ml-service.onrender.com`
- Add: `BACKEND_PORT` = `5000`

#### ML Service - Deploy on Render, Railway, etc.

Set this environment variable:

```
ML_SERVICE_PORT=5000
```

Note: Render/Railway assign a random port; this variable ensures the service uses the correct port.

#### Frontend - Deploy on Vercel, Netlify, etc.

Set these environment variables:

**Vercel Environment Variables:**
1. Go to Project Settings → Environment Variables
2. Add: `REACT_APP_BACKEND_URL` = `https://your-backend-api.com`

Example:
```
REACT_APP_BACKEND_URL=https://smart-resume-backend.onrender.com
```

### Deployment Steps

#### Backend (Flask)

1. **Create entry file** if deploying to Render/Railway (add `start.sh`):
   ```bash
   #!/bin/bash
   cd backend
   pip install -r requirements.txt
   python app.py
   ```

2. **Set Environment Variables** on your platform:
   - `ML_SERVICE_URL` = Your ML service URL
   - `BACKEND_PORT` = Port number (usually auto-assigned)

3. **Deploy** using your platform's deployment method (git push, CLI, etc.)

#### ML Service

1. **Set Environment Variable**:
   - `ML_SERVICE_PORT` = Port number

2. **Deploy** your Python Flask app normally

3. **Copy models**: Ensure `models/` directory with trained models is included

#### Frontend (React)

1. **Build the application**:
   ```bash
   npm run build
   ```

2. **Set Environment Variable** on Vercel/Netlify:
   - `REACT_APP_BACKEND_URL` = Your backend API URL

3. **Deploy** using your platform's deployment method

---

## Environment Variables Reference

### Backend (`backend/.env` or server environment)

| Variable | Default | Description |
|----------|---------|-------------|
| `BACKEND_PORT` | 5000 | Port for Flask backend |
| `ML_SERVICE_URL` | http://localhost:5001 | URL to ML service (full URL, not just port) |

### Frontend (`frontend/.env` or server environment)

| Variable | Default | Description |
|----------|---------|-------------|
| `REACT_APP_BACKEND_URL` | http://localhost:5000 | Backend API URL |

### ML Service (`ml_service/.env` or server environment)

| Variable | Default | Description |
|----------|---------|-------------|
| `ML_SERVICE_PORT` | 5001 | Port for ML service |

---

## Configuration Examples

### Example 1: Local Development (Default)

No configuration needed - just run each service and it works!

### Example 2: Backend Deployed on Render

**Render Backend Service:**
- Set `ML_SERVICE_URL` = `https://ml-service.onrender.com`

**Frontend (Vercel):**
- Set `REACT_APP_BACKEND_URL` = `https://api.onrender.com`

### Example 3: All Services Locally

Change `backend/.env`:
```
BACKEND_PORT=5000
ML_SERVICE_URL=http://localhost:5001
```

Change `frontend/.env`:
```
REACT_APP_BACKEND_URL=http://localhost:5000
```

### Example 4: Custom Docker Setup

**docker-compose.yml:**
```yaml
services:
  backend:
    environment:
      - BACKEND_PORT=5000
      - ML_SERVICE_URL=http://ml-service:5001
  
  ml-service:
    environment:
      - ML_SERVICE_PORT=5001
  
  frontend:
    environment:
      - REACT_APP_BACKEND_URL=http://localhost:5000
```

---

## Troubleshooting

### "Cannot connect to backend"

- **Check**: Has the backend been deployed and is it running?
- **Check**: Is `REACT_APP_BACKEND_URL` set correctly in frontend?
- **Solution**: Verify the backend URL: `curl https://your-backend.com/health`

### "Backend cannot reach ML service"

- **Check**: Has the ML service been deployed?
- **Check**: Is `ML_SERVICE_URL` set correctly in backend?
- **Solution**: Verify the ML service URL: `curl https://your-ml-service.com/health`

### "Frontend works locally but not in production"

- **Issue**: `REACT_APP_BACKEND_URL` not set on production platform
- **Solution**: Add environment variable to Vercel/Netlify project settings
- **Rebuild**: Redeploy frontend after adding environment variable

### "Changes to .env files not taking effect"

- **Local development**: Stop the service and restart it
- **Production**: Redeploy the application

---

## Important Notes

✅ **Backward Compatibility**: All changes are backward compatible. Existing local setups work without modification.

✅ **No Hardcoded URLs**: No production URLs are hardcoded in the code.

✅ **Fallback Defaults**: All services have sensible localhost defaults for development.

✅ **Environment Driven**: Production deployment is entirely environment-variable driven.

---

## .env Files in Version Control

### Do NOT commit to git:
- `backend/.env`
- `frontend/.env`
- `ml_service/.env`

### DO commit to git:
- `backend/.env.example`
- `frontend/.env.example`
- `ml_service/.env.example`
- `ENVIRONMENT_SETUP.md` (this file)

Update `.gitignore` to exclude:
```
.env
.env.local
.env.*.local
```

---

## Quick Reference Commands

### Local Development

```bash
# Backend
cd backend
pip install -r requirements.txt
python app.py

# ML Service
cd ml_service
pip install -r requirements.txt
python ml_api.py

# Frontend
cd frontend
npm install
npm start
```

### Verify Services

```bash
# Backend health check
curl http://localhost:5000/health

# ML Service health check
curl http://localhost:5001/health
```

### Production - Set Backend on Render

```
ML_SERVICE_URL=https://your-ml-service.onrender.com
BACKEND_PORT=5000
```

### Production - Set Frontend on Vercel

```
REACT_APP_BACKEND_URL=https://your-backend.onrender.com
```

---

Need help? Check the main [README.md](../README.md) or review the `.env.example` files in each directory.
