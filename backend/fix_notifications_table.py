#!/usr/bin/env python3
"""
Script to check and fix the notifications table structure
"""

import sys
import os
from sqlalchemy import text

# Add the backend directory to the Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from database import engine

def check_and_fix_notifications_table():
    """Check and fix the notifications table structure"""
    
    try:
        with engine.connect() as connection:
            # Check if table exists
            check_table_sql = """
            SELECT COUNT(*) as table_exists 
            FROM information_schema.tables 
            WHERE table_schema = 'dennislaw_svd' 
            AND table_name = 'notifications'
            """
            
            result = connection.execute(text(check_table_sql)).fetchone()
            table_exists = result[0] > 0 if result else False
            
            print(f"Notifications table exists: {table_exists}")
            
            if not table_exists:
                print("Creating notifications table...")
                create_table_sql = """
                CREATE TABLE notifications (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    user_id INT NOT NULL,
                    title VARCHAR(255) NOT NULL,
                    message TEXT NOT NULL,
                    type ENUM('success', 'info', 'warning', 'error') DEFAULT 'info',
                    priority ENUM('low', 'medium', 'high', 'urgent') DEFAULT 'medium',
                    status ENUM('unread', 'read', 'archived') DEFAULT 'unread',
                    category VARCHAR(100) NULL,
                    action_url VARCHAR(500) NULL,
                    notification_data JSON NULL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    read_at TIMESTAMP NULL,
                    expires_at TIMESTAMP NULL,
                    INDEX idx_user_id (user_id),
                    INDEX idx_status (status),
                    INDEX idx_type (type),
                    INDEX idx_category (category),
                    INDEX idx_created_at (created_at),
                    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
                ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
                """
                connection.execute(text(create_table_sql))
                connection.commit()
                print("✅ Notifications table created successfully!")
            else:
                # Check if category column exists
                check_columns_sql = """
                SELECT COLUMN_NAME 
                FROM information_schema.COLUMNS 
                WHERE TABLE_SCHEMA = 'dennislaw_svd' 
                AND TABLE_NAME = 'notifications'
                AND COLUMN_NAME = 'category'
                """
                
                result = connection.execute(text(check_columns_sql)).fetchone()
                category_exists = result is not None
                
                print(f"Category column exists: {category_exists}")
                
                if not category_exists:
                    print("Adding missing columns...")
                    alter_table_sql = """
                    ALTER TABLE notifications 
                    ADD COLUMN category VARCHAR(100) NULL,
                    ADD COLUMN action_url VARCHAR(500) NULL,
                    ADD COLUMN notification_data JSON NULL,
                    ADD COLUMN read_at TIMESTAMP NULL,
                    ADD COLUMN expires_at TIMESTAMP NULL,
                    ADD INDEX idx_category (category)
                    """
                    connection.execute(text(alter_table_sql))
                    connection.commit()
                    print("✅ Missing columns added successfully!")
                
                # Check if priority column exists
                check_priority_sql = """
                SELECT COLUMN_NAME 
                FROM information_schema.COLUMNS 
                WHERE TABLE_SCHEMA = 'dennislaw_svd' 
                AND TABLE_NAME = 'notifications'
                AND COLUMN_NAME = 'priority'
                """
                
                result = connection.execute(text(check_priority_sql)).fetchone()
                priority_exists = result is not None
                
                print(f"Priority column exists: {priority_exists}")
                
                if not priority_exists:
                    print("Adding priority column...")
                    alter_priority_sql = """
                    ALTER TABLE notifications 
                    ADD COLUMN priority ENUM('low', 'medium', 'high', 'urgent') DEFAULT 'medium'
                    """
                    connection.execute(text(alter_priority_sql))
                    connection.commit()
                    print("✅ Priority column added successfully!")
            
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
    print("🔧 Checking and fixing notifications table...")
    check_and_fix_notifications_table()
    print("\n🎉 Table check and fix completed!")
