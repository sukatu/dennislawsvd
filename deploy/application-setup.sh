#!/bin/bash

# Application Setup Script for Case Search App
# Run this after the system setup

set -e

echo "🔧 Setting up Case Search Application..."

# Navigate to application directory
cd /var/www/case-search

# Backend Setup
echo "Setting up backend..."
cd backend

# Create virtual environment
python3.11 -m venv venv
source venv/bin/activate

# Install Python dependencies
pip install -r requirements.txt

# Create .env file
cat > .env << EOF
DATABASE_URL=mysql+pymysql://root:your_password@localhost:3306/case_search_db
SECRET_KEY=your-secret-key-change-this-in-production
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
CORS_ORIGINS=https://your-domain.com,http://localhost:3000
REACT_APP_GOOGLE_MAPS_API_KEY=your_google_maps_api_key
DEBUG=False
EOF

# Create database
mysql -u root -p -e "CREATE DATABASE IF NOT EXISTS case_search_db;"

# Run database migrations
python create_tables.py

# Frontend Setup
echo "Setting up frontend..."
cd ..

# Install Node.js dependencies
npm install

# Create .env file for frontend
cat > .env << EOF
REACT_APP_API_URL=http://localhost:8000
REACT_APP_GOOGLE_MAPS_API_KEY=your_google_maps_api_key
EOF

# Build frontend
npm run build

echo "✅ Application setup complete!"
echo "Next steps:"
echo "1. Update .env files with your actual values"
echo "2. Configure Nginx"
echo "3. Set up SSL certificates"
echo "4. Start the services"
