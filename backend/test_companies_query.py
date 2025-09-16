#!/usr/bin/env python3

import sys
import os
sys.path.append(os.path.dirname(__file__))

from database import get_db, engine
from models.companies import Companies
from sqlalchemy.orm import sessionmaker

# Create a session
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
db = SessionLocal()

try:
    # Test basic query
    print("Testing basic companies query...")
    total = db.query(Companies).count()
    print(f"Total companies in database: {total}")
    
    companies = db.query(Companies).limit(5).all()
    print(f"Query returned {len(companies)} companies")
    
    if companies:
        for i, company in enumerate(companies):
            print(f"Company {i+1}: {company.name if hasattr(company, 'name') else 'No name'}")
            if hasattr(company, 'business_activities'):
                print(f"  business_activities type: {type(company.business_activities)}")
                print(f"  business_activities value: {company.business_activities}")
            if hasattr(company, 'directors'):
                print(f"  directors type: {type(company.directors)}")
                print(f"  directors value: {company.directors}")
            print()
    else:
        print("No companies found!")
        
except Exception as e:
    print(f"Error: {e}")
    import traceback
    traceback.print_exc()
finally:
    db.close()
