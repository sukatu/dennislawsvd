from pydantic import BaseModel, EmailStr
from typing import List, Optional
from datetime import datetime
from enum import Enum

# Enums
class UserRole(str, Enum):
    admin = "admin"
    user = "user"
    moderator = "moderator"

class UserStatus(str, Enum):
    active = "active"
    inactive = "inactive"
    suspended = "suspended"
    pending = "pending"

class PaymentStatus(str, Enum):
    pending = "pending"
    completed = "completed"
    failed = "failed"
    refunded = "refunded"
    cancelled = "cancelled"

class SubscriptionStatus(str, Enum):
    active = "active"
    inactive = "inactive"
    cancelled = "cancelled"
    expired = "expired"
    pending = "pending"

# Base Models
class BaseResponse(BaseModel):
    class Config:
        from_attributes = True

# Dashboard Statistics
class AdminStatsResponse(BaseResponse):
    total_users: int
    total_cases: int
    total_people: int
    total_banks: int
    total_insurance: int
    total_companies: int
    total_payments: int
    active_subscriptions: int
    recent_users: int
    recent_cases: int
    last_updated: datetime

# User Management
class UserBase(BaseModel):
    email: EmailStr
    first_name: str
    last_name: str
    role: UserRole = UserRole.user
    status: UserStatus = UserStatus.active
    is_admin: bool = False

class UserCreateRequest(UserBase):
    pass

class UserUpdateRequest(BaseModel):
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    role: Optional[UserRole] = None
    status: Optional[UserStatus] = None
    is_admin: Optional[bool] = None

class UserResponse(BaseResponse):
    id: int
    email: str
    first_name: str
    last_name: str
    role: str
    status: str
    is_admin: bool
    created_at: datetime
    updated_at: datetime
    last_login: Optional[datetime] = None

class UserDetailResponse(UserResponse):
    subscription: Optional[dict] = None
    notifications_count: int = 0
    api_keys_count: int = 0

class UserListResponse(BaseModel):
    users: List[UserResponse]
    total: int
    page: int
    limit: int
    total_pages: int

# API Key Management
class ApiKeyBase(BaseModel):
    user_id: int
    name: str
    expires_in_days: Optional[int] = None

class ApiKeyCreateRequest(ApiKeyBase):
    pass

class ApiKeyResponse(BaseResponse):
    id: int
    user_id: int
    name: str
    key_prefix: str
    full_key: Optional[str] = None  # Only returned on creation
    is_active: bool
    created_at: datetime
    last_used: Optional[datetime] = None
    expires_at: Optional[datetime] = None

# Case Management
class CaseResponse(BaseResponse):
    id: int
    title: str
    suit_reference_number: Optional[str] = None
    date: Optional[str] = None  # Changed to string to handle various date formats
    presiding_judge: Optional[str] = None
    protagonist: Optional[str] = None
    antagonist: Optional[str] = None
    court_type: Optional[str] = None
    court_division: Optional[str] = None
    status: Optional[str] = None
    created_at: datetime
    updated_at: datetime

class CaseDetailResponse(CaseResponse):
    statutes_cited: Optional[str] = None
    cases_cited: Optional[str] = None
    lawyers: Optional[str] = None
    commentary: Optional[str] = None
    headnotes: Optional[str] = None
    town: Optional[str] = None
    region: Optional[str] = None
    dl_citation_no: Optional[str] = None
    file_url: Optional[str] = None
    judgement: Optional[str] = None
    year: Optional[int] = None
    type: Optional[str] = None
    firebase_url: Optional[str] = None
    summernote: Optional[str] = None
    detail_content: Optional[str] = None
    decision: Optional[str] = None
    citation: Optional[str] = None
    file_name: Optional[str] = None
    c_t: Optional[str] = None
    judgement_by: Optional[str] = None
    case_summary: Optional[str] = None
    area_of_law: Optional[str] = None
    keywords_phrases: Optional[str] = None
    published: Optional[bool] = None
    dl_type: Optional[str] = None
    academic_programme_id: Optional[int] = None
    opinion_by: Optional[str] = None
    conclusion: Optional[str] = None
    ai_case_outcome: Optional[str] = None
    ai_court_orders: Optional[str] = None
    ai_financial_impact: Optional[str] = None
    ai_detailed_outcome: Optional[str] = None
    ai_summary_generated_at: Optional[str] = None  # Changed to string
    ai_summary_version: Optional[str] = None

