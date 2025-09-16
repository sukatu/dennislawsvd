#!/usr/bin/env python3
"""
Script to create an admin user for testing the admin dashboard
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models.user import User, UserRole, UserStatus
from config import settings
import bcrypt

def create_admin_user():
    """Create an admin user for testing"""
    try:
        # Create engine
        engine = create_engine(settings.database_url)
        SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
        db = SessionLocal()
        
        # Check if admin user already exists
        existing_admin = db.query(User).filter(User.email == "admin@dennislaw.com").first()
        if existing_admin:
            print("Admin user already exists!")
            print(f"Email: {existing_admin.email}")
            print(f"Role: {existing_admin.role}")
            print(f"Admin: {existing_admin.is_admin}")
            return
        
        # Create admin user
        hashed_password = bcrypt.hashpw("admin123".encode('utf-8'), bcrypt.gensalt())
        
        admin_user = User(
            email="admin@dennislaw.com",
            first_name="Admin",
            last_name="User",
            hashed_password=hashed_password.decode('utf-8'),
            role=UserRole.ADMIN,
            status=UserStatus.ACTIVE,
            is_admin=True,
            is_verified=True
        )
        
        db.add(admin_user)
        db.commit()
        db.refresh(admin_user)
        
        print("Admin user created successfully!")
        print(f"Email: {admin_user.email}")
        print(f"Password: admin123")
        print(f"Role: {admin_user.role}")
        print(f"Admin: {admin_user.is_admin}")
        
    except Exception as e:
        print(f"Error creating admin user: {e}")
        return False
    
    finally:
        db.close()
    
    return True

if __name__ == "__main__":
    create_admin_user()
