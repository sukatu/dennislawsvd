from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime

class ProfileUpdate(BaseModel):
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    phone_number: Optional[str] = None
    organization: Optional[str] = None
    job_title: Optional[str] = None
    bio: Optional[str] = None
    language: Optional[str] = "en"
    timezone: Optional[str] = "UTC"
    email_notifications: Optional[bool] = True
    sms_notifications: Optional[bool] = False

class PasswordChange(BaseModel):
    current_password: str
    new_password: str
    confirm_password: str

class ProfileResponse(BaseModel):
    id: int
    email: str
    first_name: Optional[str]
    last_name: Optional[str]
    phone_number: Optional[str]
    organization: Optional[str]
    job_title: Optional[str]
    bio: Optional[str]
    language: str
    timezone: str
    email_notifications: bool
    sms_notifications: bool
    subscription_plan: Optional[str]
    subscription_expires: Optional[datetime]
    is_premium: bool
    status: str
    created_at: datetime
    updated_at: datetime
    last_login: Optional[datetime]

    class Config:
        from_attributes = True

class SubscriptionResponse(BaseModel):
    plan: str
    status: str
    expires_at: Optional[datetime]
    is_premium: bool
    features: list[str]
    usage: dict

    class Config:
        from_attributes = True
