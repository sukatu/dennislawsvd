#!/usr/bin/env python3
"""
Script to add only the missing columns to the notifications table
"""

import sys
import os
from sqlalchemy import text

# Add the backend directory to the Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from database import engine

def add_missing_columns():
    """Add only the missing columns to the notifications table"""
    
    try:
        with engine.connect() as connection:
            # Get existing columns
            get_columns_sql = """
            SELECT COLUMN_NAME 
            FROM information_schema.COLUMNS 
            WHERE TABLE_SCHEMA = 'dennislaw_svd' 
            AND TABLE_NAME = 'notifications'
            ORDER BY ORDINAL_POSITION
            """
            
            result = connection.execute(text(get_columns_sql)).fetchall()
            existing_columns = [row[0] for row in result]
            
            print("Existing columns:", existing_columns)
            
            # Define required columns
            required_columns = {
                'category': 'VARCHAR(100) NULL',
                'action_url': 'VARCHAR(500) NULL', 
                'notification_data': 'JSON NULL',
                'read_at': 'TIMESTAMP NULL',
                'expires_at': 'TIMESTAMP NULL',
                'priority': "ENUM('low', 'medium', 'high', 'urgent') DEFAULT 'medium'"
            }
            
            # Add missing columns one by one
            for column_name, column_definition in required_columns.items():
                if column_name not in existing_columns:
                    print(f"Adding column: {column_name}")
                    alter_sql = f"ALTER TABLE notifications ADD COLUMN {column_name} {column_definition}"
                    connection.execute(text(alter_sql))
                    connection.commit()
                    print(f"✅ Added {column_name}")
                else:
                    print(f"✅ {column_name} already exists")
            
            # Add index for category if it doesn't exist
            check_index_sql = """
            SELECT COUNT(*) 
            FROM information_schema.statistics 
            WHERE table_schema = 'dennislaw_svd' 
            AND table_name = 'notifications' 
            AND index_name = 'idx_category'
            """
            
            result = connection.execute(text(check_index_sql)).fetchone()
            index_exists = result[0] > 0 if result else False
            
            if not index_exists and 'category' in existing_columns or 'category' in required_columns:
                print("Adding index for category column...")
                add_index_sql = "ALTER TABLE notifications ADD INDEX idx_category (category)"
                connection.execute(text(add_index_sql))
                connection.commit()
                print("✅ Added category index")
            
            # Show final table structure
            print("\nFinal table structure:")
            describe_sql = "DESCRIBE notifications"
            result = connection.execute(text(describe_sql)).fetchall()
            for row in result:
                print(f"  {row[0]} - {row[1]} - {row[2]} - {row[3]}")
            
    except Exception as e:
        print(f"❌ Error: {e}")
        raise

if __name__ == "__main__":
    print("🔧 Adding missing columns to notifications table...")
    add_missing_columns()
    print("\n🎉 Column addition completed!")
