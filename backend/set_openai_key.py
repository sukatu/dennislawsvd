#!/usr/bin/env python3
"""
Script to set OpenAI API key in the database
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from sqlalchemy.orm import Session
from database import get_db
from models.settings import Settings

def set_openai_key(api_key: str):
    """Set OpenAI API key in the database"""
    try:
        # Get database session
        db = next(get_db())
        
        # Find the OpenAI API key setting
        setting = db.query(Settings).filter(Settings.key == "openai_api_key").first()
        
        if not setting:
            print("❌ OpenAI API key setting not found. Please run create_openai_setting.py first.")
            return False
        
        # Update the value
        setting.value = api_key
        db.commit()
        
        print(f"✅ OpenAI API key set successfully in database")
        print(f"Key: {api_key[:10]}...")
        return True
        
    except Exception as e:
        print(f"❌ Error setting OpenAI key: {str(e)}")
        if 'db' in locals():
            db.rollback()
        return False
    finally:
        if 'db' in locals():
            db.close()

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python set_openai_key.py <api_key>")
        print("Example: python set_openai_key.py sk-proj-...")
        sys.exit(1)
    
    api_key = sys.argv[1]
    if not api_key.startswith('sk-'):
        print("❌ Invalid API key format. OpenAI API keys should start with 'sk-'")
        sys.exit(1)
    
    set_openai_key(api_key)
