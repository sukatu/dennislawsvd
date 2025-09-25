#!/bin/bash

# Deploy frontend and setup admin user on server
echo "🚀 Deploying frontend and setting up admin user..."

# Server details
SERVER="62.171.137.28"
SERVER_USER="root"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo -e "${YELLOW}📦 Uploading frontend build to server...${NC}"

# Upload the build folder to server
rsync -avz --delete build/ $SERVER_USER@$SERVER:/var/www/html/

if [ $? -eq 0 ]; then
    echo -e "${GREEN}✅ Frontend deployed successfully!${NC}"
else
    echo -e "${RED}❌ Frontend deployment failed!${NC}"
    exit 1
fi

echo -e "${YELLOW}🔧 Setting up admin user on server...${NC}"

# Create a script to run on the server
cat > setup_admin.sh << 'EOF'
#!/bin/bash

# Navigate to the backend directory
cd /var/www/juridence

# Activate virtual environment
source venv/bin/activate

# Create admin user script
cat > create_admin_user.py << 'PYEOF'
import sys
sys.path.append('/var/www/juridence')

from backend.database import get_db
from backend.models.user import User
from backend.auth import get_password_hash
from backend.models.user import UserRole, UserStatus

def create_admin_user():
    db = next(get_db())
    
    # Check if admin user already exists
    existing_admin = db.query(User).filter(User.username == "admin").first()
    if existing_admin:
        print("Admin user already exists!")
        print(f"Username: {existing_admin.username}")
        print(f"Email: {existing_admin.email}")
        print(f"Is Admin: {existing_admin.is_admin}")
        return existing_admin
    
    # Create new admin user
    hashed_password = get_password_hash("admin123")
    
    admin_user = User(
        username="admin",
        email="admin@juridence.com",
        first_name="Admin",
        last_name="User",
        hashed_password=hashed_password,
        is_admin=True,
        role=UserRole.ADMIN,
        status=UserStatus.ACTIVE,
        is_verified=True,
        is_active=True
    )
    
    db.add(admin_user)
    db.commit()
    db.refresh(admin_user)
    
    print("✅ Admin user created successfully!")
    print(f"Username: {admin_user.username}")
    print(f"Email: {admin_user.email}")
    print(f"Password: admin123")
    print(f"Is Admin: {admin_user.is_admin}")
    
    return admin_user

if __name__ == "__main__":
    create_admin_user()
PYEOF

# Run the admin user creation script
python create_admin_user.py

# Clean up
rm create_admin_user.py

# Restart the backend service
echo "🔄 Restarting backend service..."
pm2 restart juridence-backend

echo "✅ Setup complete!"
EOF

# Upload and run the setup script
scp setup_admin.sh $SERVER_USER@$SERVER:/tmp/
ssh $SERVER_USER@$SERVER "chmod +x /tmp/setup_admin.sh && /tmp/setup_admin.sh && rm /tmp/setup_admin.sh"

if [ $? -eq 0 ]; then
    echo -e "${GREEN}✅ Admin user setup completed successfully!${NC}"
else
    echo -e "${RED}❌ Admin user setup failed!${NC}"
    exit 1
fi

# Clean up local script
rm setup_admin.sh

echo -e "${GREEN}🎉 Deployment and setup completed successfully!${NC}"
echo -e "${YELLOW}📋 Summary:${NC}"
echo "• Frontend deployed to server"
echo "• Admin user created with credentials:"
echo "  - Username: admin"
echo "  - Password: admin123"
echo "• Backend service restarted"
echo ""
echo -e "${YELLOW}🔗 Test the login:${NC}"
echo "• Frontend: http://$SERVER"
echo "• Backend: http://$SERVER:8000/api/health"
echo "• Admin login should now work with username: admin, password: admin123"
