#!/usr/bin/env python3
"""
Script to create common settings for the application
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from sqlalchemy.orm import Session
from database import get_db
from models.settings import Settings
from datetime import datetime

def create_common_settings():
    """Create common settings for the application"""
    try:
        # Get database session
        db = next(get_db())
        
        # Common settings to create
        common_settings = [
            # AI Settings
            {
                "key": "openai_api_key",
                "category": "ai",
                "value": "",
                "value_type": "string",
                "description": "OpenAI API key for AI-powered features",
                "is_public": False,
                "is_editable": True,
                "is_required": True,
                "validation_rules": {"pattern": "^sk-[a-zA-Z0-9]{20,}$", "min_length": 20},
                "default_value": ""
            },
            {
                "key": "ai_model",
                "category": "ai",
                "value": "gpt-3.5-turbo",
                "value_type": "string",
                "description": "Default AI model to use for text generation",
                "is_public": True,
                "is_editable": True,
                "is_required": False,
                "validation_rules": {"enum": ["gpt-3.5-turbo", "gpt-4", "gpt-4-turbo"]},
                "default_value": "gpt-3.5-turbo"
            },
            {
                "key": "ai_max_tokens",
                "category": "ai",
                "value": "2000",
                "value_type": "number",
                "description": "Maximum tokens for AI responses",
                "is_public": True,
                "is_editable": True,
                "is_required": False,
                "validation_rules": {"min": 100, "max": 4000},
                "default_value": "2000"
            },
            
            # Email Settings
            {
                "key": "smtp_host",
                "category": "email",
                "value": "",
                "value_type": "string",
                "description": "SMTP server host for sending emails",
                "is_public": False,
                "is_editable": True,
                "is_required": False,
                "validation_rules": {},
                "default_value": ""
            },
            {
                "key": "smtp_port",
                "category": "email",
                "value": "587",
                "value_type": "number",
                "description": "SMTP server port",
                "is_public": False,
                "is_editable": True,
                "is_required": False,
                "validation_rules": {"min": 1, "max": 65535},
                "default_value": "587"
            },
            {
                "key": "smtp_username",
                "category": "email",
                "value": "",
                "value_type": "string",
                "description": "SMTP username for authentication",
                "is_public": False,
                "is_editable": True,
                "is_required": False,
                "validation_rules": {},
                "default_value": ""
            },
            {
                "key": "smtp_password",
                "category": "email",
                "value": "",
                "value_type": "string",
                "description": "SMTP password for authentication",
                "is_public": False,
                "is_editable": True,
                "is_required": False,
                "validation_rules": {},
                "default_value": ""
            },
            {
                "key": "from_email",
                "category": "email",
                "value": "noreply@dennislaw.com",
                "value_type": "string",
                "description": "Default from email address",
                "is_public": True,
                "is_editable": True,
                "is_required": False,
                "validation_rules": {"pattern": "^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\\.[a-zA-Z]{2,}$"},
                "default_value": "noreply@dennislaw.com"
            },
            
            # Payment Settings
            {
                "key": "stripe_secret_key",
                "category": "payment",
                "value": "",
                "value_type": "string",
                "description": "Stripe secret key for payment processing",
                "is_public": False,
                "is_editable": True,
                "is_required": False,
                "validation_rules": {"pattern": "^sk_test_|^sk_live_"},
                "default_value": ""
            },
            {
                "key": "stripe_publishable_key",
                "category": "payment",
                "value": "",
                "value_type": "string",
                "description": "Stripe publishable key for frontend",
                "is_public": True,
                "is_editable": True,
                "is_required": False,
                "validation_rules": {"pattern": "^pk_test_|^pk_live_"},
                "default_value": ""
            },
            {
                "key": "currency",
                "category": "payment",
                "value": "USD",
                "value_type": "string",
                "description": "Default currency for payments",
                "is_public": True,
                "is_editable": True,
                "is_required": False,
                "validation_rules": {"enum": ["USD", "EUR", "GBP", "GHS"]},
                "default_value": "USD"
            },
            
            # Security Settings
            {
                "key": "jwt_secret",
                "category": "security",
                "value": "",
                "value_type": "string",
                "description": "JWT secret key for token signing",
                "is_public": False,
                "is_editable": True,
                "is_required": True,
                "validation_rules": {"min_length": 32},
                "default_value": ""
            },
            {
                "key": "jwt_expiry_hours",
                "category": "security",
                "value": "24",
                "value_type": "number",
                "description": "JWT token expiry time in hours",
                "is_public": True,
                "is_editable": True,
                "is_required": False,
                "validation_rules": {"min": 1, "max": 168},
                "default_value": "24"
            },
            {
                "key": "password_min_length",
                "category": "security",
                "value": "8",
                "value_type": "number",
                "description": "Minimum password length",
                "is_public": True,
                "is_editable": True,
                "is_required": False,
                "validation_rules": {"min": 6, "max": 50},
                "default_value": "8"
            },
            {
                "key": "max_login_attempts",
                "category": "security",
                "value": "5",
                "value_type": "number",
                "description": "Maximum login attempts before account lockout",
                "is_public": True,
                "is_editable": True,
                "is_required": False,
                "validation_rules": {"min": 3, "max": 10},
                "default_value": "5"
            },
            
            # UI Settings
            {
                "key": "app_name",
                "category": "ui",
                "value": "Dennis Law SVD",
                "value_type": "string",
                "description": "Application name displayed in UI",
                "is_public": True,
                "is_editable": True,
                "is_required": False,
                "validation_rules": {"max_length": 100},
                "default_value": "Dennis Law SVD"
            },
            {
                "key": "app_logo_url",
                "category": "ui",
                "value": "",
                "value_type": "string",
                "description": "URL to application logo",
                "is_public": True,
                "is_editable": True,
                "is_required": False,
                "validation_rules": {"pattern": "^https?://.*"},
                "default_value": ""
            },
            {
                "key": "theme",
                "category": "ui",
                "value": "light",
                "value_type": "string",
                "description": "Default theme for the application",
                "is_public": True,
                "is_editable": True,
                "is_required": False,
                "validation_rules": {"enum": ["light", "dark", "auto"]},
                "default_value": "light"
            },
            {
                "key": "items_per_page",
                "category": "ui",
                "value": "10",
                "value_type": "number",
                "description": "Default number of items per page",
                "is_public": True,
                "is_editable": True,
                "is_required": False,
                "validation_rules": {"min": 5, "max": 100},
                "default_value": "10"
            },
            
            # Database Settings
            {
                "key": "backup_enabled",
                "category": "database",
                "value": "false",
                "value_type": "boolean",
                "description": "Enable automatic database backups",
                "is_public": False,
                "is_editable": True,
                "is_required": False,
                "validation_rules": {},
                "default_value": "false"
            },
            {
                "key": "backup_frequency_hours",
                "category": "database",
                "value": "24",
                "value_type": "number",
                "description": "Database backup frequency in hours",
                "is_public": False,
                "is_editable": True,
                "is_required": False,
                "validation_rules": {"min": 1, "max": 168},
                "default_value": "24"
            },
            {
                "key": "max_connections",
                "category": "database",
                "value": "100",
                "value_type": "number",
                "description": "Maximum database connections",
                "is_public": False,
                "is_editable": True,
                "is_required": False,
                "validation_rules": {"min": 10, "max": 1000},
                "default_value": "100"
            }
        ]
        
        created_count = 0
        updated_count = 0
        
        for setting_data in common_settings:
            # Check if setting already exists
            existing_setting = db.query(Settings).filter(Settings.key == setting_data["key"]).first()
            
            if existing_setting:
                # Update existing setting if it's missing some fields
                updated = False
                for key, value in setting_data.items():
                    if key != "key" and hasattr(existing_setting, key) and getattr(existing_setting, key) != value:
                        setattr(existing_setting, key, value)
                        updated = True
                
                if updated:
                    existing_setting.updated_at = datetime.now()
                    updated_count += 1
                    print(f"✅ Updated setting: {setting_data['key']}")
                else:
                    print(f"⏭️  Setting already exists: {setting_data['key']}")
            else:
                # Create new setting
                setting = Settings(**setting_data)
                db.add(setting)
                created_count += 1
                print(f"✅ Created setting: {setting_data['key']}")
        
        db.commit()
        
        print(f"\n🎉 Settings creation completed!")
        print(f"   Created: {created_count} settings")
        print(f"   Updated: {updated_count} settings")
        print(f"   Total settings in database: {db.query(Settings).count()}")
        
    except Exception as e:
        print(f"❌ Error creating settings: {str(e)}")
        if 'db' in locals():
            db.rollback()
    finally:
        if 'db' in locals():
            db.close()

if __name__ == "__main__":
    create_common_settings()
