# 🚀 Deployment Guide for Render

## Prerequisites
1. GitHub repository with your code
2. Render account (free tier available)
3. Database (MySQL/PostgreSQL)

## Backend Deployment

### 1. Create Backend Service on Render
1. Go to [Render Dashboard](https://dashboard.render.com)
2. Click "New +" → "Web Service"
3. Connect your GitHub repository
4. Configure the service:
   - **Name**: `case-search-backend`
   - **Environment**: `Python 3`
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `uvicorn main:app --host 0.0.0.0 --port $PORT`

### 2. Environment Variables for Backend
Set these in Render dashboard:
```
DATABASE_URL=mysql+pymysql://user:password@host:port/database
SECRET_KEY=your-secret-key-here
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
CORS_ORIGINS=https://case-search-frontend.onrender.com
REACT_APP_GOOGLE_MAPS_API_KEY=your_google_maps_api_key
```

### 3. Database Setup
1. Create a MySQL database on Render or use external service
2. Update the `DATABASE_URL` environment variable
3. The app will automatically create tables on first run

## Frontend Deployment

### 1. Create Static Site on Render
1. Go to [Render Dashboard](https://dashboard.render.com)
2. Click "New +" → "Static Site"
3. Connect your GitHub repository
4. Configure the service:
   - **Name**: `case-search-frontend`
   - **Build Command**: `npm install && npm run build`
   - **Publish Directory**: `build`

### 2. Environment Variables for Frontend
Set these in Render dashboard:
```
REACT_APP_API_URL=https://case-search-backend.onrender.com
REACT_APP_GOOGLE_MAPS_API_KEY=your_google_maps_api_key
```

## Database Migration

### Option 1: Automatic (Recommended)
The backend will automatically create tables on first startup.

### Option 2: Manual
If you need to run migrations manually:
```bash
cd backend
python create_tables.py
```

## Post-Deployment

### 1. Update CORS Settings
Make sure your backend CORS origins include your frontend URL.

### 2. Test the Application
1. Visit your frontend URL
2. Test login functionality
3. Check admin dashboard
4. Verify API endpoints

### 3. Monitor Logs
Use Render's logging feature to monitor application health.

## Troubleshooting

### Common Issues:
1. **CORS Errors**: Check CORS_ORIGINS environment variable
2. **Database Connection**: Verify DATABASE_URL format
3. **Build Failures**: Check build logs for missing dependencies
4. **API Errors**: Verify REACT_APP_API_URL is correct

### Support:
- Check Render documentation: https://render.com/docs
- Review application logs in Render dashboard
- Ensure all environment variables are set correctly

## Cost Considerations
- Render free tier includes:
  - 750 hours/month for web services
  - 100GB bandwidth for static sites
  - Automatic SSL certificates
  - Custom domains support

## Security Notes
- Use strong SECRET_KEY for production
- Enable HTTPS only
- Regularly update dependencies
- Monitor for security vulnerabilities
