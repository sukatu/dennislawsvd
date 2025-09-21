# DigitalOcean Deployment Guide for Juridence

## 🚀 **Complete Deployment Guide for DigitalOcean**

This guide will help you deploy your Juridence application on DigitalOcean using Droplets and managed PostgreSQL database.

---

## 📋 **Prerequisites**

- DigitalOcean account
- Domain name (optional but recommended)
- SSH access to your local machine
- Git repository access

---

## 🗄️ **Step 1: Create DigitalOcean PostgreSQL Database**

### **1.1 Create Database Cluster**
1. Log into DigitalOcean Control Panel
2. Navigate to **Databases** → **Create Database Cluster**
3. Choose **PostgreSQL** as the database engine
4. Select **Basic** plan (or higher based on your needs)
5. Choose your preferred region (closer to your users)
6. Set cluster name: `juridence-db`
7. Create the cluster

### **1.2 Configure Database**
1. Once created, go to your database cluster
2. Click **Settings** → **Connection Details**
3. Note down the following details:
   ```
   Host: db-postgresql-[region]-[cluster-id]-do-user-[user-id]-0.h.db.ondigitalocean.com
   Port: 25060
   Database: defaultdb
   Username: doadmin
   Password: [auto-generated password]
   SSL Mode: require
   ```

### **1.3 Create Application Database**
1. Go to **Users & Databases** tab
2. Click **Add Database**
3. Database name: `juridence`
4. Click **Add Database**

---

## 🖥️ **Step 2: Create DigitalOcean Droplet**

### **2.1 Create Droplet**
1. Navigate to **Droplets** → **Create Droplet**
2. Choose **Ubuntu 22.04 (LTS)** as the image
3. Select **Basic** plan with at least:
   - **2 GB RAM** (recommended: 4 GB)
   - **50 GB SSD** (recommended: 100 GB)
   - **1 vCPU** (recommended: 2 vCPU)
4. Choose your preferred datacenter region
5. Add SSH key or use password authentication
6. Set hostname: `juridence-app`
7. Create the droplet

### **2.2 Connect to Droplet**
```bash
ssh root@YOUR_DROPLET_IP
```

---

## ⚙️ **Step 3: Server Setup**

### **3.1 Update System**
```bash
apt update && apt upgrade -y
```

### **3.2 Install Required Software**
```bash
# Install Python 3.11 and pip
apt install -y python3.11 python3.11-venv python3.11-dev python3-pip

# Install Node.js 18.x
curl -fsSL https://deb.nodesource.com/setup_18.x | sudo -E bash -
apt install -y nodejs

# Install Nginx
apt install -y nginx

# Install Git
apt install -y git

# Install PostgreSQL client
apt install -y postgresql-client

# Install system dependencies
apt install -y build-essential libssl-dev libffi-dev python3-dev
```

### **3.3 Create Application User**
```bash
# Create user for the application
useradd -m -s /bin/bash juridence
usermod -aG sudo juridence

# Switch to juridence user
su - juridence
```

---

## 📦 **Step 4: Deploy Application**

### **4.1 Clone Repository**
```bash
# Clone your repository
git clone https://github.com/yourusername/juridence.git
cd juridence

# Or upload your project files using SCP
# scp -r /path/to/your/project juridence@YOUR_DROPLET_IP:/home/juridence/
```

### **4.2 Setup Backend**

#### **4.2.1 Create Virtual Environment**
```bash
cd backend
python3.11 -m venv venv
source venv/bin/activate
```

#### **4.2.2 Install Dependencies**
```bash
# Install Python dependencies
pip install --upgrade pip
pip install -r requirements.txt

# If you encounter issues, try minimal requirements first
pip install -r requirements-minimal.txt
```

#### **4.2.3 Configure Environment**
```bash
# Create environment file
nano .env
```

Add the following content to `.env`:
```env
# Database Configuration
DATABASE_URL_ENV=postgresql://doadmin:YOUR_PASSWORD@YOUR_DB_HOST:25060/juridence?sslmode=require

# Application Configuration
SECRET_KEY=your-super-secret-key-here-make-it-long-and-random
DEBUG=False
CORS_ORIGINS=["https://yourdomain.com", "https://www.yourdomain.com"]

# JWT Configuration
JWT_SECRET_KEY=your-jwt-secret-key-here
JWT_ALGORITHM=HS256
JWT_ACCESS_TOKEN_EXPIRE_MINUTES=30

# Email Configuration (Optional)
SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
SMTP_USERNAME=your-email@gmail.com
SMTP_PASSWORD=your-app-password
FROM_EMAIL=noreply@yourdomain.com

# OpenAI Configuration (Optional)
OPENAI_API_KEY=your-openai-api-key

# Google OAuth (Optional)
GOOGLE_CLIENT_ID=your-google-client-id
GOOGLE_CLIENT_SECRET=your-google-client-secret
```

#### **4.2.4 Test Database Connection**
```bash
# Test connection to DigitalOcean PostgreSQL
python test_digitalocean_connection.py
```

### **4.3 Setup Frontend**

#### **4.3.1 Install Dependencies**
```bash
cd ..
npm install
```

