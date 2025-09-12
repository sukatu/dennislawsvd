from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from database import get_db
from models.user import User
from schemas.profile import ProfileUpdate, PasswordChange, ProfileResponse, SubscriptionResponse
from auth import get_current_user, verify_password, get_password_hash
from typing import Dict, Any
import logging

router = APIRouter()

@router.get("/profile", response_model=ProfileResponse)
async def get_profile(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get current user's profile information"""
    try:
        return ProfileResponse(
            id=current_user.id,
            email=current_user.email,
            first_name=current_user.first_name,
            last_name=current_user.last_name,
            phone_number=current_user.phone_number,
            organization=current_user.organization,
            job_title=current_user.job_title,
            bio=current_user.bio,
            language=current_user.language or "en",
            timezone=current_user.timezone or "UTC",
            email_notifications=current_user.email_notifications,
            sms_notifications=current_user.sms_notifications,
            subscription_plan=current_user.subscription_plan,
            subscription_expires=current_user.subscription_expires,
            is_premium=current_user.is_premium,
            status=current_user.status,
            created_at=current_user.created_at,
            updated_at=current_user.updated_at,
            last_login=current_user.last_login
        )
    except Exception as e:
        logging.error(f"Error getting profile: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to retrieve profile information"
        )

@router.put("/profile", response_model=ProfileResponse)
async def update_profile(
    profile_data: ProfileUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Update current user's profile information"""
    try:
        # Update only provided fields
        update_data = profile_data.dict(exclude_unset=True)
        
        for field, value in update_data.items():
            if hasattr(current_user, field):
                setattr(current_user, field, value)
        
        db.commit()
        db.refresh(current_user)
        
        return ProfileResponse(
            id=current_user.id,
            email=current_user.email,
            first_name=current_user.first_name,
            last_name=current_user.last_name,
            phone_number=current_user.phone_number,
            organization=current_user.organization,
            job_title=current_user.job_title,
            bio=current_user.bio,
            language=current_user.language or "en",
            timezone=current_user.timezone or "UTC",
            email_notifications=current_user.email_notifications,
            sms_notifications=current_user.sms_notifications,
            subscription_plan=current_user.subscription_plan,
            subscription_expires=current_user.subscription_expires,
            is_premium=current_user.is_premium,
            status=current_user.status,
            created_at=current_user.created_at,
            updated_at=current_user.updated_at,
            last_login=current_user.last_login
        )
    except Exception as e:
        logging.error(f"Error updating profile: {str(e)}")
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to update profile"
        )

@router.post("/profile/change-password")
async def change_password(
    password_data: PasswordChange,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Change user's password"""
    try:
        # Verify current password
        if not verify_password(password_data.current_password, current_user.hashed_password):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Current password is incorrect"
            )
        
        # Validate new password
        if password_data.new_password != password_data.confirm_password:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="New password and confirmation do not match"
            )
        
        if len(password_data.new_password) < 8:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="New password must be at least 8 characters long"
            )
        
        # Update password
        current_user.hashed_password = get_password_hash(password_data.new_password)
        db.commit()
        
        return {"message": "Password updated successfully"}
    except HTTPException:
        raise
    except Exception as e:
        logging.error(f"Error changing password: {str(e)}")
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to change password"
        )

@router.get("/subscription", response_model=SubscriptionResponse)
async def get_subscription(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get current user's subscription information"""
    try:
        # Mock subscription features based on plan
        if current_user.is_premium:
            features = [
                "Unlimited searches",
                "Advanced filters",
                "Priority support",
                "Export capabilities",
                "API access"
            ]
        else:
            features = [
                "Basic searches",
                "Limited filters"
            ]
        
        # Mock usage data
        usage = {
            "searches_this_month": 24,
            "max_searches": None if current_user.is_premium else 50,
            "api_calls_this_month": 0 if not current_user.is_premium else 150,
            "max_api_calls": None if current_user.is_premium else 0
        }
        
        return SubscriptionResponse(
            plan=current_user.subscription_plan or "Free",
            status=current_user.status,
            expires_at=current_user.subscription_expires,
            is_premium=current_user.is_premium,
            features=features,
            usage=usage
        )
    except Exception as e:
        logging.error(f"Error getting subscription: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to retrieve subscription information"
        )

@router.get("/profile/activity")
async def get_account_activity(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get user's account activity"""
    try:
        # Mock activity data
        activity = [
            {
                "type": "login",
                "description": "Successful login",
                "timestamp": current_user.last_login.isoformat() if current_user.last_login else None,
                "ip_address": "192.168.1.1",
                "user_agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36"
            },
            {
                "type": "profile_update",
                "description": "Profile information updated",
                "timestamp": current_user.updated_at.isoformat(),
                "ip_address": "192.168.1.1",
                "user_agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36"
            }
        ]
        
        return {
            "user_id": current_user.id,
            "activity": activity
        }
    except Exception as e:
        logging.error(f"Error getting account activity: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to retrieve account activity"
        )
