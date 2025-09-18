#!/bin/bash

# DigitalOcean Droplet Setup Script for Case Search App
# Run this script on a fresh Ubuntu 22.04 droplet

set -e

echo "🚀 Setting up Case Search App on DigitalOcean..."

# Update system
sudo apt update && sudo apt upgrade -y

# Install Node.js 18
curl -fsSL https://deb.nodesource.com/setup_18.x | sudo -E bash -
sudo apt-get install -y nodejs

# Install Python 3.11
sudo apt install -y python3.11 python3.11-venv python3.11-dev python3-pip

# Install MySQL
sudo apt install -y mysql-server mysql-client

# Install Nginx
sudo apt install -y nginx

# Install PM2 for process management
sudo npm install -g pm2

# Install Certbot for SSL
sudo apt install -y certbot python3-certbot-nginx

# Create application directory
sudo mkdir -p /var/www/case-search
sudo chown -R $USER:$USER /var/www/case-search

# Clone repository (replace with your repo URL)
cd /var/www/case-search
# git clone https://github.com/your-username/case-search-html.git .

echo "✅ System setup complete!"
echo "Next steps:"
echo "1. Clone your repository to /var/www/case-search"
echo "2. Run the application setup script"
echo "3. Configure Nginx and SSL"
