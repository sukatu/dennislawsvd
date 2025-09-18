# 🚀 DigitalOcean Deployment Guide

## Option 1: DigitalOcean App Platform (Recommended)

### Prerequisites
1. DigitalOcean account
2. GitHub repository with your code
3. Domain name (optional but recommended)

### Steps

#### 1. Create App on DigitalOcean App Platform
1. Go to [DigitalOcean App Platform](https://cloud.digitalocean.com/apps)
2. Click "Create App"
3. Connect your GitHub repository
4. Select the `.do/app.yaml` file for configuration
5. Review and create the app

#### 2. Configure Environment Variables
In the App Platform dashboard, set these environment variables:

**Backend Service:**
```
DATABASE_URL=mysql://user:password@host:port/database
SECRET_KEY=your-secret-key-here
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
CORS_ORIGINS=https://your-frontend-url.ondigitalocean.app
REACT_APP_GOOGLE_MAPS_API_KEY=your_google_maps_api_key
```

**Frontend Service:**
```
REACT_APP_API_URL=https://your-backend-url.ondigitalocean.app
REACT_APP_GOOGLE_MAPS_API_KEY=your_google_maps_api_key
```

#### 3. Add Database
1. In App Platform, go to "Resources" tab
2. Click "Create Database"
3. Choose MySQL 8
4. Select appropriate size
5. Note the connection details

---

## Option 2: DigitalOcean Droplet (More Control)

### Prerequisites
1. DigitalOcean account
2. Domain name
3. SSH access to your droplet

### Steps

#### 1. Create Droplet
1. Go to [DigitalOcean Droplets](https://cloud.digitalocean.com/droplets)
2. Create new droplet:
   - **Image**: Ubuntu 22.04
   - **Size**: Basic $6/month (1GB RAM) or higher
   - **Region**: Choose closest to your users
   - **Authentication**: SSH key or password

#### 2. Initial Server Setup
```bash
# Connect to your droplet
ssh root@your-droplet-ip

# Run the setup script
wget https://raw.githubusercontent.com/your-username/case-search-html/main/deploy/digitalocean-setup.sh
chmod +x digitalocean-setup.sh
./digitalocean-setup.sh
```

#### 3. Deploy Application
```bash
# Clone your repository
cd /var/www/case-search
git clone https://github.com/your-username/case-search-html.git .

# Run application setup
chmod +x deploy/application-setup.sh
./deploy/application-setup.sh
```

#### 4. Configure Nginx
```bash
# Copy nginx configuration
sudo cp deploy/nginx.conf /etc/nginx/sites-available/case-search
sudo ln -s /etc/nginx/sites-available/case-search /etc/nginx/sites-enabled/
sudo rm /etc/nginx/sites-enabled/default

# Test nginx configuration
sudo nginx -t

# Restart nginx
sudo systemctl restart nginx
```

#### 5. Set up SSL with Let's Encrypt
```bash
# Install certbot
sudo apt install certbot python3-certbot-nginx

# Get SSL certificate
sudo certbot --nginx -d your-domain.com -d www.your-domain.com

# Test auto-renewal
sudo certbot renew --dry-run
```

#### 6. Start Services with PM2
```bash
# Install PM2 globally
sudo npm install -g pm2

# Start services
pm2 start ecosystem.config.js

# Save PM2 configuration
pm2 save
pm2 startup
```

---

## Option 3: Docker on DigitalOcean

### Prerequisites
1. DigitalOcean account
2. Docker and Docker Compose installed
3. Domain name

### Steps

#### 1. Create Droplet with Docker
1. Create droplet with Docker pre-installed
2. Or install Docker manually:
```bash
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh
sudo usermod -aG docker $USER
```

#### 2. Deploy with Docker Compose
```bash
# Clone repository
git clone https://github.com/your-username/case-search-html.git
cd case-search-html

# Copy environment file
cp env.production .env

# Edit environment variables
nano .env

# Start services
docker-compose up -d
```

---

## Post-Deployment

### 1. Database Setup
```bash
# Connect to your database
mysql -u root -p

# Create database and user
CREATE DATABASE case_search_db;
CREATE USER 'case_search_user'@'%' IDENTIFIED BY 'your_password';
GRANT ALL PRIVILEGES ON case_search_db.* TO 'case_search_user'@'%';
FLUSH PRIVILEGES;
```

### 2. Test Your Application
1. Visit your domain
2. Test login functionality
3. Check admin dashboard
4. Verify API endpoints

### 3. Monitor and Maintain
- Set up monitoring with DigitalOcean monitoring
- Configure log rotation
- Set up automated backups
- Monitor resource usage

---

## Cost Estimation

### App Platform (Recommended)
- **Basic Plan**: $5/month per service
- **Database**: $15/month for 1GB RAM
- **Total**: ~$25/month

### Droplet (More Control)
- **Basic Droplet**: $6/month (1GB RAM)
- **Database**: $15/month for 1GB RAM
- **Total**: ~$21/month

### Docker (Most Control)
- **Basic Droplet**: $6/month (1GB RAM)
- **Database**: $15/month for 1GB RAM
- **Total**: ~$21/month

---

## Security Considerations

1. **Firewall**: Configure UFW or iptables
2. **SSL**: Always use HTTPS
3. **Database**: Use strong passwords
4. **Updates**: Keep system and dependencies updated
5. **Backups**: Set up automated backups
6. **Monitoring**: Monitor for suspicious activity

---

## Troubleshooting

### Common Issues:
1. **Port conflicts**: Check if ports 80, 443, 3000, 8000 are available
2. **Database connection**: Verify DATABASE_URL format
3. **CORS errors**: Check CORS_ORIGINS configuration
4. **SSL issues**: Verify domain DNS settings
5. **Build failures**: Check logs for missing dependencies

### Useful Commands:
```bash
# Check service status
pm2 status

# View logs
pm2 logs

# Restart services
pm2 restart all

# Check nginx status
sudo systemctl status nginx

# Test nginx config
sudo nginx -t

# Check database
sudo systemctl status mysql
```

---

## Support Resources

- [DigitalOcean Documentation](https://docs.digitalocean.com/)
- [App Platform Guide](https://docs.digitalocean.com/products/app-platform/)
- [Droplet Management](https://docs.digitalocean.com/products/droplets/)
- [Database Management](https://docs.digitalocean.com/products/databases/)
