#!/usr/bin/env python3
"""
Script to update existing subscription plans to use Ghana Cedis (GHS)
"""

import sys
import os
from sqlalchemy.orm import Session

# Add the backend directory to the Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from database import SessionLocal
from models.tenant import SubscriptionPlan

def update_plans_to_ghs():
    """Update existing subscription plans to use Ghana Cedis"""
    
    db = SessionLocal()
    try:
        print("Updating subscription plans to Ghana Cedis (GHS)...")
        
        # Update Trial plan
        trial_plan = db.query(SubscriptionPlan).filter(SubscriptionPlan.slug == "trial").first()
        if trial_plan:
            trial_plan.currency = "GHS"
            trial_plan.price_monthly = 0.0
            trial_plan.price_yearly = 0.0
            print(f"✓ Updated Trial plan to GHS")
        
        # Update Starter plan
        starter_plan = db.query(SubscriptionPlan).filter(SubscriptionPlan.slug == "starter").first()
        if starter_plan:
            starter_plan.currency = "GHS"
            starter_plan.price_monthly = 360.00  # ~$30 USD
            starter_plan.price_yearly = 3600.00  # ~$300 USD
            print(f"✓ Updated Starter plan to GHS: ₵{starter_plan.price_monthly}/month, ₵{starter_plan.price_yearly}/year")
        
        # Update Professional plan
        professional_plan = db.query(SubscriptionPlan).filter(SubscriptionPlan.slug == "professional").first()
        if professional_plan:
            professional_plan.currency = "GHS"
            professional_plan.price_monthly = 960.00  # ~$80 USD
            professional_plan.price_yearly = 9600.00  # ~$800 USD
            print(f"✓ Updated Professional plan to GHS: ₵{professional_plan.price_monthly}/month, ₵{professional_plan.price_yearly}/year")
        
        # Update Enterprise plan
        enterprise_plan = db.query(SubscriptionPlan).filter(SubscriptionPlan.slug == "enterprise").first()
        if enterprise_plan:
            enterprise_plan.currency = "GHS"
            enterprise_plan.price_monthly = 2400.00  # ~$200 USD
            enterprise_plan.price_yearly = 24000.00  # ~$2000 USD
            print(f"✓ Updated Enterprise plan to GHS: ₵{enterprise_plan.price_monthly}/month, ₵{enterprise_plan.price_yearly}/year")
        
        db.commit()
        print("\n✅ Successfully updated all subscription plans to Ghana Cedis!")
        
        # Display updated plans
        print("\nUpdated Plans:")
        plans = db.query(SubscriptionPlan).order_by(SubscriptionPlan.sort_order).all()
        for plan in plans:
            print(f"  - {plan.name}: ₵{plan.price_monthly}/month, ₵{plan.price_yearly}/year ({plan.currency})")
        
    except Exception as e:
        db.rollback()
        print(f"❌ Error updating plans: {e}")
        raise
    finally:
        db.close()

if __name__ == "__main__":
    print("🚀 Starting subscription plans currency update...")
    update_plans_to_ghs()
    print("\n🎉 Update completed!")
