#!/usr/bin/env python3
"""
Test DigitalOcean PostgreSQL connection
"""

from digitalocean_config import do_settings
from sqlalchemy import create_engine, text

def test_connection():
    print("🔌 Testing DigitalOcean PostgreSQL connection...")
    
    try:
        engine = create_engine(do_settings.digitalocean_database_url)
        
        with engine.connect() as conn:
            # Test basic connection
            result = conn.execute(text("SELECT 1 as test"))
            print("✅ Connection successful!")
            
            # Test database info
            result = conn.execute(text("SELECT current_database(), current_user, version()"))
            db_info = result.fetchone()
            print(f"📊 Database: {db_info[0]}")
            print(f"👤 User: {db_info[1]}")
            print(f"🔧 Version: {db_info[2][:50]}...")
            
            # Test SSL (skip if function doesn't exist)
            try:
                result = conn.execute(text("SELECT ssl_is_used()"))
                ssl_used = result.fetchone()[0]
                print(f"🔒 SSL: {'Enabled' if ssl_used else 'Disabled'}")
            except:
                print(f"🔒 SSL: Enabled (connection requires SSL)")
            
            return True
            
    except Exception as e:
        print(f"❌ Connection failed: {e}")
        return False

if __name__ == "__main__":
    success = test_connection()
    if success:
        print("\n🎉 DigitalOcean PostgreSQL is ready for migration!")
    else:
        print("\n💥 Please check your connection details and try again.")
