#!/usr/bin/env python3
"""
Script to generate analytics for people who don't have them yet.
This can be run to backfill analytics for existing people in the database.
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from database import get_db
from services.auto_analytics_generator import AutoAnalyticsGenerator
from models.people import People
from models.person_analytics import PersonAnalytics
from models.person_case_statistics import PersonCaseStatistics
from sqlalchemy.orm import Session
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def generate_missing_analytics():
    """Generate analytics for people who don't have them yet"""
    try:
        # Get database session
        db = next(get_db())
        
        # Find people without analytics
        people_with_analytics = db.query(PersonAnalytics.person_id).subquery()
        people_without_analytics = db.query(People).filter(
            ~People.id.in_(people_with_analytics)
        ).all()
        
        logger.info(f"Found {len(people_without_analytics)} people without analytics")
        
        if not people_without_analytics:
            logger.info("All people already have analytics generated")
            return
        
        # Initialize analytics generator
        generator = AutoAnalyticsGenerator(db)
        
        # Generate analytics for each person
        successful = 0
        failed = 0
        errors = []
        
        for i, person in enumerate(people_without_analytics, 1):
            try:
                logger.info(f"Processing person {i}/{len(people_without_analytics)}: {person.full_name} (ID: {person.id})")
                generator.generate_analytics_for_person(person.id)
                successful += 1
                logger.info(f"✓ Analytics generated for {person.full_name}")
            except Exception as e:
                failed += 1
                error_msg = f"Person {person.id} ({person.full_name}): {str(e)}"
                errors.append(error_msg)
                logger.error(f"✗ Failed to generate analytics for {person.full_name}: {str(e)}")
        
        # Summary
        logger.info(f"\n=== ANALYTICS GENERATION SUMMARY ===")
        logger.info(f"Total people processed: {len(people_without_analytics)}")
        logger.info(f"Successful: {successful}")
        logger.info(f"Failed: {failed}")
        
        if errors:
            logger.info(f"\nErrors encountered:")
            for error in errors[:10]:  # Show first 10 errors
                logger.info(f"  - {error}")
            if len(errors) > 10:
                logger.info(f"  ... and {len(errors) - 10} more errors")
        
        # Check final status
        people_with_analytics_after = db.query(PersonAnalytics).count()
        people_with_case_stats_after = db.query(PersonCaseStatistics).count()
        total_people = db.query(People).count()
        
        logger.info(f"\n=== FINAL STATUS ===")
        logger.info(f"Total people in database: {total_people}")
        logger.info(f"People with analytics: {people_with_analytics_after}")
        logger.info(f"People with case statistics: {people_with_case_stats_after}")
        logger.info(f"Analytics coverage: {(people_with_analytics_after / total_people * 100):.1f}%")
        logger.info(f"Case stats coverage: {(people_with_case_stats_after / total_people * 100):.1f}%")
        
    except Exception as e:
        logger.error(f"Fatal error in analytics generation: {str(e)}")
        raise
    finally:
        db.close()

def regenerate_all_analytics():
    """Regenerate analytics for all people in the database"""
    try:
        # Get database session
        db = next(get_db())
        
        # Get all people
        all_people = db.query(People).all()
        logger.info(f"Regenerating analytics for {len(all_people)} people")
        
        # Initialize analytics generator
        generator = AutoAnalyticsGenerator(db)
        
        # Regenerate analytics for each person
        successful = 0
        failed = 0
        errors = []
        
        for i, person in enumerate(all_people, 1):
            try:
                logger.info(f"Processing person {i}/{len(all_people)}: {person.full_name} (ID: {person.id})")
                generator.generate_analytics_for_person(person.id)
                successful += 1
                logger.info(f"✓ Analytics regenerated for {person.full_name}")
            except Exception as e:
                failed += 1
                error_msg = f"Person {person.id} ({person.full_name}): {str(e)}"
                errors.append(error_msg)
                logger.error(f"✗ Failed to regenerate analytics for {person.full_name}: {str(e)}")
        
        # Summary
        logger.info(f"\n=== ANALYTICS REGENERATION SUMMARY ===")
        logger.info(f"Total people processed: {len(all_people)}")
        logger.info(f"Successful: {successful}")
        logger.info(f"Failed: {failed}")
        
        if errors:
            logger.info(f"\nErrors encountered:")
            for error in errors[:10]:  # Show first 10 errors
                logger.info(f"  - {error}")
            if len(errors) > 10:
                logger.info(f"  ... and {len(errors) - 10} more errors")
        
    except Exception as e:
        logger.error(f"Fatal error in analytics regeneration: {str(e)}")
        raise
    finally:
        db.close()

if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="Generate analytics for people")
    parser.add_argument("--regenerate-all", action="store_true", 
                       help="Regenerate analytics for all people (not just missing ones)")
    parser.add_argument("--person-id", type=int, 
                       help="Generate analytics for a specific person ID")
    
    args = parser.parse_args()
    
    if args.person_id:
        # Generate analytics for a specific person
        try:
            db = next(get_db())
            generator = AutoAnalyticsGenerator(db)
            generator.generate_analytics_for_person(args.person_id)
            logger.info(f"Analytics generated for person {args.person_id}")
        except Exception as e:
            logger.error(f"Failed to generate analytics for person {args.person_id}: {str(e)}")
        finally:
            db.close()
    elif args.regenerate_all:
        # Regenerate all analytics
        regenerate_all_analytics()
    else:
        # Generate missing analytics only
        generate_missing_analytics()
