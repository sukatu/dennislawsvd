#!/usr/bin/env python3
"""
Script to create the notifications table in the database
"""

import sys
import os
from sqlalchemy import text

# Add the backend directory to the Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from database import engine

def create_notifications_table():
    """Create the notifications table"""
    
    try:
        with engine.connect() as connection:
            # Create notifications table
            notifications_table_sql = """
            CREATE TABLE IF NOT EXISTS notifications (
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
            
            connection.execute(text(notifications_table_sql))
            connection.commit()
            print("✅ Notifications table created successfully!")
            
            # Create notification_preferences table
            preferences_table_sql = """
            CREATE TABLE IF NOT EXISTS notification_preferences (
                id INT AUTO_INCREMENT PRIMARY KEY,
                user_id INT NOT NULL UNIQUE,
                email_notifications BOOLEAN DEFAULT TRUE,
                email_success BOOLEAN DEFAULT TRUE,
                email_info BOOLEAN DEFAULT TRUE,
                email_warning BOOLEAN DEFAULT TRUE,
                email_error BOOLEAN DEFAULT TRUE,
                in_app_notifications BOOLEAN DEFAULT TRUE,
                in_app_success BOOLEAN DEFAULT TRUE,
                in_app_info BOOLEAN DEFAULT TRUE,
                in_app_warning BOOLEAN DEFAULT TRUE,
                in_app_error BOOLEAN DEFAULT TRUE,
                subscription_notifications BOOLEAN DEFAULT TRUE,
                case_notifications BOOLEAN DEFAULT TRUE,
                billing_notifications BOOLEAN DEFAULT TRUE,
                system_notifications BOOLEAN DEFAULT TRUE,
                security_notifications BOOLEAN DEFAULT TRUE,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
                INDEX idx_user_id (user_id),
                FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
            ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
            """
            
            connection.execute(text(preferences_table_sql))
            connection.commit()
            print("✅ Notification preferences table created successfully!")
            
    except Exception as e:
        print(f"❌ Error creating tables: {e}")
        raise

if __name__ == "__main__":
    print("🚀 Creating notifications tables...")
    create_notifications_table()
    print("\n🎉 Tables created successfully!")
