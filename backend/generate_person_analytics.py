#!/usr/bin/env python3
"""
Script to generate person analytics for all persons in the database
"""

import os
import sys
import asyncio
from sqlalchemy.orm import Session
from database import get_db
from models.people import People
from services.person_analytics_service import PersonAnalyticsService

async def generate_analytics_for_all_persons():
    """Generate analytics for all persons in the database"""
    print("🚀 Starting person analytics generation...")
    
    # Get database session
    db = next(get_db())
    
    try:
        # Get all persons
        persons = db.query(People).all()
        total_persons = len(persons)
        print(f"📊 Found {total_persons} persons to process")
        
        if total_persons == 0:
            print("✅ No persons found. Exiting.")
            return
        
        # Initialize analytics service
        analytics_service = PersonAnalyticsService(db)
        
        processed_count = 0
        success_count = 0
        error_count = 0
        
        for person in persons:
            processed_count += 1
            print(f"\n🔍 Processing person {processed_count}/{total_persons}: {person.full_name} (ID: {person.id})...")
            
            try:
                analytics = await analytics_service.generate_analytics_for_person(person.id)
                if analytics:
                    success_count += 1
                    print(f"   ✅ Analytics generated - Risk: {analytics.risk_level} ({analytics.risk_score}%), Financial: {analytics.financial_risk_level}")
                else:
                    error_count += 1
                    print(f"   ❌ Failed to generate analytics")
            except Exception as e:
                error_count += 1
                print(f"   ❌ Error: {str(e)}")
            
            # Progress update every 10 persons
            if processed_count % 10 == 0:
                print(f"\n📈 Progress: {processed_count}/{total_persons} - ✅ {success_count} successful, ❌ {error_count} failed")
        
        print(f"\n🎉 Person analytics generation complete!")
        print(f"📊 Final stats:")
        print(f"   Total processed: {processed_count}")
        print(f"   Successful: {success_count}")
        print(f"   Failed: {error_count}")
        print(f"   Success rate: {(success_count/processed_count)*100:.1f}%")
        
    except Exception as e:
        print(f"❌ Error during analytics generation: {e}")
    finally:
        db.close()

if __name__ == "__main__":
    asyncio.run(generate_analytics_for_all_persons())
