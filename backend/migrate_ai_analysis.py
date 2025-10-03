#!/usr/bin/env python3
"""
Database migration script to add AI analysis to all existing cases.
This script processes all cases in the reported_cases table and generates
AI-powered financial impact, detailed outcome, court orders, and case outcome.
"""

import os
import sys
import logging
from datetime import datetime
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker

# Add the backend directory to the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__))))

from config import settings
from services.ai_case_analysis_service import AICaseAnalysisService

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('ai_analysis_migration.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

def check_database_connection():
    """Check if database connection is working"""
    try:
        engine = create_engine(settings.database_url)
        with engine.connect() as conn:
            result = conn.execute(text("SELECT 1"))
            logger.info("Database connection successful")
            return True
    except Exception as e:
        logger.error(f"Database connection failed: {e}")
        return False

def check_openai_config():
    """Check if OpenAI configuration is available"""
    try:
        # Check environment variable
        if os.getenv('OPENAI_API_KEY'):
            logger.info("OpenAI API key found in environment variables")
            return True
        
        # Check database settings
        engine = create_engine(settings.database_url)
        SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
        db = SessionLocal()
        
        try:
            from models.settings import Settings
            settings_record = db.query(Settings).filter(Settings.key == 'openai_api_key').first()
            if settings_record and settings_record.value:
                logger.info("OpenAI API key found in database settings")
                return True
        except Exception as e:
            logger.warning(f"Could not check database settings: {e}")
        finally:
            db.close()
        
        logger.error("OpenAI API key not found in environment variables or database settings")
        return False
        
    except Exception as e:
        logger.error(f"Error checking OpenAI configuration: {e}")
        return False

def get_case_count(db):
    """Get total number of cases to process"""
    try:
        from models.reported_cases import ReportedCases
        total_cases = db.query(ReportedCases).count()
        return total_cases
    except Exception as e:
        logger.error(f"Error getting case count: {e}")
        return 0

def get_analyzed_case_count(db):
    """Get number of cases already analyzed"""
    try:
        from models.reported_cases import ReportedCases
        analyzed_cases = db.query(ReportedCases).filter(
            ReportedCases.ai_detailed_outcome.isnot(None),
            ReportedCases.ai_detailed_outcome != ''
        ).count()
        return analyzed_cases
    except Exception as e:
        logger.error(f"Error getting analyzed case count: {e}")
        return 0

def main():
    """Main migration function"""
    logger.info("Starting AI Case Analysis Migration")
    logger.info("=" * 50)
    
    # Check database connection
    if not check_database_connection():
        logger.error("Cannot proceed without database connection")
        sys.exit(1)
    
    # Check OpenAI configuration
    if not check_openai_config():
        logger.error("Cannot proceed without OpenAI configuration")
        logger.info("Please set OPENAI_API_KEY environment variable or add it to database settings")
        sys.exit(1)
    
    # Initialize database connection
    engine = create_engine(settings.database_url)
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    db = SessionLocal()
    
    try:
        # Get case statistics
        total_cases = get_case_count(db)
        analyzed_cases = get_analyzed_case_count(db)
        pending_cases = total_cases - analyzed_cases
        
        logger.info(f"Total cases in database: {total_cases}")
        logger.info(f"Already analyzed cases: {analyzed_cases}")
        logger.info(f"Pending analysis: {pending_cases}")
        
        if pending_cases == 0:
            logger.info("All cases have already been analyzed. Nothing to do.")
            return
        
        # Confirm before proceeding
        if len(sys.argv) > 1 and sys.argv[1] == '--force':
            logger.info("Force mode enabled. Proceeding with analysis...")
        else:
            response = input(f"\nProceed with AI analysis for {pending_cases} cases? (y/N): ")
            if response.lower() != 'y':
                logger.info("Migration cancelled by user")
                return
        
        # Initialize AI service
        ai_service = AICaseAnalysisService(db)
        
        # Process all cases
        logger.info("Starting AI analysis process...")
        start_time = datetime.now()
        
        result = ai_service.process_all_cases(batch_size=5)  # Smaller batch size for stability
        
        end_time = datetime.now()
        duration = end_time - start_time
        
        # Log results
        logger.info("=" * 50)
        logger.info("AI Analysis Migration Completed")
        logger.info(f"Total cases: {result.get('total_cases', 0)}")
        logger.info(f"Processed: {result.get('processed', 0)}")
        logger.info(f"Successful: {result.get('successful', 0)}")
        logger.info(f"Failed: {result.get('failed', 0)}")
        logger.info(f"Completion percentage: {result.get('completion_percentage', 0):.2f}%")
        logger.info(f"Duration: {duration}")
        
        if result.get('failed', 0) > 0:
            logger.warning(f"{result.get('failed', 0)} cases failed to process. Check logs for details.")
        
        logger.info("Migration completed successfully!")
        
    except Exception as e:
        logger.error(f"Migration failed: {e}")
        db.rollback()
        sys.exit(1)
    finally:
        db.close()

if __name__ == "__main__":
    main()
