#!/bin/bash

# Deployment script for DigitalOcean Droplet
# Run this script from your local machine

set -e

echo "🚀 Deploying Case Search App to DigitalOcean Droplet..."
echo "Server: root@138.68.178.208"
echo ""

# Server details
SERVER="root@138.68.178.208"
APP_DIR="/var/www/case-search"

echo "📋 Step 1: Setting up server environment..."

# Run the system setup script on the server
echo "Installing system dependencies..."
ssh $SERVER "bash -s" < deploy/digitalocean-setup.sh

echo ""
echo "📋 Step 2: Deploying application..."

# Create application directory
ssh $SERVER "mkdir -p $APP_DIR"

# Copy application files
echo "Copying application files..."
rsync -avz --exclude 'node_modules' --exclude '.git' --exclude 'venv' . $SERVER:$APP_DIR/

echo ""
echo "📋 Step 3: Setting up application..."

# Run application setup
ssh $SERVER "cd $APP_DIR && chmod +x deploy/application-setup.sh && ./deploy/application-setup.sh"

echo ""
echo "📋 Step 4: Configuring Nginx..."

# Copy nginx configuration
ssh $SERVER "cp $APP_DIR/deploy/nginx.conf /etc/nginx/sites-available/case-search"
ssh $SERVER "ln -sf /etc/nginx/sites-available/case-search /etc/nginx/sites-enabled/"
ssh $SERVER "rm -f /etc/nginx/sites-enabled/default"

# Test nginx configuration
ssh $SERVER "nginx -t"

# Restart nginx
ssh $SERVER "systemctl restart nginx"

echo ""
echo "📋 Step 5: Setting up SSL (optional)..."

# Install certbot if not already installed
ssh $SERVER "apt install -y certbot python3-certbot-nginx"

echo "To set up SSL, run:"
echo "ssh $SERVER 'certbot --nginx -d your-domain.com'"

echo ""
echo "📋 Step 6: Starting services with PM2..."

# Install PM2 globally
ssh $SERVER "npm install -g pm2"

# Start services
ssh $SERVER "cd $APP_DIR && pm2 start ecosystem.config.js"

# Save PM2 configuration
ssh $SERVER "pm2 save"
ssh $SERVER "pm2 startup"

echo ""
echo "🎉 Deployment complete!"
echo ""
echo "Your application should be running at:"
echo "http://138.68.178.208"
echo ""
echo "To check status:"
echo "ssh $SERVER 'pm2 status'"
echo ""
echo "To view logs:"
echo "ssh $SERVER 'pm2 logs'"
echo ""
echo "To restart services:"
echo "ssh $SERVER 'pm2 restart all'"
