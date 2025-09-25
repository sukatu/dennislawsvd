# Deployment Guide

## Issues Found and Solutions

### 1. Frontend and Backend Connection Issues
- **Problem**: Frontend was serving old JavaScript bundle without our authentication fixes
- **Solution**: Built new frontend with dynamic authentication handling

### 2. Admin User Credentials
- **Problem**: Server admin user exists but with unknown password
- **Solution**: Create new admin user with known credentials

## Manual Deployment Steps

### Step 1: Upload Frontend Build
```bash
# From your local machine, upload the build folder to the server
scp -r build/* root@62.171.137.28:/var/www/html/
```

### Step 2: Create Admin User on Server
```bash
# SSH into the server
ssh root@62.171.137.28

# Navigate to the backend directory
cd /var/www/juridence

# Activate virtual environment
source venv/bin/activate

# Upload and run the admin user creation script
# (Upload create_admin_user.py to the server first)
python create_admin_user.py
```

### Step 3: Restart Backend Service
```bash
# Restart the backend service
pm2 restart juridence-backend

# Check if it's running
pm2 status
```

### Step 4: Test the Application
1. **Frontend**: Visit http://62.171.137.28
2. **Backend Health**: Visit http://62.171.137.28:8000/api/health
3. **Admin Login**: Use username `admin` and password `admin123`

## Expected Results

### Frontend Changes
- ✅ Dynamic authentication (detects server vs local environment)
- ✅ Uses `/api/auth/login` for server, `/auth/login` for local
- ✅ Uses `username` field for server, `email` field for local
- ✅ "Login as Admin" button works with correct credentials

### Admin User
- ✅ Username: `admin`
- ✅ Password: `admin123`
- ✅ Email: `admin@juridence.com`
- ✅ Admin privileges enabled

## Troubleshooting

### If Frontend Still Shows Old Version
1. Clear browser cache (Ctrl+F5 or Cmd+Shift+R)
2. Check if build files were uploaded correctly:
   ```bash
   ls -la /var/www/html/static/js/
   ```

### If Admin Login Still Fails
1. Check if admin user was created:
   ```bash
   cd /var/www/juridence
   source venv/bin/activate
   python -c "
   from backend.database import get_db
   from backend.models.user import User
   db = next(get_db())
   admin = db.query(User).filter(User.username == 'admin').first()
   print(f'Admin user exists: {admin is not None}')
   if admin:
       print(f'Username: {admin.username}, Email: {admin.email}, Is Admin: {admin.is_admin}')
   "
   ```

### If Backend is Not Running
```bash
pm2 status
pm2 logs juridence-backend
pm2 restart juridence-backend
```

## API Endpoints
- **Health Check**: `GET http://62.171.137.28:8000/api/health`
- **Admin Login**: `POST http://62.171.137.28:8000/api/auth/login`
  ```json
  {
    "username": "admin",
    "password": "admin123"
  }
  ```

## Next Steps
After successful deployment:
1. Test the admin login functionality
2. Verify all admin features work correctly
3. Test case hearing management features
4. Ensure all CRUD operations work properly