#### **4.3.2 Build Frontend**
```bash
npm run build
```

---

## 🔧 **Step 5: Configure Services**

### **5.1 Create Systemd Service for Backend**

```bash
# Switch back to root user
exit

# Create service file
nano /etc/systemd/system/juridence-backend.service
```

Add the following content:
```ini
[Unit]
Description=Juridence Backend Service
After=network.target

[Service]
Type=exec
User=juridence
Group=juridence
WorkingDirectory=/home/juridence/juridence/backend
Environment=PATH=/home/juridence/juridence/backend/venv/bin
ExecStart=/home/juridence/juridence/backend/venv/bin/uvicorn main:app --host 0.0.0.0 --port 8000
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
```

### **5.2 Enable and Start Services**
```bash
# Reload systemd
systemctl daemon-reload

# Enable services
systemctl enable juridence-backend

# Start services
systemctl start juridence-backend

# Check status
systemctl status juridence-backend
```

### **5.3 Configure Nginx**

#### **5.3.1 Create Nginx Configuration**
```bash
nano /etc/nginx/sites-available/juridence
```

Add the following content:
```nginx
server {
    listen 80;
    server_name yourdomain.com www.yourdomain.com;

    # Frontend
    location / {
        root /home/juridence/juridence/build;
        index index.html index.htm;
        try_files $uri $uri/ /index.html;
        
        # Security headers
        add_header X-Frame-Options "SAMEORIGIN" always;
        add_header X-XSS-Protection "1; mode=block" always;
        add_header X-Content-Type-Options "nosniff" always;
        add_header Referrer-Policy "no-referrer-when-downgrade" always;
        add_header Content-Security-Policy "default-src 'self' http: https: data: blob: 'unsafe-inline'" always;
    }

    # Backend API
    location /api/ {
        proxy_pass http://127.0.0.1:8000;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection 'upgrade';
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        proxy_cache_bypass $http_upgrade;
    }

    # Static files
    location /static/ {
        alias /home/juridence/juridence/backend/uploads/;
        expires 1y;
        add_header Cache-Control "public, immutable";
    }

    # File upload size limit
    client_max_body_size 100M;
}
```

#### **5.3.2 Enable Site and Restart Nginx**
```bash
# Enable the site
ln -s /etc/nginx/sites-available/juridence /etc/nginx/sites-enabled/

# Remove default site
rm /etc/nginx/sites-enabled/default

# Test configuration
nginx -t

# Restart Nginx
systemctl restart nginx
```

---

## 🔒 **Step 6: SSL Certificate (Optional but Recommended)**

### **6.1 Install Certbot**
```bash
apt install -y certbot python3-certbot-nginx
```

### **6.2 Obtain SSL Certificate**
```bash
# Replace with your actual domain
certbot --nginx -d yourdomain.com -d www.yourdomain.com
```

### **6.3 Auto-renewal**
```bash
# Test auto-renewal
certbot renew --dry-run

# The certificate will auto-renew via cron job
```

---

## 🗄️ **Step 7: Database Migration**

### **7.1 Migrate Data (if needed)**
```bash
# Switch to juridence user
su - juridence
cd juridence/backend

# Activate virtual environment
source venv/bin/activate

# Run migration script
python migrate_to_digitalocean_fixed.py
```

### **7.2 Verify Database**
```bash
# Test database connection
python test_digitalocean_connection.py

# Check if tables are created
python -c "
from config import settings
from database import engine
from sqlalchemy import text

with engine.connect() as conn:
    result = conn.execute(text('SELECT table_name FROM information_schema.tables WHERE table_schema = \\'public\\''))
    tables = [row[0] for row in result.fetchall()]
    print(f'Found {len(tables)} tables: {tables[:10]}...')
"
```

---

## 🚀 **Step 8: Deploy and Test**

### **8.1 Final Deployment Steps**
```bash
# Switch to root user
exit

# Restart all services
systemctl restart juridence-backend
systemctl restart nginx

# Check service status
systemctl status juridence-backend
systemctl status nginx
```

### **8.2 Test Application**
1. **Backend API**: `http://YOUR_DROPLET_IP/api/health`
2. **Frontend**: `http://YOUR_DROPLET_IP`
3. **Database**: Check logs for any connection issues

### **8.3 Monitor Logs**
```bash
# Backend logs
journalctl -u juridence-backend -f

# Nginx logs
tail -f /var/log/nginx/access.log
tail -f /var/log/nginx/error.log
```

---

## 🔧 **Step 9: Production Optimizations**

### **9.1 Firewall Configuration**
```bash
# Enable UFW firewall
ufw enable

# Allow SSH, HTTP, and HTTPS
ufw allow 22/tcp
ufw allow 80/tcp
ufw allow 443/tcp

# Check status
ufw status
```

### **9.2 Performance Tuning**

#### **9.2.1 Nginx Optimization**
```bash
nano /etc/nginx/nginx.conf
```

Add these optimizations:
```nginx
worker_processes auto;
worker_connections 1024;

gzip on;
gzip_vary on;
gzip_min_length 1024;
gzip_types text/plain text/css application/json application/javascript text/xml application/xml application/xml+rss text/javascript;
```

