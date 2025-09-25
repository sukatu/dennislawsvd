# 🚀 Fresh Server Setup Guide for Case Hearing Management App

This guide will help you set up a fresh server to run your case hearing management application (Juridence Legal Database Platform).

## 📋 Prerequisites

- Fresh Ubuntu 20.04+ server
- Root or sudo access
- Domain name (optional but recommended)
- Basic command line knowledge

## 🔧 Step 1: System Updates and Basic Setup

```bash
# Update system packages
sudo apt update && sudo apt upgrade -y

# Install essential packages
sudo apt install -y curl wget git vim unzip software-properties-common apt-transport-https ca-certificates gnupg lsb-release

# Set timezone (replace with your timezone)
sudo timedatectl set-timezone Africa/Accra
```

## 🐍 Step 2: Install Python 3.11+ and pip

```bash
# Install Python 3.11
sudo apt install -y python3.11 python3.11-venv python3.11-dev python3-pip

# Set Python 3.11 as default
sudo update-alternatives --install /usr/bin/python3 python3 /usr/bin/python3.11 1
sudo update-alternatives --install /usr/bin/python python /usr/bin/python3.11 1

# Verify installation
python3 --version
pip3 --version
```

## 🗄️ Step 3: Install PostgreSQL Database

```bash
# Install PostgreSQL
sudo apt install -y postgresql postgresql-contrib postgresql-client

# Start and enable PostgreSQL
sudo systemctl start postgresql
sudo systemctl enable postgresql

# Create database and user
sudo -u postgres psql << EOF
CREATE DATABASE juridence_db;
CREATE USER juridence_user WITH PASSWORD 'your_secure_password_here';
ALTER USER juridence_user CREATEDB;
GRANT ALL PRIVILEGES ON DATABASE juridence_db TO juridence_user;
\q
EOF

# Configure PostgreSQL for remote connections (optional)
sudo nano /etc/postgresql/*/main/postgresql.conf
# Uncomment and modify: listen_addresses = 'localhost'

sudo nano /etc/postgresql/*/main/pg_hba.conf
# Add line: host    juridence_db    juridence_user    127.0.0.1/32    md5
```

## 🟢 Step 4: Install Node.js and npm

```bash
# Install Node.js 18 LTS
curl -fsSL https://deb.nodesource.com/setup_18.x | sudo -E bash -
sudo apt-get install -y nodejs

# Verify installation
node --version
npm --version

# Install PM2 for process management
sudo npm install -g pm2
```

## 🌐 Step 5: Install Nginx Web Server

```bash
# Install Nginx
sudo apt install -y nginx

# Start and enable Nginx
sudo systemctl start nginx
sudo systemctl enable nginx

# Check status
sudo systemctl status nginx
```

## 📁 Step 6: Clone and Setup Application

```bash
# Create application directory
sudo mkdir -p /var/www/juridence
sudo chown -R $USER:$USER /var/www/juridence

# Clone repository
cd /var/www/juridence
git clone https://github.com/sukatu/dennislawsvd.git .

# Set proper permissions
sudo chown -R www-data:www-data /var/www/juridence
sudo chmod -R 755 /var/www/juridence
```

## 🔧 Step 7: Setup Backend (FastAPI)

```bash
# Navigate to backend directory
cd /var/www/juridence

# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install Python dependencies
pip install -r requirements.txt

# Create environment file
cat > .env << EOF
# Database Configuration
DATABASE_URL=postgresql://juridence_user:your_secure_password_here@localhost:5432/juridence_db

# Security
SECRET_KEY=your_very_secure_secret_key_here
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

# CORS
ALLOWED_ORIGINS=["http://localhost:3000", "http://your-domain.com", "https://your-domain.com"]

# OpenAI (optional)
OPENAI_API_KEY=your_openai_api_key_here

# Environment
ENVIRONMENT=production
DEBUG=false
EOF

# Create database tables
python -c "
from backend.database import engine, Base
Base.metadata.create_all(bind=engine)
print('Database tables created successfully!')
"

# Test backend
python -m uvicorn backend.main:app --host 0.0.0.0 --port 8000 --reload
```

## ⚛️ Step 8: Setup Frontend (React)

