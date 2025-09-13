#!/usr/bin/env python3
"""
Script to create person_analytics table for storing AI-generated person analytics
"""

import mysql.connector
from mysql.connector import Error
import sys
import os

# Add the backend directory to the Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '.')))

from config import settings

def create_person_analytics_table():
    """Create the person_analytics table"""
    
    DATABASE_CONFIG = {
        'host': settings.mysql_host,
        'port': settings.mysql_port,
        'user': settings.mysql_user,
        'password': settings.mysql_password,
        'database': settings.mysql_database
    }
    
    connection = None
    try:
        connection = mysql.connector.connect(**DATABASE_CONFIG)
        cursor = connection.cursor()
        
        # Create person_analytics table
        create_table_query = """
        CREATE TABLE IF NOT EXISTS person_analytics (
            id INT AUTO_INCREMENT PRIMARY KEY,
            person_id INT NOT NULL,
            risk_score INT DEFAULT 0,
            risk_level ENUM('Low', 'Medium', 'High', 'Critical') DEFAULT 'Low',
            risk_factors JSON,
            total_monetary_amount DECIMAL(15,2) DEFAULT 0.00,
            average_case_value DECIMAL(15,2) DEFAULT 0.00,
            financial_risk_level ENUM('Low', 'Medium', 'High', 'Critical') DEFAULT 'Low',
            primary_subject_matter VARCHAR(255),
            subject_matter_categories JSON,
            legal_issues JSON,
            financial_terms JSON,
            case_complexity_score INT DEFAULT 0,
            success_rate DECIMAL(5,2) DEFAULT 0.00,
            last_updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            UNIQUE KEY unique_person (person_id),
            FOREIGN KEY (person_id) REFERENCES people(id) ON DELETE CASCADE,
            INDEX idx_risk_score (risk_score),
            INDEX idx_risk_level (risk_level),
            INDEX idx_financial_risk (financial_risk_level)
        ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
        """
        
        cursor.execute(create_table_query)
        connection.commit()
        print("✅ person_analytics table created successfully!")
        
        # Show table structure
        cursor.execute("DESCRIBE person_analytics")
        columns = cursor.fetchall()
        print("\n📋 Table structure:")
        for column in columns:
            print(f"  {column[0]}: {column[1]} {column[2]} {column[3]} {column[4]} {column[5]}")
            
    except Error as e:
        print(f"❌ Error creating person_analytics table: {e}")
        return False
    finally:
        if connection and connection.is_connected():
            cursor.close()
            connection.close()
    
    return True

if __name__ == "__main__":
    print("🚀 Creating person_analytics table...")
    success = create_person_analytics_table()
    if success:
        print("🎉 Database setup completed successfully!")
    else:
        print("💥 Database setup failed!")
        sys.exit(1)
