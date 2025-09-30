import psycopg2
import json
import csv
from datetime import datetime

def export_all_tables():
    # Connect to local PostgreSQL
    conn = psycopg2.connect(
        host='localhost',
        database='juridence',
        user='postgres',
        password='62579011'
    )
    cursor = conn.cursor()
    
    # All tables from your server database
    tables = [
        'access_logs', 'activity_logs', 'ai_chat_sessions', 'api_keys', 'audit_logs',
        'bank_analytics', 'bank_case_statistics', 'banks', 'billing_summary',
        'case_hearings', 'case_mentions', 'case_metadata', 'case_search_index',
        'companies', 'company_analytics', 'company_case_statistics', 'court_types',
        'courts', 'error_logs', 'insurance', 'insurance_analytics', 'insurance_case_statistics',
        'judges', 'legal_history', 'legal_search_index', 'login_sessions',
        'notification_preferences', 'notifications', 'payments', 'people',
        'permissions', 'person_analytics', 'person_case_statistics', 'reported_cases',
        'request_details', 'roles', 'security_events', 'security_logs', 'settings',
        'subscription_plans', 'subscription_requests', 'subscriptions', 'tenant_settings',
        'tenants', 'two_factor_auth', 'usage_records', 'usage_tracking', 'user_roles', 'users'
    ]
    
    # Increase CSV field size limit
    csv.field_size_limit(1000000)
    
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
            
            print(f'  Found {len(rows)} rows in {table}')
            
            if len(rows) > 0:
                # Export to CSV
                with open(f'{table}_export.csv', 'w', newline='', encoding='utf-8') as csvfile:
                    writer = csv.writer(csvfile)
                    writer.writerow(column_names)
                    writer.writerows(rows)
                
                print(f'  ✅ Exported {len(rows)} rows to {table}_export.csv')
            else:
                print(f'  ⚠️ No data in {table}')
            
        except Exception as e:
            print(f'  ❌ Error exporting {table}: {e}')
            continue
    
    conn.close()
    print('\n🎉 Export completed!')

if __name__ == '__main__':
    export_all_tables()
