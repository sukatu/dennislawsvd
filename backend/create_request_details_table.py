#!/usr/bin/env python3
"""
Script to create the request_details table in the database.
Run this script to add the request details functionality to the database.
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from sqlalchemy import create_engine, text
from database import Base, engine
from models.request_details import RequestDetails
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def create_request_details_table():
    """Create the request_details table"""
    try:
        # Create all tables (this will create request_details if it doesn't exist)
        Base.metadata.create_all(bind=engine)
        logger.info("✅ Successfully created request_details table")
        
        # Verify the table was created
        with engine.connect() as connection:
            result = connection.execute(text("""
                SELECT table_name 
                FROM information_schema.tables 
                WHERE table_schema = 'dennislaw_svd' 
                AND table_name = 'request_details'
            """))
            
            if result.fetchone():
                logger.info("✅ Verified: request_details table exists")
                
                # Show table structure
                result = connection.execute(text("""
                    SELECT column_name, data_type, is_nullable, column_default
                    FROM information_schema.columns 
                    WHERE table_schema = 'dennislaw_svd' 
                    AND table_name = 'request_details'
                    ORDER BY ordinal_position
                """))
                
                logger.info("📋 Table structure:")
                for row in result:
                    logger.info(f"  - {row[0]}: {row[1]} {'(nullable)' if row[2] == 'YES' else '(not null)'} {f'default: {row[3]}' if row[3] else ''}")
                
            else:
                logger.error("❌ request_details table was not created")
                return False
                
        return True
        
    except Exception as e:
        logger.error(f"❌ Error creating request_details table: {str(e)}")
        return False

def add_sample_data():
    """Add some sample request data for testing"""
    try:
        from sqlalchemy.orm import sessionmaker
        from models.request_details import RequestDetails, RequestType, EntityType, RequestStatus, Priority
        
        SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
        db = SessionLocal()
        
        # Check if sample data already exists
        existing_count = db.query(RequestDetails).count()
        if existing_count > 0:
            logger.info(f"ℹ️  Sample data already exists ({existing_count} records)")
            return True
        
        # Create sample requests
        sample_requests = [
            RequestDetails(
                request_type=RequestType.CASE_DETAILS,
                entity_type=EntityType.CASE,
                case_id=1,
                case_suit_number="SC/123/2023",
                entity_name="Sample Case",
                message="Please provide detailed information about this case",
                requester_name="John Doe",
                requester_email="john.doe@example.com",
                requester_phone="+1234567890",
                requester_organization="Law Firm ABC",
                status=RequestStatus.PENDING,
                priority=Priority.MEDIUM,
                is_urgent=False
            ),
            RequestDetails(
                request_type=RequestType.PROFILE_INFORMATION,
                entity_type=EntityType.PERSON,
                entity_id=1,
                entity_name="Jane Smith",
                message="Need contact details and legal history",
                requester_name="Legal Researcher",
                requester_email="researcher@example.com",
                requester_phone="+1234567891",
                status=RequestStatus.IN_PROGRESS,
                priority=Priority.HIGH,
                is_urgent=True
            ),
            RequestDetails(
                request_type=RequestType.FINANCIAL_INFORMATION,
                entity_type=EntityType.BANK,
                entity_id=1,
                entity_name="First National Bank",
                message="Requesting financial statements and risk assessment",
                requester_name="Financial Analyst",
                requester_email="analyst@example.com",
                requester_phone="+1234567892",
                requester_organization="Investment Firm XYZ",
                status=RequestStatus.COMPLETED,
                priority=Priority.MEDIUM,
                is_urgent=False
            ),
            RequestDetails(
                request_type=RequestType.LEGAL_DOCUMENTS,
                entity_type=EntityType.CASE,
                case_id=2,
                case_suit_number="HC/456/2023",
                entity_name="Contract Dispute Case",
                message="Need copies of all legal documents and court filings",
                requester_name="Paralegal Assistant",
                requester_email="paralegal@example.com",
                requester_phone="+1234567893",
                requester_organization="Legal Services Inc",
                status=RequestStatus.PENDING,
                priority=Priority.LOW,
                is_urgent=False
            ),
            RequestDetails(
                request_type=RequestType.MANAGEMENT_DETAILS,
                entity_type=EntityType.COMPANY,
                entity_id=1,
                entity_name="Tech Solutions Ltd",
                message="Requesting board of directors and management information",
                requester_name="Due Diligence Team",
                requester_email="duediligence@example.com",
                requester_phone="+1234567894",
                requester_organization="M&A Consultants",
                status=RequestStatus.PENDING,
                priority=Priority.HIGH,
                is_urgent=False
            )
        ]
        
        for request in sample_requests:
            db.add(request)
        
        db.commit()
        logger.info("✅ Successfully added sample request data")
        
        # Show summary
        total_requests = db.query(RequestDetails).count()
        pending_requests = db.query(RequestDetails).filter(RequestDetails.status == RequestStatus.PENDING).count()
        urgent_requests = db.query(RequestDetails).filter(RequestDetails.is_urgent == True).count()
        
        logger.info(f"📊 Sample data summary:")
        logger.info(f"  - Total requests: {total_requests}")
        logger.info(f"  - Pending requests: {pending_requests}")
        logger.info(f"  - Urgent requests: {urgent_requests}")
        
        db.close()
        return True
        
    except Exception as e:
        logger.error(f"❌ Error adding sample data: {str(e)}")
        return False

def main():
    """Main function to create table and add sample data"""
    logger.info("🚀 Starting request_details table creation...")
    
    # Create the table
    if create_request_details_table():
        logger.info("✅ Table creation completed successfully")
        
        # Ask if user wants to add sample data
        add_samples = input("\n🤔 Would you like to add sample data for testing? (y/n): ").lower().strip()
        if add_samples in ['y', 'yes']:
            if add_sample_data():
                logger.info("✅ Sample data added successfully")
            else:
                logger.error("❌ Failed to add sample data")
        else:
            logger.info("ℹ️  Skipping sample data creation")
            
        logger.info("\n🎉 Request details functionality is now ready!")
        logger.info("📝 You can now use the API endpoints at /api/request-details/")
        
    else:
        logger.error("❌ Failed to create request_details table")
        sys.exit(1)

if __name__ == "__main__":
    main()
