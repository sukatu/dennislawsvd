# Deployment to Production Server

## 🚀 Quick Deployment Guide

### ✅ Changes Already Completed
- All code changes have been committed to the `main` branch
- Frontend build completed successfully
- AI Chat Assistant added to Documentation page
- All features tested locally

### 📋 Option 1: Automated Deployment (Recommended)

Run the deployment script:

```bash
./deploy_to_server.sh
```

**Note:** You'll need SSH access to the server. Enter the password when prompted.

---

### 📋 Option 2: Manual Deployment

If the automated script doesn't work, follow these manual steps:

#### Step 1: SSH into the Server

```bash
ssh root@62.171.137.28
```

#### Step 2: Navigate to Project Directory

```bash
cd /var/www/juridence
```

#### Step 3: Pull Latest Changes

```bash
git pull origin main
```

#### Step 4: Update Backend Dependencies

```bash
cd backend
source venv/bin/activate
pip install -r requirements.txt
```

#### Step 5: Restart Backend Service

```bash
pm2 restart juridence-backend
```

#### Step 6: Build and Deploy Frontend

```bash
cd /var/www/juridence
npm install
npm run build
```

#### Step 7: Restart Frontend Service

```bash
pm2 restart juridence-frontend
```

#### Step 8: Verify Deployment

```bash
pm2 status
pm2 logs
```

---

### 📋 Option 3: Direct Git Pull on Server

The simplest approach since all changes are already pushed to GitHub:

```bash
# SSH into server
ssh root@62.171.137.28

# Pull latest changes
cd /var/www/juridence && git pull origin main

# Restart services
pm2 restart all

# Verify
pm2 status
```

---

## 🔍 Verify Deployment

After deployment, verify that:

1. **Website is accessible**: http://62.171.137.28
2. **AI Chat button appears**: Navigate to Admin Dashboard > Documentation
3. **Services are running**: Check `pm2 status` shows both services as "online"

---

## 🆕 New Features Deployed

### AI Chat Assistant in Documentation
- Floating AI assistant button in bottom-right corner
- Gradient blue-purple button with MessageCircle icon
- Accessible from the Admin Dashboard Documentation page
- Helps users navigate and understand system documentation

---

## 🐛 Troubleshooting

### If services are not running:

```bash
# Restart all services
pm2 restart all

# Check logs for errors
pm2 logs

# Restart individual services
pm2 restart juridence-backend
pm2 restart juridence-frontend
```

### If changes don't appear:

```bash
# Hard refresh the browser (Ctrl+F5 or Cmd+Shift+R)
# Or clear browser cache

# Force rebuild on server
cd /var/www/juridence
npm run build
pm2 restart juridence-frontend
```

### If git pull fails:

```bash
# Stash any local changes
git stash

# Pull latest changes
git pull origin main

# If needed, apply stashed changes
git stash pop
```

---

## 📊 Service Management Commands

```bash
# View all services
pm2 status

# View logs
pm2 logs

# View specific service logs
pm2 logs juridence-backend
pm2 logs juridence-frontend

# Restart a specific service
pm2 restart juridence-backend

# Stop a service
pm2 stop juridence-backend

# Start a service
pm2 start juridence-backend

# Restart all services
pm2 restart all

# Save PM2 configuration
pm2 save

# Show detailed info
pm2 show juridence-backend
```

---

## 🔒 Security Notes

- Always use SSH keys for production deployments
- Keep server credentials secure
- Regularly update server packages: `apt update && apt upgrade`
- Monitor logs for any security issues: `pm2 logs`

---

## 📝 Deployment Checklist

- [x] Code changes committed to Git
- [x] Changes pushed to GitHub main branch
- [x] Frontend built successfully
- [ ] SSH into production server
- [ ] Pull latest changes from Git
- [ ] Install/update dependencies
- [ ] Restart backend service
- [ ] Build frontend on server
- [ ] Restart frontend service
- [ ] Verify services are running
- [ ] Test in browser
- [ ] Check AI Chat functionality

---

## 🎉 Success!

Once deployed, your users will have access to the new AI Chat Assistant feature in the documentation page!

**Server URL:** http://62.171.137.28

**Admin Dashboard:** http://62.171.137.28/admin/dashboard

**Documentation:** http://62.171.137.28/admin/dashboard (Navigate to Documentation tab)

