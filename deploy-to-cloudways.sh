#!/bin/bash

# DennisLaw SVD - Cloudways Deployment Script
# This script helps prepare and deploy your React app to Cloudways

echo "🚀 DennisLaw SVD - Cloudways Deployment Helper"
echo "=============================================="

# Check if build folder exists
if [ ! -d "build" ]; then
    echo "❌ Build folder not found. Running npm run build..."
    npm run build
    if [ $? -ne 0 ]; then
        echo "❌ Build failed. Please fix errors and try again."
        exit 1
    fi
fi

echo "✅ Build folder found"

# Create deployment package
echo "📦 Creating deployment package..."
cd build
tar -czf ../dennislaw-svd-deployment.tar.gz .
cd ..

echo "✅ Deployment package created: dennislaw-svd-deployment.tar.gz"

# Display file sizes
echo ""
echo "📊 Build Statistics:"
echo "==================="
du -sh build/
echo ""
echo "📁 Files to upload:"
ls -la build/

echo ""
echo "🎯 Next Steps:"
echo "============="
echo "1. Log into your Cloudways account"
echo "2. Go to your application"
echo "3. Open File Manager"
echo "4. Navigate to public_html folder"
echo "5. Upload all files from the 'build' folder"
echo "6. Or extract dennislaw-svd-deployment.tar.gz in public_html"
echo ""
echo "📖 For detailed instructions, see: CLOUDWAYS_DEPLOYMENT.md"
echo ""
echo "🌐 Your app will be available at: https://your-domain.com"
echo ""
echo "✨ Deployment package ready!"
