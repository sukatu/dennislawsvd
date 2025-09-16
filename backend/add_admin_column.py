#!/usr/bin/env python3
"""
Script to add is_admin column to the users table
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from sqlalchemy import create_engine, text
from config import settings

def add_admin_column():
    """Add is_admin column to users table"""
    try:
        # Create engine
        engine = create_engine(settings.database_url)
        
        with engine.connect() as connection:
            # Check if column already exists
            result = connection.execute(text("""
                SELECT COLUMN_NAME 
                FROM INFORMATION_SCHEMA.COLUMNS 
                WHERE TABLE_NAME = 'users' 
                AND COLUMN_NAME = 'is_admin'
            """))
            
            if result.fetchone():
                print("is_admin column already exists in users table")
                return
            
            # Add the column
            connection.execute(text("""
                ALTER TABLE users 
                ADD COLUMN is_admin BOOLEAN DEFAULT FALSE NOT NULL
            """))
            
            connection.commit()
            print("Successfully added is_admin column to users table")
            
    except Exception as e:
        print(f"Error adding is_admin column: {e}")
        return False
    
    return True

if __name__ == "__main__":
    add_admin_column()
