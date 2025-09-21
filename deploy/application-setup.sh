#!/bin/bash

# Application Setup Script for Juridence
# Run this script as the juridence user after server setup

set -e

echo "🚀 Setting up Juridence application..."

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Function to print colored output
print_status() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

print_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Check if running as juridence user
if [ "$USER" != "juridence" ]; then
    print_error "Please run this script as the juridence user"
    exit 1
fi

# Navigate to application directory
cd /home/juridence/juridence

print_status "Setting up backend..."

# Create virtual environment
if [ ! -d "backend/venv" ]; then
    print_status "Creating Python virtual environment..."
    cd backend
    python3.11 -m venv venv
    cd ..
fi

# Activate virtual environment and install dependencies
print_status "Installing Python dependencies..."
cd backend
source venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
cd ..

print_success "Backend setup completed"

print_status "Setting up frontend..."
npm install
npm run build
print_success "Frontend setup completed"

print_status "Creating systemd service files..."

# Create backend service file
sudo tee /etc/systemd/system/juridence-backend.service > /dev/null <<EOF
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
EOF

print_status "Creating Nginx configuration..."

# Create Nginx configuration
sudo tee /etc/nginx/sites-available/juridence > /dev/null <<EOF
server {
    listen 80;
    server_name _;

    # Frontend
    location / {
        root /home/juridence/juridence/build;
        index index.html index.htm;
        try_files \$uri \$uri/ /index.html;
        
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
        proxy_set_header Upgrade \$http_upgrade;
        proxy_set_header Connection 'upgrade';
        proxy_set_header Host \$host;
        proxy_set_header X-Real-IP \$remote_addr;
        proxy_set_header X-Forwarded-For \$proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto \$scheme;
        proxy_cache_bypass \$http_upgrade;
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
EOF

print_status "Configuring Nginx..."

# Enable site and remove default
sudo ln -sf /etc/nginx/sites-available/juridence /etc/nginx/sites-enabled/
sudo rm -f /etc/nginx/sites-enabled/default

# Test Nginx configuration
sudo nginx -t

print_status "Enabling and starting services..."

# Enable and start backend service
sudo systemctl daemon-reload
sudo systemctl enable juridence-backend
sudo systemctl start juridence-backend

# Restart Nginx
sudo systemctl restart nginx

print_status "Checking service status..."

# Check backend service
if sudo systemctl is-active --quiet juridence-backend; then
    print_success "Backend service is running"
else
    print_error "Backend service failed to start"
    sudo systemctl status juridence-backend
fi

# Check Nginx
if sudo systemctl is-active --quiet nginx; then
    print_success "Nginx is running"
else
    print_error "Nginx failed to start"
    sudo systemctl status nginx
fi

print_status "Creating backup script..."

# Create backup script
tee /home/juridence/backup.sh > /dev/null <<EOF
#!/bin/bash
DATE=\$(date +%Y%m%d_%H%M%S)
BACKUP_DIR="/home/juridence/backups"

mkdir -p \$BACKUP_DIR

# Database backup (if .env exists)
if [ -f "/home/juridence/juridence/backend/.env" ]; then
    source /home/juridence/juridence/backend/.env
    if [ ! -z "\$DATABASE_URL_ENV" ]; then
        pg_dump "\$DATABASE_URL_ENV" > \$BACKUP_DIR/db_backup_\$DATE.sql
        echo "Database backup created: db_backup_\$DATE.sql"
    fi
fi

# Application backup
tar -czf \$BACKUP_DIR/app_backup_\$DATE.tar.gz /home/juridence/juridence

# Keep only last 7 days of backups
find \$BACKUP_DIR -name "*.sql" -mtime +7 -delete
find \$BACKUP_DIR -name "*.tar.gz" -mtime +7 -delete

echo "Backup completed: \$DATE"
EOF

chmod +x /home/juridence/backup.sh

print_status "Creating deployment script..."

# Create deployment script
tee /home/juridence/deploy.sh > /dev/null <<EOF
#!/bin/bash
echo "🚀 Deploying Juridence application..."

cd /home/juridence/juridence

# Pull latest changes (if using git)
if [ -d ".git" ]; then
    git pull origin main
fi

# Update backend
cd backend
source venv/bin/activate
pip install -r requirements.txt
cd ..

# Update frontend
npm install
npm run build

# Restart services
sudo systemctl restart juridence-backend
sudo systemctl reload nginx

echo "✅ Deployment completed!"
EOF

chmod +x /home/juridence/deploy.sh

print_success "Application setup completed successfully!"

print_warning "IMPORTANT: You still need to:"
echo "1. Create /home/juridence/juridence/backend/.env file with your database credentials"
echo "2. Test your database connection"
echo "3. Run database migrations if needed"
echo "4. Configure your domain name in Nginx configuration"
echo "5. Set up SSL certificate (recommended)"

print_status "Useful commands:"
echo "- Check backend logs: sudo journalctl -u juridence-backend -f"
echo "- Check Nginx logs: sudo tail -f /var/log/nginx/error.log"
echo "- Restart backend: sudo systemctl restart juridence-backend"
echo "- Deploy updates: /home/juridence/deploy.sh"
echo "- Create backup: /home/juridence/backup.sh"

print_status "Application should be accessible at:"
echo "- Frontend: http://YOUR_SERVER_IP"
echo "- Backend API: http://YOUR_SERVER_IP/api/health"
