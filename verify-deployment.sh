#!/bin/bash

echo "🔍 DennisLaw SVD - Deployment Verification"
echo "=========================================="

echo "📁 Checking build folder contents..."
if [ -d "build" ]; then
    echo "✅ Build folder exists"
    echo ""
    echo "📋 Files in build folder:"
    ls -la build/
    echo ""
    echo "📋 Files in build/static folder:"
    ls -la build/static/
    echo ""
    echo "📋 Files in build/static/css folder:"
    ls -la build/static/css/
    echo ""
    echo "📋 Files in build/static/js folder:"
    ls -la build/static/js/
    echo ""
    echo "📄 .htaccess content preview:"
    head -10 build/.htaccess
    echo ""
    echo "📄 index.html content preview:"
    head -10 build/index.html
else
    echo "❌ Build folder not found. Run 'npm run build' first."
    exit 1
fi

echo ""
echo "🎯 What to upload to Cloudways public_html:"
echo "==========================================="
echo "1. .htaccess (from build/.htaccess)"
echo "2. index.html (from build/index.html)"
echo "3. asset-manifest.json (from build/asset-manifest.json)"
echo "4. static/ folder (from build/static/)"
echo ""
echo "⚠️  IMPORTANT:"
echo "- Upload files DIRECTLY to public_html (not in a subfolder)"
echo "- Delete any default files (index.php, default.html, etc.)"
echo "- Make sure .htaccess file is uploaded"
echo ""
echo "🌐 After upload, your app should be available at:"
echo "https://your-domain.com or https://your-app.cloudwaysapps.com"
