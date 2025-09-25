# 🔧 Manual Server Setup Guide

**Server Details:**
- IP: 62.171.137.28
- User: root
- Password: OJTn3IDq6umk6FagN

## Step 1: Connect to Your Server

Open your terminal and connect to the server:

```bash
ssh root@62.171.137.28
```

When prompted, enter the password: `OJTn3IDq6umk6FagN`

## Step 2: Update System and Install Dependencies

Run these commands on your server:

```bash
# Update system packages
apt update && apt upgrade -y

# Install essential packages
apt install -y curl wget git vim unzip software-properties-common apt-transport-https ca-certificates gnupg lsb-release

# Install Python 3.11
apt install -y python3.11 python3.11-venv python3.11-dev python3-pip

# Install PostgreSQL
apt install -y postgresql postgresql-contrib postgresql-client

# Install Node.js 18 LTS
curl -fsSL https://deb.nodesource.com/setup_18.x | bash -
apt-get install -y nodejs

# Install Nginx
apt install -y nginx

# Install PM2 and serve
npm install -g pm2 serve

# Install UFW firewall
apt install -y ufw
```

## Step 3: Start and Enable Services

```bash
# Start PostgreSQL
systemctl start postgresql
systemctl enable postgresql

# Start Nginx
systemctl start nginx
systemctl enable nginx

# Check status
systemctl status postgresql
systemctl status nginx
```

## Step 4: Setup Database

```bash
# Create database and user
sudo -u postgres psql << EOF
CREATE DATABASE juridence_db;
CREATE USER juridence_user WITH PASSWORD 'JuridenceSecure2024!';
ALTER USER juridence_user CREATEDB;
GRANT ALL PRIVILEGES ON DATABASE juridence_db TO juridence_user;
\q
EOF
```

## Step 5: Clone Your Application

```bash
# Create application directory
mkdir -p /var/www/juridence
cd /var/www/juridence

# Clone your repository
git clone https://github.com/sukatu/dennislawsvd.git .

# Set proper permissions
chown -R www-data:www-data /var/www/juridence
chmod -R 755 /var/www/juridence
```

## Step 6: Setup Backend

```bash
# Navigate to project directory
cd /var/www/juridence

# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install Python dependencies
pip install -r requirements.txt

# Create environment file
cat > .env << EOF
# Database Configuration
DATABASE_URL=postgresql://juridence_user:JuridenceSecure2024!@localhost:5432/juridence_db

# Security
SECRET_KEY=JuridenceSuperSecretKey2024!@#SecureRandomString
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

# CORS
ALLOWED_ORIGINS=["http://localhost:3000", "http://62.171.137.28", "https://62.171.137.28"]

# Environment
ENVIRONMENT=production
DEBUG=false
EOF

# Create database tables
python -c "
import sys
sys.path.append('.')
from backend.database import engine, Base
try:
    Base.metadata.create_all(bind=engine)
    print('✅ Database tables created successfully!')
except Exception as e:
    print(f'❌ Error creating tables: {e}')
"
```

## Step 7: Setup Frontend

```bash
# Install frontend dependencies
npm install

# Create production build
npm run build
```

## Step 8: Create PM2 Configuration

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

# Create log directory
mkdir -p /var/log/juridence
chown -R www-data:www-data /var/log/juridence

# Start applications with PM2
pm2 start ecosystem.config.js
pm2 save
pm2 startup
```

## Step 9: Configure Nginx

```bash
# Create Nginx configuration
cat > /etc/nginx/sites-available/juridence << EOF
server {
    listen 80;
    server_name 62.171.137.28;

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
}
EOF

# Enable the site
ln -sf /etc/nginx/sites-available/juridence /etc/nginx/sites-enabled/
rm -f /etc/nginx/sites-enabled/default

# Test Nginx configuration
nginx -t

# Restart Nginx
systemctl restart nginx
```

## Step 10: Configure Firewall

```bash
# Configure UFW firewall
ufw default deny incoming
ufw default allow outgoing
ufw allow ssh
ufw allow 'Nginx Full'
ufw --force enable

# Check status
ufw status
```

## Step 11: Verify Installation

```bash
# Check all services
pm2 status
systemctl status nginx
systemctl status postgresql

# Test the application
curl http://localhost:8000/api/health
curl http://localhost:3000

# Check logs
pm2 logs
```

## 🎉 Your Application is Now Live!

**Access your application at:**
- **Frontend:** http://62.171.137.28
- **Backend API:** http://62.171.137.28/api

## 🔧 Useful Commands

```bash
# Check application status
pm2 status
pm2 logs

# Restart services
pm2 restart all
systemctl restart nginx

# Update application
cd /var/www/juridence
git pull origin main
npm run build
pm2 restart all

# View logs
tail -f /var/log/juridence/backend-error.log
tail -f /var/log/nginx/access.log
```

## 🆘 Troubleshooting

If you encounter any issues:

1. **Check PM2 status:** `pm2 status`
2. **Check Nginx:** `systemctl status nginx`
3. **Check PostgreSQL:** `systemctl status postgresql`
4. **View logs:** `pm2 logs` or `journalctl -u nginx`

## 📋 Next Steps

1. **Test the application** by visiting http://62.171.137.28
2. **Create an admin user** through the application
3. **Add sample data** if needed
4. **Set up SSL** if you have a domain name
5. **Configure backups** for your database

---

**🎉 Congratulations! Your Juridence Case Hearing Management App is now running on your server!**
