#!/usr/bin/env python3
"""
Simple script to generate case natures for all cases in the database using AI
"""

import mysql.connector
from services.case_nature_service import CaseNatureService
from config import settings
import time

# Database connection
DATABASE_CONFIG = {
    'host': settings.mysql_host,
    'port': settings.mysql_port,
    'user': settings.mysql_user,
    'password': settings.mysql_password,
    'database': settings.mysql_database
}

def get_cases_batch(offset: int = 0, limit: int = 100) -> list:
    """Get a batch of cases from the database using direct SQL"""
    try:
        connection = mysql.connector.connect(**DATABASE_CONFIG)
        cursor = connection.cursor(dictionary=True)
        
        query = """
        SELECT id, title, area_of_law, case_summary, keywords_phrases, 
               decision, judgement, conclusion, headnotes, commentary, type
        FROM reported_cases 
        ORDER BY id 
        LIMIT %s OFFSET %s
        """
        
        cursor.execute(query, (limit, offset))
        cases = cursor.fetchall()
        
        return cases
    except Exception as e:
        print(f"Error fetching cases: {e}")
        return []
    finally:
        if connection and connection.is_connected():
            cursor.close()
            connection.close()

def update_case_nature(case_id: int, nature: str) -> bool:
    """Update case nature in the database"""
    try:
        connection = mysql.connector.connect(**DATABASE_CONFIG)
        cursor = connection.cursor()
        
        # Update the case with the generated nature
        update_query = """
        UPDATE reported_cases 
        SET area_of_law = %s 
        WHERE id = %s
        """
        
        cursor.execute(update_query, (nature, case_id))
        connection.commit()
        
        return True
    except Exception as e:
        print(f"Error updating case {case_id}: {e}")
        return False
    finally:
        if connection and connection.is_connected():
            cursor.close()
            connection.close()

def get_total_cases() -> int:
    """Get total number of cases"""
    try:
        connection = mysql.connector.connect(**DATABASE_CONFIG)
        cursor = connection.cursor()
        
        cursor.execute("SELECT COUNT(*) FROM reported_cases")
        total = cursor.fetchone()[0]
        
        return total
    except Exception as e:
        print(f"Error getting total cases: {e}")
        return 0
    finally:
        if connection and connection.is_connected():
            cursor.close()
            connection.close()

def generate_sample_natures():
    """Generate natures for a small sample of cases for testing"""
    print("🧪 Generating sample case natures...")
    
    service = CaseNatureService()
    cases = get_cases_batch(0, 5)  # Get first 5 cases
    
    print(f"📊 Processing {len(cases)} sample cases")
    
    for case in cases:
        print(f"\n🔍 Case {case['id']}: {case['title'][:50]}...")
        print(f"   Current area_of_law: {case['area_of_law']}")
        print(f"   Type: {case['type']}")
        
        nature = service.generate_case_nature(case)
        print(f"   Generated nature: {nature}")
        
        # Update database
        if update_case_nature(case['id'], nature):
            print(f"   ✅ Updated in database")
        else:
            print(f"   ❌ Failed to update")

def generate_all_case_natures():
    """Generate case natures for all cases in the database"""
    print("🚀 Starting case nature generation...")
    
    # Initialize the service
    service = CaseNatureService()
    
    # Get total count
    total_cases = get_total_cases()
    print(f"📊 Total cases to process: {total_cases}")
    
    batch_size = 20  # Process in smaller batches
    processed = 0
    successful = 0
    failed = 0
    
    for offset in range(0, total_cases, batch_size):
        print(f"\n📦 Processing batch {offset//batch_size + 1} (cases {offset+1}-{min(offset+batch_size, total_cases)})")
        
        # Get batch of cases
        cases = get_cases_batch(offset, batch_size)
        
        if not cases:
            break
            
        # Process each case in the batch
        for case in cases:
            try:
                print(f"  🔍 Processing case {case['id']}: {case['title'][:50]}...")
                
                # Skip if already has area_of_law
                if case['area_of_law'] and case['area_of_law'].strip() and case['area_of_law'] != 'N/A':
                    print(f"    ⏭️  Skipping - already has nature: {case['area_of_law']}")
                    processed += 1
                    continue
                
                # Generate nature
                nature = service.generate_case_nature(case)
                print(f"    ✅ Generated nature: {nature}")
                
                # Update database
                if update_case_nature(case['id'], nature):
                    successful += 1
                    print(f"    💾 Updated in database")
                else:
                    failed += 1
                    print(f"    ❌ Failed to update database")
                
                processed += 1
                
                # Add small delay to avoid rate limiting
                time.sleep(0.2)
                
            except Exception as e:
                print(f"    ❌ Error processing case {case['id']}: {e}")
                failed += 1
                processed += 1
        
        # Progress update
        progress = (processed / total_cases) * 100
        print(f"📈 Progress: {processed}/{total_cases} ({progress:.1f}%) - ✅ {successful} successful, ❌ {failed} failed")
        
        # Longer delay between batches
        time.sleep(2)
    
    print(f"\n🎉 Case nature generation completed!")
    print(f"📊 Final stats:")
    print(f"   Total processed: {processed}")
    print(f"   Successful: {successful}")
    print(f"   Failed: {failed}")
    print(f"   Success rate: {(successful/processed*100):.1f}%" if processed > 0 else "   Success rate: 0%")

if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description='Generate case natures using AI')
    parser.add_argument('--sample', action='store_true', help='Process only a sample of cases')
    
    args = parser.parse_args()
    
    if args.sample:
        generate_sample_natures()
    else:
        generate_all_case_natures()
