#!/usr/bin/env python3
"""
Script to fetch ALL two_factor_auth data from MySQL to PostgreSQL
"""

import os
import sys
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from datetime import datetime
from dotenv import load_dotenv
import pymysql
import json

# Load environment variables
load_dotenv()

# MySQL Configuration
MYSQL_HOST = os.getenv("MYSQL_HOST", "localhost")
MYSQL_PORT = int(os.getenv("MYSQL_PORT", 3306))
MYSQL_USER = os.getenv("MYSQL_USER", "root")
MYSQL_PASSWORD = os.getenv("MYSQL_PASSWORD", "")
MYSQL_DATABASE = os.getenv("MYSQL_DATABASE", "dennislaw_svd")

# PostgreSQL Configuration
from config import settings

def log(message):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"[{timestamp}] {message}")

def get_mysql_connection():
    """Establishes and returns a connection to the MySQL database."""
    return pymysql.connect(
        host=MYSQL_HOST,
        port=MYSQL_PORT,
        user=MYSQL_USER,
        password=MYSQL_PASSWORD,
        database=MYSQL_DATABASE,
        cursorclass=pymysql.cursors.DictCursor
    )

def get_postgres_engine():
    """Creates and returns a SQLAlchemy engine for the PostgreSQL database."""
    return create_engine(settings.database_url)

def safe_convert_date(date_value):
    """Safely converts date values from MySQL to PostgreSQL format."""
    if isinstance(date_value, datetime):
        return date_value
    if isinstance(date_value, str):
        try:
            return datetime.fromisoformat(date_value)
        except ValueError:
            pass
    return None

def safe_convert_json(json_value):
    """Safely converts JSON strings to Python objects."""
    if isinstance(json_value, str):
        try:
            return json.loads(json_value)
        except json.JSONDecodeError:
            return json_value
    return json_value

def safe_convert_boolean(bool_value):
    """Safely converts MySQL TINYINT(1) to PostgreSQL boolean."""
    if isinstance(bool_value, int):
        return bool(bool_value)
    return bool_value

