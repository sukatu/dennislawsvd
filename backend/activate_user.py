#!/usr/bin/env python3
"""
Script to activate a user for testing purposes
"""

from database import SessionLocal
from models.user import User, UserStatus

def activate_user(email: str):
    """Activate a user by email."""
    db = SessionLocal()
    try:
        user = db.query(User).filter(User.email == email).first()
        if user:
            user.status = UserStatus.ACTIVE
            user.is_verified = True
            db.commit()
            print(f"✅ User {email} activated successfully!")
            return True
        else:
            print(f"❌ User {email} not found!")
            return False
    except Exception as e:
        print(f"❌ Error activating user: {e}")
        return False
    finally:
        db.close()

if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1:
        email = sys.argv[1]
        activate_user(email)
    else:
        print("Usage: python activate_user.py <email>")
