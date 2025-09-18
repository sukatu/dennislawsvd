#!/usr/bin/env python3
"""
Database table creation script for production deployment
"""

from database import engine, Base
from models import user, case_search, people, banks, insurance, companies, payment, subscription, notification, logs, courts, profile, settings
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def create_tables():
    """Create all database tables"""
    try:
        logger.info("Creating database tables...")
        Base.metadata.create_all(bind=engine)
        logger.info("Database tables created successfully!")
    except Exception as e:
        logger.error(f"Error creating tables: {e}")
        raise

if __name__ == "__main__":
    create_tables()
