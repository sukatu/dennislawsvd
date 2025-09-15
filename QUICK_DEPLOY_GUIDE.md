# 🚀 Quick Deploy Guide - Cloudways

## 📋 Prerequisites

1. **Cloudways Account** with server access
2. **Domain name** (or use Cloudways subdomain)
3. **SSH access** to your Cloudways server
4. **Database credentials** from Cloudways dashboard

## ⚡ Quick Start (5 Steps)

### Step 1: Configure Deployment Script
Edit `deploy-to-cloudways.sh` and update these values:
```bash
SERVER_IP="your-server-ip"
SERVER_USER="master"  # Usually 'master' on Cloudways
APP_NAME="your-app-name"
DOMAIN="yourdomain.com"
```

### Step 2: Get Database Credentials
1. Go to Cloudways Dashboard
2. Select your application
3. Go to "Application Management" → "Database"
4. Note down:
   - Database name
   - Username
   - Password
   - Host (usually localhost)

### Step 3: Update Backend Configuration
Edit `backend/cloudways_config.py`:
```python
DATABASE_NAME = "your_database_name"
DATABASE_USER = "your_database_user" 
DATABASE_PASSWORD = "your_database_password"
ALLOWED_ORIGINS = ["https://yourdomain.com"]
```

### Step 4: Deploy Everything
```bash
# Make script executable
chmod +x deploy-to-cloudways.sh

# Deploy both frontend and backend
./deploy-to-cloudways.sh
```

### Step 5: Configure Domain & SSL
1. **Domain Setup**:
   - Point your domain to Cloudways server IP
   - Add domain in Cloudways dashboard

2. **SSL Certificate**:
   - Go to "Application Management" → "SSL Certificate"
   - Enable "Let's Encrypt" (free)

## 🔧 Manual Deployment (Alternative)

### Frontend Only:
```bash
# Build frontend
npm run build

# Upload to Cloudways
rsync -avz build/ user@server-ip:/home/master/applications/your-app/public_html/
```

### Backend Only:
```bash
# Upload backend
rsync -avz backend/ user@server-ip:/home/master/applications/your-app/backend/

# SSH into server and setup
ssh user@server-ip
cd /home/master/applications/your-app/backend
python3 -m venv venv
source venv/bin/activate
pip install -r requirements-cloudways.txt
```

## 🌐 URL Structure

After deployment, your app will be available at:
- **Frontend**: `https://yourdomain.com`
- **Backend API**: `https://api.yourdomain.com` or `https://yourdomain.com/api`
- **API Docs**: `https://api.yourdomain.com/docs`

## 🔍 Testing Deployment

### Test Frontend:
```bash
curl https://yourdomain.com
# Should return HTML content
```

### Test Backend:
```bash
curl https://api.yourdomain.com/docs
# Should return API documentation
```

### Test Database:
```bash
curl https://api.yourdomain.com/api/companies/search?page=1&limit=1
# Should return companies data
```

## 🚨 Troubleshooting

### Common Issues:

1. **Backend not starting**:
   ```bash
   # Check service status
   sudo systemctl status dennislaw-api
   
   # Check logs
   sudo journalctl -u dennislaw-api -f
   ```

2. **Database connection error**:
   - Verify database credentials in `cloudways_config.py`
   - Check if database is running in Cloudways dashboard

3. **CORS errors**:
   - Update `ALLOWED_ORIGINS` in `cloudways_config.py`
   - Restart backend service

4. **Frontend not loading**:
   - Check if `.htaccess` file is uploaded
   - Verify file permissions (644 for files, 755 for directories)

## 📊 Monitoring

### Check Backend Status:
```bash
# Service status
sudo systemctl status dennislaw-api

# Real-time logs
sudo journalctl -u dennislaw-api -f

# Restart service
sudo systemctl restart dennislaw-api
```

### Check Server Resources:
- Go to Cloudways Dashboard
- Monitor CPU, Memory, and Disk usage
- Set up alerts for high usage

## 🔄 Updates

### Update Frontend:
```bash
npm run build
rsync -avz build/ user@server-ip:/home/master/applications/your-app/public_html/
```

### Update Backend:
```bash
rsync -avz backend/ user@server-ip:/home/master/applications/your-app/backend/
ssh user@server-ip "sudo systemctl restart dennislaw-api"
```

## 📞 Support

If you need help:
1. Check the detailed guide: `CLOUDWAYS_FULL_DEPLOYMENT.md`
2. Review server logs
3. Contact Cloudways support
4. Check this quick guide

---

**🎉 Your DennisLaw SVD app should now be live on Cloudways!**

## 📋 Quick Checklist

- [ ] Script configured with server details
- [ ] Database credentials updated
- [ ] Domain pointed to server
- [ ] SSL certificate enabled
- [ ] Frontend accessible
- [ ] Backend API responding
- [ ] Database connected
- [ ] All features working
