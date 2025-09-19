# Juridence Deployment Guide for Render

## Backend Deployment

### 1. Create Web Service on Render
- Go to [Render Dashboard](https://dashboard.render.com)
- Click "New +" → "Web Service"
- Choose "Build and deploy from a Git repository" (NOT Docker)
- Connect your GitHub repository
- Choose the `backend` folder as root directory

### 2. Backend Configuration
```
Name: juridence-backend
Environment: Python 3
Branch: main (or your default branch)
Root Directory: backend
Build Command: pip install -r requirements.txt
Start Command: uvicorn main:app --host 0.0.0.0 --port $PORT
```

**IMPORTANT**: Make sure to select "Python" environment, NOT "Docker"!

### 3. Backend Environment Variables
Add these in Render dashboard → Environment tab:
```
DATABASE_URL=postgresql://username:password@hostname:port/database
SECRET_KEY=your-production-secret-key-here
ACCESS_TOKEN_EXPIRE_MINUTES=30
CORS_ORIGINS=["https://your-frontend-app.onrender.com"]
ENVIRONMENT=production
```

### 4. Database Setup
- In Render dashboard, create a PostgreSQL database
- Copy the DATABASE_URL to your backend environment variables

## Frontend Deployment

### 1. Create Static Site on Render
- Go to [Render Dashboard](https://dashboard.render.com)
- Click "New +" → "Static Site"
- Choose "Build and deploy from a Git repository" (NOT Docker)
- Connect your GitHub repository
- Choose root directory (not backend folder)

### 2. Frontend Configuration
```
Name: juridence-frontend
Branch: main (or your default branch)
Root Directory: / (root)
Build Command: npm install && npm run build
Publish Directory: build
```

**IMPORTANT**: Make sure to select "Static Site" environment, NOT "Docker"!

### 3. Frontend Environment Variables
Add these in Render dashboard → Environment tab:
```
REACT_APP_API_URL=https://your-backend-app.onrender.com
```

## Deployment Steps

1. **Push your code to GitHub**
2. **Deploy backend first** (it will create the database and admin user)
3. **Deploy frontend** (it will build and connect to backend)
4. **Update CORS_ORIGINS** in backend with your frontend URL
5. **Test the application**

## URLs
- Frontend: `https://juridence-frontend.onrender.com`
- Backend: `https://juridence-backend.onrender.com`
- API Docs: `https://juridence-backend.onrender.com/docs`

## Admin Access
- Email: `admin@juridence.com`
- Password: `admin123`

## Troubleshooting
- Check Render logs for any errors
- Ensure DATABASE_URL is correct
- Verify CORS_ORIGINS includes your frontend URL
- Check that all environment variables are set
