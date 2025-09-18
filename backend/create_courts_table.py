#!/usr/bin/env python3
"""
Create courts table for Justice Locator system
"""

import pymysql
from config import settings

def create_courts_table():
    """Create the courts table"""
    try:
        # Connect to MySQL database
        connection = pymysql.connect(
            host=settings.mysql_host,
            user=settings.mysql_user,
            password=settings.mysql_password,
            database=settings.mysql_database,
            charset='utf8mb4'
        )
        
        cursor = connection.cursor()
        
        # Create courts table
        create_table_sql = """
        CREATE TABLE IF NOT EXISTS courts (
            id INT AUTO_INCREMENT PRIMARY KEY,
            name VARCHAR(255) NOT NULL,
            registry_name VARCHAR(255) NULL,
            court_type VARCHAR(100) NOT NULL,
            region VARCHAR(100) NOT NULL,
            location VARCHAR(255) NOT NULL,
            address TEXT NULL,
            city VARCHAR(100) NULL,
            district VARCHAR(100) NULL,
            
            -- Google Maps integration
            latitude DECIMAL(10, 8) NULL,
            longitude DECIMAL(11, 8) NULL,
            google_place_id VARCHAR(255) NULL,
            
            -- Court details
            area_coverage TEXT NULL,
            contact_phone VARCHAR(50) NULL,
            contact_email VARCHAR(255) NULL,
            website VARCHAR(255) NULL,
            
            -- Media
            court_picture_url VARCHAR(500) NULL,
            additional_images TEXT NULL,
            
            -- Operational details
            operating_hours TEXT NULL,
            is_active BOOLEAN NOT NULL DEFAULT TRUE,
            is_verified BOOLEAN NOT NULL DEFAULT FALSE,
            
            -- Metadata
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
            created_by INT NULL,
            updated_by INT NULL,
            
            -- Search and analytics
            search_count INT NOT NULL DEFAULT 0,
            last_searched TIMESTAMP NULL,
            
            -- Additional fields
            notes TEXT NULL,
            status VARCHAR(50) NOT NULL DEFAULT 'ACTIVE',
            
            -- Indexes
            INDEX idx_name (name),
            INDEX idx_court_type (court_type),
            INDEX idx_region (region),
            INDEX idx_location (location),
            INDEX idx_city (city),
            INDEX idx_is_active (is_active),
            INDEX idx_coordinates (latitude, longitude),
            
            -- Foreign keys
            FOREIGN KEY (created_by) REFERENCES users(id) ON DELETE SET NULL,
            FOREIGN KEY (updated_by) REFERENCES users(id) ON DELETE SET NULL
        ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
        """
        
        cursor.execute(create_table_sql)
        connection.commit()
        
        print("✅ Courts table created successfully!")
        
        # Insert sample data
        sample_courts = [
            {
                'name': 'Supreme Court of Ghana',
                'registry_name': 'Supreme Court Registry',
                'court_type': 'Supreme Court',
                'region': 'Greater Accra',
                'location': 'Accra',
                'address': 'Supreme Court Building, Independence Avenue, Accra',
                'city': 'Accra',
                'district': 'Accra Metropolitan',
                'latitude': 5.6037,
                'longitude': -0.1870,
                'area_coverage': 'National',
                'contact_phone': '+233 302 663 421',
                'contact_email': 'info@supremecourt.gov.gh',
                'website': 'https://www.supremecourt.gov.gh',
                'is_active': True,
                'is_verified': True
            },
            {
                'name': 'High Court - Accra',
                'registry_name': 'High Court Registry Accra',
                'court_type': 'High Court',
                'region': 'Greater Accra',
                'location': 'Accra',
                'address': 'High Court Complex, Independence Avenue, Accra',
                'city': 'Accra',
                'district': 'Accra Metropolitan',
                'latitude': 5.6037,
                'longitude': -0.1870,
                'area_coverage': 'Greater Accra Region',
                'contact_phone': '+233 302 663 421',
                'is_active': True,
                'is_verified': True
            },
            {
                'name': 'Circuit Court - Kumasi',
                'registry_name': 'Circuit Court Registry Kumasi',
                'court_type': 'Circuit Court',
                'region': 'Ashanti',
                'location': 'Kumasi',
                'address': 'Circuit Court Building, Adum, Kumasi',
                'city': 'Kumasi',
                'district': 'Kumasi Metropolitan',
                'latitude': 6.6885,
                'longitude': -1.6244,
                'area_coverage': 'Ashanti Region',
                'contact_phone': '+233 322 202 456',
                'is_active': True,
                'is_verified': True
            },
            {
                'name': 'District Court - Tamale',
                'registry_name': 'District Court Registry Tamale',
                'court_type': 'District Court',
                'region': 'Northern',
                'location': 'Tamale',
                'address': 'District Court Building, Tamale',
                'city': 'Tamale',
                'district': 'Tamale Metropolitan',
                'latitude': 9.4008,
                'longitude': -0.8393,
                'area_coverage': 'Northern Region',
                'contact_phone': '+233 372 022 123',
                'is_active': True,
                'is_verified': True
            },
            {
                'name': 'Commercial Court - Accra',
                'registry_name': 'Commercial Court Registry',
                'court_type': 'Commercial Court',
                'region': 'Greater Accra',
                'location': 'Accra',
                'address': 'Commercial Court Building, Accra',
                'city': 'Accra',
                'district': 'Accra Metropolitan',
                'latitude': 5.6037,
                'longitude': -0.1870,
                'area_coverage': 'National',
                'contact_phone': '+233 302 663 421',
                'is_active': True,
                'is_verified': True
            }
        ]
        
        insert_sql = """
        INSERT INTO courts (
            name, registry_name, court_type, region, location, address, city, district,
            latitude, longitude, area_coverage, contact_phone, contact_email, website,
            is_active, is_verified
        ) VALUES (
            %(name)s, %(registry_name)s, %(court_type)s, %(region)s, %(location)s, 
            %(address)s, %(city)s, %(district)s, %(latitude)s, %(longitude)s, 
            %(area_coverage)s, %(contact_phone)s, %(contact_email)s, %(website)s,
            %(is_active)s, %(is_verified)s
        )
        """
        
        for court in sample_courts:
            cursor.execute(insert_sql, court)
        
        connection.commit()
        print("✅ Sample court data inserted successfully!")
        
    except Exception as e:
        print(f"❌ Error creating courts table: {e}")
        if connection:
            connection.rollback()
    finally:
        if connection:
            cursor.close()
            connection.close()

if __name__ == "__main__":
    create_courts_table()