```bash
# Install frontend dependencies
npm install

# Create production build
npm run build

# Test frontend
npm start
```

## 🔄 Step 9: Setup Process Management with PM2

```bash
# Create PM2 ecosystem file
cat > ecosystem.config.js << EOF
module.exports = {
  apps: [
    {
      name: 'juridence-backend',
      script: 'python',
      args: '-m uvicorn backend.main:app --host 0.0.0.0 --port 8000',
      cwd: '/var/www/juridence',
      interpreter: '/var/www/juridence/venv/bin/python',
      env: {
        NODE_ENV: 'production'
      },
      instances: 1,
      autorestart: true,
      watch: false,
      max_memory_restart: '1G',
      error_file: '/var/log/juridence/backend-error.log',
      out_file: '/var/log/juridence/backend-out.log',
      log_file: '/var/log/juridence/backend-combined.log'
    },
    {
      name: 'juridence-frontend',
      script: 'serve',
      args: '-s build -l 3000',
      cwd: '/var/www/juridence',
      env: {
        NODE_ENV: 'production'
      },
      instances: 1,
      autorestart: true,
      watch: false,
      max_memory_restart: '1G'
    }
  ]
};
EOF

# Install serve for frontend
npm install -g serve

# Create log directory
sudo mkdir -p /var/log/juridence
sudo chown -R $USER:$USER /var/log/juridence

# Start applications with PM2
pm2 start ecosystem.config.js

# Save PM2 configuration
pm2 save
pm2 startup

# Check status
pm2 status
```

## 🌐 Step 10: Configure Nginx Reverse Proxy

```bash
# Create Nginx configuration
sudo tee /etc/nginx/sites-available/juridence << EOF
server {
    listen 80;
    server_name your-domain.com www.your-domain.com;

    # Frontend (React)
    location / {
        proxy_pass http://localhost:3000;
        proxy_http_version 1.1;
        proxy_set_header Upgrade \$http_upgrade;
        proxy_set_header Connection 'upgrade';
        proxy_set_header Host \$host;
        proxy_set_header X-Real-IP \$remote_addr;
        proxy_set_header X-Forwarded-For \$proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto \$scheme;
        proxy_cache_bypass \$http_upgrade;
    }

    # Backend API
    location /api {
        proxy_pass http://localhost:8000;
        proxy_http_version 1.1;
        proxy_set_header Upgrade \$http_upgrade;
        proxy_set_header Connection 'upgrade';
        proxy_set_header Host \$host;
        proxy_set_header X-Real-IP \$remote_addr;
        proxy_set_header X-Forwarded-For \$proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto \$scheme;
        proxy_cache_bypass \$http_upgrade;
    }

    # Security headers
    add_header X-Frame-Options "SAMEORIGIN" always;
    add_header X-XSS-Protection "1; mode=block" always;
    add_header X-Content-Type-Options "nosniff" always;
    add_header Referrer-Policy "no-referrer-when-downgrade" always;
    add_header Content-Security-Policy "default-src 'self' http: https: data: blob: 'unsafe-inline'" always;
}
EOF

# Enable the site
sudo ln -s /etc/nginx/sites-available/juridence /etc/nginx/sites-enabled/

# Remove default site
sudo rm /etc/nginx/sites-enabled/default

# Test Nginx configuration
sudo nginx -t

# Restart Nginx
sudo systemctl restart nginx
```

## 🔒 Step 11: Setup SSL with Let's Encrypt (Optional but Recommended)

```bash
# Install Certbot
sudo apt install -y certbot python3-certbot-nginx

# Obtain SSL certificate
sudo certbot --nginx -d your-domain.com -d www.your-domain.com

# Test automatic renewal
sudo certbot renew --dry-run
```

## 🔥 Step 12: Configure Firewall

```bash
# Install UFW
sudo apt install -y ufw

# Configure firewall
sudo ufw default deny incoming
sudo ufw default allow outgoing
sudo ufw allow ssh
sudo ufw allow 'Nginx Full'
sudo ufw allow 8000  # Backend port (if needed for direct access)

# Enable firewall
sudo ufw enable

# Check status
sudo ufw status
```

