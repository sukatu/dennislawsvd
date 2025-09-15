#!/usr/bin/env python3
"""
Script to generate analytics and case statistics for all companies.
This will analyze all cases related to each company and generate real analytics data.
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from database import get_db
from models.companies import Companies
from models.company_analytics import CompanyAnalytics
from models.company_case_statistics import CompanyCaseStatistics
from services.company_analytics_service import CompanyAnalyticsService
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def generate_all_company_analytics():
    """Generate analytics and case statistics for all companies."""
    try:
        db = next(get_db())
        analytics_service = CompanyAnalyticsService(db)
        
        # Get all companies
        companies = db.query(Companies).filter(Companies.is_active == True).all()
        logger.info(f"Found {len(companies)} active companies to process")
        
        analytics_count = 0
        case_stats_count = 0
        errors = 0
        
        for i, company in enumerate(companies, 1):
            try:
                logger.info(f"Processing company {i}/{len(companies)}: {company.name}")
                
                # Generate analytics
                analytics = analytics_service.generate_company_analytics(company.id)
                if analytics:
                    analytics_count += 1
                    logger.info(f"  ✅ Generated analytics for {company.name}")
                else:
                    logger.info(f"  ⚠️  No analytics generated for {company.name} (no cases found)")
                
                # Generate case statistics
                case_stats = analytics_service.generate_company_case_statistics(company.id)
                if case_stats:
                    case_stats_count += 1
                    logger.info(f"  ✅ Generated case statistics for {company.name}")
                else:
                    logger.info(f"  ⚠️  No case statistics generated for {company.name} (no cases found)")
                    
            except Exception as e:
                errors += 1
                logger.error(f"  ❌ Error processing {company.name}: {e}")
                continue
        
        logger.info(f"\n🎉 Company analytics generation completed!")
        logger.info(f"📊 Analytics generated for: {analytics_count} companies")
        logger.info(f"📈 Case statistics generated for: {case_stats_count} companies")
        logger.info(f"❌ Errors encountered: {errors}")
        
    except Exception as e:
        logger.error(f"❌ Error in generate_all_company_analytics: {e}")

if __name__ == "__main__":
    generate_all_company_analytics()
