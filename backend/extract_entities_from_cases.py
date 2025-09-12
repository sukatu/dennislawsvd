#!/usr/bin/env python3
"""
Entity Extraction Script
Extracts people, banks, and insurance companies from case titles and populates respective tables
"""

from database import get_db
from services.entity_extraction_service import EntityExtractionService
import time

def main():
    print("🚀 Starting Entity Extraction from Legal Cases")
    print("=" * 60)
    
    # Get database session
    db = next(get_db())
    
    try:
        # Initialize extraction service
        extraction_service = EntityExtractionService(db)
        
        # Start extraction
        start_time = time.time()
        
        results = extraction_service.extract_all_entities()
        
        end_time = time.time()
        duration = end_time - start_time
        
        # Print results
        print("\n" + "=" * 60)
        print("✅ ENTITY EXTRACTION COMPLETED SUCCESSFULLY!")
        print("=" * 60)
        print(f"📊 EXTRACTION RESULTS:")
        print(f"   🏦 Banks extracted: {results['banks']:,}")
        print(f"   🛡️ Insurance companies extracted: {results['insurance']:,}")
        print(f"   👥 People extracted: {results['people']:,}")
        print(f"   ⏱️ Total time: {duration:.2f} seconds")
        print("=" * 60)
        
        # Verify extraction
        print("\n🔍 VERIFICATION:")
        
        from sqlalchemy import text
        
        # Count banks
        bank_count = db.execute(text("SELECT COUNT(*) FROM banks")).scalar()
        print(f"   Banks in database: {bank_count:,}")
        
        # Count insurance
        insurance_count = db.execute(text("SELECT COUNT(*) FROM insurance")).scalar()
        print(f"   Insurance companies in database: {insurance_count:,}")
        
        # Count people
        people_count = db.execute(text("SELECT COUNT(*) FROM people")).scalar()
        print(f"   People in database: {people_count:,}")
        
        # Show sample data
        print("\n📋 SAMPLE DATA:")
        
        # Sample banks
        banks = db.execute(text("SELECT name, city, bank_type FROM banks LIMIT 5")).fetchall()
        print("   Sample Banks:")
        for bank in banks:
            print(f"     • {bank[0]} ({bank[1]}) - {bank[2]}")
        
        # Sample insurance
        insurance = db.execute(text("SELECT name, city, insurance_type FROM insurance LIMIT 5")).fetchall()
        print("   Sample Insurance Companies:")
        for ins in insurance:
            print(f"     • {ins[0]} ({ins[1]}) - {ins[2]}")
        
        # Sample people
        people = db.execute(text("SELECT full_name, occupation, city FROM people LIMIT 5")).fetchall()
        print("   Sample People:")
        for person in people:
            print(f"     • {person[0]} ({person[1]}) - {person[2]}")
        
        print("\n🎉 Entity extraction completed successfully!")
        print("   All entities are now ready for legal history search!")
        
    except Exception as e:
        print(f"❌ Error during extraction: {e}")
        db.rollback()
        raise
    finally:
        db.close()

if __name__ == "__main__":
    main()
