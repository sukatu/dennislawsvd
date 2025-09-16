from pydantic import BaseModel, EmailStr, validator
from typing import Optional, List
from datetime import datetime
from models.user import UserRole, UserStatus

# Base user schema
class UserBase(BaseModel):
    email: EmailStr
    first_name: str
    last_name: str
    phone_number: Optional[str] = None
    organization: Optional[str] = None
    job_title: Optional[str] = None
    bio: Optional[str] = None
    language: str = "en"
    timezone: str = "UTC"
    email_notifications: bool = True
    sms_notifications: bool = False

# User creation schema
class UserCreate(UserBase):
    password: str
    username: Optional[str] = None
    
    @validator('password')
    def validate_password(cls, v):
        if len(v) < 8:
            raise ValueError('Password must be at least 8 characters long')
        return v
    
    @validator('first_name', 'last_name')
    def validate_names(cls, v):
        if not v or len(v.strip()) < 2:
            raise ValueError('Name must be at least 2 characters long')
        return v.strip()

# User update schema
class UserUpdate(BaseModel):
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    phone_number: Optional[str] = None
    organization: Optional[str] = None
    job_title: Optional[str] = None
    bio: Optional[str] = None
    language: Optional[str] = None
    timezone: Optional[str] = None
    email_notifications: Optional[bool] = None
    sms_notifications: Optional[bool] = None
    profile_picture: Optional[str] = None
    
    @validator('first_name', 'last_name')
    def validate_names(cls, v):
        if v is not None and (not v or len(v.strip()) < 2):
            raise ValueError('Name must be at least 2 characters long')
        return v.strip() if v else v

# User response schema (what gets returned to client)
class UserResponse(UserBase):
    id: int
    username: Optional[str]
    is_verified: bool
    role: UserRole
    status: UserStatus
    is_admin: bool
    profile_picture: Optional[str]
    subscription_plan: Optional[str]
    is_premium: bool
    created_at: datetime
    updated_at: datetime
    last_login: Optional[datetime]
    
    class Config:
        from_attributes = True

# User login schema
class UserLogin(BaseModel):
    email: EmailStr
    password: str

# Password change schema
class PasswordChange(BaseModel):
    current_password: str
    new_password: str
    
    @validator('new_password')
    def validate_new_password(cls, v):
        if len(v) < 8:
            raise ValueError('Password must be at least 8 characters long')
        return v

# Password reset request schema
class PasswordResetRequest(BaseModel):
    email: EmailStr

# Password reset schema
class PasswordReset(BaseModel):
    token: str
    new_password: str
    
    @validator('new_password')
    def validate_new_password(cls, v):
        if len(v) < 8:
            raise ValueError('Password must be at least 8 characters long')
        return v

# Google OAuth schema
class GoogleAuth(BaseModel):
    google_token: str

# User list response (for admin)
class UserListResponse(BaseModel):
    users: List[UserResponse]
    total: int
    page: int
    per_page: int
    total_pages: int

# User stats schema
class UserStats(BaseModel):
    total_users: int
    active_users: int
    premium_users: int
    new_users_today: int
    new_users_this_month: int
