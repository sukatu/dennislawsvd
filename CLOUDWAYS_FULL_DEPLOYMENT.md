# 🚀 Complete Cloudways Deployment Guide - Frontend + Backend

## 📋 Overview

This guide will help you deploy both the React frontend and Python FastAPI backend to Cloudways. We'll use a hybrid approach where the frontend is served as static files and the backend runs as a Python application.

## 🏗️ Architecture

- **Frontend**: React app served as static files from `public_html`
- **Backend**: Python FastAPI app running on a subdomain or subdirectory
- **Database**: MySQL (provided by Cloudways)
- **Domain Structure**: 
  - `yourdomain.com` → Frontend
  - `api.yourdomain.com` → Backend API

## 🛠️ Prerequisites

1. Cloudways account with server access
2. Domain name (optional, can use Cloudways subdomain)
3. SSH access to your Cloudways server
4. Python 3.8+ support (check with Cloudways support)

## 📦 Step 1: Prepare Your Files

### Frontend Build
```bash
# In your project root
npm run build
```

### Backend Preparation
```bash
# Create deployment package
cd backend
tar -czf ../backend-deployment.tar.gz --exclude=venv --exclude=__pycache__ --exclude=*.pyc .
```

## 🌐 Step 2: Cloudways Server Setup

### 2.1 Create Applications

1. **Frontend Application**:
   - Application Type: **PHP** (for static file serving)
   - Document Root: `public_html`
   - Domain: `yourdomain.com`

2. **Backend Application**:
   - Application Type: **Python** (if available) or **PHP** with custom setup
   - Document Root: `api` or `backend`
   - Domain: `api.yourdomain.com` or `yourdomain.com/api`

### 2.2 Database Setup
1. Go to "Application Management" → "Database"
2. Create a new MySQL database
3. Note down the database credentials
4. Import your database schema if needed

## 📁 Step 3: Deploy Frontend

### 3.1 Upload Frontend Files
```bash
# Upload all contents from build/ folder to public_html/
rsync -avz build/ user@your-server-ip:/home/master/applications/your-app/public_html/
```

Or use Cloudways File Manager:
1. Go to "Application Management" → "File Manager"
2. Navigate to `public_html`
3. Upload all files from `build/` folder

### 3.2 Configure Frontend
Create/update `.htaccess` in `public_html`:
```apache
RewriteEngine On

# Handle client-side routing
RewriteCond %{REQUEST_FILENAME} !-f
RewriteCond %{REQUEST_FILENAME} !-d
RewriteRule . /index.html [L]

# Enable Gzip compression
<IfModule mod_deflate.c>
    AddOutputFilterByType DEFLATE text/plain
    AddOutputFilterByType DEFLATE text/html
    AddOutputFilterByType DEFLATE text/xml
    AddOutputFilterByType DEFLATE text/css
    AddOutputFilterByType DEFLATE application/xml
    AddOutputFilterByType DEFLATE application/xhtml+xml
    AddOutputFilterByType DEFLATE application/rss+xml
    AddOutputFilterByType DEFLATE application/javascript
    AddOutputFilterByType DEFLATE application/x-javascript
</IfModule>

# Cache static assets
<IfModule mod_expires.c>
    ExpiresActive on
    ExpiresByType text/css "access plus 1 year"
    ExpiresByType application/javascript "access plus 1 year"
    ExpiresByType image/png "access plus 1 year"
    ExpiresByType image/jpg "access plus 1 year"
    ExpiresByType image/jpeg "access plus 1 year"
    ExpiresByType image/gif "access plus 1 year"
    ExpiresByType image/svg+xml "access plus 1 year"
</IfModule>
```

## 🐍 Step 4: Deploy Backend

### 4.1 Upload Backend Files
```bash
# Upload backend files to a subdirectory
rsync -avz backend/ user@your-server-ip:/home/master/applications/your-app/backend/
```

### 4.2 Install Python Dependencies
SSH into your Cloudways server:
```bash
# Navigate to backend directory
cd /home/master/applications/your-app/backend

# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### 4.3 Configure Backend
Create `config.py` in backend directory:
```python
import os

class Settings:
    # Database configuration
    database_url = "mysql+pymysql://username:password@localhost:3306/database_name"
    
    # API configuration
    api_host = "0.0.0.0"
    api_port = 8000
    
    # CORS settings
    allowed_origins = [
        "https://yourdomain.com",
        "https://www.yourdomain.com",
        "http://localhost:3000"  # For development
    ]

settings = Settings()
```

### 4.4 Create WSGI Configuration
Create `wsgi.py` in backend directory:
```python
import sys
import os

# Add the backend directory to Python path
sys.path.insert(0, '/home/master/applications/your-app/backend')

from main import app

if __name__ == "__main__":
    app.run()
```

### 4.5 Create .htaccess for Backend
Create `.htaccess` in backend directory:
```apache
RewriteEngine On

# Proxy requests to FastAPI
RewriteCond %{REQUEST_FILENAME} !-f
RewriteCond %{REQUEST_FILENAME} !-d
RewriteRule ^(.*)$ http://localhost:8000/$1 [P,L]

# Set headers
Header always set Access-Control-Allow-Origin "*"
Header always set Access-Control-Allow-Methods "GET, POST, PUT, DELETE, OPTIONS"
Header always set Access-Control-Allow-Headers "Content-Type, Authorization"
```

## 🔧 Step 5: Configure Apache/Nginx

### 5.1 Apache Configuration
Add to your Apache virtual host configuration:
```apache
# Backend API
<Location /api>
    ProxyPass http://localhost:8000/
    ProxyPassReverse http://localhost:8000/
    ProxyPreserveHost On