#### **9.2.2 PostgreSQL Connection Pooling**
Consider using PgBouncer for connection pooling if you have high traffic.

### **9.3 Backup Strategy**
```bash
# Create backup script
nano /home/juridence/backup.sh
```

```bash
#!/bin/bash
DATE=$(date +%Y%m%d_%H%M%S)
BACKUP_DIR="/home/juridence/backups"
DB_HOST="YOUR_DB_HOST"
DB_NAME="juridence"

mkdir -p $BACKUP_DIR

# Database backup
pg_dump "postgresql://doadmin:YOUR_PASSWORD@$DB_HOST:25060/$DB_NAME?sslmode=require" > $BACKUP_DIR/db_backup_$DATE.sql

# Application backup
tar -czf $BACKUP_DIR/app_backup_$DATE.tar.gz /home/juridence/juridence

# Keep only last 7 days of backups
find $BACKUP_DIR -name "*.sql" -mtime +7 -delete
find $BACKUP_DIR -name "*.tar.gz" -mtime +7 -delete
```

```bash
chmod +x /home/juridence/backup.sh

# Add to crontab for daily backups
crontab -e
# Add: 0 2 * * * /home/juridence/backup.sh
```

---

## 🐛 **Troubleshooting**

### **Common Issues and Solutions**

#### **1. Backend Service Won't Start**
```bash
# Check logs
journalctl -u juridence-backend -n 50

# Common fixes:
# - Check .env file exists and has correct values
# - Verify database connection
# - Check if port 8000 is available
```

#### **2. Database Connection Issues**
```bash
# Test connection manually
psql "postgresql://doadmin:YOUR_PASSWORD@YOUR_DB_HOST:25060/juridence?sslmode=require"

# Check firewall rules in DigitalOcean
# Ensure database allows connections from your droplet
```

#### **3. Frontend Not Loading**
```bash
# Check if build files exist
ls -la /home/juridence/juridence/build/

# Rebuild if necessary
cd /home/juridence/juridence
npm run build

# Check Nginx configuration
nginx -t
```

#### **4. SSL Certificate Issues**
```bash
# Check certificate status
certbot certificates

# Renew if needed
certbot renew
```

---

## 📊 **Monitoring and Maintenance**

### **System Monitoring**
```bash
# Install monitoring tools
apt install -y htop iotop nethogs

# Monitor system resources
htop
```

### **Application Monitoring**
Consider setting up:
- **Uptime monitoring** (UptimeRobot, Pingdom)
- **Error tracking** (Sentry)
- **Performance monitoring** (New Relic, DataDog)

### **Regular Maintenance**
```bash
# Weekly system updates
apt update && apt upgrade -y

# Database maintenance
# - Regular VACUUM and ANALYZE
# - Monitor database size and performance

# Log rotation
logrotate -d /etc/logrotate.conf
```

---

## 💰 **Cost Optimization**

### **DigitalOcean Resources**
- **Droplet**: $12-24/month (2-4 GB RAM)
- **Database**: $15-30/month (Basic plan)
- **Load Balancer**: $12/month (if needed)
- **Spaces**: $5/month (for file storage)

### **Optimization Tips**
1. Use **DigitalOcean Spaces** for file uploads instead of local storage
2. Implement **CDN** for static assets
3. Use **database connection pooling**
4. Monitor resource usage and scale accordingly

---

## 🔄 **Updates and Deployments**

### **Deployment Process**
```bash
# 1. Pull latest changes
cd /home/juridence/juridence
git pull origin main

# 2. Update backend
cd backend
source venv/bin/activate
pip install -r requirements.txt

# 3. Update frontend
cd ..
npm install
npm run build

# 4. Restart services
sudo systemctl restart juridence-backend
sudo systemctl reload nginx
```

### **Zero-Downtime Deployment**
Consider implementing:
- **Blue-Green deployment**
- **Rolling updates**
- **Database migrations** with backward compatibility

---

## 📞 **Support and Resources**

### **DigitalOcean Resources**
- [DigitalOcean Documentation](https://docs.digitalocean.com/)
- [DigitalOcean Community](https://www.digitalocean.com/community)
- [DigitalOcean Support](https://cloud.digitalocean.com/support)

### **Application Resources**
- Check application logs regularly
- Monitor database performance
- Keep dependencies updated
- Implement proper error handling

---

## ✅ **Deployment Checklist**

- [ ] DigitalOcean PostgreSQL database created and configured
- [ ] Droplet created with appropriate resources
- [ ] Server software installed (Python, Node.js, Nginx)
- [ ] Application code deployed
- [ ] Environment variables configured
- [ ] Database migrated successfully
- [ ] Backend service running
- [ ] Frontend built and served by Nginx
- [ ] SSL certificate installed (optional)
- [ ] Firewall configured
- [ ] Backup strategy implemented
- [ ] Monitoring setup
- [ ] Domain DNS configured (if using custom domain)
- [ ] Application tested end-to-end

---

**🎉 Congratulations! Your Juridence application should now be running on DigitalOcean!**

For any issues, check the troubleshooting section or refer to the application logs for detailed error messages.
