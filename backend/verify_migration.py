#!/usr/bin/env python3
"""
Script to verify database migration status between MySQL and PostgreSQL
"""

import os
from dotenv import load_dotenv
import pymysql
from sqlalchemy import create_engine, text
from config import settings

def log(message):
    print(message)

def main():
    # Load environment variables
    load_dotenv()

    # MySQL Configuration
    MYSQL_HOST = os.getenv("MYSQL_HOST", "localhost")
    MYSQL_PORT = int(os.getenv("MYSQL_PORT", 3306))
    MYSQL_USER = os.getenv("MYSQL_USER", "root")
    MYSQL_PASSWORD = os.getenv("MYSQL_PASSWORD", "")
    MYSQL_DATABASE = os.getenv("MYSQL_DATABASE", "dennislaw_svd")

    log("🔍 COMPREHENSIVE DATABASE MIGRATION VERIFICATION")
    log("=" * 60)

    # Get MySQL tables and counts
    mysql_conn = pymysql.connect(
        host=MYSQL_HOST,
        port=MYSQL_PORT,
        user=MYSQL_USER,
        password=MYSQL_PASSWORD,
        database=MYSQL_DATABASE,
        charset='utf8mb4'
    )

    mysql_tables = {}
    with mysql_conn.cursor() as cursor:
        cursor.execute("SHOW TABLES")
        tables = cursor.fetchall()
        
        for table in tables:
            table_name = table[0]
            try:
                cursor.execute(f"SELECT COUNT(*) FROM `{table_name}`")
                count = cursor.fetchone()[0]
                mysql_tables[table_name] = count
            except Exception as e:
                log(f"Error counting {table_name}: {e}")
                mysql_tables[table_name] = 0

    mysql_conn.close()

    # Get PostgreSQL tables and counts
    postgres_engine = create_engine(settings.database_url)
    postgres_tables = {}

    with postgres_engine.connect() as conn:
        result = conn.execute(text("SELECT table_name FROM information_schema.tables WHERE table_schema = 'public' ORDER BY table_name"))
        tables = result.fetchall()
        
        for table in tables:
            table_name = table[0]
            try:
                result = conn.execute(text(f"SELECT COUNT(*) FROM {table_name}"))
                count = result.fetchone()[0]
                postgres_tables[table_name] = count
            except Exception as e:
                log(f"Error counting {table_name}: {e}")
                postgres_tables[table_name] = 0

    postgres_engine.dispose()

    log(f"📊 MIGRATION STATUS SUMMARY")
    log(f"MySQL Tables: {len(mysql_tables)}")
    log(f"PostgreSQL Tables: {len(postgres_tables)}")
    log("")

    # Compare tables
    all_tables = set(mysql_tables.keys()) | set(postgres_tables.keys())
    successful_migrations = []
    failed_migrations = []
    missing_tables = []
    extra_tables = []

    for table in sorted(all_tables):
        mysql_count = mysql_tables.get(table, 0)
        postgres_count = postgres_tables.get(table, 0)
        
        if table not in mysql_tables:
            extra_tables.append((table, postgres_count))
        elif table not in postgres_tables:
            missing_tables.append((table, mysql_count))
        elif mysql_count == postgres_count:
            successful_migrations.append((table, mysql_count, postgres_count))
        else:
            failed_migrations.append((table, mysql_count, postgres_count))

    log(f"✅ SUCCESSFUL MIGRATIONS ({len(successful_migrations)}):")
    log("-" * 50)
    for table, mysql_count, postgres_count in successful_migrations:
        log(f"  {table:<30} MySQL: {mysql_count:>8,} → PostgreSQL: {postgres_count:>8,} ✅")

    log("")
    log(f"❌ FAILED MIGRATIONS ({len(failed_migrations)}):")
    log("-" * 50)
    for table, mysql_count, postgres_count in failed_migrations:
        log(f"  {table:<30} MySQL: {mysql_count:>8,} → PostgreSQL: {postgres_count:>8,} ❌")

    log("")
    log(f"⚠️  MISSING TABLES ({len(missing_tables)}):")
    log("-" * 50)
    for table, mysql_count in missing_tables:
        log(f"  {table:<30} MySQL: {mysql_count:>8,} → PostgreSQL: Not Found ❌")

    log("")
    log(f"ℹ️  EXTRA TABLES ({len(extra_tables)}):")
    log("-" * 50)
    for table, postgres_count in extra_tables:
        log(f"  {table:<30} MySQL: Not Found → PostgreSQL: {postgres_count:>8,} ℹ️")

    log("")
    log(f"📈 MIGRATION SUMMARY:")
    log(f"  Total Tables: {len(all_tables)}")
    log(f"  Successful: {len(successful_migrations)}")
    log(f"  Failed: {len(failed_migrations)}")
    log(f"  Missing: {len(missing_tables)}")
    log(f"  Extra: {len(extra_tables)}")
    if len(mysql_tables) > 0:
        log(f"  Success Rate: {len(successful_migrations)/len(mysql_tables)*100:.1f}%")

    # Show pending migrations
    if missing_tables:
        log("")
        log("🔄 PENDING MIGRATIONS:")
        log("-" * 50)
        for table, mysql_count in missing_tables:
            log(f"  {table:<30} ({mysql_count:>8,} records)")

if __name__ == "__main__":
    main()
