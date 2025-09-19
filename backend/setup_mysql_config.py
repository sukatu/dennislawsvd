#!/usr/bin/env python3
"""
MySQL Configuration Setup Script
This script helps you configure MySQL connection details for migration.
"""

import os
import sys
import getpass
from urllib.parse import quote_plus

def create_mysql_env_file():
    """Create .env file with MySQL configuration"""
    
    print("=" * 60)
    print("🔧 MYSQL CONFIGURATION SETUP")
    print("=" * 60)
    print("Enter your MySQL database connection details:")
    print("(Press Enter to use default values)")
    print()
    
    # Get MySQL connection details
    mysql_host = input("MySQL Host [localhost]: ").strip() or "localhost"
    mysql_port = input("MySQL Port [3306]: ").strip() or "3306"
    mysql_user = input("MySQL Username [root]: ").strip() or "root"
    mysql_password = getpass.getpass("MySQL Password: ")
    mysql_database = input("MySQL Database Name: ").strip()
    
    if not mysql_database:
        print("❌ Database name is required!")
        return False
    
    # Create .env file content
    env_content = f"""# MySQL Configuration for Migration
MYSQL_HOST={mysql_host}
MYSQL_PORT={mysql_port}
MYSQL_USER={mysql_user}
MYSQL_PASSWORD={mysql_password}
MYSQL_DATABASE={mysql_database}

# PostgreSQL Configuration (already set in config.py)
POSTGRES_HOST=localhost
POSTGRES_PORT=5432
POSTGRES_USER=postgres
POSTGRES_PASSWORD=62579011
POSTGRES_DATABASE=juridence
"""
    
    # Write .env file
    env_file_path = os.path.join(os.path.dirname(__file__), '.env')
    with open(env_file_path, 'w') as f:
        f.write(env_content)
    
    print(f"\n✅ MySQL configuration saved to {env_file_path}")
    print("\n📋 Configuration Summary:")
    print(f"   Host: {mysql_host}")
    print(f"   Port: {mysql_port}")
    print(f"   Username: {mysql_user}")
    print(f"   Database: {mysql_database}")
    print(f"   Password: {'*' * len(mysql_password)}")
    
    return True

def test_mysql_connection():
    """Test MySQL connection"""
    try:
        import pymysql
        from dotenv import load_dotenv
        
        # Load environment variables
        load_dotenv()
        
        # Get connection details
        config = {
            'host': os.getenv('MYSQL_HOST', 'localhost'),
            'port': int(os.getenv('MYSQL_PORT', 3306)),
            'user': os.getenv('MYSQL_USER', 'root'),
            'password': os.getenv('MYSQL_PASSWORD', ''),
            'database': os.getenv('MYSQL_DATABASE', '')
        }
        
        print("\n🔄 Testing MySQL connection...")
        
        # Test connection
        connection = pymysql.connect(**config)
        cursor = connection.cursor()
        
        # Get table count
        cursor.execute("SHOW TABLES")
        tables = cursor.fetchall()
        
        connection.close()
        
        print(f"✅ MySQL connection successful!")
        print(f"📊 Found {len(tables)} tables in database")
        
        if tables:
            print("\n📋 Tables found:")
            for table in tables:
                print(f"   - {table[0]}")
        
        return True
        
    except ImportError:
        print("❌ pymysql not installed. Install it with: pip install pymysql")
        return False
    except Exception as e:
        print(f"❌ MySQL connection failed: {e}")
        return False

def main():
    """Main function"""
    print("This script will help you configure MySQL connection for migration.")
    print()
    
    # Check if .env already exists
    env_file = os.path.join(os.path.dirname(__file__), '.env')
    if os.path.exists(env_file):
        overwrite = input("⚠️ .env file already exists. Overwrite? (y/N): ").strip().lower()
        if overwrite != 'y':
            print("❌ Migration cancelled.")
            return
    
    # Create MySQL configuration
    if not create_mysql_env_file():
        return
    
    # Test connection
    test_connection = input("\n🔄 Test MySQL connection now? (Y/n): ").strip().lower()
    if test_connection != 'n':
        test_mysql_connection()
    
    print("\n🎯 Next steps:")
    print("1. Run the migration script: python migrate_to_postgres.py")
    print("2. Check the migration log for any issues")
    print("3. Start your application with PostgreSQL")

if __name__ == "__main__":
    main()
