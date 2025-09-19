#!/usr/bin/env python3
"""
Robust Database Migration Script: MySQL to PostgreSQL
This script handles data type conversion and transaction management properly.
"""

import os
import sys
import pymysql
import psycopg2
from psycopg2.extras import RealDictCursor
from urllib.parse import quote_plus
import json
from datetime import datetime
from dotenv import load_dotenv
import re

# Load environment variables
load_dotenv()

class RobustDatabaseMigrator:
    def __init__(self):
        self.mysql_conn = None
        self.postgres_conn = None
        self.migration_log = []
        
    def log(self, message):
        """Log migration progress"""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        log_message = f"[{timestamp}] {message}"
        print(log_message)
        self.migration_log.append(log_message)
    
    def connect_to_mysql(self):
        """Connect to MySQL database"""
        try:
            config = {
                'host': os.getenv('MYSQL_HOST', 'localhost'),
                'port': int(os.getenv('MYSQL_PORT', 3306)),
                'user': os.getenv('MYSQL_USER', 'root'),
                'password': os.getenv('MYSQL_PASSWORD', ''),
                'database': os.getenv('MYSQL_DATABASE', 'dennislaw_svd')
            }
            
            self.mysql_conn = pymysql.connect(**config)
            self.log("✅ Connected to MySQL successfully")
            return True
        except Exception as e:
            self.log(f"❌ Failed to connect to MySQL: {e}")
            return False
    
    def connect_to_postgres(self):
        """Connect to PostgreSQL database"""
        try:
            config = {
                'host': os.getenv('POSTGRES_HOST', 'localhost'),
                'port': int(os.getenv('POSTGRES_PORT', 5432)),
                'user': os.getenv('POSTGRES_USER', 'postgres'),
                'password': os.getenv('POSTGRES_PASSWORD', '62579011'),
                'database': os.getenv('POSTGRES_DATABASE', 'juridence')
            }
            
            self.postgres_conn = psycopg2.connect(**config)
            self.postgres_conn.autocommit = False  # Use manual transactions
            self.log("✅ Connected to PostgreSQL successfully")
            return True
        except Exception as e:
            self.log(f"❌ Failed to connect to PostgreSQL: {e}")
            return False
    
    def get_mysql_tables(self):
        """Get list of tables from MySQL"""
        try:
            cursor = self.mysql_conn.cursor()
            cursor.execute("SHOW TABLES")
            tables = [table[0] for table in cursor.fetchall()]
            cursor.close()
            return tables
        except Exception as e:
            self.log(f"❌ Failed to get MySQL tables: {e}")
            return []
    
    def get_table_columns(self, table_name):
        """Get column information for a table"""
        try:
            cursor = self.mysql_conn.cursor()
            cursor.execute(f"DESCRIBE {table_name}")
            columns = cursor.fetchall()
            cursor.close()
            return columns
        except Exception as e:
            self.log(f"❌ Failed to get columns for {table_name}: {e}")
            return []
    
    def get_table_count(self, table_name):
        """Get count of records in table"""
        try:
            cursor = self.mysql_conn.cursor()
            cursor.execute(f"SELECT COUNT(*) FROM {table_name}")
            count = cursor.fetchone()[0]
            cursor.close()
            return count
        except Exception as e:
            self.log(f"❌ Failed to get count for {table_name}: {e}")
            return 0
    
    def get_table_data_batch(self, table_name, offset=0, limit=1000):
        """Get data from MySQL table in batches"""
        try:
            cursor = self.mysql_conn.cursor(pymysql.cursors.DictCursor)
            cursor.execute(f"SELECT * FROM {table_name} LIMIT {limit} OFFSET {offset}")
            data = cursor.fetchall()
            cursor.close()
            return data
        except Exception as e:
            self.log(f"❌ Failed to get data from {table_name}: {e}")
            return []
    
    def convert_mysql_type_to_postgres(self, mysql_type, col_name, col_key, col_extra):
        """Convert MySQL data type to PostgreSQL"""
        mysql_type = mysql_type.lower()
        
        # Handle integers
        if 'tinyint(1)' in mysql_type:
            return 'BOOLEAN'
        elif 'int' in mysql_type:
            if 'auto_increment' in col_extra.lower():
                return 'SERIAL PRIMARY KEY'
            return 'INTEGER'
        
        # Handle strings
        elif 'varchar' in mysql_type:
            # Extract length if specified
            match = re.search(r'varchar\((\d+)\)', mysql_type)
            if match:
                length = min(int(match.group(1)), 255)  # Cap at 255 for safety
                return f'VARCHAR({length})'
            return 'VARCHAR(255)'
        elif 'char' in mysql_type:
            match = re.search(r'char\((\d+)\)', mysql_type)
            if match:
                length = min(int(match.group(1)), 255)
                return f'CHAR({length})'
            return 'CHAR(1)'
        elif 'text' in mysql_type:
            return 'TEXT'
        
        # Handle dates and times
        elif 'datetime' in mysql_type:
            return 'TIMESTAMP'
        elif 'date' in mysql_type:
            return 'DATE'
        elif 'time' in mysql_type:
            return 'TIME'
        elif 'timestamp' in mysql_type:
            return 'TIMESTAMP'
        
        # Handle numbers
        elif 'float' in mysql_type or 'double' in mysql_type:
            return 'REAL'
        elif 'decimal' in mysql_type or 'numeric' in mysql_type:
            return 'DECIMAL'
        
        # Handle JSON
        elif 'json' in mysql_type:
            return 'JSONB'
        
        # Handle boolean
        elif 'boolean' in mysql_type or 'bool' in mysql_type:
            return 'BOOLEAN'
        
        # Handle binary
        elif 'blob' in mysql_type or 'binary' in mysql_type:
            return 'BYTEA'
        
        # Default to text for unknown types
        else:
            return 'TEXT'
    
    def create_postgres_table_from_mysql(self, table_name, columns):
        """Create PostgreSQL table based on MySQL structure"""
        try:
            cursor = self.postgres_conn.cursor()
            
            # Drop table if exists
            cursor.execute(f"DROP TABLE IF EXISTS {table_name} CASCADE")
            
            # Build CREATE TABLE statement
            column_definitions = []
            primary_keys = []
            
            for col in columns:
                col_name = col[0]
                col_type = col[1]
                col_null = col[2]
                col_key = col[3]
                col_default = col[4]
                col_extra = col[5]
                
                # Convert MySQL type to PostgreSQL
                pg_type = self.convert_mysql_type_to_postgres(col_type, col_name, col_key, col_extra)
                
                # Handle primary key
                if col_key == 'PRI':
                    if 'SERIAL PRIMARY KEY' in pg_type:
                        # Already handled in type conversion
                        pass
                    else:
                        pg_type += ' PRIMARY KEY'
                    primary_keys.append(col_name)
                
                # Handle NOT NULL
                if col_null == 'NO' and col_key != 'PRI' and 'PRIMARY KEY' not in pg_type:
                    pg_type += ' NOT NULL'
                
                column_definitions.append(f"{col_name} {pg_type}")
            
            create_sql = f"CREATE TABLE {table_name} ({', '.join(column_definitions)})"
            cursor.execute(create_sql)
            
            self.log(f"✅ Created PostgreSQL table: {table_name}")
            return True
            
        except Exception as e:
            self.log(f"❌ Failed to create PostgreSQL table {table_name}: {e}")
            self.postgres_conn.rollback()
            return False
    
    def clean_data_for_postgres(self, data):
        """Clean data for PostgreSQL insertion"""
        cleaned_data = []
        for row in data:
            cleaned_row = {}
            for key, value in row.items():
                if value is None:
                    cleaned_row[key] = None
                elif isinstance(value, datetime):
                    cleaned_row[key] = value.isoformat()
                elif isinstance(value, str):
                    # Handle problematic string values
                    if value in ['VIEW', 'CREATE', 'UPDATE', 'DELETE', 'LOGIN', 'LOGOUT']:
                        # These might be enum values that should be treated as strings
                        cleaned_row[key] = value
                    else:
                        # Escape single quotes and handle other special characters
                        cleaned_row[key] = value.replace("'", "''")
                elif isinstance(value, (int, float)):
                    cleaned_row[key] = value
                elif isinstance(value, bool):
                    cleaned_row[key] = value
                else:
                    # Convert everything else to string
                    cleaned_row[key] = str(value)
            cleaned_data.append(cleaned_row)
        return cleaned_data
    
    def insert_data_to_postgres(self, table_name, data):
        """Insert data into PostgreSQL table"""
        if not data:
            return True
            
        try:
            cursor = self.postgres_conn.cursor()
            
            # Clean data first
            cleaned_data = self.clean_data_for_postgres(data)
            
            # Get column names from first row
            columns = list(cleaned_data[0].keys())
            placeholders = ', '.join(['%s'] * len(columns))
            insert_sql = f"INSERT INTO {table_name} ({', '.join(columns)}) VALUES ({placeholders})"
            
            # Prepare data for insertion
            values_list = []
            for row in cleaned_data:
                values = []
                for col in columns:
                    value = row[col]
                    # Handle None values and datetime strings
                    if value is None:
                        values.append(None)
                    elif isinstance(value, str) and 'T' in value and ('+' in value or 'Z' in value):
                        # Try to parse as datetime
                        try:
                            dt = datetime.fromisoformat(value.replace('Z', '+00:00'))
                            values.append(dt)
                        except:
                            values.append(value)
                    else:
                        values.append(value)
                values_list.append(tuple(values))
            
            # Insert data in batches
            batch_size = 100
            for i in range(0, len(values_list), batch_size):
                batch = values_list[i:i + batch_size]
                cursor.executemany(insert_sql, batch)
            
            return True
            
        except Exception as e:
            self.log(f"❌ Failed to insert data into {table_name}: {e}")
            self.postgres_conn.rollback()
            return False
    
    def migrate_table(self, table_name):
        """Migrate a single table from MySQL to PostgreSQL"""
        self.log(f"🔄 Migrating table: {table_name}")
        
        try:
            # Start transaction
            self.postgres_conn.commit()  # End any previous transaction
            
            # Get table structure
            columns = self.get_table_columns(table_name)
            if not columns:
                return False
            
            # Create PostgreSQL table
            if not self.create_postgres_table_from_mysql(table_name, columns):
                return False
            
            # Get total count
            total_count = self.get_table_count(table_name)
            self.log(f"📊 Table {table_name} has {total_count} records")
            
            if total_count == 0:
                self.postgres_conn.commit()
                return True
            
            # Migrate data in batches
            batch_size = 1000
            offset = 0
            total_inserted = 0
            
            while offset < total_count:
                data = self.get_table_data_batch(table_name, offset, batch_size)
                if not data:
                    break
                
                if not self.insert_data_to_postgres(table_name, data):
                    return False
                
                total_inserted += len(data)
                offset += batch_size
                
                # Commit batch
                self.postgres_conn.commit()
                self.log(f"✅ Inserted {total_inserted}/{total_count} records into {table_name}")
            
            self.log(f"✅ Successfully migrated {total_inserted} records to {table_name}")
            return True
            
        except Exception as e:
            self.log(f"❌ Failed to migrate table {table_name}: {e}")
            self.postgres_conn.rollback()
            return False
    
    def migrate_all_data(self):
        """Migrate all tables from MySQL to PostgreSQL"""
        tables = self.get_mysql_tables()
        if not tables:
            self.log("❌ No tables found in MySQL database")
            return False
        
        self.log(f"📋 Found {len(tables)} tables to migrate")
        
        # Migrate each table
        successful_migrations = 0
        for table_name in tables:
            if self.migrate_table(table_name):
                successful_migrations += 1
        
        self.log(f"✅ Migration completed: {successful_migrations}/{len(tables)} tables migrated successfully")
        return successful_migrations == len(tables)
    
    def save_migration_log(self):
        """Save migration log to file"""
        log_file = os.path.join(os.path.dirname(__file__), 'robust_migration_log.txt')
        with open(log_file, 'w') as f:
            f.write('\n'.join(self.migration_log))
        self.log(f"📝 Migration log saved to {log_file}")
    
    def run_migration(self):
        """Run the complete migration process"""
        self.log("🚀 Starting robust database migration to PostgreSQL...")
        
        # Connect to databases
        if not self.connect_to_mysql():
            return False
        
        if not self.connect_to_postgres():
            return False
        
        # Migrate all data
        success = self.migrate_all_data()
        
        # Save migration log
        self.save_migration_log()
        
        # Close connections
        if self.mysql_conn:
            self.mysql_conn.close()
        if self.postgres_conn:
            self.postgres_conn.close()
        
        return success

def main():
    """Main function to run the migration"""
    print("=" * 60)
    print("🗄️  ROBUST DATABASE MIGRATION TOOL")
    print("   MySQL → PostgreSQL")
    print("=" * 60)
    
    migrator = RobustDatabaseMigrator()
    
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
