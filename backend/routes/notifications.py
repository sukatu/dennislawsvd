from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from database import get_db
from models.user import User
from models.notification import Notification, NotificationPreference, NotificationType, NotificationStatus, NotificationPriority
from schemas.notification import (
    NotificationResponse, NotificationCreate, NotificationUpdate,
    NotificationPreferenceResponse, NotificationPreferenceUpdate, NotificationStatsResponse
)
from auth import get_current_user
from typing import List, Optional
import logging
from datetime import datetime, timedelta

router = APIRouter()

@router.get("/", response_model=List[NotificationResponse])
async def get_notifications(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
    status_filter: Optional[str] = Query(None, description="Filter by status: unread, read, archived"),
    type_filter: Optional[str] = Query(None, description="Filter by type"),
    limit: int = Query(50, le=100),
    offset: int = Query(0, ge=0)
):
    """Get user's notifications with optional filtering"""
    try:
        query = db.query(Notification).filter(Notification.user_id == current_user.id)
        
        if status_filter:
            query = query.filter(Notification.status == NotificationStatus(status_filter))
        
        if type_filter:
            query = query.filter(Notification.type == NotificationType(type_filter))
        
        notifications = query.order_by(Notification.created_at.desc()).offset(offset).limit(limit).all()
        
        return [NotificationResponse.from_orm(notification) for notification in notifications]
    except Exception as e:
        logging.error(f"Error getting notifications: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to retrieve notifications"
        )

@router.get("/stats", response_model=NotificationStatsResponse)
async def get_notification_stats(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get notification statistics for the user"""
    try:
        # Get total counts
        total = db.query(Notification).filter(Notification.user_id == current_user.id).count()
        unread = db.query(Notification).filter(
            Notification.user_id == current_user.id,
            Notification.status == NotificationStatus.UNREAD
        ).count()
        read = db.query(Notification).filter(
            Notification.user_id == current_user.id,
            Notification.status == NotificationStatus.READ
        ).count()
        archived = db.query(Notification).filter(
            Notification.user_id == current_user.id,
            Notification.status == NotificationStatus.ARCHIVED
        ).count()
        
        # Get counts by type
        by_type = {}
        for notification_type in NotificationType:
            count = db.query(Notification).filter(
                Notification.user_id == current_user.id,
                Notification.type == notification_type
            ).count()
            by_type[notification_type.value] = count
        
        # Get counts by priority
        by_priority = {}
        for priority in NotificationPriority:
            count = db.query(Notification).filter(
                Notification.user_id == current_user.id,
                Notification.priority == priority
            ).count()
            by_priority[priority.value] = count
        
        return NotificationStatsResponse(
            total=total,
            unread=unread,
            read=read,
            archived=archived,
            by_type=by_type,
            by_priority=by_priority
        )
    except Exception as e:
        logging.error(f"Error getting notification stats: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to retrieve notification statistics"
        )

@router.post("/", response_model=NotificationResponse)
async def create_notification(
    notification_data: NotificationCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Create a new notification for the user"""
    try:
        notification = Notification(
            user_id=current_user.id,
            title=notification_data.title,
            message=notification_data.message,
            type=NotificationType(notification_data.type),
            priority=NotificationPriority(notification_data.priority),
            action_url=notification_data.action_url,
            action_text=notification_data.action_text,
            notification_metadata=notification_data.notification_metadata
        )
        
        db.add(notification)
        db.commit()
        db.refresh(notification)
        
        return NotificationResponse.from_orm(notification)
    except Exception as e:
        logging.error(f"Error creating notification: {str(e)}")
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to create notification"
        )

@router.put("/{notification_id}", response_model=NotificationResponse)
async def update_notification(
    notification_id: int,
    notification_data: NotificationUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Update a notification"""
    try:
        notification = db.query(Notification).filter(
            Notification.id == notification_id,
            Notification.user_id == current_user.id
        ).first()
        
        if not notification:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Notification not found"
            )
        
        # Update fields
        if notification_data.status:
            notification.status = NotificationStatus(notification_data.status)
            if notification_data.status == "read" and not notification.read_at:
                notification.read_at = datetime.now()
            elif notification_data.status == "archived" and not notification.archived_at:
                notification.archived_at = datetime.now()
        
        if notification_data.read_at:
            notification.read_at = notification_data.read_at
        
        if notification_data.archived_at:
            notification.archived_at = notification_data.archived_at
        
        db.commit()
        db.refresh(notification)
        
        return NotificationResponse.from_orm(notification)
    except HTTPException:
        raise
    except Exception as e:
        logging.error(f"Error updating notification: {str(e)}")
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to update notification"
        )

@router.delete("/{notification_id}")
async def delete_notification(
    notification_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Delete a notification"""
    try:
        notification = db.query(Notification).filter(
            Notification.id == notification_id,
            Notification.user_id == current_user.id
        ).first()
        
        if not notification:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Notification not found"
            )
        
        db.delete(notification)
        db.commit()
        
        return {"message": "Notification deleted successfully"}
    except HTTPException:
        raise
    except Exception as e:
        logging.error(f"Error deleting notification: {str(e)}")
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to delete notification"
        )

@router.post("/mark-all-read")
async def mark_all_notifications_read(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Mark all notifications as read"""
    try:
        db.query(Notification).filter(
            Notification.user_id == current_user.id,
            Notification.status == NotificationStatus.UNREAD
        ).update({
            "status": NotificationStatus.READ,
            "read_at": datetime.now()
        })
        
        db.commit()
        
        return {"message": "All notifications marked as read"}
    except Exception as e:
        logging.error(f"Error marking notifications as read: {str(e)}")
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to mark notifications as read"
        )

@router.get("/preferences", response_model=NotificationPreferenceResponse)
async def get_notification_preferences(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get user's notification preferences"""
    try:
        preferences = current_user.notification_preferences
        
        if not preferences:
            # Create default preferences
            preferences = NotificationPreference(
                user_id=current_user.id,
                email_enabled=True,
                email_system=True,
                email_subscription=True,
                email_security=True,
                email_search=False,
                email_case_updates=False,
                email_payments=True,
                sms_enabled=False,
                sms_system=True,
                sms_subscription=True,
                sms_security=True,
                sms_payments=True,
                push_enabled=True,
                push_system=True,
                push_subscription=True,
                push_security=True,
                push_search=False,
                push_case_updates=False,
                push_payments=True,
                digest_frequency="daily"
            )
            db.add(preferences)
            db.commit()
            db.refresh(preferences)
        
        return NotificationPreferenceResponse.from_orm(preferences)
    except Exception as e:
        logging.error(f"Error getting notification preferences: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to retrieve notification preferences"
        )

@router.put("/preferences", response_model=NotificationPreferenceResponse)
async def update_notification_preferences(
    preferences_data: NotificationPreferenceUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Update user's notification preferences"""
    try:
        preferences = current_user.notification_preferences
        
        if not preferences:
            # Create new preferences
            preferences = NotificationPreference(user_id=current_user.id)
            db.add(preferences)
        
        # Update only provided fields
        update_data = preferences_data.dict(exclude_unset=True)
        for field, value in update_data.items():
            if hasattr(preferences, field):
                setattr(preferences, field, value)
        
        db.commit()
        db.refresh(preferences)
        
        return NotificationPreferenceResponse.from_orm(preferences)
    except Exception as e:
        logging.error(f"Error updating notification preferences: {str(e)}")
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to update notification preferences"
        )
