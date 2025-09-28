#!/usr/bin/env python3
"""
Script to create usage tracking tables in the database
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from database import engine, Base
from models.usage_tracking import UsageTracking, BillingSummary
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def create_usage_tracking_tables():
    """Create usage tracking tables"""
    try:
        logger.info("Creating usage tracking tables...")
        
        # Create the tables
        UsageTracking.__table__.create(engine, checkfirst=True)
        BillingSummary.__table__.create(engine, checkfirst=True)
        
        logger.info("✅ Usage tracking tables created successfully!")
        
    except Exception as e:
        logger.error(f"❌ Error creating usage tracking tables: {e}")
        raise

if __name__ == "__main__":
    create_usage_tracking_tables()
