#!/usr/bin/env python3
"""
Script to create company analytics tables in the database.
"""

import sys
import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv
import logging

# Add the backend directory to the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '.')))

from database import Base
from config import settings
from models.company_analytics import CompanyAnalytics
from models.company_case_statistics import CompanyCaseStatistics
from models.companies import Companies  # Ensure Companies model is imported for relationships

# Load environment variables
load_dotenv()

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def create_company_analytics_tables():
    """Create company analytics tables in the database."""
    logger.info("Creating company analytics tables...")
    DATABASE_URL = settings.database_url
    engine = create_engine(DATABASE_URL)

    try:
        # Create tables for all models that inherit from Base
        # This will create company_analytics and company_case_statistics tables
        # It also ensures the 'companies' table exists if it doesn't already
        Base.metadata.create_all(engine)
        logger.info("✅ Company analytics tables created successfully!")
    except Exception as e:
        logger.error(f"❌ Error creating company analytics tables: {e}")

if __name__ == "__main__":
    create_company_analytics_tables()
