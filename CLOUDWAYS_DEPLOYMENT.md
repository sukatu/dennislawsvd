# Cloudways Deployment Guide for DennisLaw SVD

## 🚀 Quick Deployment Steps

### 1. Prepare Your Cloudways Server
- Log into your Cloudways account
- Create a new application or use an existing one
- Choose **PHP** as the application type (even though this is a React app, we'll serve it as static files)
- Select your preferred server and location

### 2. Upload Files to Cloudways
You need to upload the contents of the `build` folder to your Cloudways server.

#### Option A: Using Cloudways File Manager
1. Log into your Cloudways platform
2. Go to your application
3. Click on "File Manager" or "Application Management" → "File Manager"
4. Navigate to `public_html` folder
5. Upload all files from the `build` folder to `public_html`

#### Option B: Using FTP/SFTP
1. Get your FTP credentials from Cloudways:
   - Go to your application
   - Click on "Application Management" → "Access Details"
   - Note down FTP/SFTP credentials
2. Use an FTP client (FileZilla, WinSCP, etc.)
3. Connect to your server
4. Navigate to `public_html` folder
5. Upload all files from the `build` folder

#### Option C: Using Git (Recommended)
1. Initialize a git repository in your project:
   ```bash
   git init
   git add .
   git commit -m "Initial commit"
   ```
2. Push to GitHub/GitLab
3. In Cloudways, go to "Application Management" → "Git"
4. Connect your repository
5. Set deployment path to `public_html`

### 3. Configure Domain (Optional)
- If you have a custom domain, point it to your Cloudways server
- Update DNS settings with your domain provider
- Add the domain in Cloudways under "Domain Management"

### 4. SSL Certificate
- Go to "Application Management" → "SSL Certificate"
- Enable "Let's Encrypt" for free SSL
- Or upload your own SSL certificate

## 📁 Files to Upload

Upload these files from the `build` folder to your `public_html` directory:

```
public_html/
├── .htaccess          (for routing and optimization)
├── index.html         (main HTML file)
├── asset-manifest.json
└── static/
    ├── css/
    │   ├── main.b45eee49.css
    │   └── main.b45eee49.css.map
    └── js/
        ├── main.b56b267d.js
        ├── main.b56b267d.js.LICENSE.txt
        └── main.b56b267d.js.map
```

## 🔧 Important Configuration

### .htaccess File
The `.htaccess` file is already included in the build folder and handles:
- Client-side routing (React Router)
- Gzip compression
- Cache headers for better performance
- Security headers

### Environment Variables
If you need to add environment variables later:
1. Create a `.env` file in your project root
2. Add your variables (e.g., `REACT_APP_API_URL=https://your-api.com`)
3. Rebuild the project: `npm run build`
4. Upload the new build files

## 🚨 Troubleshooting

### Common Issues:

1. **404 Error on Page Refresh**
   - Ensure `.htaccess` file is uploaded
   - Check that mod_rewrite is enabled on your server

2. **CSS/JS Files Not Loading**
   - Check file permissions (should be 644 for files, 755 for directories)
   - Verify all files in `static` folder are uploaded

3. **Slow Loading**
   - Enable Gzip compression in Cloudways
   - Check that cache headers are working

4. **SSL Issues**
   - Ensure SSL certificate is properly configured
   - Check for mixed content warnings

## 📊 Performance Optimization

### Cloudways Settings:
1. **Enable Redis** (if available)
2. **Enable Varnish** (if available)
3. **Enable CDN** (Cloudways CDN or Cloudflare)

### Additional Optimizations:
1. **Image Optimization**: Compress images before upload
2. **Code Splitting**: Already implemented in React build
3. **Lazy Loading**: Already implemented in React components

## 🔄 Updates and Maintenance

### To Update Your App:
1. Make changes to your React code
2. Run `npm run build` locally
3. Upload new files from `build` folder to `public_html`
4. Clear any caches (Varnish, CDN)

### Automated Deployment (Advanced):
Consider setting up automated deployment using:
- GitHub Actions
- Cloudways Git integration
- CI/CD pipelines

## 📞 Support

If you encounter issues:
1. Check Cloudways documentation
2. Contact Cloudways support
3. Review server logs in Cloudways dashboard

## 🎯 Post-Deployment Checklist

- [ ] All files uploaded to `public_html`
- [ ] `.htaccess` file is present
- [ ] SSL certificate is active
- [ ] Domain is properly configured
- [ ] All pages are accessible
- [ ] Search functionality works
- [ ] Navigation works correctly
- [ ] Mobile responsiveness is working
- [ ] Performance is acceptable

---

**Your DennisLaw SVD application should now be live on Cloudways! 🎉**
