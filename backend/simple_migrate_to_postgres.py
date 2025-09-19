#!/usr/bin/env python3
"""
Simple Database Migration Script: MySQL to PostgreSQL
This script migrates data directly without complex table creation.
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

# Load environment variables
load_dotenv()

class SimpleDatabaseMigrator:
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
    
    def get_table_data(self, table_name, limit=1000):
        """Get data from MySQL table"""
        try:
            cursor = self.mysql_conn.cursor(pymysql.cursors.DictCursor)
            cursor.execute(f"SELECT * FROM {table_name} LIMIT {limit}")
            data = cursor.fetchall()
            cursor.close()
            return data
        except Exception as e:
            self.log(f"❌ Failed to get data from {table_name}: {e}")
            return []
    
    def create_postgres_table_from_mysql(self, table_name, columns):
        """Create PostgreSQL table based on MySQL structure"""
        try:
            cursor = self.postgres_conn.cursor()
            
            # Drop table if exists
            cursor.execute(f"DROP TABLE IF EXISTS {table_name} CASCADE")
            
            # Build CREATE TABLE statement
            column_definitions = []
            for col in columns:
                col_name = col[0]
                col_type = col[1]
                col_null = col[2]
                col_key = col[3]
                col_default = col[4]
                col_extra = col[5]
                
                # Convert MySQL types to PostgreSQL
                if 'int' in col_type.lower():
                    pg_type = 'INTEGER'
                elif 'varchar' in col_type.lower():
                    pg_type = 'VARCHAR(255)'
                elif 'text' in col_type.lower():
                    pg_type = 'TEXT'
                elif 'datetime' in col_type.lower():
                    pg_type = 'TIMESTAMP'
                elif 'date' in col_type.lower():
                    pg_type = 'DATE'
                elif 'time' in col_type.lower():
                    pg_type = 'TIME'
                elif 'float' in col_type.lower() or 'double' in col_type.lower():
                    pg_type = 'REAL'
                elif 'decimal' in col_type.lower():
                    pg_type = 'DECIMAL'
                elif 'json' in col_type.lower():
                    pg_type = 'JSONB'
                elif 'boolean' in col_type.lower() or 'tinyint(1)' in col_type.lower():
                    pg_type = 'BOOLEAN'
                else:
                    pg_type = 'TEXT'
                
                # Handle primary key
                if col_key == 'PRI':
                    pg_type += ' PRIMARY KEY'
                
                # Handle auto increment
                if 'auto_increment' in col_extra.lower():
                    pg_type = pg_type.replace('INTEGER', 'SERIAL')
                    if 'PRIMARY KEY' not in pg_type:
                        pg_type += ' PRIMARY KEY'
                
                # Handle NOT NULL
                if col_null == 'NO' and col_key != 'PRI':
                    pg_type += ' NOT NULL'
                
                column_definitions.append(f"{col_name} {pg_type}")
            
            create_sql = f"CREATE TABLE {table_name} ({', '.join(column_definitions)})"
            cursor.execute(create_sql)
            self.postgres_conn.commit()
            cursor.close()
            
            self.log(f"✅ Created PostgreSQL table: {table_name}")
            return True
            
        except Exception as e:
            self.log(f"❌ Failed to create PostgreSQL table {table_name}: {e}")
            return False
    
    def insert_data_to_postgres(self, table_name, data):
        """Insert data into PostgreSQL table"""
        if not data:
            return True
            
        try:
            cursor = self.postgres_conn.cursor()
            
            # Get column names from first row
            columns = list(data[0].keys())
            placeholders = ', '.join(['%s'] * len(columns))
            insert_sql = f"INSERT INTO {table_name} ({', '.join(columns)}) VALUES ({placeholders})"
            
            # Prepare data for insertion
            values_list = []
            for row in data:
                values = []
                for col in columns:
                    value = row[col]
                    # Handle None values and datetime objects
                    if value is None:
                        values.append(None)
                    elif isinstance(value, datetime):
                        values.append(value.isoformat())
                    else:
                        values.append(str(value))
                values_list.append(tuple(values))
            
            # Insert data in batches
            batch_size = 100
            for i in range(0, len(values_list), batch_size):
                batch = values_list[i:i + batch_size]
                cursor.executemany(insert_sql, batch)
            
            self.postgres_conn.commit()
            cursor.close()
            
            self.log(f"✅ Inserted {len(data)} records into {table_name}")
            return True
            
        except Exception as e:
            self.log(f"❌ Failed to insert data into {table_name}: {e}")
            return False
    
    def migrate_table(self, table_name):
        """Migrate a single table from MySQL to PostgreSQL"""
        self.log(f"🔄 Migrating table: {table_name}")
        
        # Get table structure
        columns = self.get_table_columns(table_name)
        if not columns:
            return False
        
        # Create PostgreSQL table
        if not self.create_postgres_table_from_mysql(table_name, columns):
            return False
        
        # Get and insert data
        data = self.get_table_data(table_name)
        if data:
            if not self.insert_data_to_postgres(table_name, data):
                return False
        
        return True
    
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
        log_file = os.path.join(os.path.dirname(__file__), 'simple_migration_log.txt')
        with open(log_file, 'w') as f:
            f.write('\n'.join(self.migration_log))
        self.log(f"📝 Migration log saved to {log_file}")
    
    def run_migration(self):
        """Run the complete migration process"""
        self.log("🚀 Starting simple database migration to PostgreSQL...")
        
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
    print("🗄️  SIMPLE DATABASE MIGRATION TOOL")
    print("   MySQL → PostgreSQL")
    print("=" * 60)
    
    migrator = SimpleDatabaseMigrator()
    
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
