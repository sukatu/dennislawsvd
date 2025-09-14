#!/usr/bin/env python3
"""
Script to create bank_analytics and bank_case_statistics tables.
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from sqlalchemy import create_engine, text
from database import Base, engine
from models import BankAnalytics, BankCaseStatistics
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def create_bank_analytics_tables():
    """Create bank analytics and case statistics tables."""
    try:
        logger.info("Creating bank analytics tables...")
        
        # Create the tables
        BankAnalytics.__table__.create(engine, checkfirst=True)
        BankCaseStatistics.__table__.create(engine, checkfirst=True)
        
        logger.info("✅ Bank analytics tables created successfully!")
        
        # Verify tables were created
        with engine.connect() as conn:
            # Check if bank_analytics table exists
            result = conn.execute(text("SHOW TABLES LIKE 'bank_analytics'"))
            if result.fetchone():
                logger.info("✅ bank_analytics table exists")
            else:
                logger.error("❌ bank_analytics table not found")
                
            # Check if bank_case_statistics table exists
            result = conn.execute(text("SHOW TABLES LIKE 'bank_case_statistics'"))
            if result.fetchone():
                logger.info("✅ bank_case_statistics table exists")
            else:
                logger.error("❌ bank_case_statistics table not found")
        
        return True
        
    except Exception as e:
        logger.error(f"❌ Error creating bank analytics tables: {e}")
        return False

def main():
    """Main function."""
    logger.info("Starting bank analytics tables creation...")
    
    success = create_bank_analytics_tables()
    
    if success:
        logger.info("🎉 Bank analytics tables setup completed successfully!")
    else:
        logger.error("💥 Bank analytics tables setup failed!")
        sys.exit(1)

if __name__ == "__main__":
    main()