def fetch_and_insert_two_factor_auth_data():
    log("============================================================")
    log("🔄 Migrating 'two_factor_auth' table from MySQL to PostgreSQL")
    log("============================================================")

    mysql_conn = None
    postgres_engine = None
    try:
        mysql_conn = get_mysql_connection()
        mysql_cursor = mysql_conn.cursor()
        postgres_engine = get_postgres_engine()

        log("✅ Connected to both MySQL and PostgreSQL databases")

        # Check if two_factor_auth table exists in MySQL
        mysql_cursor.execute("SHOW TABLES LIKE 'two_factor_auth'")
        if not mysql_cursor.fetchone():
            log("❌ Table 'two_factor_auth' not found in MySQL database")
            return

        # Get table structure from MySQL
        mysql_cursor.execute("DESCRIBE two_factor_auth")
        columns = mysql_cursor.fetchall()
        column_names = [col['Field'] for col in columns]
        
        log(f"📋 Found table 'two_factor_auth' with {len(columns)} columns")
        log(f"📋 Columns: {', '.join(column_names)}")

        # Count total records in MySQL
        mysql_cursor.execute("SELECT COUNT(*) as count FROM two_factor_auth")
        total_count = mysql_cursor.fetchone()['count']
        log(f"📊 Total records to migrate: {total_count:,}")

        if total_count == 0:
            log("ℹ️ No records found in MySQL two_factor_auth table")
            return

        # Create table if it doesn't exist and clear existing data
        with postgres_engine.connect() as conn:
            # Check if table exists
            result = conn.execute(text("SELECT EXISTS (SELECT FROM information_schema.tables WHERE table_name = 'two_factor_auth')"))
            table_exists = result.fetchone()[0]
            
            if not table_exists:
                log("📋 Creating two_factor_auth table in PostgreSQL...")
                # Import and create the table using SQLAlchemy models
                from database import Base
                from models.two_factor_auth import TwoFactorAuth
                Base.metadata.create_all(postgres_engine, tables=[TwoFactorAuth.__table__])
                log("✅ Created two_factor_auth table in PostgreSQL")
            else:
                # Clear existing data
                conn.execute(text("DELETE FROM two_factor_auth"))
                conn.commit()
                log("🗑️ Cleared existing two_factor_auth data in PostgreSQL")

        # Fetch data in batches from MySQL
        batch_size = 1000
        offset = 0
        total_inserted = 0

        while offset < total_count:
            log(f"🔄 Fetching batch {offset//batch_size + 1} (records {offset + 1} to {min(offset + batch_size, total_count)})")
            
            mysql_cursor.execute(f"SELECT * FROM two_factor_auth LIMIT {batch_size} OFFSET {offset}")
            batch_records = mysql_cursor.fetchall()

            if not batch_records:
                break

            # Prepare data for insertion
            data_to_insert = []
            for record in batch_records:
                # Convert dates and JSON as needed
                record_dict = {}
                for col_name, value in record.items():
                    if value is None:
                        record_dict[col_name] = None
                    elif 'date' in col_name.lower() or 'created' in col_name.lower() or 'updated' in col_name.lower() or 'last' in col_name.lower():
                        record_dict[col_name] = safe_convert_date(value) or value
                    elif isinstance(value, str) and value.startswith('{'):
                        record_dict[col_name] = safe_convert_json(value)
                    elif col_name.lower() in ['is_enabled', 'is_processed', 'is_verified', 'is_public', 'is_read', 'is_sent', 'is_email', 'is_sms', 'is_push', 'is_email_sent', 'is_sms_sent', 'is_push_sent', 'is_system_permission', 'is_system_role', 'is_public_setting', 'is_encrypted', 'is_required', 'is_editable', 'is_popular', 'is_featured', 'is_unlimited', 'is_trial_available', 'is_approved', 'is_rejected', 'is_pending', 'is_completed', 'is_cancelled', 'is_trial', 'is_auto_renew', 'is_paused', 'is_suspended', 'is_deleted', 'is_default', 'sms_verified', 'email_verified']:
                        record_dict[col_name] = safe_convert_boolean(value)
                    else:
                        record_dict[col_name] = value
                
                data_to_insert.append(record_dict)

            # Insert batch into PostgreSQL
            if data_to_insert:
                # Insert records one by one with individual transactions to handle errors better
                successful_inserts = 0
                for record in data_to_insert:
                    try:
                        with postgres_engine.connect() as conn:
                            # Prepare values for insertion
                            values = []
                            for col_name in column_names:
                                value = record.get(col_name)
                                # Handle special data types
                                if isinstance(value, datetime):
                                    values.append(value)
                                elif isinstance(value, dict) or isinstance(value, list):
                                    values.append(json.dumps(value))
                                elif isinstance(value, str) and value.lower() in ['null', 'none']:
                                    values.append(None)
                                elif col_name.lower() in ['is_enabled', 'is_processed', 'is_verified', 'is_public', 'is_read', 'is_sent', 'is_email', 'is_sms', 'is_push', 'is_email_sent', 'is_sms_sent', 'is_push_sent', 'is_system_permission', 'is_system_role', 'is_public_setting', 'is_encrypted', 'is_required', 'is_editable', 'is_popular', 'is_featured', 'is_unlimited', 'is_trial_available', 'is_approved', 'is_rejected', 'is_pending', 'is_completed', 'is_cancelled', 'is_trial', 'is_auto_renew', 'is_paused', 'is_suspended', 'is_deleted', 'is_default', 'sms_verified', 'email_verified']:
                                    # Convert integer to boolean for PostgreSQL
                                    if isinstance(value, int):
                                        values.append(bool(value))
                                    elif isinstance(value, str):
                                        values.append(value.lower() in ['true', '1', 'yes'])
                                    else:
                                        values.append(bool(value) if value is not None else None)
                                else:
                                    values.append(value)
                            
                            # Create insert statement with named parameters
                            placeholders = ', '.join([f':{col}' for col in column_names])
                            columns_str = ', '.join(column_names)
                            insert_sql = f"INSERT INTO two_factor_auth ({columns_str}) VALUES ({placeholders})"
                            
                            # Create parameter dictionary
                            params = {col: values[i] for i, col in enumerate(column_names)}
                            
                            # Execute insert
                            conn.execute(text(insert_sql), params)
                            conn.commit()
                            successful_inserts += 1
                            
                    except Exception as e:
                        log(f"⚠️ Warning: Failed to insert record {record.get('id', 'unknown')}: {e}")
                        continue
                
                total_inserted += successful_inserts
                log(f"✅ Inserted {successful_inserts} records (Total: {total_inserted:,}/{total_count:,})")

            offset += batch_size

        log("============================================================")
        log(f"🎉 SUCCESSFULLY MIGRATED TWO FACTOR AUTH DATA!")
        log(f"📊 Total records migrated: {total_inserted:,}")
        log("============================================================")

    except Exception as e:
        log(f"❌ Error during migration: {e}")
        import traceback
        traceback.print_exc()
    finally:
        if mysql_conn:
            mysql_conn.close()
        if postgres_engine:
            postgres_engine.dispose()

if __name__ == "__main__":
    fetch_and_insert_two_factor_auth_data()
