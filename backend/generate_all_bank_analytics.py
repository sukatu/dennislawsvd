#!/usr/bin/env python3
"""
Script to generate analytics and statistics for all banks in the database.
This will populate the bank_analytics and bank_case_statistics tables with data for all banks.
"""

import sys
import os
from sqlalchemy.orm import sessionmaker
from database import engine
from models.banks import Banks
from services.bank_analytics_service import BankAnalyticsService
import logging
from datetime import datetime

# Add the parent directory to the sys.path to allow importing models and database
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Load environment variables
from dotenv import load_dotenv
load_dotenv()

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(levelname)s:%(name)s:%(message)s')
logger = logging.getLogger(__name__)

def generate_all_bank_analytics():
    """Generate analytics and statistics for all banks in the database."""
    logger.info("Starting bulk bank analytics generation...")
    
    # Create a session
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    db = SessionLocal()
    
    try:
        # Get all active banks
        banks = db.query(Banks).filter(Banks.is_active == True).all()
        total_banks = len(banks)
        logger.info(f"Found {total_banks} active banks to process")
        
        if total_banks == 0:
            logger.warning("No active banks found in database")
            return
        
        # Initialize the analytics service
        analytics_service = BankAnalyticsService(db)
        
        # Track progress
        processed = 0
        errors = 0
        start_time = datetime.now()
        
        for i, bank in enumerate(banks, 1):
            try:
                logger.info(f"Processing bank {i}/{total_banks}: {bank.name} (ID: {bank.id})")
                
                # Generate analytics
                analytics = analytics_service.generate_bank_analytics(bank.id)
                if analytics:
                    logger.info(f"  ✅ Analytics generated for {bank.name}")
                else:
                    logger.warning(f"  ⚠️  No analytics generated for {bank.name}")
                
                # Generate statistics
                statistics = analytics_service.generate_bank_case_statistics(bank.id)
                if statistics:
                    logger.info(f"  ✅ Statistics generated for {bank.name}")
                else:
                    logger.warning(f"  ⚠️  No statistics generated for {bank.name}")
                
                processed += 1
                
                # Commit after each bank to ensure data is saved
                db.commit()
                
                # Progress update every 5 banks
                if i % 5 == 0:
                    elapsed = datetime.now() - start_time
                    rate = i / elapsed.total_seconds() if elapsed.total_seconds() > 0 else 0
                    logger.info(f"Progress: {i}/{total_banks} banks processed ({rate:.1f} banks/sec)")
                
            except Exception as e:
                logger.error(f"  ❌ Error processing {bank.name} (ID: {bank.id}): {str(e)}")
                errors += 1
                # Rollback this bank's changes but continue with others
                db.rollback()
                continue
        
        # Final summary
        elapsed = datetime.now() - start_time
        logger.info("=" * 60)
        logger.info("BULK ANALYTICS GENERATION COMPLETE")
        logger.info("=" * 60)
        logger.info(f"Total banks processed: {processed}")
        logger.info(f"Errors encountered: {errors}")
        logger.info(f"Total time: {elapsed}")
        logger.info(f"Average rate: {processed / elapsed.total_seconds():.1f} banks/sec" if elapsed.total_seconds() > 0 else "N/A")
        
        if errors > 0:
            logger.warning(f"⚠️  {errors} banks had errors during processing")
        else:
            logger.info("🎉 All banks processed successfully!")
            
    except Exception as e:
        logger.error(f"❌ Fatal error during bulk processing: {str(e)}", exc_info=True)
        db.rollback()
        sys.exit(1)
    finally:
        db.close()

def verify_analytics_data():
    """Verify that analytics data was generated for all banks."""
    logger.info("Verifying analytics data...")
    
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    db = SessionLocal()
    
    try:
        from models.bank_analytics import BankAnalytics
        from models.bank_case_statistics import BankCaseStatistics
        
        # Count banks with analytics
        analytics_count = db.query(BankAnalytics).count()
        stats_count = db.query(BankCaseStatistics).count()
        
        logger.info(f"Banks with analytics data: {analytics_count}")
        logger.info(f"Banks with statistics data: {stats_count}")
        
        # Get some sample data
        sample_analytics = db.query(BankAnalytics).limit(3).all()
        sample_stats = db.query(BankCaseStatistics).limit(3).all()
        
        logger.info("Sample analytics data:")
        for analytics in sample_analytics:
            logger.info(f"  Bank ID {analytics.bank_id}: Risk Level {analytics.risk_level}, Score {analytics.risk_score}")
        
        logger.info("Sample statistics data:")
        for stats in sample_stats:
            logger.info(f"  Bank ID {stats.bank_id}: {stats.total_cases} cases, Outcome {stats.case_outcome}")
            
    except Exception as e:
        logger.error(f"Error verifying data: {str(e)}")
    finally:
        db.close()

if __name__ == "__main__":
    logger.info("🚀 Starting bulk bank analytics generation...")
    generate_all_bank_analytics()
    verify_analytics_data()
    logger.info("✅ Bulk analytics generation completed!")
