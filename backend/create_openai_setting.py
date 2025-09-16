#!/usr/bin/env python3
"""
Script to create OpenAI API key setting in the database
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from sqlalchemy.orm import Session
from database import get_db, engine, Base
from models.settings import Settings

def create_openai_setting():
    """Create OpenAI API key setting in the database"""
    try:
        # Create tables if they don't exist
        Base.metadata.create_all(bind=engine)
        
        # Get database session
        db = next(get_db())
        
        # Check if OpenAI API key setting already exists
        existing_setting = db.query(Settings).filter(Settings.key == "openai_api_key").first()
        
        if existing_setting:
            print("OpenAI API key setting already exists in database")
            print(f"Current value: {existing_setting.value[:10]}..." if existing_setting.value else "No value set")
            return
        
        # Create new OpenAI API key setting
        openai_setting = Settings(
            key="openai_api_key",
            category="ai",
            value="",  # Empty initially, will be set via admin panel
            value_type="string",
            description="OpenAI API key for AI-powered features",
            is_public=False,
            is_editable=True,
            is_required=True,
            validation_rules={
                "pattern": "^sk-[a-zA-Z0-9]{20,}$",
                "min_length": 20
            },
            default_value=""
        )
        
        db.add(openai_setting)
        db.commit()
        
        print("✅ OpenAI API key setting created successfully in database")
        print("You can now set the API key via the admin panel or directly in the database")
        
    except Exception as e:
        print(f"❌ Error creating OpenAI setting: {str(e)}")
        if 'db' in locals():
            db.rollback()
    finally:
        if 'db' in locals():
            db.close()

if __name__ == "__main__":
    create_openai_setting()