class CaseCreateRequest(BaseModel):
    title: str
    suit_reference_number: Optional[str] = None
    date: Optional[datetime] = None
    presiding_judge: Optional[str] = None
    protagonist: Optional[str] = None
    antagonist: Optional[str] = None
    court_type: Optional[str] = None
    court_division: Optional[str] = None
    status: Optional[str] = None
    statutes_cited: Optional[str] = None
    cases_cited: Optional[str] = None
    lawyers: Optional[str] = None
    commentary: Optional[str] = None
    headnotes: Optional[str] = None
    town: Optional[str] = None
    region: Optional[str] = None
    dl_citation_no: Optional[str] = None
    file_url: Optional[str] = None
    judgement: Optional[str] = None
    year: Optional[int] = None
    type: Optional[str] = None
    firebase_url: Optional[str] = None
    summernote: Optional[str] = None
    detail_content: Optional[str] = None
    decision: Optional[str] = None
    citation: Optional[str] = None
    file_name: Optional[str] = None
    c_t: Optional[str] = None
    judgement_by: Optional[str] = None
    case_summary: Optional[str] = None
    area_of_law: Optional[str] = None
    keywords_phrases: Optional[str] = None
    published: Optional[bool] = None
    dl_type: Optional[str] = None
    academic_programme_id: Optional[int] = None
    opinion_by: Optional[str] = None
    conclusion: Optional[str] = None

class CaseUpdateRequest(BaseModel):
    title: Optional[str] = None
    suit_reference_number: Optional[str] = None
    date: Optional[datetime] = None
    presiding_judge: Optional[str] = None
    protagonist: Optional[str] = None
    antagonist: Optional[str] = None
    court_type: Optional[str] = None
    court_division: Optional[str] = None
    status: Optional[str] = None
    statutes_cited: Optional[str] = None
    cases_cited: Optional[str] = None
    lawyers: Optional[str] = None
    commentary: Optional[str] = None
    headnotes: Optional[str] = None
    town: Optional[str] = None
    region: Optional[str] = None
    dl_citation_no: Optional[str] = None
    file_url: Optional[str] = None
    judgement: Optional[str] = None
    year: Optional[int] = None
    type: Optional[str] = None
    firebase_url: Optional[str] = None
    summernote: Optional[str] = None
    detail_content: Optional[str] = None
    decision: Optional[str] = None
    citation: Optional[str] = None
    file_name: Optional[str] = None
    c_t: Optional[str] = None
    judgement_by: Optional[str] = None
    case_summary: Optional[str] = None
    area_of_law: Optional[str] = None
    keywords_phrases: Optional[str] = None
    published: Optional[bool] = None
    dl_type: Optional[str] = None
    academic_programme_id: Optional[int] = None
    opinion_by: Optional[str] = None
    conclusion: Optional[str] = None

class CaseListResponse(BaseModel):
    cases: List[CaseResponse]
    total: int
    page: int
    limit: int
    total_pages: int

# People Management
class PeopleResponse(BaseResponse):
    id: int
    first_name: str
    last_name: str
    full_name: str
    previous_names: Optional[str] = None
    date_of_birth: Optional[datetime] = None
    date_of_death: Optional[datetime] = None
    id_number: Optional[str] = None
    phone_number: Optional[str] = None
    email: Optional[str] = None
    address: Optional[str] = None
    city: Optional[str] = None
    region: Optional[str] = None
    country: Optional[str] = None
    postal_code: Optional[str] = None
    risk_level: Optional[str] = None
    risk_score: Optional[float] = None
    case_count: Optional[int] = None
    case_types: Optional[str] = None
    court_records: Optional[str] = None
    occupation: Optional[str] = None
    employer: Optional[str] = None
    organization: Optional[str] = None
    job_title: Optional[str] = None
    marital_status: Optional[str] = None
    spouse_name: Optional[str] = None
    children_count: Optional[int] = None
    emergency_contact: Optional[str] = None
    emergency_phone: Optional[str] = None
    nationality: Optional[str] = None
    gender: Optional[str] = None
    education_level: Optional[str] = None
    languages: Optional[str] = None
    is_verified: Optional[bool] = None
    verification_date: Optional[datetime] = None
    verification_notes: Optional[str] = None
    last_searched: Optional[datetime] = None
    search_count: Optional[int] = None
    created_at: datetime
    updated_at: datetime
    created_by: Optional[int] = None
    updated_by: Optional[int] = None
    status: Optional[str] = None
    notes: Optional[str] = None

class PeopleListResponse(BaseModel):
    people: List[PeopleResponse]
    total: int
    page: int
    limit: int
    total_pages: int

# Bank Management
class BankResponse(BaseResponse):
    id: int
    name: str
    short_name: Optional[str] = None
    logo_url: Optional[str] = None
    website: Optional[str] = None
    phone: Optional[str] = None
    email: Optional[str] = None
    address: Optional[str] = None
    city: Optional[str] = None
    region: Optional[str] = None
    country: Optional[str] = None
    postal_code: Optional[str] = None
    bank_code: Optional[str] = None
    swift_code: Optional[str] = None
    license_number: Optional[str] = None
    established_date: Optional[datetime] = None
    bank_type: Optional[str] = None
    ownership_type: Optional[str] = None
    services: Optional[str] = None
    previous_names: Optional[str] = None
    branches_count: Optional[int] = None
    atm_count: Optional[int] = None
    total_assets: Optional[float] = None
    net_worth: Optional[float] = None
    rating: Optional[float] = None
    head_office_address: Optional[str] = None
    customer_service_phone: Optional[str] = None
    customer_service_email: Optional[str] = None
    has_mobile_app: Optional[bool] = None
    has_online_banking: Optional[bool] = None
    has_atm_services: Optional[bool] = None
    has_foreign_exchange: Optional[bool] = None
    is_active: Optional[bool] = None
    is_verified: Optional[bool] = None
    verification_date: Optional[datetime] = None
    verification_notes: Optional[str] = None
    search_count: Optional[int] = None
    last_searched: Optional[datetime] = None
    created_at: datetime
    updated_at: datetime
    created_by: Optional[int] = None
    updated_by: Optional[int] = None
    description: Optional[str] = None
    notes: Optional[str] = None
    status: Optional[str] = None

