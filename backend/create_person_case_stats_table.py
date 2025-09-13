#!/usr/bin/env python3
"""
Create person_case_statistics table to store calculated case data for each person.
This table will store pre-calculated statistics to improve performance.
"""

import mysql.connector
from config import settings

# Create DATABASE_CONFIG from settings
DATABASE_CONFIG = {
    'host': settings.mysql_host,
    'port': settings.mysql_port,
    'user': settings.mysql_user,
    'password': settings.mysql_password,
    'database': settings.mysql_database
}

def create_person_case_stats_table():
    """Create the person_case_statistics table."""
    
    connection = None
    try:
        # Connect to MySQL database
        connection = mysql.connector.connect(**DATABASE_CONFIG)
        cursor = connection.cursor()
        
        print("Creating person_case_statistics table...")
        
        # Create the table
        create_table_query = """
        CREATE TABLE IF NOT EXISTS person_case_statistics (
            id INT AUTO_INCREMENT PRIMARY KEY,
            person_id INT NOT NULL,
            total_cases INT DEFAULT 0,
            resolved_cases INT DEFAULT 0,
            unresolved_cases INT DEFAULT 0,
            favorable_cases INT DEFAULT 0,
            unfavorable_cases INT DEFAULT 0,
            mixed_cases INT DEFAULT 0,
            case_outcome VARCHAR(50) DEFAULT 'N/A',
            last_updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (person_id) REFERENCES people(id) ON DELETE CASCADE,
            UNIQUE KEY unique_person_stats (person_id),
            INDEX idx_person_id (person_id),
            INDEX idx_total_cases (total_cases),
            INDEX idx_resolved_cases (resolved_cases),
            INDEX idx_case_outcome (case_outcome)
        ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
        """
        
        cursor.execute(create_table_query)
        connection.commit()
        
        print("✅ person_case_statistics table created successfully!")
        
        # Show table structure
        cursor.execute("DESCRIBE person_case_statistics")
        columns = cursor.fetchall()
        
        print("\n📋 Table Structure:")
        print("-" * 80)
        for column in columns:
            print(f"{column[0]:<20} {column[1]:<20} {column[2]:<10} {column[3]:<10} {column[4] or ''}")
        print("-" * 80)
        
    except mysql.connector.Error as e:
        print(f"❌ Error creating table: {e}")
        return False
        
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        return False
        
    finally:
        if connection and connection.is_connected():
            cursor.close()
            connection.close()
            print("\n🔌 Database connection closed.")
    
    return True

if __name__ == "__main__":
    print("🚀 Creating person_case_statistics table...")
    success = create_person_case_stats_table()
    
    if success:
        print("\n✅ Database setup completed successfully!")
    else:
        print("\n❌ Database setup failed!")
