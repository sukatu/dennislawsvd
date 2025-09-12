#!/usr/bin/env python3
"""
Script to populate summernote_content field in case_metadata table
by copying the summernote field from reported_cases table
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from sqlalchemy.orm import Session
from database import get_db, engine
from models.reported_cases import ReportedCases
from models.case_metadata import CaseMetadata
from sqlalchemy import text
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def add_summernote_column():
    """Add summernote_content column to case_metadata table if it doesn't exist"""
    try:
        with engine.connect() as conn:
            # Check if column exists
            result = conn.execute(text("""
                SELECT COUNT(*) 
                FROM INFORMATION_SCHEMA.COLUMNS 
                WHERE TABLE_NAME = 'case_metadata' 
                AND COLUMN_NAME = 'summernote_content'
            """))
            
            if result.scalar() == 0:
                # Add the column
                conn.execute(text("""
                    ALTER TABLE case_metadata 
                    ADD COLUMN summernote_content TEXT
                """))
                conn.commit()
                logger.info("Added summernote_content column to case_metadata table")
            else:
                logger.info("summernote_content column already exists")
                
    except Exception as e:
        logger.error(f"Error adding column: {e}")

def populate_summernote_content():
    """Populate summernote_content field in case_metadata from reported_cases.summernote"""
    try:
        db = next(get_db())
        
        # Get all cases with metadata that don't have summernote_content yet
        cases_with_metadata = db.query(ReportedCases, CaseMetadata).join(
            CaseMetadata, ReportedCases.id == CaseMetadata.case_id
        ).filter(
            CaseMetadata.summernote_content.is_(None),
            ReportedCases.summernote.isnot(None)
        ).all()
        
        logger.info(f"Found {len(cases_with_metadata)} cases to update")
        
        updated_count = 0
        for case, metadata in cases_with_metadata:
            if case.summernote:
                metadata.summernote_content = case.summernote
                updated_count += 1
                
                if updated_count % 100 == 0:
                    logger.info(f"Updated {updated_count} cases...")
        
        db.commit()
        logger.info(f"Successfully updated {updated_count} cases with summernote content")
        
        # Verify the update
        total_with_summernote = db.query(CaseMetadata).filter(
            CaseMetadata.summernote_content.isnot(None)
        ).count()
        
        logger.info(f"Total cases with summernote_content: {total_with_summernote}")
        
    except Exception as e:
        logger.error(f"Error populating summernote content: {e}")
        db.rollback()
    finally:
        db.close()

def main():
    """Main function to run the population process"""
    logger.info("Starting summernote content population...")
    
    # Add column if it doesn't exist
    add_summernote_column()
    
    # Populate the content
    populate_summernote_content()
    
    logger.info("Summernote content population completed!")

if __name__ == "__main__":
    main()