class BankListResponse(BaseModel):
    banks: List[BankResponse]
    total: int
    page: int
    limit: int
    total_pages: int

# Insurance Management
class InsuranceResponse(BaseResponse):
    id: int
    name: str
    short_name: Optional[str] = None
    logo_url: Optional[str] = None
    website: Optional[str] = None
    phone: Optional[str] = None
    email: Optional[str] = None
    address: Optional[str] = None
    city: Optional[str] = None
    region: Optional[str] = None
    country: Optional[str] = None
    postal_code: Optional[str] = None
    license_number: Optional[str] = None
    established_date: Optional[datetime] = None
    insurance_type: Optional[str] = None
    ownership_type: Optional[str] = None
    services: Optional[str] = None
    previous_names: Optional[str] = None
    branches_count: Optional[int] = None
    total_assets: Optional[float] = None
    net_worth: Optional[float] = None
    rating: Optional[float] = None
    head_office_address: Optional[str] = None
    customer_service_phone: Optional[str] = None
    customer_service_email: Optional[str] = None
    has_mobile_app: Optional[bool] = None
    has_online_portal: Optional[bool] = None
    has_claims_processing: Optional[bool] = None
    has_underwriting: Optional[bool] = None
    is_active: Optional[bool] = None
    is_verified: Optional[bool] = None
    verification_date: Optional[datetime] = None
    verification_notes: Optional[str] = None
    search_count: Optional[int] = None
    last_searched: Optional[datetime] = None
    created_at: datetime
    updated_at: datetime
    created_by: Optional[int] = None
    updated_by: Optional[int] = None
    description: Optional[str] = None
    notes: Optional[str] = None
    status: Optional[str] = None

class InsuranceListResponse(BaseModel):
    insurance: List[InsuranceResponse]
    total: int
    page: int
    limit: int
    total_pages: int

# Company Management
class CompanyResponse(BaseResponse):
    id: int
    name: str
    short_name: Optional[str] = None
    logo_url: Optional[str] = None
    website: Optional[str] = None
    phone: Optional[str] = None
    email: Optional[str] = None
    address: Optional[str] = None
    city: Optional[str] = None
    region: Optional[str] = None
    country: Optional[str] = None
    postal_code: Optional[str] = None
    registration_number: Optional[str] = None
    tax_identification_number: Optional[str] = None
    established_date: Optional[datetime] = None
    company_type: Optional[str] = None
    ownership_type: Optional[str] = None
    business_activities: Optional[str] = None
    directors: Optional[str] = None
    secretary: Optional[str] = None
    auditor: Optional[str] = None
    total_assets: Optional[float] = None
    net_worth: Optional[float] = None
    rating: Optional[float] = None
    head_office_address: Optional[str] = None
    customer_service_phone: Optional[str] = None
    customer_service_email: Optional[str] = None
    is_active: Optional[bool] = None
    is_verified: Optional[bool] = None
    verification_date: Optional[datetime] = None
    verification_notes: Optional[str] = None
    search_count: Optional[int] = None
    last_searched: Optional[datetime] = None
    created_at: datetime
    updated_at: datetime
    created_by: Optional[int] = None
    updated_by: Optional[int] = None
    description: Optional[str] = None
    notes: Optional[str] = None
    status: Optional[str] = None

class CompanyListResponse(BaseModel):
    companies: List[CompanyResponse]
    total: int
    page: int
    limit: int
    total_pages: int

# Payment Management
class PaymentResponse(BaseResponse):
    id: int
    user_id: int
    subscription_id: Optional[int] = None
    amount: float
    currency: str
    status: str
    payment_method: Optional[str] = None
    transaction_id: Optional[str] = None
    gateway_response: Optional[str] = None
    created_at: datetime
    updated_at: datetime

class PaymentListResponse(BaseModel):
    payments: List[PaymentResponse]
    total: int
    page: int
    limit: int
    total_pages: int

# Subscription Management
class SubscriptionResponse(BaseResponse):
    id: int
    user_id: int
    plan: str
    status: str
    start_date: datetime
    end_date: Optional[datetime] = None
    auto_renew: bool
    created_at: datetime
    updated_at: datetime

class SubscriptionListResponse(BaseModel):
    subscriptions: List[SubscriptionResponse]
    total: int
    page: int
    limit: int
    total_pages: int
