import psycopg2
import json
import csv
from datetime import datetime

def migrate_all_tables():
    # Connect to local PostgreSQL
    local_conn = psycopg2.connect(
        host='localhost',
        database='juridence',
        user='postgres',
        password='62579011'
    )
    local_cursor = local_conn.cursor()
    
    # Connect to server PostgreSQL
    server_conn = psycopg2.connect(
        host='localhost',
        database='juridence_db',
        user='juridence_user',
        password='juridence_password123'
    )
    server_cursor = server_conn.cursor()
    
    # Get all tables from local database
    local_cursor.execute("""
        SELECT table_name 
        FROM information_schema.tables 
        WHERE table_schema = 'public' 
        AND table_type = 'BASE TABLE'
        ORDER BY table_name;
    """)
    
    tables = [row[0] for row in local_cursor.fetchall()]
    print(f'Found {len(tables)} tables to migrate:')
    for table in tables:
        print(f'  - {table}')
    
    # Increase CSV field size limit
    csv.field_size_limit(1000000)
    
    for table in tables:
        try:
            print(f'\n🔄 Migrating {table}...')
            
            # Get table structure from local
            local_cursor.execute(f"SELECT column_name, data_type FROM information_schema.columns WHERE table_name = '{table}' ORDER BY ordinal_position")
            columns = local_cursor.fetchall()
            column_names = [col[0] for col in columns]
            
            # Get all data from local
            local_cursor.execute(f"SELECT * FROM {table}")
            rows = local_cursor.fetchall()
            
            print(f'  Found {len(rows)} rows in {table}')
            
            if len(rows) > 0:
                # Clear existing data in server
                server_cursor.execute(f"DELETE FROM {table}")
                server_conn.commit()
                
                # Insert data in batches
                batch_size = 50 if table in ['reported_cases', 'case_hearings'] else 100
                batch = []
                row_count = 0
                
                for row in rows:
                    try:
                        # Process the row
                        processed_row = []
                        for i, value in enumerate(row):
                            if value is None or value == '':
                                processed_row.append(None)
                            elif value and (str(value).startswith('[') or str(value).startswith('{')):
                                try:
                                    # Handle JSON fields
                                    value_str = str(value)
                                    if value_str.startswith('[') and value_str.endswith(']'):
                                        # Fix single quotes in JSON
                                        if "'" in value_str and '"' not in value_str:
                                            value_str = value_str.replace("'", '"')
                                        
                                        # Try to parse as Python literal and convert to JSON
                                        import ast
                                        parsed = ast.literal_eval(value_str)
                                        processed_row.append(json.dumps(parsed))
                                    else:
                                        # Try to parse as JSON
                                        json.loads(value_str)
                                        processed_row.append(value_str)
                                except:
                                    # If all else fails, store as string
                                    processed_row.append(str(value))
                            else:
                                processed_row.append(value)
                        
                        batch.append(processed_row)
                        
                        # Insert batch when it reaches batch_size
                        if len(batch) >= batch_size:
                            try:
                                columns_str = ', '.join(column_names)
                                placeholders = ', '.join(['%s'] * len(column_names))
                                insert_sql = f"INSERT INTO {table} ({columns_str}) VALUES ({placeholders})"
                                server_cursor.executemany(insert_sql, batch)
                                server_conn.commit()
                                row_count += len(batch)
                                print(f'    Inserted {len(batch)} rows (total: {row_count})')
                                batch = []
                            except Exception as e:
                                print(f'    Error inserting batch: {e}')
                                server_conn.rollback()
                                batch = []
                                continue
                        
                    except Exception as e:
                        print(f'    Error processing row: {e}')
                        continue
                
                # Insert remaining batch
                if batch:
                    try:
                        columns_str = ', '.join(column_names)
                        placeholders = ', '.join(['%s'] * len(column_names))
                        insert_sql = f"INSERT INTO {table} ({columns_str}) VALUES ({placeholders})"
                        server_cursor.executemany(insert_sql, batch)
                        server_conn.commit()
                        row_count += len(batch)
                        print(f'    Inserted {len(batch)} rows (total: {row_count})')
                    except Exception as e:
                        print(f'    Error inserting final batch: {e}')
                        server_conn.rollback()
                
                print(f'✅ Migrated {row_count} rows to {table}')
            
        except Exception as e:
            print(f'❌ Error migrating {table}: {e}')
            continue
    
    # Close connections
    local_conn.close()
    server_conn.close()
    print('\n🎉 Migration completed!')

if __name__ == '__main__':
    migrate_all_tables()
