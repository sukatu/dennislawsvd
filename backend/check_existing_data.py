#!/usr/bin/env python3
"""
Check Existing Data Script
This script checks what data exists in your current database (SQLite or MySQL).
"""

import os
import sys
import sqlite3
import pymysql
from sqlalchemy import create_engine, text
from urllib.parse import quote_plus

def check_sqlite_data():
    """Check SQLite database for data"""
    sqlite_path = os.path.join(os.path.dirname(__file__), '..', 'case_search.db')
    
    if not os.path.exists(sqlite_path):
        print("❌ SQLite database file not found")
        return False
    
    try:
        conn = sqlite3.connect(sqlite_path)
        cursor = conn.cursor()
        
        # Get all tables
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tables = cursor.fetchall()
        
        if not tables:
            print("⚠️ SQLite database exists but is empty")
            return False
        
        print(f"✅ SQLite database found with {len(tables)} tables:")
        
        total_records = 0
        for table in tables:
            table_name = table[0]
            cursor.execute(f"SELECT COUNT(*) FROM {table_name}")
            count = cursor.fetchone()[0]
            total_records += count
            print(f"   📋 {table_name}: {count} records")
        
        print(f"\n📊 Total records: {total_records}")
        
        conn.close()
        return total_records > 0
        
    except Exception as e:
        print(f"❌ Error reading SQLite database: {e}")
        return False

def check_mysql_data():
    """Check MySQL database for data"""
    try:
        # Load environment variables from .env file
        from dotenv import load_dotenv
        load_dotenv()
        
        # Try to get MySQL config from environment
        config = {
            'host': os.getenv('MYSQL_HOST', 'localhost'),
            'port': int(os.getenv('MYSQL_PORT', 3306)),
            'user': os.getenv('MYSQL_USER', 'root'),
            'password': os.getenv('MYSQL_PASSWORD', ''),
            'database': os.getenv('MYSQL_DATABASE', 'juridence')
        }
        
        print("🔄 Attempting to connect to MySQL...")
        
        connection = pymysql.connect(**config)
        cursor = connection.cursor()
        
        # Get all tables
        cursor.execute("SHOW TABLES")
        tables = cursor.fetchall()
        
        if not tables:
            print("⚠️ MySQL database exists but is empty")
            return False
        
        print(f"✅ MySQL database found with {len(tables)} tables:")
        
        total_records = 0
        for table in tables:
            table_name = table[0]
            cursor.execute(f"SELECT COUNT(*) FROM {table_name}")
            count = cursor.fetchone()[0]
            total_records += count
            print(f"   📋 {table_name}: {count} records")
        
        print(f"\n📊 Total records: {total_records}")
        
        connection.close()
        return total_records > 0
        
    except Exception as e:
        print(f"❌ Error connecting to MySQL: {e}")
        print("💡 Make sure MySQL is running and credentials are correct")
        return False

def main():
    """Main function"""
    print("=" * 60)
    print("🔍 CHECKING EXISTING DATA")
    print("=" * 60)
    
    has_data = False
    
    # Check SQLite first
    print("\n1️⃣ Checking SQLite database...")
    if check_sqlite_data():
        has_data = True
    
    # Check MySQL
    print("\n2️⃣ Checking MySQL database...")
    if check_mysql_data():
        has_data = True
    
    print("\n" + "=" * 60)
    
    if has_data:
        print("✅ Data found! You can proceed with migration.")
        print("\n📋 Next steps:")
        print("1. If you need to configure MySQL connection:")
        print("   python setup_mysql_config.py")
        print("2. Run the migration:")
        print("   python migrate_to_postgres.py")
    else:
        print("⚠️ No data found in existing databases.")
        print("\n💡 This could mean:")
        print("   - Your database is empty")
        print("   - You're using a different database location")
        print("   - MySQL credentials need to be configured")
        print("\n🔧 To configure MySQL connection:")
        print("   python setup_mysql_config.py")

if __name__ == "__main__":
    main()
