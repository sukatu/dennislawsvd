#!/bin/bash

# Deployment script for Juridence Legal Platform
# This script deploys the latest changes to the production server

echo "🚀 Starting deployment to production server..."

# Server details
SERVER="root@62.171.137.28"
SERVER_PATH="/var/www/juridence"

echo "📦 Building frontend locally..."
npm run build

echo "📤 Connecting to server and deploying..."

# SSH into server and execute deployment commands
ssh $SERVER << 'EOF'
    cd /var/www/juridence
    
    echo "📥 Pulling latest changes from Git..."
    git pull origin main
    
    echo "🔧 Installing backend dependencies..."
    cd backend
    source venv/bin/activate
    pip install -r requirements.txt
    
    echo "🔄 Restarting backend service..."
    pm2 restart juridence-backend
    
    echo "📦 Building frontend on server..."
    cd /var/www/juridence
    npm install
    npm run build
    
    echo "🔄 Restarting frontend service..."
    pm2 restart juridence-frontend
    
    echo "✅ Deployment completed successfully!"
    
    echo "📊 Service Status:"
    pm2 status
EOF

echo "🎉 Deployment process completed!"
echo ""
echo "🌐 Your application should now be updated at: http://62.171.137.28"
echo ""
echo "To verify the deployment:"
echo "  - Visit the website and check for the AI Chat button in the documentation"
echo "  - Check service status: ssh $SERVER 'pm2 status'"
echo "  - View logs: ssh $SERVER 'pm2 logs'"

