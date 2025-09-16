from pydantic import BaseModel
from typing import Optional, List, Dict, Any
from datetime import datetime

class NotificationCreate(BaseModel):
    title: str
    message: str
    type: str = "general"
    priority: str = "medium"
    action_url: Optional[str] = None
    action_text: Optional[str] = None
    notification_metadata: Optional[Dict[str, Any]] = None

class NotificationUpdate(BaseModel):
    status: Optional[str] = None
    read_at: Optional[datetime] = None
    archived_at: Optional[datetime] = None

class NotificationResponse(BaseModel):
    id: int
    user_id: int
    title: str
    message: str
    type: str
    priority: str
    status: str
    is_email_sent: bool
    is_sms_sent: bool
    is_push_sent: bool
    action_url: Optional[str]
    action_text: Optional[str]
    notification_metadata: Optional[Dict[str, Any]]
    created_at: datetime
    read_at: Optional[datetime]
    archived_at: Optional[datetime]

    class Config:
        from_attributes = True

class NotificationPreferenceUpdate(BaseModel):
    # Email preferences
    email_enabled: Optional[bool] = None
    email_system: Optional[bool] = None
    email_subscription: Optional[bool] = None
    email_security: Optional[bool] = None
    email_search: Optional[bool] = None
    email_case_updates: Optional[bool] = None
    email_payments: Optional[bool] = None
    
    # SMS preferences
    sms_enabled: Optional[bool] = None
    sms_system: Optional[bool] = None
    sms_subscription: Optional[bool] = None
    sms_security: Optional[bool] = None
    sms_payments: Optional[bool] = None
    
    # Push preferences
    push_enabled: Optional[bool] = None
    push_system: Optional[bool] = None
    push_subscription: Optional[bool] = None
    push_security: Optional[bool] = None
    push_search: Optional[bool] = None
    push_case_updates: Optional[bool] = None
    push_payments: Optional[bool] = None
    
    # Frequency settings
    digest_frequency: Optional[str] = None
    quiet_hours_start: Optional[str] = None
    quiet_hours_end: Optional[str] = None

class NotificationPreferenceResponse(BaseModel):
    id: int
    user_id: int
    email_enabled: bool
    email_system: bool
    email_subscription: bool
    email_security: bool
    email_search: bool
    email_case_updates: bool
    email_payments: bool
    sms_enabled: bool
    sms_system: bool
    sms_subscription: bool
    sms_security: bool
    sms_payments: bool
    push_enabled: bool
    push_system: bool
    push_subscription: bool
    push_security: bool
    push_search: bool
    push_case_updates: bool
    push_payments: bool
    digest_frequency: str
    quiet_hours_start: Optional[str]
    quiet_hours_end: Optional[str]
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

class NotificationStatsResponse(BaseModel):
    total: int
    unread: int
    read: int
    archived: int
    by_type: Dict[str, int]
    by_priority: Dict[str, int]
