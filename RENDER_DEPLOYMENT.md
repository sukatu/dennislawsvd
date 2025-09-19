# Juridence Deployment Guide for Render

## Backend Deployment

### 1. Create Web Service on Render
- Go to [Render Dashboard](https://dashboard.render.com)
- Click "New +" → "Web Service"
- Choose "Build and deploy from a Git repository" (NOT Docker)
- Connect your GitHub repository
- Set the `backend` folder as root directory

### 2. Backend Configuration
```
Name: juridence-backend
Environment: Python 3
Branch: main (or your default branch)
Root Directory: backend
Build Command: pip install -r requirements.txt
Start Command: uvicorn main:app --host 0.0.0.0 --port $PORT
```

**Note**: Since frontend and backend are in the same repo, the Root Directory should be `backend` for the backend service.

**IMPORTANT**: Make sure to select "Python" environment, NOT "Docker"!

### 3. Backend Environment Variables
Add these in Render dashboard → Environment tab:
```
DATABASE_URL_ENV=mysql+pymysql://username:password@hostname:port/database
SECRET_KEY=your-production-secret-key-here
ACCESS_TOKEN_EXPIRE_MINUTES=30
CORS_ORIGINS=["https://your-frontend-app.onrender.com"]
ENVIRONMENT=production
```

### 4. Database Setup
- In Render dashboard, create a MySQL database
- Copy the DATABASE_URL to your backend environment variables as `DATABASE_URL_ENV`
- Make sure the URL starts with `mysql+pymysql://` instead of `mysql://`

## Frontend Deployment

### 1. Create Static Site on Render
- Go to [Render Dashboard](https://dashboard.render.com)
- Click "New +" → "Static Site"
- Choose "Build and deploy from a Git repository" (NOT Docker)
- Connect your GitHub repository
- Set root directory to `/` (the main project folder)

### 2. Frontend Configuration
```
Name: juridence-frontend
Branch: main (or your default branch)
Root Directory: / (root - main project folder)
Build Command: npm install && npm run build
Publish Directory: build
```

**Note**: Since frontend and backend are in the same repo, the Root Directory should be `/` (root) for the frontend service, so it can access package.json and src/ folder.

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

### Build Errors
- **Metadata generation failed**: Try using the minimal requirements.txt
- **Rust/Cargo errors**: Make sure you're not using packages that require Rust compilation
- **Package conflicts**: Use version ranges (>=) instead of exact versions

### Database Connection Issues
- Check Render logs for any errors
- Ensure DATABASE_URL_ENV is correct and starts with `mysql+pymysql://`
- Verify CORS_ORIGINS includes your frontend URL
- Check that all environment variables are set

### Alternative Requirements File
If you get metadata generation errors, try using `requirements-minimal.txt` instead:
- Change Build Command to: `pip install -r requirements-minimal.txt`
