#!/usr/bin/env python3
"""
Script to create admin user on the server
"""
import sys
import os

# Add the backend path
sys.path.append('/var/www/juridence')

from backend.database import get_db
from backend.models.user import User, UserRole, UserStatus
from backend.auth import get_password_hash

def create_admin_user():
    """Create admin user if it doesn't exist"""
    db = next(get_db())
    
    try:
        # Check if admin user already exists
        existing_admin = db.query(User).filter(User.username == "admin").first()
        if existing_admin:
            print("✅ Admin user already exists!")
            print(f"Username: {existing_admin.username}")
            print(f"Email: {existing_admin.email}")
            print(f"Is Admin: {existing_admin.is_admin}")
            print(f"Status: {existing_admin.status}")
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
            is_verified=True
        )
        
        db.add(admin_user)
        db.commit()
        db.refresh(admin_user)
        
        print("✅ Admin user created successfully!")
        print(f"Username: {admin_user.username}")
        print(f"Email: {admin_user.email}")
        print(f"Password: admin123")
        print(f"Is Admin: {admin_user.is_admin}")
        print(f"Status: {admin_user.status}")
        
        return admin_user
        
    except Exception as e:
        print(f"❌ Error creating admin user: {e}")
        db.rollback()
        return None

def test_admin_login():
    """Test admin login credentials"""
    from backend.auth import authenticate_user
    from backend.database import get_db
    
    db = next(get_db())
    
    try:
        # Test with username
        user = authenticate_user(db, "admin", "admin123")
        if user:
            print("✅ Admin login test successful with username!")
            print(f"User: {user.username}, Email: {user.email}, Is Admin: {user.is_admin}")
            return True
        else:
            print("❌ Admin login test failed with username")
            return False
    except Exception as e:
        print(f"❌ Error testing admin login: {e}")
        return False

if __name__ == "__main__":
    print("🔧 Creating admin user...")
    admin_user = create_admin_user()
    
    if admin_user:
        print("\n🧪 Testing admin login...")
        test_admin_login()
        
        print("\n📋 Admin credentials:")
        print("Username: admin")
        print("Password: admin123")
        print("Email: admin@juridence.com")
    else:
        print("❌ Failed to create admin user")
