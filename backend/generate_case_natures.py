#!/usr/bin/env python3
"""
Script to generate case natures for all cases in the database using AI
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from sqlalchemy.orm import sessionmaker
from database import engine
from models.reported_cases import ReportedCases
from services.case_nature_service import CaseNatureService
from config import settings
import mysql.connector
from typing import Dict, Any
import time

# Database connection for direct SQL updates
DATABASE_CONFIG = {
    'host': settings.mysql_host,
    'port': settings.mysql_port,
    'user': settings.mysql_user,
    'password': settings.mysql_password,
    'database': settings.mysql_database
}

def get_cases_batch(offset: int = 0, limit: int = 100) -> list:
    """Get a batch of cases from the database"""
    Session = sessionmaker(bind=engine)
    session = Session()
    
    try:
        cases = session.query(ReportedCases).offset(offset).limit(limit).all()
        return [
            {
                'id': case.id,
                'title': case.title,
                'area_of_law': case.area_of_law,
                'case_summary': case.case_summary,
                'keywords_phrases': case.keywords_phrases,
                'decision': case.decision,
                'judgement': case.judgement,
                'conclusion': case.conclusion,
                'headnotes': case.headnotes,
                'commentary': case.commentary,
                'type': case.type
            }
            for case in cases
        ]
    finally:
        session.close()

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

def generate_all_case_natures():
    """Generate case natures for all cases in the database"""
    print("🚀 Starting case nature generation...")
    
    # Initialize the service
    service = CaseNatureService()
    
    # Get total count
    Session = sessionmaker(bind=engine)
    session = Session()
    total_cases = session.query(ReportedCases).count()
    session.close()
    
    print(f"📊 Total cases to process: {total_cases}")
    
    batch_size = 50  # Process in smaller batches
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
                time.sleep(0.1)
                
            except Exception as e:
                print(f"    ❌ Error processing case {case['id']}: {e}")
                failed += 1
                processed += 1
        
        # Progress update
        progress = (processed / total_cases) * 100
        print(f"📈 Progress: {processed}/{total_cases} ({progress:.1f}%) - ✅ {successful} successful, ❌ {failed} failed")
        
        # Longer delay between batches
        time.sleep(1)
    
    print(f"\n🎉 Case nature generation completed!")
    print(f"📊 Final stats:")
    print(f"   Total processed: {processed}")
    print(f"   Successful: {successful}")
    print(f"   Failed: {failed}")
    print(f"   Success rate: {(successful/processed*100):.1f}%" if processed > 0 else "   Success rate: 0%")

def generate_sample_natures():
    """Generate natures for a small sample of cases for testing"""
    print("🧪 Generating sample case natures...")
    
    service = CaseNatureService()
    cases = get_cases_batch(0, 10)  # Get first 10 cases
    
    print(f"📊 Processing {len(cases)} sample cases")
    
    for case in cases:
        print(f"\n🔍 Case {case['id']}: {case['title']}")
        print(f"   Area of law: {case['area_of_law']}")
        print(f"   Type: {case['type']}")
        
        nature = service.generate_case_nature(case)
        print(f"   Generated nature: {nature}")
        
        # Update database
        if update_case_nature(case['id'], nature):
            print(f"   ✅ Updated in database")
        else:
            print(f"   ❌ Failed to update")

if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description='Generate case natures using AI')
    parser.add_argument('--sample', action='store_true', help='Process only a sample of cases')
    parser.add_argument('--batch-size', type=int, default=50, help='Batch size for processing')
    
    args = parser.parse_args()
    
    if args.sample:
        generate_sample_natures()
    else:
        generate_all_case_natures()
