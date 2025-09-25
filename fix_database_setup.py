#!/usr/bin/env python3
"""
Database setup script for Juridence application
Run this script to create all database tables
"""

import sys
import os

# Add the current directory to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

try:
    # Import required modules
    from backend.config import settings
    from backend.database import engine, Base
    
    # Import all models to ensure they are registered
    from backend.models.user import User
    from backend.models.people import People
    from backend.models.banks import Banks
    from backend.models.insurance import Insurance
    from backend.models.reported_cases import ReportedCases
    from backend.models.legal_history import LegalHistory, CaseMention, LegalSearchIndex
    from backend.models.judges import Judges
    from backend.models.court_types import CourtTypes
    from backend.models.case_hearings import CaseHearing
    from backend.models.case_metadata import CaseMetadata
    from backend.models.companies import Companies
    from backend.models.person_analytics import PersonAnalytics
    from backend.models.bank_analytics import BankAnalytics
    from backend.models.insurance_analytics import InsuranceAnalytics
    from backend.models.company_analytics import CompanyAnalytics
    
    print("✅ All modules imported successfully!")
    print(f"📊 Database URL: {settings.database_url}")
    
    # Create all tables
    print("🔨 Creating database tables...")
    Base.metadata.create_all(bind=engine)
    
    print("✅ Database tables created successfully!")
    print("🎉 Setup completed!")
    
except ImportError as e:
    print(f"❌ Import error: {e}")
    print("Make sure you're running this script from the project root directory")
    sys.exit(1)
except Exception as e:
    print(f"❌ Error creating tables: {e}")
    sys.exit(1)
