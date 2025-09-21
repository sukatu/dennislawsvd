#!/bin/bash

# DigitalOcean Deployment Script for Juridence
# This script automates the server setup process

set -e

echo "🚀 Starting DigitalOcean server setup for Juridence..."

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

# Check if running as root
if [ "$EUID" -ne 0 ]; then
    print_error "Please run this script as root (use sudo)"
    exit 1
fi

print_status "Updating system packages..."
apt update && apt upgrade -y

print_status "Installing Python 3.11 and dependencies..."
apt install -y python3.11 python3.11-venv python3.11-dev python3-pip

print_status "Installing Node.js 18.x..."
curl -fsSL https://deb.nodesource.com/setup_18.x | sudo -E bash -
apt install -y nodejs

print_status "Installing Nginx..."
apt install -y nginx

print_status "Installing Git..."
apt install -y git

print_status "Installing PostgreSQL client..."
apt install -y postgresql-client

print_status "Installing system dependencies..."
apt install -y build-essential libssl-dev libffi-dev python3-dev

print_status "Installing additional tools..."
apt install -y htop iotop nethogs curl wget unzip

print_status "Creating application user..."
if ! id "juridence" &>/dev/null; then
    useradd -m -s /bin/bash juridence
    usermod -aG sudo juridence
    print_success "Created juridence user"
else
    print_warning "User juridence already exists"
fi

print_status "Setting up application directory..."
mkdir -p /home/juridence/juridence
chown -R juridence:juridence /home/juridence/juridence

print_status "Configuring firewall..."
ufw --force enable
ufw allow 22/tcp
ufw allow 80/tcp
ufw allow 443/tcp
print_success "Firewall configured"

print_status "Creating backup directory..."
mkdir -p /home/juridence/backups
chown juridence:juridence /home/juridence/backups

print_status "Installing PM2 for process management..."
npm install -g pm2

print_success "Server setup completed successfully!"
print_status "Next steps:"
echo "1. Upload your application code to /home/juridence/juridence/"
echo "2. Run the application setup script as the juridence user"
echo "3. Configure your environment variables"
echo "4. Start the services"

print_warning "Please note: You'll need to configure your database connection and environment variables manually."
