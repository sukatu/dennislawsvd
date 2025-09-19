#!/usr/bin/env python3
"""
Database seeding script to populate the database with initial data
"""

import os
import sys
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from passlib.context import CryptContext
from datetime import datetime, timedelta
import json

# Add current directory to path for imports
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from config import settings
from database import Base
from models.user import User, UserRole, UserStatus
from models.role import Role, Permission
from models.tenant import Tenant, SubscriptionPlan

def log(message):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"[{timestamp}] {message}")

def create_password_context():
    """Create password hashing context"""
    return CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_password(password: str) -> str:
    """Hash a password"""
    pwd_context = create_password_context()
    return pwd_context.hash(password)

def seed_database():
    """Seed the database with initial data"""
    log("🌱 Starting database seeding...")
    
    # Create database engine
    engine = create_engine(settings.database_url)
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    db = SessionLocal()
    
    try:
        # 1. Create default roles
        log("👥 Creating default roles...")
        
        # Check if roles already exist
        existing_roles = db.query(Role).count()
        if existing_roles == 0:
            roles_data = [
                {"name": "super_admin", "display_name": "Super Admin", "description": "Full system access", "is_active": True, "is_system_role": True},
                {"name": "admin", "display_name": "Admin", "description": "Administrative access", "is_active": True, "is_system_role": True},
                {"name": "user", "display_name": "User", "description": "Regular user access", "is_active": True, "is_system_role": True},
                {"name": "premium_user", "display_name": "Premium User", "description": "Premium user with extended features", "is_active": True, "is_system_role": False},
            ]
            
            for role_data in roles_data:
                role = Role(**role_data)
                db.add(role)
            
            db.commit()
            log("✅ Created default roles")
        else:
            log("ℹ️ Roles already exist, skipping...")
        
        # 2. Create default permissions
        log("🔐 Creating default permissions...")
        
        existing_permissions = db.query(Permission).count()
        if existing_permissions == 0:
            permissions_data = [
                {"name": "user_read", "display_name": "Read User Data", "description": "Read user data", "category": "users", "resource": "user", "action": "read", "is_system_permission": True},
                {"name": "user_write", "display_name": "Write User Data", "description": "Create/update user data", "category": "users", "resource": "user", "action": "write", "is_system_permission": True},
                {"name": "user_delete", "display_name": "Delete User Data", "description": "Delete user data", "category": "users", "resource": "user", "action": "delete", "is_system_permission": True},
                {"name": "case_read", "display_name": "Read Case Data", "description": "Read case data", "category": "cases", "resource": "case", "action": "read", "is_system_permission": True},
                {"name": "case_write", "display_name": "Write Case Data", "description": "Create/update case data", "category": "cases", "resource": "case", "action": "write", "is_system_permission": True},
                {"name": "case_delete", "display_name": "Delete Case Data", "description": "Delete case data", "category": "cases", "resource": "case", "action": "delete", "is_system_permission": True},
                {"name": "admin_access", "display_name": "Admin Access", "description": "Administrative access", "category": "admin", "resource": "system", "action": "admin", "is_system_permission": True},
                {"name": "premium_features", "display_name": "Premium Features", "description": "Access to premium features", "category": "features", "resource": "premium", "action": "access", "is_system_permission": False},
            ]
            
            for perm_data in permissions_data:
                permission = Permission(**perm_data)
                db.add(permission)
            
            db.commit()
            log("✅ Created default permissions")
        else:
            log("ℹ️ Permissions already exist, skipping...")
        
        # 3. Create default tenant
        log("🏢 Creating default tenant...")
        
        existing_tenant = db.query(Tenant).filter(Tenant.slug == "default").first()
        if not existing_tenant:
            tenant_data = {
                "name": "Default Tenant",
                "slug": "default",
                "description": "Default system tenant",
                "primary_color": "#2563eb",
                "secondary_color": "#1d4ed8",
                "accent_color": "#3b82f6",
                "font_family": "Inter",
                "app_name": "Juridence",
                "app_tagline": "Legal Intelligence Platform",
                "subscription_status": "active",
                "max_users": 1000,
                "max_cases_per_month": 10000,
                "max_storage_gb": 100.0,
                "features_enabled": json.dumps([
                    "case_search", "user_management", "analytics", 
                    "notifications", "api_access", "premium_features"
                ]),
                "is_active": True,
                "is_approved": True,
                "is_verified": True,
            }
            
            tenant = Tenant(**tenant_data)
            db.add(tenant)
            db.commit()
            log("✅ Created default tenant")
        else:
            log("ℹ️ Default tenant already exists, skipping...")
        
        # 4. Create subscription plans
        log("💳 Creating subscription plans...")
        
        existing_plans = db.query(SubscriptionPlan).count()
        if existing_plans == 0:
            plans_data = [
                {
                    "name": "Free",
                    "description": "Basic features for individual users",
                    "slug": "free",
                    "price_monthly": 0.0,
                    "price_yearly": 0.0,
                    "currency": "USD",
                    "max_users": 1,
                    "max_cases_per_month": 100,
                    "max_storage_gb": 1.0,
                    "features": json.dumps(["case_search", "basic_analytics"]),
                    "is_active": True,
                    "is_popular": False,
                    "sort_order": 1,
                },
                {
                    "name": "Professional",
                    "description": "Advanced features for professionals",
                    "slug": "professional",
                    "price_monthly": 29.99,
                    "price_yearly": 299.99,
                    "currency": "USD",
                    "max_users": 5,
                    "max_cases_per_month": 1000,
                    "max_storage_gb": 10.0,
                    "features": json.dumps([
                        "case_search", "advanced_analytics", "notifications", 
                        "api_access", "priority_support"
                    ]),
                    "is_active": True,
                    "is_popular": True,
                    "sort_order": 2,
                },
                {
                    "name": "Enterprise",
                    "description": "Full features for organizations",
                    "slug": "enterprise",
                    "price_monthly": 99.99,
                    "price_yearly": 999.99,
                    "currency": "USD",
                    "max_users": 100,
                    "max_cases_per_month": 10000,
                    "max_storage_gb": 100.0,
                    "features": json.dumps([
                        "case_search", "advanced_analytics", "notifications", 
                        "api_access", "priority_support", "custom_branding", 
                        "sso", "audit_logs"
                    ]),
                    "is_active": True,
                    "is_popular": False,
                    "sort_order": 3,
                },
            ]
            
            for plan_data in plans_data:
                plan = SubscriptionPlan(**plan_data)
                db.add(plan)
            
            db.commit()
            log("✅ Created subscription plans")
        else:
            log("ℹ️ Subscription plans already exist, skipping...")
        
        # 5. Create admin user
        log("👤 Creating admin user...")
        
        existing_admin = db.query(User).filter(User.email == "admin@juridence.com").first()
        if not existing_admin:
            # Get the default tenant
            default_tenant = db.query(Tenant).filter(Tenant.slug == "default").first()
            
            admin_data = {
                "email": "admin@juridence.com",
                "username": "admin",
                "first_name": "System",
                "last_name": "Administrator",
                "hashed_password": hash_password("admin123"),  # Default password
                "is_verified": True,
                "role": UserRole.ADMIN,
                "status": UserStatus.ACTIVE,
                "is_admin": True,
                "tenant_id": default_tenant.id if default_tenant else None,
                "is_tenant_admin": True,
                "organization": "Juridence",
                "job_title": "System Administrator",
                "email_notifications": True,
                "sms_notifications": False,
                "language": "en",
                "timezone": "UTC",
                "is_premium": True,
                "failed_login_attempts": 0,
            }
            
            admin_user = User(**admin_data)
            db.add(admin_user)
            db.commit()
            log("✅ Created admin user (admin@juridence.com / admin123)")
        else:
            log("ℹ️ Admin user already exists, skipping...")
        
        # 6. Create test user
        log("🧪 Creating test user...")
        
        existing_test_user = db.query(User).filter(User.email == "test@juridence.com").first()
        if not existing_test_user:
            # Get the default tenant
            default_tenant = db.query(Tenant).filter(Tenant.slug == "default").first()
            
            test_user_data = {
                "email": "test@juridence.com",
                "username": "testuser",
                "first_name": "Test",
                "last_name": "User",
                "hashed_password": hash_password("test123"),  # Default password
                "is_verified": True,
                "role": UserRole.USER,
                "status": UserStatus.ACTIVE,
                "is_admin": False,
                "tenant_id": default_tenant.id if default_tenant else None,
                "is_tenant_admin": False,
                "organization": "Test Organization",
                "job_title": "Legal Researcher",
                "email_notifications": True,
                "sms_notifications": False,
                "language": "en",
                "timezone": "UTC",
                "is_premium": False,
                "failed_login_attempts": 0,
            }
            
            test_user = User(**test_user_data)
            db.add(test_user)
            db.commit()
            log("✅ Created test user (test@juridence.com / test123)")
        else:
            log("ℹ️ Test user already exists, skipping...")
        
        log("🎉 Database seeding completed successfully!")
        
        # Show summary
        user_count = db.query(User).count()
        role_count = db.query(Role).count()
        permission_count = db.query(Permission).count()
        tenant_count = db.query(Tenant).count()
        plan_count = db.query(SubscriptionPlan).count()
        
        print(f"\n📊 Database Summary:")
        print(f"  👥 Users: {user_count}")
        print(f"  👤 Roles: {role_count}")
        print(f"  🔐 Permissions: {permission_count}")
        print(f"  🏢 Tenants: {tenant_count}")
        print(f"  💳 Subscription Plans: {plan_count}")
        
        print(f"\n🔑 Login Credentials:")
        print(f"  Admin: admin@juridence.com / admin123")
        print(f"  Test User: test@juridence.com / test123")
        
    except Exception as e:
        log(f"❌ Error during seeding: {e}")
        db.rollback()
        raise
    finally:
        db.close()

if __name__ == "__main__":
    seed_database()
