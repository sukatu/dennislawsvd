#!/usr/bin/env python3
"""
Script to create default roles and permissions for the application
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from sqlalchemy.orm import Session
from database import SessionLocal, engine
from models.role import Role, Permission, UserRole
from models.user import User
from datetime import datetime

def create_default_permissions(db: Session):
    """Create default permissions"""
    print("Creating default permissions...")
    
    permissions_data = [
        # User Management
        {"name": "users.create", "display_name": "Create Users", "description": "Create new user accounts", "category": "users", "resource": "user", "action": "create", "is_system_permission": True},
        {"name": "users.read", "display_name": "View Users", "description": "View user information", "category": "users", "resource": "user", "action": "read", "is_system_permission": True},
        {"name": "users.update", "display_name": "Update Users", "description": "Update user information", "category": "users", "resource": "user", "action": "update", "is_system_permission": True},
        {"name": "users.delete", "display_name": "Delete Users", "description": "Delete user accounts", "category": "users", "resource": "user", "action": "delete", "is_system_permission": True},
        
        # Case Management
        {"name": "cases.create", "display_name": "Create Cases", "description": "Create new case records", "category": "cases", "resource": "case", "action": "create", "is_system_permission": True},
        {"name": "cases.read", "display_name": "View Cases", "description": "View case information", "category": "cases", "resource": "case", "action": "read", "is_system_permission": True},
        {"name": "cases.update", "display_name": "Update Cases", "description": "Update case information", "category": "cases", "resource": "case", "action": "update", "is_system_permission": True},
        {"name": "cases.delete", "display_name": "Delete Cases", "description": "Delete case records", "category": "cases", "resource": "case", "action": "delete", "is_system_permission": True},
        {"name": "cases.process", "display_name": "Process Cases", "description": "Process case metadata and analytics", "category": "cases", "resource": "case", "action": "process", "is_system_permission": True},
        
        # People Management
        {"name": "people.create", "display_name": "Create People", "description": "Create new people records", "category": "people", "resource": "person", "action": "create", "is_system_permission": True},
        {"name": "people.read", "display_name": "View People", "description": "View people information", "category": "people", "resource": "person", "action": "read", "is_system_permission": True},
        {"name": "people.update", "display_name": "Update People", "description": "Update people information", "category": "people", "resource": "person", "action": "update", "is_system_permission": True},
        {"name": "people.delete", "display_name": "Delete People", "description": "Delete people records", "category": "people", "resource": "person", "action": "delete", "is_system_permission": True},
        
        # Bank Management
        {"name": "banks.create", "display_name": "Create Banks", "description": "Create new bank records", "category": "banks", "resource": "bank", "action": "create", "is_system_permission": True},
        {"name": "banks.read", "display_name": "View Banks", "description": "View bank information", "category": "banks", "resource": "bank", "action": "read", "is_system_permission": True},
        {"name": "banks.update", "display_name": "Update Banks", "description": "Update bank information", "category": "banks", "resource": "bank", "action": "update", "is_system_permission": True},
        {"name": "banks.delete", "display_name": "Delete Banks", "description": "Delete bank records", "category": "banks", "resource": "bank", "action": "delete", "is_system_permission": True},
        
        # Insurance Management
        {"name": "insurance.create", "display_name": "Create Insurance", "description": "Create new insurance records", "category": "insurance", "resource": "insurance", "action": "create", "is_system_permission": True},
        {"name": "insurance.read", "display_name": "View Insurance", "description": "View insurance information", "category": "insurance", "resource": "insurance", "action": "read", "is_system_permission": True},
        {"name": "insurance.update", "display_name": "Update Insurance", "description": "Update insurance information", "category": "insurance", "resource": "insurance", "action": "update", "is_system_permission": True},
        {"name": "insurance.delete", "display_name": "Delete Insurance", "description": "Delete insurance records", "category": "insurance", "resource": "insurance", "action": "delete", "is_system_permission": True},
        
        # Company Management
        {"name": "companies.create", "display_name": "Create Companies", "description": "Create new company records", "category": "companies", "resource": "company", "action": "create", "is_system_permission": True},
        {"name": "companies.read", "display_name": "View Companies", "description": "View company information", "category": "companies", "resource": "company", "action": "read", "is_system_permission": True},
        {"name": "companies.update", "display_name": "Update Companies", "description": "Update company information", "category": "companies", "resource": "company", "action": "update", "is_system_permission": True},
        {"name": "companies.delete", "display_name": "Delete Companies", "description": "Delete company records", "category": "companies", "resource": "company", "action": "delete", "is_system_permission": True},
        
        # Payment Management
        {"name": "payments.create", "display_name": "Create Payments", "description": "Create new payment records", "category": "payments", "resource": "payment", "action": "create", "is_system_permission": True},
        {"name": "payments.read", "display_name": "View Payments", "description": "View payment information", "category": "payments", "resource": "payment", "action": "read", "is_system_permission": True},
        {"name": "payments.update", "display_name": "Update Payments", "description": "Update payment information", "category": "payments", "resource": "payment", "action": "update", "is_system_permission": True},
        {"name": "payments.delete", "display_name": "Delete Payments", "description": "Delete payment records", "category": "payments", "resource": "payment", "action": "delete", "is_system_permission": True},
        
        # Admin Management
        {"name": "admin.dashboard", "display_name": "Access Admin Dashboard", "description": "Access the admin dashboard", "category": "admin", "resource": "dashboard", "action": "read", "is_system_permission": True},
        {"name": "admin.settings", "display_name": "Manage Settings", "description": "Manage system settings", "category": "admin", "resource": "settings", "action": "manage", "is_system_permission": True},
        {"name": "admin.roles", "display_name": "Manage Roles", "description": "Manage user roles and permissions", "category": "admin", "resource": "roles", "action": "manage", "is_system_permission": True},
        {"name": "admin.api_keys", "display_name": "Manage API Keys", "description": "Manage API keys", "category": "admin", "resource": "api_keys", "action": "manage", "is_system_permission": True},
        {"name": "admin.analytics", "display_name": "View Analytics", "description": "View system analytics and reports", "category": "admin", "resource": "analytics", "action": "read", "is_system_permission": True},
        
        # Reports
        {"name": "reports.generate", "display_name": "Generate Reports", "description": "Generate system reports", "category": "reports", "resource": "report", "action": "create", "is_system_permission": True},
        {"name": "reports.export", "display_name": "Export Data", "description": "Export system data", "category": "reports", "resource": "data", "action": "export", "is_system_permission": True},
    ]
    
    created_permissions = []
    for perm_data in permissions_data:
        existing = db.query(Permission).filter(Permission.name == perm_data["name"]).first()
        if not existing:
            permission = Permission(**perm_data)
            db.add(permission)
            created_permissions.append(permission)
        else:
            created_permissions.append(existing)
    
    db.commit()
    print(f"Created/verified {len(created_permissions)} permissions")
    return created_permissions

def create_default_roles(db: Session, permissions: list):
    """Create default roles"""
    print("Creating default roles...")
    
    # Get permission IDs by name
    permission_map = {p.name: p.id for p in permissions}
    
    roles_data = [
        {
            "name": "super_admin",
            "display_name": "Super Administrator",
            "description": "Full system access with all permissions",
            "is_system_role": True,
            "permissions": list(permission_map.values())  # All permissions
        },
        {
            "name": "admin",
            "display_name": "Administrator",
            "description": "Administrative access to most system functions",
            "is_system_role": True,
            "permissions": [
                permission_map["users.read"],
                permission_map["users.update"],
                permission_map["cases.read"],
                permission_map["cases.update"],
                permission_map["people.read"],
                permission_map["people.update"],
                permission_map["banks.read"],
                permission_map["banks.update"],
                permission_map["insurance.read"],
                permission_map["insurance.update"],
                permission_map["companies.read"],
                permission_map["companies.update"],
                permission_map["payments.read"],
                permission_map["admin.dashboard"],
                permission_map["admin.analytics"],
                permission_map["reports.generate"],
                permission_map["reports.export"]
            ]
        },
        {
            "name": "moderator",
            "display_name": "Moderator",
            "description": "Moderate access to view and update content",
            "is_system_role": True,
            "permissions": [
                permission_map["users.read"],
                permission_map["cases.read"],
                permission_map["cases.update"],
                permission_map["people.read"],
                permission_map["people.update"],
                permission_map["banks.read"],
                permission_map["insurance.read"],
                permission_map["companies.read"],
                permission_map["admin.dashboard"],
                permission_map["reports.generate"]
            ]
        },
        {
            "name": "viewer",
            "display_name": "Viewer",
            "description": "Read-only access to view content",
            "is_system_role": True,
            "permissions": [
                permission_map["users.read"],
                permission_map["cases.read"],
                permission_map["people.read"],
                permission_map["banks.read"],
                permission_map["insurance.read"],
                permission_map["companies.read"],
                permission_map["admin.dashboard"]
            ]
        },
        {
            "name": "user",
            "display_name": "Regular User",
            "description": "Basic user access",
            "is_system_role": True,
            "permissions": [
                permission_map["cases.read"],
                permission_map["people.read"],
                permission_map["banks.read"],
                permission_map["insurance.read"],
                permission_map["companies.read"]
            ]
        }
    ]
    
    created_roles = []
    for role_data in roles_data:
        existing = db.query(Role).filter(Role.name == role_data["name"]).first()
        if not existing:
            role = Role(**role_data)
            db.add(role)
            created_roles.append(role)
        else:
            # Update existing role with new permissions
            existing.permissions = role_data["permissions"]
            created_roles.append(existing)
    
    db.commit()
    print(f"Created/verified {len(created_roles)} roles")
    return created_roles

def assign_admin_role(db: Session, roles: list):
    """Assign super_admin role to existing admin users"""
    print("Assigning admin roles to existing users...")
    
    super_admin_role = next((r for r in roles if r.name == "super_admin"), None)
    if not super_admin_role:
        print("Super admin role not found!")
        return
    
    # Find users with admin privileges
    admin_users = db.query(User).filter(
        (User.role == 'admin') | (User.is_admin == True)
    ).all()
    
    assigned_count = 0
    for user in admin_users:
        # Check if user already has this role
        existing_assignment = db.query(UserRole).filter(
            UserRole.user_id == user.id,
            UserRole.role_id == super_admin_role.id
        ).first()
        
        if not existing_assignment:
            user_role = UserRole(
                user_id=user.id,
                role_id=super_admin_role.id,
                is_active=True,
                notes="Auto-assigned during setup"
            )
            db.add(user_role)
            assigned_count += 1
    
    db.commit()
    print(f"Assigned super admin role to {assigned_count} users")

def main():
    """Main function to create default roles and permissions"""
    print("Creating default roles and permissions...")
    
    # Create database session
    db = SessionLocal()
    
    try:
        # Create permissions
        permissions = create_default_permissions(db)
        
        # Create roles
        roles = create_default_roles(db, permissions)
        
        # Assign admin roles
        assign_admin_role(db, roles)
        
        print("\n✅ Default roles and permissions created successfully!")
        print(f"📊 Created {len(permissions)} permissions")
        print(f"👥 Created {len(roles)} roles")
        
        # Print role summary
        print("\n📋 Role Summary:")
        for role in roles:
            permission_count = len(role.permissions) if role.permissions else 0
            print(f"  • {role.display_name} ({role.name}): {permission_count} permissions")
        
    except Exception as e:
        print(f"❌ Error creating roles and permissions: {str(e)}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    main()
