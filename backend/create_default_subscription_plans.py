#!/usr/bin/env python3
"""
Script to create default subscription plans for the multi-tenant system
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from sqlalchemy.orm import Session
from database import SessionLocal, engine, Base
from models.tenant import SubscriptionPlan

def create_subscription_plans():
    """Create default subscription plans"""
    
    # Create tables if they don't exist
    Base.metadata.create_all(bind=engine)
    
    db = SessionLocal()
    
    try:
        # Check if plans already exist
        existing_plans = db.query(SubscriptionPlan).count()
        if existing_plans > 0:
            print(f"Subscription plans already exist ({existing_plans} plans found)")
            return
        
        # Define default subscription plans
        default_plans = [
            {
                "name": "Starter",
                "description": "Perfect for small law firms and individual practitioners",
                "slug": "starter",
                "price_monthly": 360.00,  # ~$30 USD
                "price_yearly": 3600.00,  # ~$300 USD
                "currency": "GHS",
                "max_users": 2,
                "max_cases_per_month": 500,
                "max_storage_gb": 1.0,
                "features": [
                    "Basic case search",
                    "People database access",
                    "Email support",
                    "Basic analytics"
                ],
                "is_active": True,
                "is_popular": False,
                "sort_order": 1
            },
            {
                "name": "Professional",
                "description": "Ideal for medium-sized law firms and legal departments",
                "slug": "professional",
                "price_monthly": 960.00,  # ~$80 USD
                "price_yearly": 9600.00,  # ~$800 USD
                "currency": "GHS",
                "max_users": 10,
                "max_cases_per_month": 2000,
                "max_storage_gb": 5.0,
                "features": [
                    "Advanced case search",
                    "Full database access",
                    "AI-powered analysis",
                    "Priority support",
                    "Advanced analytics",
                    "Custom branding",
                    "API access"
                ],
                "is_active": True,
                "is_popular": True,
                "sort_order": 2
            },
            {
                "name": "Enterprise",
                "description": "Comprehensive solution for large law firms and organizations",
                "slug": "enterprise",
                "price_monthly": 2400.00,  # ~$200 USD
                "price_yearly": 24000.00,  # ~$2000 USD
                "currency": "GHS",
                "max_users": 50,
                "max_cases_per_month": 10000,
                "max_storage_gb": 25.0,
                "features": [
                    "Unlimited case search",
                    "Full database access",
                    "Advanced AI analysis",
                    "24/7 phone support",
                    "Custom analytics dashboard",
                    "Full branding customization",
                    "Full API access",
                    "White-label solution",
                    "Custom integrations",
                    "Dedicated account manager"
                ],
                "is_active": True,
                "is_popular": False,
                "sort_order": 3
            },
            {
                "name": "Trial",
                "description": "Free trial for new organizations",
                "slug": "trial",
                "price_monthly": 0.0,
                "price_yearly": 0.0,
                "currency": "GHS",
                "max_users": 1,
                "max_cases_per_month": 100,
                "max_storage_gb": 0.1,
                "features": [
                    "Basic case search",
                    "Limited database access",
                    "Email support",
                    "14-day trial period"
                ],
                "is_active": True,
                "is_popular": False,
                "sort_order": 0
            }
        ]
        
        # Create plans
        created_plans = []
        for plan_data in default_plans:
            plan = SubscriptionPlan(**plan_data)
            db.add(plan)
            created_plans.append(plan)
        
        # Commit to database
        db.commit()
        
        print(f"Successfully created {len(created_plans)} subscription plans:")
        for plan in created_plans:
            print(f"  - {plan.name} ({plan.slug}): ${plan.price_monthly}/month")
        
        return created_plans
        
    except Exception as e:
        db.rollback()
        print(f"Error creating subscription plans: {str(e)}")
        raise
    finally:
        db.close()

def create_sample_tenant():
    """Create a sample tenant for testing"""
    from models.tenant import Tenant
    from models.user import User
    
    db = SessionLocal()
    
    try:
        # Check if sample tenant already exists
        existing_tenant = db.query(Tenant).filter(Tenant.slug == "demo-organization").first()
        if existing_tenant:
            print("Sample tenant already exists")
            return existing_tenant
        
        # Get the starter plan
        starter_plan = db.query(SubscriptionPlan).filter(SubscriptionPlan.slug == "starter").first()
        if not starter_plan:
            print("Starter plan not found, creating subscription plans first...")
            create_subscription_plans()
            starter_plan = db.query(SubscriptionPlan).filter(SubscriptionPlan.slug == "starter").first()
        
        # Create sample tenant
        tenant_data = {
            "name": "Demo Legal Organization",
            "slug": "demo-organization",
            "description": "A sample legal organization for demonstration purposes",
            "website": "https://demo-legal.com",
            "email": "admin@demo-legal.com",
            "phone": "+1-555-0123",
            "address_line_1": "123 Legal Street",
            "city": "New York",
            "state": "NY",
            "country": "USA",
            "postal_code": "10001",
            "app_name": "Demo Legal Search",
            "app_tagline": "Advanced Legal Research for Demo Organization",
            "primary_color": "#2563EB",
            "secondary_color": "#1D4ED8",
            "accent_color": "#F59E0B",
            "subscription_plan_id": starter_plan.id,
            "subscription_status": "trial",
            "max_users": 2,
            "max_cases_per_month": 500,
            "max_storage_gb": 1.0,
            "features_enabled": ["basic_search", "people_database", "email_support"],
            "is_active": True,
            "is_approved": True,
            "is_verified": True,
            "contact_person_name": "John Demo",
            "contact_person_email": "john@demo-legal.com",
            "contact_person_phone": "+1-555-0123"
        }
        
        tenant = Tenant(**tenant_data)
        db.add(tenant)
        db.commit()
        db.refresh(tenant)
        
        print(f"Successfully created sample tenant: {tenant.name} ({tenant.slug})")
        return tenant
        
    except Exception as e:
        db.rollback()
        print(f"Error creating sample tenant: {str(e)}")
        raise
    finally:
        db.close()

if __name__ == "__main__":
    print("Creating default subscription plans...")
    create_subscription_plans()
    
    print("\nCreating sample tenant...")
    create_sample_tenant()
    
    print("\nSetup completed successfully!")
