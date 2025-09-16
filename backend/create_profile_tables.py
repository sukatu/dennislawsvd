#!/usr/bin/env python3
"""
Create Profile, Subscription, Notification, and Security Tables

This script creates all the necessary database tables for the enhanced profile system.
"""

import os
import sys
from sqlalchemy import create_engine
from config import settings

# Add the current directory to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from models import (
    Subscription, Payment, UsageRecord, SubscriptionStatus, SubscriptionPlan, PaymentStatus,
    Notification, NotificationPreference, NotificationType, NotificationStatus, NotificationPriority,
    SecurityEvent, TwoFactorAuth, ApiKey, LoginSession, SecurityEventType
)

def create_tables():
    """Create all profile-related tables"""
    try:
        # Create engine
        engine = create_engine(settings.database_url)
        
        print("Creating profile-related tables...")
        
        # Create subscription tables
        Subscription.__table__.create(engine, checkfirst=True)
        Payment.__table__.create(engine, checkfirst=True)
        UsageRecord.__table__.create(engine, checkfirst=True)
        print("✅ Subscription tables created")
        
        # Create notification tables
        Notification.__table__.create(engine, checkfirst=True)
        NotificationPreference.__table__.create(engine, checkfirst=True)
        print("✅ Notification tables created")
        
        # Create security tables
        SecurityEvent.__table__.create(engine, checkfirst=True)
        TwoFactorAuth.__table__.create(engine, checkfirst=True)
        ApiKey.__table__.create(engine, checkfirst=True)
        LoginSession.__table__.create(engine, checkfirst=True)
        print("✅ Security tables created")
        
        print("\n🎉 All profile-related tables created successfully!")
        
    except Exception as e:
        print(f"❌ Error creating tables: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    create_tables()
