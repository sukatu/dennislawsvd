# 🚀 DigitalOcean Quick Start Guide

## **Prerequisites Checklist**
- [ ] DigitalOcean account created
- [ ] Domain name registered (optional)
- [ ] SSH key pair generated
- [ ] Your application code ready

---

## **Step 1: Create Infrastructure (5 minutes)**

### **1.1 Create PostgreSQL Database**
1. Go to **Databases** → **Create Database Cluster**
2. Select **PostgreSQL** → **Basic Plan**
3. Choose region → Name: `juridence-db`
4. **Save connection details:**
   ```
   Host: db-postgresql-[region]-[id].h.db.ondigitalocean.com
   Port: 25060
   Username: doadmin
   Password: [auto-generated]
   Database: defaultdb
   ```

### **1.2 Create Droplet**
1. Go to **Droplets** → **Create Droplet**
2. **Ubuntu 22.04 LTS** → **2GB RAM, 50GB SSD** (minimum)
3. Add your SSH key → Name: `juridence-app`
4. **Save IP address:** `YOUR_DROPLET_IP`

---

## **Step 2: Automated Server Setup (10 minutes)**

### **2.1 Connect and Run Setup**
```bash
# Connect to your droplet
ssh root@YOUR_DROPLET_IP

# Download and run server setup script
curl -fsSL https://raw.githubusercontent.com/yourusername/juridence/main/deploy/digitalocean-setup.sh | bash
```

### **2.2 Upload Application Code**
```bash
# Option 1: Clone from Git (if public repo)
su - juridence
git clone https://github.com/yourusername/juridence.git
cd juridence

# Option 2: Upload via SCP (from your local machine)
# scp -r /path/to/your/juridence juridence@YOUR_DROPLET_IP:/home/juridence/
```

### **2.3 Run Application Setup**
```bash
# Run as juridence user
cd /home/juridence/juridence
chmod +x deploy/application-setup.sh
./deploy/application-setup.sh
```

---

## **Step 3: Configure Environment (5 minutes)**

### **3.1 Create Environment File**
```bash
# Create .env file
cd backend
cp deploy/env.example .env
nano .env
```

### **3.2 Update Database Connection**
```env
DATABASE_URL_ENV=postgresql://doadmin:YOUR_PASSWORD@YOUR_DB_HOST:25060/juridence?sslmode=require
SECRET_KEY=your-super-secret-key-here-make-it-long-and-random
DEBUG=False
```

### **3.3 Test Database Connection**
```bash
source venv/bin/activate
python test_digitalocean_connection.py
```

---

## **Step 4: Final Deployment (5 minutes)**

### **4.1 Start Services**
```bash
# Start backend service
sudo systemctl start juridence-backend
sudo systemctl enable juridence-backend

# Restart Nginx
sudo systemctl restart nginx
```

### **4.2 Test Application**
- **Frontend:** `http://YOUR_DROPLET_IP`
- **API Health:** `http://YOUR_DROPLET_IP/api/health`

---

## **Step 5: SSL Certificate (Optional - 5 minutes)**

```bash
# Install Certbot
sudo apt install -y certbot python3-certbot-nginx

# Get SSL certificate (replace with your domain)
sudo certbot --nginx -d yourdomain.com -d www.yourdomain.com
```

---

## **🎉 You're Done!**

Your Juridence application is now live at:
- **HTTP:** `http://YOUR_DROPLET_IP`
- **HTTPS:** `https://yourdomain.com` (if SSL configured)

---

## **Useful Commands**

```bash
# Check service status
sudo systemctl status juridence-backend
sudo systemctl status nginx

# View logs
sudo journalctl -u juridence-backend -f
sudo tail -f /var/log/nginx/error.log

# Deploy updates
/home/juridence/deploy.sh

# Create backup
/home/juridence/backup.sh

# Restart services
sudo systemctl restart juridence-backend
sudo systemctl reload nginx
```

---

## **Troubleshooting**

### **Backend won't start?**
```bash
# Check logs
sudo journalctl -u juridence-backend -n 50

# Check .env file
cat backend/.env

# Test database connection
cd backend && source venv/bin/activate && python test_digitalocean_connection.py
```

### **Frontend not loading?**
```bash
# Check if build exists
ls -la build/

# Rebuild if needed
npm run build

# Check Nginx config
sudo nginx -t
```

### **Database connection issues?**
```bash
# Test connection manually
psql "postgresql://doadmin:YOUR_PASSWORD@YOUR_DB_HOST:25060/juridence?sslmode=require"

# Check firewall (in DigitalOcean dashboard)
# Ensure database allows connections from your droplet IP
```

---

## **Next Steps**

1. **Configure Domain DNS** (point to your droplet IP)
2. **Set up monitoring** (UptimeRobot, Pingdom)
3. **Configure backups** (automated daily backups)
4. **Set up error tracking** (Sentry)
5. **Implement CDN** (CloudFlare, DigitalOcean Spaces)

---

## **Cost Breakdown**

- **Droplet (2GB RAM):** $12/month
- **PostgreSQL Database:** $15/month
- **Domain:** $10-15/year
- **SSL Certificate:** Free (Let's Encrypt)
- **Total:** ~$27/month

---

**Need help?** Check the full deployment guide: `DIGITALOCEAN_DEPLOYMENT_GUIDE.md`