## 📊 Step 13: Setup Monitoring and Logging

```bash
# Install monitoring tools
sudo apt install -y htop iotop nethogs

# Setup log rotation
sudo tee /etc/logrotate.d/juridence << EOF
/var/log/juridence/*.log {
    daily
    missingok
    rotate 52
    compress
    delaycompress
    notifempty
    create 644 www-data www-data
    postrotate
        pm2 reloadLogs
    endscript
}
EOF
```

## 🗃️ Step 14: Database Setup and Sample Data

```bash
# Navigate to project directory
cd /var/www/juridence

# Activate virtual environment
source venv/bin/activate

# Run database migrations (if you have any)
# python -m alembic upgrade head

# Create sample data (if needed)
# python backend/seed_database.py

# Create admin user (if needed)
# python backend/create_admin_user.py
```

## ✅ Step 15: Final Verification

```bash
# Check all services status
sudo systemctl status nginx
sudo systemctl status postgresql
pm2 status

# Test backend API
curl http://localhost:8000/api/health

# Test frontend
curl http://localhost:3000

# Check logs
pm2 logs
sudo tail -f /var/log/nginx/access.log
sudo tail -f /var/log/nginx/error.log
```

## 🚀 Step 16: Production Optimizations

```bash
# Optimize PostgreSQL
sudo nano /etc/postgresql/*/main/postgresql.conf
# Uncomment and modify:
# shared_buffers = 256MB
# effective_cache_size = 1GB
# maintenance_work_mem = 64MB
# checkpoint_completion_target = 0.9
# wal_buffers = 16MB
# default_statistics_target = 100

# Restart PostgreSQL
sudo systemctl restart postgresql

# Setup automatic backups
sudo mkdir -p /var/backups/juridence
sudo tee /usr/local/bin/backup-juridence.sh << EOF
#!/bin/bash
BACKUP_DIR="/var/backups/juridence"
DATE=\$(date +%Y%m%d_%H%M%S)
pg_dump -h localhost -U juridence_user -d juridence_db > \$BACKUP_DIR/juridence_backup_\$DATE.sql
find \$BACKUP_DIR -name "*.sql" -mtime +7 -delete
EOF

sudo chmod +x /usr/local/bin/backup-juridence.sh

# Add to crontab for daily backups
(crontab -l 2>/dev/null; echo "0 2 * * * /usr/local/bin/backup-juridence.sh") | crontab -
```

## 📋 Post-Installation Checklist

- [ ] All services are running (Nginx, PostgreSQL, PM2)
- [ ] Database is accessible and tables created
- [ ] Frontend is accessible at http://your-domain.com
- [ ] Backend API is accessible at http://your-domain.com/api
- [ ] SSL certificate is installed (if using domain)
- [ ] Firewall is configured
- [ ] Monitoring is set up
- [ ] Backups are scheduled
- [ ] Admin user is created
- [ ] Sample data is loaded (if needed)

## 🔧 Useful Commands

```bash
# Restart services
sudo systemctl restart nginx
sudo systemctl restart postgresql
pm2 restart all

# View logs
pm2 logs
sudo tail -f /var/log/nginx/error.log
sudo tail -f /var/log/juridence/backend-error.log

# Database operations
sudo -u postgres psql -d juridence_db
pm2 monit

# Update application
cd /var/www/juridence
git pull origin main
npm install
npm run build
pm2 restart all
```

## 🆘 Troubleshooting

### Common Issues:

1. **Port already in use**: `sudo netstat -tulpn | grep :8000`
2. **Permission denied**: `sudo chown -R www-data:www-data /var/www/juridence`
3. **Database connection failed**: Check PostgreSQL status and credentials
4. **Nginx 502 error**: Check if backend is running on port 8000
5. **Frontend not loading**: Check if build was successful and PM2 is running

### Log Locations:
- Nginx: `/var/log/nginx/`
- PM2: `/var/log/juridence/`
- PostgreSQL: `/var/log/postgresql/`

## 📞 Support

If you encounter any issues during setup, check the logs and ensure all services are running properly. The application should be accessible at your domain or server IP address.

---

**🎉 Congratulations! Your case hearing management application is now running on your fresh server!**
