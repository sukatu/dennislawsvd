#!/bin/bash

# 🚀 DennisLaw SVD - Cloudways Deployment Script
# This script helps deploy both frontend and backend to Cloudways

set -e  # Exit on any error

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Configuration - UPDATE THESE VALUES
SERVER_IP=""
SERVER_USER=""
APP_NAME=""
DOMAIN=""
API_SUBDOMAIN="api"

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

# Function to check if required tools are installed
check_dependencies() {
    print_status "Checking dependencies..."
    
    if ! command -v rsync &> /dev/null; then
        print_error "rsync is not installed. Please install it first."
        exit 1
    fi
    
    if ! command -v ssh &> /dev/null; then
        print_error "ssh is not installed. Please install it first."
        exit 1
    fi
    
    if ! command -v npm &> /dev/null; then
        print_error "npm is not installed. Please install it first."
        exit 1
    fi
    
    print_success "All dependencies are available"
}

# Function to build frontend
build_frontend() {
    print_status "Building frontend..."
    
    if [ ! -f "package.json" ]; then
        print_error "package.json not found. Are you in the project root?"
        exit 1
    fi
    
    # Install dependencies if node_modules doesn't exist
    if [ ! -d "node_modules" ]; then
        print_status "Installing frontend dependencies..."
        npm install
    fi
    
    # Build the project
    print_status "Running npm run build..."
    npm run build
    
    if [ ! -d "build" ]; then
        print_error "Build failed. build/ directory not found."
        exit 1
    fi
    
    print_success "Frontend built successfully"
}

# Function to prepare backend
prepare_backend() {
    print_status "Preparing backend..."
    
    if [ ! -f "backend/main.py" ]; then
        print_error "Backend main.py not found. Are you in the project root?"
        exit 1
    fi
    
    # Create backend deployment directory
    mkdir -p backend-deployment
    
    # Copy backend files excluding unnecessary files
    rsync -av --exclude='venv' --exclude='__pycache__' --exclude='*.pyc' --exclude='.git' backend/ backend-deployment/
    
    print_success "Backend prepared successfully"
}

# Function to deploy frontend
deploy_frontend() {
    print_status "Deploying frontend to Cloudways..."
    
    if [ -z "$SERVER_IP" ] || [ -z "$SERVER_USER" ] || [ -z "$APP_NAME" ]; then
        print_error "Please configure SERVER_IP, SERVER_USER, and APP_NAME in the script"
        exit 1
    fi
    
    # Upload frontend files
    print_status "Uploading frontend files..."
    rsync -avz --delete build/ ${SERVER_USER}@${SERVER_IP}:/home/master/applications/${APP_NAME}/public_html/
    
    print_success "Frontend deployed successfully"
}

# Function to deploy backend
deploy_backend() {
    print_status "Deploying backend to Cloudways..."
    
    if [ -z "$SERVER_IP" ] || [ -z "$SERVER_USER" ] || [ -z "$APP_NAME" ]; then
        print_error "Please configure SERVER_IP, SERVER_USER, and APP_NAME in the script"
        exit 1
    fi
    
    # Upload backend files
    print_status "Uploading backend files..."
    rsync -avz --delete backend-deployment/ ${SERVER_USER}@${SERVER_IP}:/home/master/applications/${APP_NAME}/backend/
    
    print_success "Backend deployed successfully"
}

