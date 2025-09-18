#!/usr/bin/env python3
"""
Script to create sample notifications in the database
"""

import sys
import os
from sqlalchemy.orm import Session
from datetime import datetime, timedelta

# Add the backend directory to the Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from database import SessionLocal
from models.notification import Notification, NotificationType, NotificationPriority, NotificationStatus
from models.user import User

def create_sample_notifications():
    """Create sample notifications for testing"""
    
    db = SessionLocal()
    try:
        # Get the first user (assuming there's at least one user)
        user = db.query(User).first()
        if not user:
            print("No users found in database. Please create a user first.")
            return
        
        print(f"Creating sample notifications for user: {user.email}")
        
        # Check if notifications already exist
        existing_count = db.query(Notification).filter(Notification.user_id == user.id).count()
        if existing_count > 0:
            print(f"User already has {existing_count} notifications. Skipping creation.")
            return
        
        # Sample notifications
        sample_notifications = [
            {
                "title": "Subscription Approved",
                "message": "Your Professional plan subscription has been approved and activated. You now have access to all premium features including AI-powered case analysis and advanced search capabilities.",
                "type": NotificationType.SUBSCRIPTION,
                "priority": NotificationPriority.HIGH,
                "category": "subscription",
                "action_url": "/subscribe",
                "notification_data": {"plan": "professional", "amount": 960.00, "currency": "GHS"},
                "created_at": datetime.utcnow() - timedelta(minutes=2)
            },
            {
                "title": "New Case Added",
                "message": "A new case 'Smith vs. Johnson - Contract Dispute' has been added to your watchlist. This case involves breach of contract and may be relevant to your current research.",
                "type": NotificationType.CASE_UPDATE,
                "priority": NotificationPriority.MEDIUM,
                "category": "cases",
                "action_url": "/case-details/123",
                "notification_data": {"case_id": 123, "case_title": "Smith vs. Johnson - Contract Dispute"},
                "created_at": datetime.utcnow() - timedelta(hours=1)
            },
            {
                "title": "Payment Due",
                "message": "Your subscription payment is due in 3 days. Please update your payment method to avoid service interruption. You can update your billing information in Settings.",
                "type": NotificationType.PAYMENT,
                "priority": NotificationPriority.HIGH,
                "category": "billing",
                "action_url": "/settings",
                "notification_data": {"due_date": "2025-09-20", "amount": 960.00},
                "created_at": datetime.utcnow() - timedelta(hours=2)
            },
            {
                "title": "System Update",
                "message": "We've released new features including AI-powered case analysis, enhanced search filters, and improved mobile experience. Check out the new features in your dashboard.",
                "type": NotificationType.SYSTEM,
                "priority": NotificationPriority.MEDIUM,
                "category": "system",
                "action_url": "/",
                "notification_data": {"version": "2.1.0", "features": ["ai_analysis", "enhanced_search", "mobile_ui"]},
                "created_at": datetime.utcnow() - timedelta(days=1)
            },
            {
                "title": "Profile Updated",
                "message": "Your profile information has been successfully updated. Your new preferences are now active across all features.",
                "type": NotificationType.GENERAL,
                "priority": NotificationPriority.LOW,
                "category": "profile",
                "action_url": "/settings",
                "notification_data": {"updated_fields": ["email", "phone"]},
                "created_at": datetime.utcnow() - timedelta(days=2)
            },
            {
                "title": "Weekly Report",
                "message": "Your weekly activity report is ready. You've searched 15 cases this week and saved 3 to your watchlist. View detailed analytics in your dashboard.",
                "type": NotificationType.GENERAL,
                "priority": NotificationPriority.LOW,
                "category": "reports",
                "action_url": "/admin",
                "notification_data": {"searches": 15, "saved_cases": 3, "week": "2025-W37"},
                "created_at": datetime.utcnow() - timedelta(days=3)
            },
            {
                "title": "Storage Limit",
                "message": "You're approaching your storage limit (85% used). Consider upgrading your plan or cleaning up old files to avoid service interruption.",
                "type": NotificationType.SYSTEM,
                "priority": NotificationPriority.MEDIUM,
                "category": "storage",
                "action_url": "/settings",
                "notification_data": {"usage_percent": 85, "used_gb": 4.25, "total_gb": 5.0},
                "created_at": datetime.utcnow() - timedelta(days=7)
            },
            {
                "title": "New Feature Available",
                "message": "Document upload and AI analysis is now available for all users. Upload your legal documents and get instant AI-powered insights.",
                "type": NotificationType.SYSTEM,
                "priority": NotificationPriority.MEDIUM,
                "category": "features",
                "action_url": "/",
                "notification_data": {"feature": "document_upload", "ai_analysis": True},
                "created_at": datetime.utcnow() - timedelta(days=7)
            }
        ]
        
        # Create notifications
        created_count = 0
        for notification_data in sample_notifications:
            notification = Notification(
                user_id=user.id,
                **notification_data
            )
            db.add(notification)
            created_count += 1
        
        db.commit()
        print(f"✅ Successfully created {created_count} sample notifications!")
        
        # Display created notifications
        print("\nCreated Notifications:")
        notifications = db.query(Notification).filter(Notification.user_id == user.id).order_by(Notification.created_at.desc()).all()
        for notification in notifications:
            print(f"  - {notification.title} ({notification.type.value}) - {notification.created_at.strftime('%Y-%m-%d %H:%M')}")
        
    except Exception as e:
        db.rollback()
        print(f"❌ Error creating notifications: {e}")
        raise
    finally:
        db.close()

if __name__ == "__main__":
    print("🚀 Creating sample notifications...")
    create_sample_notifications()
    print("\n🎉 Sample notifications created successfully!")
