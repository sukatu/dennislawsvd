#!/bin/bash

# Deploy Application Script for Juridence
# This script deploys your case hearing management app to the server

SERVER_IP="62.171.137.28"
SERVER_USER="root"
APP_DIR="/var/www/juridence"

echo "🚀 Deploying Juridence Application to Server..."
echo "Server: $SERVER_USER@$SERVER_IP"
echo "=============================================="

# Deploy the application
ssh $SERVER_USER@$SERVER_IP << EOF
#!/bin/bash

echo "📥 Cloning repository..."
cd /var/www
rm -rf juridence
git clone https://github.com/sukatu/dennislawsvd.git juridence
cd juridence

echo "🔧 Setting up backend..."
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

echo "📝 Creating environment file..."
cat > .env << 'EOL'
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
EOL

echo "🗃️ Creating database tables..."
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

echo "⚛️ Setting up frontend..."
npm install
npm run build

echo "🔄 Creating PM2 ecosystem file..."
cat > ecosystem.config.js << 'EOL'
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
EOL

echo "📁 Creating log directory..."
mkdir -p /var/log/juridence
chown -R www-data:www-data /var/log/juridence

echo "🚀 Starting applications with PM2..."
pm2 delete all 2>/dev/null || true
pm2 start ecosystem.config.js
pm2 save
pm2 startup systemd -u root --hp /root

echo "🌐 Configuring Nginx..."
cat > /etc/nginx/sites-available/juridence << 'EOL'
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
EOL

# Enable the site
ln -sf /etc/nginx/sites-available/juridence /etc/nginx/sites-enabled/
rm -f /etc/nginx/sites-enabled/default

echo "🔍 Testing Nginx configuration..."
nginx -t

echo "🔄 Restarting Nginx..."
systemctl restart nginx

echo "✅ Application deployed successfully!"
echo "=================================="
echo "🌐 Your application is now running at:"
echo "   Frontend: http://62.171.137.28"
echo "   Backend API: http://62.171.137.28/api"
echo ""
echo "📊 Check status with:"
echo "   pm2 status"
echo "   systemctl status nginx"
echo "   systemctl status postgresql"
EOF

echo "🎉 Deployment completed!"
echo "=================================="
echo "Your Juridence Case Hearing Management App is now live!"
echo "Access it at: http://62.171.137.28"
echo ""
echo "🔧 Useful commands:"
echo "  ssh root@62.171.137.28 'pm2 status'"
echo "  ssh root@62.171.137.28 'pm2 logs'"
echo "  ssh root@62.171.137.28 'systemctl status nginx'"
