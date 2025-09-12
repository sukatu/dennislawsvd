#!/usr/bin/env python3
"""
Setup script for Dennislaw SVD Backend
This script helps set up the database and run initial migrations.
"""

import sys
import subprocess
import pymysql
from sqlalchemy import create_engine, text
from config import settings

def check_mysql_connection():
    """Check if MySQL connection is working."""
    try:
        connection = pymysql.connect(
            host=settings.mysql_host,
            port=settings.mysql_port,
            user=settings.mysql_user,
            password=settings.mysql_password,
            charset='utf8mb4'
        )
        print("✅ MySQL connection successful!")
        connection.close()
        return True
    except Exception as e:
        print(f"❌ MySQL connection failed: {e}")
        return False

def create_database():
    """Create the database if it doesn't exist."""
    try:
        connection = pymysql.connect(
            host=settings.mysql_host,
            port=settings.mysql_port,
            user=settings.mysql_user,
            password=settings.mysql_password,
            charset='utf8mb4'
        )
        
        with connection.cursor() as cursor:
            cursor.execute(f"CREATE DATABASE IF NOT EXISTS {settings.mysql_database}")
            print(f"✅ Database '{settings.mysql_database}' created/verified!")
        
        connection.close()
        return True
    except Exception as e:
        print(f"❌ Database creation failed: {e}")
        return False

def create_tables():
    """Create all database tables."""
    try:
        from database import create_tables
        create_tables()
        print("✅ Database tables created successfully!")
        return True
    except Exception as e:
        print(f"❌ Table creation failed: {e}")
        return False

def install_dependencies():
    """Install Python dependencies."""
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
        print("✅ Dependencies installed successfully!")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Dependency installation failed: {e}")
        return False

def main():
    """Main setup function."""
    print("🚀 Setting up Dennislaw SVD Backend...")
    print("=" * 50)
    
    # Step 1: Install dependencies
    print("\n1. Installing dependencies...")
    if not install_dependencies():
        print("❌ Setup failed at dependency installation")
        return False
    
    # Step 2: Check MySQL connection
    print("\n2. Checking MySQL connection...")
    if not check_mysql_connection():
        print("❌ Setup failed at MySQL connection check")
        return False
    
    # Step 3: Create database
    print("\n3. Creating database...")
    if not create_database():
        print("❌ Setup failed at database creation")
        return False
    
    # Step 4: Create tables
    print("\n4. Creating database tables...")
    if not create_tables():
        print("❌ Setup failed at table creation")
        return False
    
    print("\n" + "=" * 50)
    print("🎉 Setup completed successfully!")
    print("\nNext steps:")
    print("1. Run the backend: python main.py")
    print("2. Visit http://localhost:8000/docs for API documentation")
    print("3. Test the health endpoint: http://localhost:8000/health")
    
    return True

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
