# Render Deployment Checklist

## Pre-Deployment Checklist

### 1. Database Setup
- [ ] Create PostgreSQL database on Render
- [ ] Copy the DATABASE_URL from PostgreSQL service
- [ ] Note the database credentials

### 2. Backend Service Setup
- [ ] Create Web Service (Python 3, NOT Docker)
- [ ] Set Root Directory to `backend`
- [ ] Set Build Command: `pip install -r requirements.txt`
- [ ] Set Start Command: `python start_render.py`

### 3. Environment Variables (Backend)
- [ ] `DATABASE_URL_ENV` = PostgreSQL connection string from Render
- [ ] `SECRET_KEY` = Strong random secret key
- [ ] `CORS_ORIGINS` = Your frontend URL (will be set after frontend deployment)
- [ ] `ENVIRONMENT` = production

### 4. Frontend Service Setup
- [ ] Create Static Site (NOT Docker)
- [ ] Set Root Directory to `/` (root)
- [ ] Set Build Command: `npm install && npm run build`
- [ ] Set Publish Directory: `build`

### 5. Environment Variables (Frontend)
- [ ] `REACT_APP_API_URL` = Your backend URL (https://your-backend.onrender.com)

## Deployment Steps

### Step 1: Deploy Backend
1. Push code to GitHub
2. Deploy backend service
3. Check logs for successful startup
4. Test API endpoint: `https://your-backend.onrender.com/docs`

### Step 2: Deploy Frontend
1. Deploy frontend service
2. Get frontend URL
3. Update backend CORS_ORIGINS with frontend URL
4. Restart backend service

### Step 3: Test Application
1. Visit frontend URL
2. Test login functionality
3. Verify all features work

## Troubleshooting

### Database Connection Issues
If you see "connection to server at localhost failed":
1. Go to Render backend service → Environment
2. Add/update: `DATABASE_URL_ENV=postgresql://username:password@hostname:port/database`
3. Use the exact DATABASE_URL from your PostgreSQL service
4. Restart the service

### Build Errors
- Try using `requirements-minimal.txt` if metadata generation fails
- Check that all dependencies are compatible

### CORS Issues
- Make sure CORS_ORIGINS includes your frontend URL
- Restart backend after updating CORS settings

## URLs After Deployment
- Frontend: `https://your-frontend.onrender.com`
- Backend: `https://your-backend.onrender.com`
- API Docs: `https://your-backend.onrender.com/docs`

## Admin Access
- Email: `admin@juridence.com`
- Password: `admin123`