</Location>

# Frontend
DocumentRoot /home/master/applications/your-app/public_html
```

### 5.2 Nginx Configuration (if using Nginx)
```nginx
# Frontend
location / {
    root /home/master/applications/your-app/public_html;
    try_files $uri $uri/ /index.html;
}

# Backend API
location /api/ {
    proxy_pass http://localhost:8000/;
    proxy_set_header Host $host;
    proxy_set_header X-Real-IP $remote_addr;
    proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
    proxy_set_header X-Forwarded-Proto $scheme;
}
```

## 🚀 Step 6: Start Services

### 6.1 Start Backend Service
```bash
# SSH into server
cd /home/master/applications/your-app/backend
source venv/bin/activate

# Start FastAPI with Gunicorn
gunicorn -w 4 -k uvicorn.workers.UvicornWorker -b 0.0.0.0:8000 main:app
```

### 6.2 Create Systemd Service (Optional)
Create `/etc/systemd/system/dennislaw-api.service`:
```ini
[Unit]
Description=DennisLaw SVD API
After=network.target

[Service]
Type=simple
User=master
WorkingDirectory=/home/master/applications/your-app/backend
Environment=PATH=/home/master/applications/your-app/backend/venv/bin
ExecStart=/home/master/applications/your-app/backend/venv/bin/gunicorn -w 4 -k uvicorn.workers.UvicornWorker -b 0.0.0.0:8000 main:app
Restart=always

[Install]
WantedBy=multi-user.target
```

Enable and start the service:
```bash
sudo systemctl enable dennislaw-api
sudo systemctl start dennislaw-api
sudo systemctl status dennislaw-api
```

## 🔐 Step 7: SSL Configuration

### 7.1 Enable SSL for Frontend
1. Go to "Application Management" → "SSL Certificate"
2. Enable "Let's Encrypt" for your main domain
3. Or upload your own SSL certificate

### 7.2 Enable SSL for Backend
1. Enable SSL for your API subdomain
2. Update CORS settings in backend to use HTTPS

## 🌍 Step 8: Environment Configuration

### 8.1 Update Frontend API URLs
Update your frontend to use the production API URL:
```javascript
// In your React app, update API base URL
const API_BASE_URL = 'https://api.yourdomain.com';
// or
const API_BASE_URL = 'https://yourdomain.com/api';
```

### 8.2 Database Migration
If you need to set up the database:
```bash
# SSH into server
cd /home/master/applications/your-app/backend
source venv/bin/activate

# Run database setup scripts
python create_company_analytics_tables.py
python generate_all_company_analytics.py
```

## 🔍 Step 9: Testing

### 9.1 Test Frontend
- Visit `https://yourdomain.com`
- Test all navigation and functionality
- Verify API calls are working

### 9.2 Test Backend
- Visit `https://api.yourdomain.com/docs` (FastAPI docs)
- Test API endpoints
- Check database connectivity

### 9.3 Test Integration
- Verify frontend can communicate with backend
- Test all CRUD operations
- Check error handling

## 📊 Step 10: Monitoring & Maintenance

### 10.1 Log Monitoring
```bash
# Check application logs
tail -f /home/master/applications/your-app/backend/logs/app.log

# Check systemd service logs
sudo journalctl -u dennislaw-api -f
```

### 10.2 Performance Monitoring
- Monitor server resources in Cloudways dashboard
- Set up alerts for high CPU/memory usage
- Monitor database performance

### 10.3 Backup Strategy
- Regular database backups
- Code repository backups
- Configuration file backups

## 🚨 Troubleshooting

### Common Issues:

1. **Backend Not Starting**
   - Check Python version compatibility
   - Verify all dependencies are installed
   - Check port availability

2. **Database Connection Issues**
   - Verify database credentials
   - Check network connectivity
   - Ensure database is running

3. **CORS Issues**
   - Update CORS settings in backend
   - Check allowed origins
   - Verify HTTPS configuration

4. **Static File Issues**
   - Check file permissions
   - Verify .htaccess configuration
   - Clear browser cache

## 📈 Performance Optimization

### Frontend Optimization:
- Enable Cloudways CDN
- Optimize images
- Enable Gzip compression
- Use browser caching

### Backend Optimization:
- Use Gunicorn with multiple workers
- Enable database connection pooling
- Implement caching (Redis)
- Monitor and optimize queries

## 🔄 Updates and Maintenance

### Frontend Updates:
```bash
# Build new version
npm run build

# Upload to server
rsync -avz build/ user@your-server-ip:/home/master/applications/your-app/public_html/
```

### Backend Updates:
```bash
# Upload new code
rsync -avz backend/ user@your-server-ip:/home/master/applications/your-app/backend/

# Restart service
sudo systemctl restart dennislaw-api
```

## 📞 Support

If you encounter issues:
1. Check Cloudways documentation
2. Review server logs
3. Contact Cloudways support
4. Check this deployment guide

---

**🎉 Your DennisLaw SVD application (Frontend + Backend) should now be live on Cloudways!**

## 📋 Deployment Checklist

- [ ] Frontend files uploaded to `public_html`
- [ ] Backend files uploaded to `backend` directory
- [ ] Python dependencies installed
- [ ] Database configured and connected
- [ ] Backend service running
- [ ] SSL certificates configured
- [ ] CORS settings updated
- [ ] API endpoints tested
- [ ] Frontend-backend integration tested
- [ ] Monitoring set up
- [ ] Backup strategy implemented
