from sqlalchemy import Column, Integer, String, DateTime, Boolean, Text, Enum, ForeignKey, JSON
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from database import Base
import enum

class NotificationType(str, enum.Enum):
    SYSTEM = "system"
    SUBSCRIPTION = "subscription"
    SECURITY = "security"
    SEARCH = "search"
    CASE_UPDATE = "case_update"
    PAYMENT = "payment"
    GENERAL = "general"

class NotificationStatus(str, enum.Enum):
    UNREAD = "unread"
    READ = "read"
    ARCHIVED = "archived"

class NotificationPriority(str, enum.Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    URGENT = "urgent"

class Notification(Base):
    __tablename__ = "notifications"
    
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)
    
    # Notification content
    title = Column(String(255), nullable=False)
    message = Column(Text, nullable=False)
    type = Column(Enum(NotificationType), nullable=False, default=NotificationType.GENERAL)
    priority = Column(Enum(NotificationPriority), nullable=False, default=NotificationPriority.MEDIUM)
    
    # Status and delivery
    status = Column(Enum(NotificationStatus), nullable=False, default=NotificationStatus.UNREAD)
    is_email_sent = Column(Boolean, default=False, nullable=False)
    is_sms_sent = Column(Boolean, default=False, nullable=False)
    is_push_sent = Column(Boolean, default=False, nullable=False)
    
    # Action and metadata
    action_url = Column(String(500), nullable=True)  # URL to navigate to when clicked
    action_text = Column(String(100), nullable=True)  # Text for action button
    notification_metadata = Column(JSON, nullable=True)  # Additional data
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    read_at = Column(DateTime(timezone=True), nullable=True)
    archived_at = Column(DateTime(timezone=True), nullable=True)
    
    # Relationships
    user = relationship("User", back_populates="notifications")

class NotificationPreference(Base):
    __tablename__ = "notification_preferences"
    
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True, unique=True)
    
    # Email preferences
    email_enabled = Column(Boolean, default=True, nullable=False)
    email_system = Column(Boolean, default=True, nullable=False)
    email_subscription = Column(Boolean, default=True, nullable=False)
    email_security = Column(Boolean, default=True, nullable=False)
    email_search = Column(Boolean, default=False, nullable=False)
    email_case_updates = Column(Boolean, default=False, nullable=False)
    email_payments = Column(Boolean, default=True, nullable=False)
    
    # SMS preferences
    sms_enabled = Column(Boolean, default=False, nullable=False)
    sms_system = Column(Boolean, default=True, nullable=False)
    sms_subscription = Column(Boolean, default=True, nullable=False)
    sms_security = Column(Boolean, default=True, nullable=False)
    sms_payments = Column(Boolean, default=True, nullable=False)
    
    # Push preferences
    push_enabled = Column(Boolean, default=True, nullable=False)
    push_system = Column(Boolean, default=True, nullable=False)
    push_subscription = Column(Boolean, default=True, nullable=False)
    push_security = Column(Boolean, default=True, nullable=False)
    push_search = Column(Boolean, default=False, nullable=False)
    push_case_updates = Column(Boolean, default=False, nullable=False)
    push_payments = Column(Boolean, default=True, nullable=False)
    
    # Frequency settings
    digest_frequency = Column(String(20), default="daily", nullable=False)  # daily, weekly, never
    quiet_hours_start = Column(String(5), nullable=True)  # HH:MM format
    quiet_hours_end = Column(String(5), nullable=True)   # HH:MM format
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)
    
    # Relationships
    user = relationship("User", back_populates="notification_preferences")
