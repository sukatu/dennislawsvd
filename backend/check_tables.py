import psycopg2

def check_tables():
    # Connect to local PostgreSQL
    conn = psycopg2.connect(
        host='localhost',
        database='juridence',
        user='postgres',
        password='62579011'
    )
    cursor = conn.cursor()
    
    # Get all tables
    cursor.execute("""
        SELECT table_name 
        FROM information_schema.tables 
        WHERE table_schema = 'public' 
        ORDER BY table_name;
    """)
    
    tables = cursor.fetchall()
    print(f'Found {len(tables)} tables:')
    for table in tables:
        print(f'  - {table[0]}')
    
    conn.close()

if __name__ == '__main__':
    check_tables()
