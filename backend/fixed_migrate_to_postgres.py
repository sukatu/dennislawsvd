#!/usr/bin/env python3
"""
Fixed migration script that handles boolean and date type conversions properly
"""

import os
import sys
from sqlalchemy import create_engine, text, inspect, MetaData, Table, Column
from sqlalchemy.dialects import postgresql, mysql
from sqlalchemy.types import Integer, String, Text, DateTime, Boolean, Float, DECIMAL, JSON, Date, Time
from datetime import datetime, date, time
from dotenv import load_dotenv
import pymysql
import json

# Load environment variables
load_dotenv()

# --- Source Database Configuration (MySQL) ---
MYSQL_HOST = os.getenv("MYSQL_HOST", "localhost")
MYSQL_PORT = int(os.getenv("MYSQL_PORT", 3306))
MYSQL_USER = os.getenv("MYSQL_USER", "root")
MYSQL_PASSWORD = os.getenv("MYSQL_PASSWORD", "")
MYSQL_DATABASE = os.getenv("MYSQL_DATABASE", "dennislaw_svd")

# --- Target Database Configuration (PostgreSQL) ---
POSTGRES_HOST = os.getenv("POSTGRES_HOST", "localhost")
POSTGRES_PORT = int(os.getenv("POSTGRES_PORT", 5432))
POSTGRES_USER = os.getenv("POSTGRES_USER", "postgres")
POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD", "")
POSTGRES_DATABASE = os.getenv("POSTGRES_DATABASE", "juridence")

POSTGRES_URL = f"postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_DATABASE}"

def log(message):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"[{timestamp}] {message}")

def get_mysql_engine():
    """Creates and returns a SQLAlchemy engine for the MySQL database."""
    from urllib.parse import quote_plus
    password = quote_plus(MYSQL_PASSWORD)
    mysql_url = f"mysql+pymysql://{MYSQL_USER}:{password}@{MYSQL_HOST}:{MYSQL_PORT}/{MYSQL_DATABASE}"
    return create_engine(mysql_url)

def get_postgres_engine():
    """Creates and returns a SQLAlchemy engine for the PostgreSQL database."""
    return create_engine(POSTGRES_URL)

def convert_value_for_postgres(value, mysql_col_type, pg_col_type):
    """Converts a value from MySQL type to a compatible PostgreSQL type."""
    if value is None:
        return None

    # Convert MySQL TINYINT(1) to Python bool for PostgreSQL BOOLEAN
    if isinstance(mysql_col_type, mysql.TINYINT) and mysql_col_type.display_width == 1:
        return bool(value) if value is not None else None
    
    # Convert MySQL ENUM to string for PostgreSQL TEXT
    if isinstance(mysql_col_type, mysql.ENUM):
        return str(value) if value is not None else None

    # Handle boolean columns that might be stored as integers
    if isinstance(pg_col_type, postgresql.BOOLEAN):
        if isinstance(value, (int, str)):
            return str(value).lower() in ('1', 'true', 'yes', 'on')
        return bool(value) if value is not None else None

    # Handle datetime/date/time objects if they are strings
    if isinstance(pg_col_type, (postgresql.TIMESTAMP, postgresql.DATE)):
        if isinstance(value, str):
            try:
                if 'T' in value:  # ISO datetime format
                    return datetime.fromisoformat(value.replace('Z', '+00:00'))
                else:  # Date format
                    return date.fromisoformat(value)
            except ValueError:
                log(f"⚠️  Warning: Could not convert string '{value}' to {pg_col_type} type. Setting to NULL.")
                return None
    elif isinstance(pg_col_type, postgresql.TIME):
        if isinstance(value, str):
            try:
                return time.fromisoformat(value)
            except ValueError:
                log(f"⚠️  Warning: Could not convert string '{value}' to {pg_col_type} type. Setting to NULL.")
                return None
            
    # Handle JSON strings that might need parsing
    if isinstance(pg_col_type, postgresql.JSONB) and isinstance(value, str):
        try:
            return json.loads(value)
        except json.JSONDecodeError:
            log(f"⚠️  Warning: Could not parse JSON string '{value}'. Keeping as string.")
            return value

    return value

