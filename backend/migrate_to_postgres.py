#!/usr/bin/env python3
"""
Database Migration Script: MySQL/SQLite to PostgreSQL
This script migrates all data from your existing MySQL/SQLite database to PostgreSQL.
"""

import os
import sys
import sqlite3
import pymysql
import psycopg2
from sqlalchemy import create_engine, text, inspect
from sqlalchemy.orm import sessionmaker
from urllib.parse import quote_plus
import json
from datetime import datetime

# Add current directory to path for imports
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from config import settings
from database import Base

class DatabaseMigrator:
    def __init__(self):
        self.postgres_engine = None
        self.source_engine = None
        self.source_type = None
        self.migration_log = []
        
    def log(self, message):
        """Log migration progress"""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        log_message = f"[{timestamp}] {message}"
        print(log_message)
        self.migration_log.append(log_message)
    
    def connect_to_postgres(self):
        """Connect to PostgreSQL database"""
        try:
            self.postgres_engine = create_engine(
                settings.database_url,
                echo=True
            )
            
            # Test connection
            with self.postgres_engine.connect() as conn:
                conn.execute(text("SELECT 1"))
            
            self.log("✅ Connected to PostgreSQL successfully")
            return True
        except Exception as e:
            self.log(f"❌ Failed to connect to PostgreSQL: {e}")
            return False
    
    def detect_source_database(self):
        """Detect and connect to source database (MySQL or SQLite)"""
        
        # Load environment variables
        from dotenv import load_dotenv
        load_dotenv()
        
        # Try SQLite first
        sqlite_path = os.path.join(os.path.dirname(__file__), '..', 'case_search.db')
        if os.path.exists(sqlite_path):
            try:
                # Check if SQLite database has data
                conn = sqlite3.connect(sqlite_path)
                cursor = conn.cursor()
                cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
                tables = cursor.fetchall()
                conn.close()
                
                if tables:
                    self.source_type = 'sqlite'
                    self.source_engine = create_engine(f'sqlite:///{sqlite_path}')
                    self.log(f"✅ Detected SQLite database with {len(tables)} tables")
                    return True
                else:
                    self.log("⚠️ SQLite database exists but is empty")
            except Exception as e:
                self.log(f"❌ Error accessing SQLite database: {e}")
        
        # Try MySQL
        try:
            # Check for MySQL connection details in environment or config
            mysql_config = {
                'host': os.getenv('MYSQL_HOST', 'localhost'),
                'port': int(os.getenv('MYSQL_PORT', 3306)),
                'user': os.getenv('MYSQL_USER', 'root'),
                'password': os.getenv('MYSQL_PASSWORD', ''),
                'database': os.getenv('MYSQL_DATABASE', 'juridence')
            }
            
            # Test MySQL connection
            connection = pymysql.connect(**mysql_config)
            cursor = connection.cursor()
            cursor.execute("SHOW TABLES")
            tables = cursor.fetchall()
            connection.close()
            
            if tables:
                self.source_type = 'mysql'
                mysql_url = f"mysql+pymysql://{mysql_config['user']}:{quote_plus(mysql_config['password'])}@{mysql_config['host']}:{mysql_config['port']}/{mysql_config['database']}"
                self.source_engine = create_engine(mysql_url)
                self.log(f"✅ Detected MySQL database with {len(tables)} tables")
                return True
            else:
                self.log("⚠️ MySQL database exists but is empty")
                
        except Exception as e:
            self.log(f"❌ Error accessing MySQL database: {e}")
        
        self.log("❌ No source database found with data")
        return False
    
    def create_postgres_tables(self):
        """Create all tables in PostgreSQL"""
        try:
            # Import all models to ensure they're registered
            from models.user import User
            from models.reported_cases import ReportedCases
            from models.people import People
            from models.companies import Companies
            from models.banks import Banks
            from models.insurance import Insurance
            from models.court import Court
            from models.subscription import Subscription
            from models.payment import Payment
            from models.notification import Notification
            from models.role import Role
            from models.tenant import Tenant
            from models.person_analytics import PersonAnalytics
            from models.bank_analytics import BankAnalytics
            from models.company_analytics import CompanyAnalytics
            from models.insurance_analytics import InsuranceAnalytics
            from models.logs import AccessLog, ActivityLog
            
            # Create all tables
            Base.metadata.create_all(self.postgres_engine)
            self.log("✅ Created all tables in PostgreSQL")
            return True
        except Exception as e:
            self.log(f"❌ Failed to create PostgreSQL tables: {e}")
            return False
    
    def get_table_data(self, table_name):
        """Get all data from a source table"""
        try:
            if self.source_type == 'sqlite':
                with self.source_engine.connect() as conn:
                    result = conn.execute(text(f"SELECT * FROM {table_name}"))
                    return result.fetchall()
            else:  # MySQL
                with self.source_engine.connect() as conn:
                    result = conn.execute(text(f"SELECT * FROM {table_name}"))
                    return result.fetchall()
        except Exception as e:
            self.log(f"⚠️ Could not read data from {table_name}: {e}")
            return []
    
    def migrate_table_data(self, table_name, model_class):
        """Migrate data from source table to PostgreSQL"""
        try:
            # Get source data
            source_data = self.get_table_data(table_name)
            
            if not source_data:
                self.log(f"⚠️ No data found in {table_name}")
                return True
            
            # Get column names
            if self.source_type == 'sqlite':
                with self.source_engine.connect() as conn:
                    result = conn.execute(text(f"PRAGMA table_info({table_name})"))
                    columns = [row[1] for row in result.fetchall()]
            else:  # MySQL
                with self.source_engine.connect() as conn:
                    result = conn.execute(text(f"DESCRIBE {table_name}"))
                    columns = [row[0] for row in result.fetchall()]
            
            # Create PostgreSQL session
            SessionLocal = sessionmaker(bind=self.postgres_engine)
            session = SessionLocal()
            
            migrated_count = 0
            for row in source_data:
                try:
                    # Create row data dictionary
                    row_data = dict(zip(columns, row))
                    
                    # Handle datetime fields
                    for key, value in row_data.items():
                        if isinstance(value, str) and 'T' in value:
                            try:
                                row_data[key] = datetime.fromisoformat(value.replace('Z', '+00:00'))
                            except:
                                pass
                    
                    # Create model instance
                    instance = model_class(**row_data)
                    session.add(instance)
                    migrated_count += 1
                    
                except Exception as e:
                    self.log(f"⚠️ Error migrating row in {table_name}: {e}")
                    continue
            
            session.commit()
            session.close()
            
            self.log(f"✅ Migrated {migrated_count} records from {table_name}")
            return True
            
        except Exception as e:
            self.log(f"❌ Failed to migrate {table_name}: {e}")
            return False
    
    def migrate_all_data(self):
        """Migrate all data from source to PostgreSQL"""
        
        # Define tables to migrate with their corresponding models
        tables_to_migrate = [
            ('users', User),
            ('reported_cases', ReportedCases),
            ('people', People),
            ('companies', Companies),
            ('banks', Banks),
            ('insurance', Insurance),
            ('courts', Court),
            ('subscriptions', Subscription),
            ('payments', Payment),
            ('notifications', Notification),
            ('roles', Role),
            ('tenants', Tenant),
            ('person_analytics', PersonAnalytics),
            ('bank_analytics', BankAnalytics),
            ('company_analytics', CompanyAnalytics),
            ('insurance_analytics', InsuranceAnalytics),
            ('access_logs', AccessLog),
            ('activity_logs', ActivityLog),
        ]
        
        total_tables = len(tables_to_migrate)
        successful_migrations = 0
        
        for table_name, model_class in tables_to_migrate:
            self.log(f"🔄 Migrating {table_name}...")
            if self.migrate_table_data(table_name, model_class):
                successful_migrations += 1
        
        self.log(f"✅ Migration completed: {successful_migrations}/{total_tables} tables migrated successfully")
        return successful_migrations == total_tables
    
    def save_migration_log(self):
        """Save migration log to file"""
        log_file = os.path.join(os.path.dirname(__file__), 'migration_log.txt')
        with open(log_file, 'w') as f:
            f.write('\n'.join(self.migration_log))
        self.log(f"📝 Migration log saved to {log_file}")
    
    def run_migration(self):
        """Run the complete migration process"""
        self.log("🚀 Starting database migration to PostgreSQL...")
        
        # Step 1: Connect to PostgreSQL
        if not self.connect_to_postgres():
            return False
        
        # Step 2: Detect and connect to source database
        if not self.detect_source_database():
            return False
        
        # Step 3: Create PostgreSQL tables
        if not self.create_postgres_tables():
            return False
        
        # Step 4: Migrate all data
        if not self.migrate_all_data():
            self.log("⚠️ Migration completed with some errors")
        
        # Step 5: Save migration log
        self.save_migration_log()
        
        self.log("🎉 Database migration completed!")
        return True

def main():
    """Main function to run the migration"""
    print("=" * 60)
    print("🗄️  DATABASE MIGRATION TOOL")
    print("   MySQL/SQLite → PostgreSQL")
    print("=" * 60)
    
    migrator = DatabaseMigrator()
    
    try:
        success = migrator.run_migration()
        if success:
            print("\n✅ Migration completed successfully!")
            print("🎯 Your PostgreSQL database is ready to use.")
        else:
            print("\n⚠️ Migration completed with some issues.")
            print("📝 Check the migration log for details.")
    except KeyboardInterrupt:
        print("\n⏹️ Migration cancelled by user.")
    except Exception as e:
        print(f"\n❌ Migration failed with error: {e}")
        migrator.log(f"❌ Migration failed: {e}")
        migrator.save_migration_log()

if __name__ == "__main__":
    main()
