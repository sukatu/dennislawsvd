#!/usr/bin/env python3
"""
Setup script for AI Case Analysis system.
This script helps configure the OpenAI API key and test the system.
"""

import os
import sys
import logging
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker

# Add the backend directory to the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), 'backend')))

from backend.config import settings

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def setup_openai_key():
    """Setup OpenAI API key in database settings"""
    try:
        # Initialize database connection
        engine = create_engine(settings.database_url)
        SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
        db = SessionLocal()
        
        # Get API key from user
        api_key = input("Enter your OpenAI API key: ").strip()
        if not api_key:
            logger.error("API key is required")
            return False
        
        # Check if settings table exists and create if needed
        db.execute(text("""
            CREATE TABLE IF NOT EXISTS settings (
                id SERIAL PRIMARY KEY,
                key VARCHAR(255) UNIQUE NOT NULL,
                value TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """))
        
        # Insert or update API key
        db.execute(text("""
            INSERT INTO settings (key, value) 
            VALUES ('openai_api_key', :api_key)
            ON CONFLICT (key) 
            DO UPDATE SET value = :api_key, updated_at = CURRENT_TIMESTAMP
        """), {"api_key": api_key})
        
        # Insert or update model setting
        db.execute(text("""
            INSERT INTO settings (key, value) 
            VALUES ('openai_model', 'gpt-3.5-turbo')
            ON CONFLICT (key) 
            DO UPDATE SET value = 'gpt-3.5-turbo', updated_at = CURRENT_TIMESTAMP
        """))
        
        db.commit()
        logger.info("✅ OpenAI API key configured successfully")
        return True
        
    except Exception as e:
        logger.error(f"Failed to setup OpenAI key: {e}")
        if 'db' in locals():
            db.rollback()
        return False
    finally:
        if 'db' in locals():
            db.close()

def test_system():
    """Test the AI analysis system"""
    try:
        # Test database connection
        engine = create_engine(settings.database_url)
        SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
        db = SessionLocal()
        
        # Get case count
        result = db.execute(text("SELECT COUNT(*) FROM reported_cases")).scalar()
        logger.info(f"Total cases in database: {result}")
        
        # Get cases with content
        result = db.execute(text("""
            SELECT COUNT(*) FROM reported_cases 
            WHERE (decision IS NOT NULL AND decision != '') 
               OR (judgement IS NOT NULL AND judgement != '')
        """)).scalar()
        logger.info(f"Cases with decision content: {result}")
        
        # Test OpenAI configuration
        result = db.execute(text("SELECT value FROM settings WHERE key = 'openai_api_key'")).scalar()
        if result:
            logger.info("✅ OpenAI API key found in database")
        else:
            logger.warning("⚠️ OpenAI API key not found in database")
        
        return True
        
    except Exception as e:
        logger.error(f"System test failed: {e}")
        return False
    finally:
        if 'db' in locals():
            db.close()

def show_usage_instructions():
    """Show usage instructions"""
    print("\n" + "="*60)
    print("AI CASE ANALYSIS SYSTEM - USAGE INSTRUCTIONS")
    print("="*60)
    print()
    print("1. SETUP COMPLETE!")
    print("   - OpenAI API key configured in database")
    print("   - AI analysis service ready to use")
    print()
    print("2. RUN AI ANALYSIS:")
    print("   # Test with a single case:")
    print("   python test_ai_simple.py")
    print()
    print("   # Process all cases:")
    print("   python backend/migrate_ai_analysis.py")
    print()
    print("   # Process all cases (force mode):")
    print("   python backend/migrate_ai_analysis.py --force")
    print()
    print("3. API ENDPOINTS:")
    print("   # Analyze single case:")
    print("   POST /api/ai-case-analysis/analyze-case/{case_id}")
    print()
    print("   # Analyze all cases (background):")
    print("   POST /api/ai-case-analysis/analyze-all-cases")
    print()
    print("   # Get statistics:")
    print("   GET /api/ai-case-analysis/stats")
    print()
    print("4. MONITORING:")
    print("   - Check logs in 'ai_analysis_migration.log'")
    print("   - Monitor progress in console output")
    print()
    print("5. COSTS:")
    print("   - Estimated cost: $0.01-0.05 per case")
    print("   - Processing time: 2-5 seconds per case")
    print("   - Recommended batch size: 5-10 cases")
    print()

def main():
    """Main setup function"""
    print("AI Case Analysis System Setup")
    print("=" * 40)
    
    # Test current system
    logger.info("Testing current system...")
    if not test_system():
        logger.error("System test failed")
        return
    
    # Setup OpenAI key
    logger.info("Setting up OpenAI API key...")
    if not setup_openai_key():
        logger.error("OpenAI setup failed")
        return
    
    # Final test
    logger.info("Running final test...")
    if test_system():
        logger.info("✅ Setup completed successfully!")
        show_usage_instructions()
    else:
        logger.error("❌ Setup failed")

if __name__ == "__main__":
    main()
