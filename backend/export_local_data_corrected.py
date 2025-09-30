import psycopg2
import json
import csv
from datetime import datetime

def export_data():
    # Connect to local PostgreSQL
    conn = psycopg2.connect(
        host='localhost',
        database='juridence',
        user='postgres',
        password='62579011'
    )
    cursor = conn.cursor()
    
    # Tables to export (using correct table names)
    tables = ['people', 'reported_cases', 'companies', 'banks', 'insurance', 'courts', 'judges', 'case_hearings']
    
    for table in tables:
        try:
            print(f'Exporting {table}...')
            
            # Get table structure
            cursor.execute(f"SELECT column_name, data_type FROM information_schema.columns WHERE table_name = '{table}' ORDER BY ordinal_position")
            columns = cursor.fetchall()
            column_names = [col[0] for col in columns]
            
            # Get all data
            cursor.execute(f"SELECT * FROM {table}")
            rows = cursor.fetchall()
            
            print(f'Found {len(rows)} rows in {table}')
            
            if len(rows) > 0:
                # Export to CSV
                with open(f'{table}_export.csv', 'w', newline='', encoding='utf-8') as csvfile:
                    writer = csv.writer(csvfile)
                    writer.writerow(column_names)
                    writer.writerows(rows)
                
                print(f'✅ Exported {len(rows)} rows to {table}_export.csv')
            
        except Exception as e:
            print(f'Error exporting {table}: {e}')
            continue
    
    conn.close()
    print('Export completed!')

if __name__ == '__main__':
    export_data()
