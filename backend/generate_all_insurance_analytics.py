#!/usr/bin/env python3
"""
Script to generate analytics and case statistics for all insurance companies.
This will analyze all cases related to each insurance company and generate real analytics data.
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from database import get_db
from models.insurance import Insurance
from models.insurance_analytics import InsuranceAnalytics
from models.insurance_case_statistics import InsuranceCaseStatistics
from services.insurance_analytics_service import InsuranceAnalyticsService
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def generate_all_insurance_analytics():
    """Generate analytics and case statistics for all insurance companies."""
    try:
        db = next(get_db())
        analytics_service = InsuranceAnalyticsService(db)
        
        # Get all active insurance companies
        insurance_companies = db.query(Insurance).filter(Insurance.is_active == True).all()
        
        logger.info(f"Found {len(insurance_companies)} active insurance companies to process")
        
        processed_count = 0
        success_count = 0
        error_count = 0
        
        for insurance in insurance_companies:
            try:
                logger.info(f"Processing insurance company: {insurance.name} (ID: {insurance.id})")
                
                # Generate analytics
                analytics = analytics_service.generate_insurance_analytics(insurance.id)
                if analytics:
                    logger.info(f"✅ Generated analytics for {insurance.name}")
                else:
                    logger.warning(f"⚠️  No analytics generated for {insurance.name} (no related cases found)")
                
                # Generate case statistics
                stats = analytics_service.generate_insurance_case_statistics(insurance.id)
                if stats:
                    logger.info(f"✅ Generated case statistics for {insurance.name}")
                else:
                    logger.warning(f"⚠️  No case statistics generated for {insurance.name} (no related cases found)")
                
                processed_count += 1
                if analytics or stats:
                    success_count += 1
                
            except Exception as e:
                logger.error(f"❌ Error processing {insurance.name}: {e}")
                error_count += 1
                continue
        
        logger.info(f"\n📊 Processing Summary:")
        logger.info(f"   Total insurance companies processed: {processed_count}")
        logger.info(f"   Successfully generated data for: {success_count}")
        logger.info(f"   Errors encountered: {error_count}")
        
        # Generate summary report
        generate_summary_report(db)
        
    except Exception as e:
        logger.error(f"❌ Error in generate_all_insurance_analytics: {e}")
        raise
    finally:
        if 'db' in locals():
            db.close()

def generate_summary_report(db):
    """Generate a summary report of the analytics data."""
    try:
        logger.info("\n📈 Analytics Summary Report:")
        
        # Count analytics records
        analytics_count = db.query(InsuranceAnalytics).count()
        stats_count = db.query(InsuranceCaseStatistics).count()
        
        logger.info(f"   Total analytics records: {analytics_count}")
        logger.info(f"   Total case statistics records: {stats_count}")
        
        # Get some sample analytics data
        sample_analytics = db.query(InsuranceAnalytics).limit(5).all()
        if sample_analytics:
            logger.info("\n📋 Sample Analytics Data:")
            for analytics in sample_analytics:
                insurance = db.query(Insurance).filter(Insurance.id == analytics.insurance_id).first()
                logger.info(f"   {insurance.name if insurance else 'Unknown'}:")
                logger.info(f"     Risk Score: {analytics.risk_score}")
                logger.info(f"     Risk Level: {analytics.risk_level}")
                logger.info(f"     Total Cases: {analytics.total_monetary_amount}")
                logger.info(f"     Success Rate: {analytics.success_rate}%")
        
        # Get some sample statistics data
        sample_stats = db.query(InsuranceCaseStatistics).limit(5).all()
        if sample_stats:
            logger.info("\n📊 Sample Case Statistics:")
            for stats in sample_stats:
                insurance = db.query(Insurance).filter(Insurance.id == stats.insurance_id).first()
                logger.info(f"   {insurance.name if insurance else 'Unknown'}:")
                logger.info(f"     Total Cases: {stats.total_cases}")
                logger.info(f"     Resolved Cases: {stats.resolved_cases}")
                logger.info(f"     Favorable Cases: {stats.favorable_cases}")
                logger.info(f"     Case Outcome: {stats.case_outcome}")
        
    except Exception as e:
        logger.error(f"Error generating summary report: {e}")

def generate_insurance_analytics_for_company(insurance_id: int):
    """Generate analytics for a specific insurance company."""
    try:
        db = next(get_db())
        analytics_service = InsuranceAnalyticsService(db)
        
        insurance = db.query(Insurance).filter(Insurance.id == insurance_id).first()
        if not insurance:
            logger.error(f"Insurance company with ID {insurance_id} not found")
            return False
        
        logger.info(f"Generating analytics for {insurance.name} (ID: {insurance_id})")
        
        # Generate analytics
        analytics = analytics_service.generate_insurance_analytics(insurance_id)
        if analytics:
            logger.info(f"✅ Generated analytics for {insurance.name}")
        else:
            logger.warning(f"⚠️  No analytics generated for {insurance.name}")
        
        # Generate case statistics
        stats = analytics_service.generate_insurance_case_statistics(insurance_id)
        if stats:
            logger.info(f"✅ Generated case statistics for {insurance.name}")
        else:
            logger.warning(f"⚠️  No case statistics generated for {insurance.name}")
        
        return analytics is not None or stats is not None
        
    except Exception as e:
        logger.error(f"Error generating analytics for insurance ID {insurance_id}: {e}")
        return False
    finally:
        if 'db' in locals():
            db.close()

if __name__ == "__main__":
    if len(sys.argv) > 1:
        # Generate for specific insurance company
        insurance_id = int(sys.argv[1])
        generate_insurance_analytics_for_company(insurance_id)
    else:
        # Generate for all insurance companies
        generate_all_insurance_analytics()