def migrate_table_with_type_conversion(mysql_engine, postgres_engine, table_name):
    """Migrates data for a single table with proper type conversion"""
    log(f"🔄 Migrating table: {table_name}")
    
    mysql_conn = mysql_engine.connect()
    postgres_conn = postgres_engine.connect()
    
    try:
        # Reflect the table from the MySQL database
        mysql_metadata = MetaData()
        mysql_table = Table(table_name, mysql_metadata, autoload_with=mysql_engine)

        # Drop table in PostgreSQL if it exists (for clean re-runs)
        postgres_metadata = MetaData()
        if postgres_engine.dialect.has_table(postgres_conn, table_name):
            log(f"🗑️  Dropping existing PostgreSQL table: {table_name}")
            Table(table_name, postgres_metadata, autoload_with=postgres_engine).drop(postgres_engine)

        # Create the table in PostgreSQL with proper type mapping
        columns = []
        column_type_map = {}
        
        for col in mysql_table.columns:
            # Map MySQL types to PostgreSQL types
            if isinstance(col.type, mysql.VARCHAR):
                pg_type = postgresql.VARCHAR(col.type.length)
            elif isinstance(col.type, mysql.TEXT):
                pg_type = postgresql.TEXT
            elif isinstance(col.type, mysql.INTEGER):
                pg_type = postgresql.INTEGER
            elif isinstance(col.type, mysql.BIGINT):
                pg_type = postgresql.BIGINT
            elif isinstance(col.type, mysql.SMALLINT):
                pg_type = postgresql.SMALLINT
            elif isinstance(col.type, mysql.TINYINT):
                if col.type.display_width == 1:
                    pg_type = postgresql.BOOLEAN  # TINYINT(1) is usually boolean
                else:
                    pg_type = postgresql.SMALLINT
            elif isinstance(col.type, mysql.BOOLEAN):
                pg_type = postgresql.BOOLEAN
            elif isinstance(col.type, mysql.DATETIME):
                pg_type = postgresql.TIMESTAMP
            elif isinstance(col.type, mysql.TIMESTAMP):
                pg_type = postgresql.TIMESTAMP
            elif isinstance(col.type, mysql.DATE):
                pg_type = postgresql.DATE
            elif isinstance(col.type, mysql.TIME):
                pg_type = postgresql.TIME
            elif isinstance(col.type, mysql.FLOAT):
                pg_type = postgresql.REAL
            elif isinstance(col.type, mysql.DOUBLE):
                pg_type = postgresql.DOUBLE_PRECISION
            elif isinstance(col.type, mysql.DECIMAL):
                pg_type = postgresql.DECIMAL(col.type.precision, col.type.scale)
            elif isinstance(col.type, mysql.JSON):
                pg_type = postgresql.JSONB
            elif isinstance(col.type, mysql.ENUM):
                pg_type = postgresql.TEXT  # Convert ENUM to TEXT
            else:
                log(f"⚠️  Warning: Unhandled MySQL type: {col.type}. Defaulting to TEXT.")
                pg_type = postgresql.TEXT
            
            column_type_map[col.name] = {'mysql_type': col.type, 'pg_type': pg_type}
            
            # Handle autoincrement for primary keys
            if col.primary_key and col.autoincrement:
                columns.append(Column(col.name, pg_type, primary_key=True, autoincrement=True))
            else:
                columns.append(Column(col.name, pg_type, primary_key=col.primary_key, nullable=col.nullable))
        
        postgres_table = Table(table_name, postgres_metadata, *columns)
        postgres_metadata.create_all(postgres_engine, tables=[postgres_table])
        log(f"✅ Created PostgreSQL table: {table_name}")

        # Fetch data from MySQL
        select_stmt = mysql_table.select()
        result = mysql_conn.execute(select_stmt)
        rows = result.fetchall()

        if rows:
            log(f"📊 Table {table_name} has {len(rows)} records")
            data_to_insert = []
            
            for row in rows:
                row_dict = {}
                for col_name, value in row._mapping.items():
                    types = column_type_map.get(col_name)
                    if types:
                        converted_value = convert_value_for_postgres(value, types['mysql_type'], types['pg_type'])
                        row_dict[col_name] = converted_value
                    else:
                        row_dict[col_name] = value
                data_to_insert.append(row_dict)

            # Insert data into PostgreSQL in chunks
            chunk_size = 1000
            for i in range(0, len(data_to_insert), chunk_size):
                chunk = data_to_insert[i:i + chunk_size]
                with postgres_conn.begin():
                    insert_stmt = postgres_table.insert()
                    postgres_conn.execute(insert_stmt, chunk)
                log(f"✅ Inserted {min(i + chunk_size, len(data_to_insert))}/{len(data_to_insert)} records into {table_name}")
            
            log(f"✅ Successfully migrated {len(rows)} records to {table_name}")
            return True
        else:
            log(f"ℹ️ No data found in {table_name} to migrate.")
            return True
            
    except Exception as e:
        log(f"❌ Failed to migrate table {table_name}: {e}")
        return False
    finally:
        mysql_conn.close()
        postgres_conn.close()

def main_fixed_migrate():
    log("============================================================")
    log("🗄️  FIXED DATABASE MIGRATION TOOL")
    log("   MySQL → PostgreSQL (with type conversion)")
    log("============================================================")
    log("🚀 Starting fixed database migration to PostgreSQL...")

    mysql_engine = None
    postgres_engine = None
    successful_migrations = 0
    total_tables = 0

    try:
        mysql_engine = get_mysql_engine()
        mysql_engine.connect()
        log("✅ Connected to MySQL successfully")
    except Exception as e:
        log(f"❌ Failed to connect to MySQL: {e}")
        return

    try:
        postgres_engine = get_postgres_engine()
        postgres_engine.connect()
        log("✅ Connected to PostgreSQL successfully")
    except Exception as e:
        log(f"❌ Failed to connect to PostgreSQL: {e}")
        return

    # Key tables to migrate (prioritize important ones)
    priority_tables = [
        'users', 'people', 'companies', 'banks', 'insurance', 
        'reported_cases', 'courts', 'case_hearings', 'subscriptions'
    ]
    
    try:
        inspector = inspect(mysql_engine)
        all_tables = inspector.get_table_names()
        
        # First migrate priority tables
        log(f"📋 Migrating priority tables first...")
        for table_name in priority_tables:
            if table_name in all_tables:
                if migrate_table_with_type_conversion(mysql_engine, postgres_engine, table_name):
                    successful_migrations += 1
                    total_tables += 1
        
        # Then migrate remaining tables
        remaining_tables = [t for t in all_tables if t not in priority_tables]
        log(f"📋 Migrating remaining {len(remaining_tables)} tables...")
        
        for table_name in remaining_tables:
            if migrate_table_with_type_conversion(mysql_engine, postgres_engine, table_name):
                successful_migrations += 1
                total_tables += 1

    except Exception as e:
        log(f"❌ An error occurred during migration process: {e}")
    finally:
        if mysql_engine:
            mysql_engine.dispose()
        if postgres_engine:
            postgres_engine.dispose()
        
        log(f"✅ Migration completed: {successful_migrations}/{total_tables} tables migrated successfully")
        print(f"\n🎉 Fixed migration completed!")
        print(f"📝 Check the database for your real MySQL data.")

if __name__ == "__main__":
    main_fixed_migrate()