# Function to setup backend on server
setup_backend() {
    print_status "Setting up backend on server..."
    
    # Create setup script
    cat > setup_backend.sh << 'EOF'
#!/bin/bash
set -e

cd /home/master/applications/${APP_NAME}/backend

# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install --upgrade pip
pip install -r requirements.txt

# Create config.py if it doesn't exist
if [ ! -f "config.py" ]; then
    cat > config.py << 'EOL'
import os

class Settings:
    # Database configuration - UPDATE THESE VALUES
    database_url = "mysql+pymysql://username:password@localhost:3306/database_name"
    
    # API configuration
    api_host = "0.0.0.0"
    api_port = 8000
    
    # CORS settings - UPDATE YOUR DOMAIN
    allowed_origins = [
        "https://yourdomain.com",
        "https://www.yourdomain.com",
        "http://localhost:3000"
    ]

settings = Settings()
EOL
fi

# Create .htaccess for backend
cat > .htaccess << 'EOL'
RewriteEngine On

# Proxy requests to FastAPI
RewriteCond %{REQUEST_FILENAME} !-f
RewriteCond %{REQUEST_FILENAME} !-d
RewriteRule ^(.*)$ http://localhost:8000/$1 [P,L]

# Set headers
Header always set Access-Control-Allow-Origin "*"
Header always set Access-Control-Allow-Methods "GET, POST, PUT, DELETE, OPTIONS"
Header always set Access-Control-Allow-Headers "Content-Type, Authorization"
EOL

# Create systemd service
sudo tee /etc/systemd/system/dennislaw-api.service > /dev/null << 'EOL'
[Unit]
Description=DennisLaw SVD API
After=network.target

[Service]
Type=simple
User=master
WorkingDirectory=/home/master/applications/${APP_NAME}/backend
Environment=PATH=/home/master/applications/${APP_NAME}/backend/venv/bin
ExecStart=/home/master/applications/${APP_NAME}/backend/venv/bin/gunicorn -w 4 -k uvicorn.workers.UvicornWorker -b 0.0.0.0:8000 main:app
Restart=always

[Install]
WantedBy=multi-user.target
EOL

# Enable and start service
sudo systemctl daemon-reload
sudo systemctl enable dennislaw-api
sudo systemctl start dennislaw-api

echo "Backend setup completed!"
echo "Service status:"
sudo systemctl status dennislaw-api --no-pager
EOF

    # Upload and run setup script
    scp setup_backend.sh ${SERVER_USER}@${SERVER_IP}:/tmp/
    ssh ${SERVER_USER}@${SERVER_IP} "chmod +x /tmp/setup_backend.sh && APP_NAME=${APP_NAME} /tmp/setup_backend.sh"
    
    # Cleanup
    rm setup_backend.sh
    
    print_success "Backend setup completed"
}

# Function to create .htaccess for frontend
create_frontend_htaccess() {
    print_status "Creating .htaccess for frontend..."
    
    cat > build/.htaccess << 'EOF'
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
EOF

    print_success ".htaccess created for frontend"
}

# Function to show deployment summary
show_summary() {
    print_success "Deployment completed!"
    echo ""
    echo "📋 Deployment Summary:"
    echo "====================="
    echo "Frontend URL: https://${DOMAIN:-yourdomain.com}"
    echo "Backend API: https://${API_SUBDOMAIN}.${DOMAIN:-yourdomain.com}"
    echo "API Docs: https://${API_SUBDOMAIN}.${DOMAIN:-yourdomain.com}/docs"
    echo ""
    echo "🔧 Next Steps:"
    echo "1. Update database credentials in backend/config.py"
    echo "2. Update CORS settings with your actual domain"
    echo "3. Update frontend API URLs to use production endpoints"
    echo "4. Set up SSL certificates in Cloudways dashboard"
    echo "5. Test all functionality"
    echo ""
    echo "📞 Support:"
    echo "- Check logs: sudo journalctl -u dennislaw-api -f"
    echo "- Restart backend: sudo systemctl restart dennislaw-api"
    echo "- Check status: sudo systemctl status dennislaw-api"
}

# Main deployment function
main() {
    echo "🚀 DennisLaw SVD - Cloudways Deployment Script"
    echo "=============================================="
    echo ""
    
    # Check if configuration is set
    if [ -z "$SERVER_IP" ] || [ -z "$SERVER_USER" ] || [ -z "$APP_NAME" ]; then
        print_error "Please configure the script variables first:"
        echo "  SERVER_IP: Your Cloudways server IP"
        echo "  SERVER_USER: Your Cloudways username (usually 'master')"
        echo "  APP_NAME: Your Cloudways application name"
        echo "  DOMAIN: Your domain name (optional)"
        echo ""
        print_warning "Edit this script and update the configuration section at the top"
        exit 1
    fi
    
    # Run deployment steps
    check_dependencies
    build_frontend
    create_frontend_htaccess
    prepare_backend
    deploy_frontend
    deploy_backend
    setup_backend
    show_summary
}

# Handle command line arguments
case "${1:-}" in
    "frontend")
        check_dependencies
        build_frontend
        create_frontend_htaccess
        deploy_frontend
        print_success "Frontend deployment completed!"
        ;;
    "backend")
        check_dependencies
        prepare_backend
        deploy_backend
        setup_backend
        print_success "Backend deployment completed!"
        ;;
    "build")
        check_dependencies
        build_frontend
        create_frontend_htaccess
        prepare_backend
        print_success "Build completed! Ready for deployment."
        ;;
    *)
        main
        ;;
esac