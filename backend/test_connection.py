#!/usr/bin/env python3
"""
Test script to verify database connection and basic functionality
"""

import sys
from sqlalchemy import create_engine, text
from config import settings

def test_database_connection():
    """Test database connection and create a test table."""
    try:
        # Create engine
        engine = create_engine(settings.database_url)
        
        # Test connection
        with engine.connect() as connection:
            result = connection.execute(text("SELECT 1 as test"))
            test_value = result.fetchone()[0]
            
            if test_value == 1:
                print("✅ Database connection test successful!")
                return True
            else:
                print("❌ Database connection test failed!")
                return False
                
    except Exception as e:
        print(f"❌ Database connection failed: {e}")
        return False

def test_user_table():
    """Test if users table exists and can be queried."""
    try:
        from database import SessionLocal
        from models.user import User
        
        db = SessionLocal()
        
        # Try to query the users table
        user_count = db.query(User).count()
        print(f"✅ Users table accessible! Current user count: {user_count}")
        
        db.close()
        return True
        
    except Exception as e:
        print(f"❌ Users table test failed: {e}")
        return False

def main():
    """Run all tests."""
    print("🧪 Testing Dennislaw SVD Backend...")
    print("=" * 40)
    
    # Test 1: Database connection
    print("\n1. Testing database connection...")
    if not test_database_connection():
        print("❌ Database connection test failed!")
        return False
    
    # Test 2: Users table
    print("\n2. Testing users table...")
    if not test_user_table():
        print("❌ Users table test failed!")
        return False
    
    print("\n" + "=" * 40)
    print("🎉 All tests passed! Backend is ready to use.")
    print("\nYou can now run: python main.py")
    
    return True

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
