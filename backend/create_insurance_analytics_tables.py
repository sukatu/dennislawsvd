#!/usr/bin/env python3
"""
Script to create insurance analytics and case statistics tables.
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from database import engine, Base
from models.insurance_analytics import InsuranceAnalytics
from models.insurance_case_statistics import InsuranceCaseStatistics
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def create_insurance_analytics_tables():
    """Create insurance analytics and case statistics tables."""
    try:
        logger.info("Creating insurance analytics tables...")
        
        # Create the tables
        InsuranceAnalytics.__table__.create(engine, checkfirst=True)
        InsuranceCaseStatistics.__table__.create(engine, checkfirst=True)
        
        logger.info("✅ Insurance analytics tables created successfully!")
        
    except Exception as e:
        logger.error(f"❌ Error creating insurance analytics tables: {e}")
        raise

if __name__ == "__main__":
    create_insurance_analytics_tables()
