# Juridence Legal Database API v1.0.0

Comprehensive API for the Juridence Legal Database System

## Base URL
```
https://api.juridence.com
```

## Authentication
Include your API key in the Authorization header

```
Authorization: Bearer your-api-key-here
```

## Rate Limits
- **Free Tier**: 100 requests/hour
- **Professional**: 1,000 requests/hour
- **Enterprise**: 10,000 requests/hour

## API Endpoints

### General

#### GET, HEAD /openapi.json

**Parameters:**

- `req` (<class 'starlette.requests.Request'>) ✓

---

#### GET, HEAD /docs

**Parameters:**

- `req` (<class 'starlette.requests.Request'>) ✓

---

#### GET, HEAD /docs/oauth2-redirect

**Parameters:**

- `req` (<class 'starlette.requests.Request'>) ✓

---

#### GET, HEAD /redoc

**Parameters:**

- `req` (<class 'starlette.requests.Request'>) ✓

---

#### GET /

---

#### GET /health

---

### Authentication

#### POST /auth/register

**Register a new user.**

**Parameters:**

- `user_data` (<class 'schemas.user.UserCreate'>) ✓

---

#### POST /auth/login

**Login user with email and password.**

**Parameters:**

- `login_data` (<class 'schemas.user.UserLogin'>) ✓

---

#### POST /auth/google

**Login/Register with Google OAuth.**

**Parameters:**

- `google_data` (<class 'schemas.user.GoogleAuth'>) ✓

---

#### POST /auth/forgot-password

**Request password reset.**

**Parameters:**

- `request` (<class 'schemas.user.PasswordResetRequest'>) ✓

---

#### POST /auth/reset-password

**Reset password with token.**

**Parameters:**

- `reset_data` (<class 'schemas.user.PasswordReset'>) ✓

---

#### POST /auth/change-password

**Change user password.**

**Parameters:**

- `password_data` (<class 'schemas.user.PasswordChange'>) ✓

---

#### GET /auth/me

**Get current user information.**

---

#### POST /auth/verify-email

**Verify user email with token.**

**Parameters:**

- `token` (<class 'str'>) ✓

---

#### POST /auth/logout

**Logout user (client should discard token).**

---

### Profile

#### GET /api/profile/me

**Get current user's profile information.**

---

#### GET /api/profile/me

**Get current user's profile information.**

---

#### PUT /api/profile/me

**Update current user's profile information.**

**Parameters:**

- `profile_data` (<class 'schemas.user.UserUpdate'>) ✓

---

#### PUT /api/profile/me

**Update current user's profile information.**

**Parameters:**

- `profile_data` (<class 'schemas.user.UserUpdate'>) ✓

---

#### POST /api/profile/change-password

**Change user password.**

**Parameters:**

- `password_data` (<class 'schemas.user.PasswordChange'>) ✓

---

#### POST /api/profile/change-password

**Change user password.**

**Parameters:**

- `password_data` (<class 'schemas.user.PasswordChange'>) ✓

---

#### POST /api/profile/upload-avatar

**Upload profile picture.**

**Parameters:**

- `file` (<class 'fastapi.datastructures.UploadFile'>) ○ (default: annotation=UploadFile required=True alias='file' json_schema_extra={})

---

#### POST /api/profile/upload-avatar

**Upload profile picture.**

**Parameters:**

- `file` (<class 'fastapi.datastructures.UploadFile'>) ○ (default: annotation=UploadFile required=True alias='file' json_schema_extra={})

---

#### DELETE /api/profile/avatar

**Delete profile picture.**

---

#### DELETE /api/profile/avatar

**Delete profile picture.**

---

#### GET /api/profile/activity

**Get user activity summary.**

---

#### GET /api/profile/activity

**Get user activity summary.**

---

#### POST /api/profile/deactivate

**Deactivate user account.**

---

#### POST /api/profile/deactivate

**Deactivate user account.**

---

#### GET /api/profile/users

**Get all users (admin only).**

**Parameters:**

- `skip` (<class 'int'>) ○ (default: 0)
- `limit` (<class 'int'>) ○ (default: 100)

---

#### GET /api/profile/users

**Get all users (admin only).**

**Parameters:**

- `skip` (<class 'int'>) ○ (default: 0)
- `limit` (<class 'int'>) ○ (default: 100)

---

#### GET /api/profile/users/{user_id}

**Get user by ID (admin only).**

**Parameters:**

- `user_id` (<class 'int'>) ✓

---

#### GET /api/profile/users/{user_id}

**Get user by ID (admin only).**

**Parameters:**

- `user_id` (<class 'int'>) ✓

---

#### PUT /api/profile/users/{user_id}

**Update user by ID (admin only).**

**Parameters:**

- `user_id` (<class 'int'>) ✓
- `profile_data` (<class 'schemas.user.UserUpdate'>) ✓

---

#### PUT /api/profile/users/{user_id}

**Update user by ID (admin only).**

**Parameters:**

- `user_id` (<class 'int'>) ✓
- `profile_data` (<class 'schemas.user.UserUpdate'>) ✓

---

#### DELETE /api/profile/users/{user_id}

**Delete user by ID (admin only).**

**Parameters:**

- `user_id` (<class 'int'>) ✓

---

#### DELETE /api/profile/users/{user_id}

**Delete user by ID (admin only).**

**Parameters:**

- `user_id` (<class 'int'>) ✓

---

#### POST /api/profile/users/{user_id}/toggle-status

**Toggle user active/inactive status (admin only).**

**Parameters:**

- `user_id` (<class 'int'>) ✓

---

#### POST /api/profile/users/{user_id}/toggle-status

**Toggle user active/inactive status (admin only).**

**Parameters:**

- `user_id` (<class 'int'>) ✓

---

### People

#### GET /api/people/search

**Search for people with various filters**

**Parameters:**

- `query` (typing.Optional[str]) ○ (default: annotation=Union[str, NoneType] required=False default=None alias='query' description='General search query' json_schema_extra={})
- `first_name` (typing.Optional[str]) ○ (default: annotation=Union[str, NoneType] required=False default=None alias='first_name' description='First name filter' json_schema_extra={})
- `last_name` (typing.Optional[str]) ○ (default: annotation=Union[str, NoneType] required=False default=None alias='last_name' description='Last name filter' json_schema_extra={})
- `id_number` (typing.Optional[str]) ○ (default: annotation=Union[str, NoneType] required=False default=None alias='id_number' description='ID number filter' json_schema_extra={})
- `phone_number` (typing.Optional[str]) ○ (default: annotation=Union[str, NoneType] required=False default=None alias='phone_number' description='Phone number filter' json_schema_extra={})
- `email` (typing.Optional[str]) ○ (default: annotation=Union[str, NoneType] required=False default=None alias='email' description='Email filter' json_schema_extra={})
- `city` (typing.Optional[str]) ○ (default: annotation=Union[str, NoneType] required=False default=None alias='city' description='City filter' json_schema_extra={})
- `region` (typing.Optional[str]) ○ (default: annotation=Union[str, NoneType] required=False default=None alias='region' description='Region filter' json_schema_extra={})
- `risk_level` (typing.Optional[str]) ○ (default: annotation=Union[str, NoneType] required=False default=None alias='risk_level' description='Risk level filter' json_schema_extra={})
- `occupation` (typing.Optional[str]) ○ (default: annotation=Union[str, NoneType] required=False default=None alias='occupation' description='Occupation filter' json_schema_extra={})
- `employer` (typing.Optional[str]) ○ (default: annotation=Union[str, NoneType] required=False default=None alias='employer' description='Employer filter' json_schema_extra={})
- `organization` (typing.Optional[str]) ○ (default: annotation=Union[str, NoneType] required=False default=None alias='organization' description='Organization filter' json_schema_extra={})
- `gender` (typing.Optional[str]) ○ (default: annotation=Union[str, NoneType] required=False default=None alias='gender' description='Gender filter' json_schema_extra={})
- `nationality` (typing.Optional[str]) ○ (default: annotation=Union[str, NoneType] required=False default=None alias='nationality' description='Nationality filter' json_schema_extra={})
- `is_verified` (typing.Optional[bool]) ○ (default: annotation=Union[bool, NoneType] required=False default=None alias='is_verified' description='Verification status filter' json_schema_extra={})
- `person_status` (typing.Optional[str]) ○ (default: annotation=Union[str, NoneType] required=False default=None alias='person_status' description='Status filter' json_schema_extra={})
- `min_risk_score` (typing.Optional[float]) ○ (default: annotation=Union[float, NoneType] required=False default=None alias='min_risk_score' description='Minimum risk score' json_schema_extra={} metadata=[Ge(ge=0), Le(le=200)])
- `max_risk_score` (typing.Optional[float]) ○ (default: annotation=Union[float, NoneType] required=False default=None alias='max_risk_score' description='Maximum risk score' json_schema_extra={} metadata=[Ge(ge=0), Le(le=200)])
- `min_case_count` (typing.Optional[int]) ○ (default: annotation=Union[int, NoneType] required=False default=None alias='min_case_count' description='Minimum case count' json_schema_extra={} metadata=[Ge(ge=0)])
- `max_case_count` (typing.Optional[int]) ○ (default: annotation=Union[int, NoneType] required=False default=None alias='max_case_count' description='Maximum case count' json_schema_extra={} metadata=[Ge(ge=0)])
- `sort_by` (<class 'str'>) ○ (default: annotation=str required=False default='full_name' alias='sort_by' description='Sort field' json_schema_extra={})
- `sort_order` (<class 'str'>) ○ (default: annotation=str required=False default='asc' alias='sort_order' description='Sort order' json_schema_extra={} metadata=[_PydanticGeneralMetadata(pattern='^(asc|desc)$')])
- `page` (<class 'int'>) ○ (default: annotation=int required=False default=1 alias='page' description='Page number' json_schema_extra={} metadata=[Ge(ge=1)])
- `limit` (<class 'int'>) ○ (default: annotation=int required=False default=20 alias='limit' description='Items per page' json_schema_extra={} metadata=[Ge(ge=1), Le(le=100)])

---

#### GET /api/people/{people_id}

**Get a specific person by ID**

**Parameters:**

- `people_id` (<class 'int'>) ✓

---

#### POST /api/people/

**Create a new person record**

**Parameters:**

- `person_data` (<class 'schemas.people.PeopleCreate'>) ✓

---

#### PUT /api/people/{people_id}

**Update a person record**

**Parameters:**

- `people_id` (<class 'int'>) ✓
- `person_data` (<class 'schemas.people.PeopleUpdate'>) ✓

---

#### DELETE /api/people/{people_id}

**Delete a person record (soft delete)**

**Parameters:**

- `people_id` (<class 'int'>) ✓

---

#### GET /api/people/stats/overview

**Get people statistics overview**

---

### Banks

#### GET /api/banks/search

**Search banks with various filters**

**Parameters:**

- `query` (typing.Optional[str]) ○ (default: annotation=Union[str, NoneType] required=False default=None alias='query' description='General search query' json_schema_extra={})
- `name` (typing.Optional[str]) ○ (default: annotation=Union[str, NoneType] required=False default=None alias='name' description='Bank name filter' json_schema_extra={})
- `city` (typing.Optional[str]) ○ (default: annotation=Union[str, NoneType] required=False default=None alias='city' description='City filter' json_schema_extra={})
- `region` (typing.Optional[str]) ○ (default: annotation=Union[str, NoneType] required=False default=None alias='region' description='Region filter' json_schema_extra={})
- `bank_type` (typing.Optional[str]) ○ (default: annotation=Union[str, NoneType] required=False default=None alias='bank_type' description='Bank type filter' json_schema_extra={})
- `ownership_type` (typing.Optional[str]) ○ (default: annotation=Union[str, NoneType] required=False default=None alias='ownership_type' description='Ownership type filter' json_schema_extra={})
- `has_mobile_app` (typing.Optional[bool]) ○ (default: annotation=Union[bool, NoneType] required=False default=None alias='has_mobile_app' description='Has mobile app filter' json_schema_extra={})
- `has_online_banking` (typing.Optional[bool]) ○ (default: annotation=Union[bool, NoneType] required=False default=None alias='has_online_banking' description='Has online banking filter' json_schema_extra={})
- `has_atm_services` (typing.Optional[bool]) ○ (default: annotation=Union[bool, NoneType] required=False default=None alias='has_atm_services' description='Has ATM services filter' json_schema_extra={})
- `has_foreign_exchange` (typing.Optional[bool]) ○ (default: annotation=Union[bool, NoneType] required=False default=None alias='has_foreign_exchange' description='Has foreign exchange filter' json_schema_extra={})
- `rating` (typing.Optional[str]) ○ (default: annotation=Union[str, NoneType] required=False default=None alias='rating' description='Rating filter' json_schema_extra={})
- `min_assets` (typing.Optional[float]) ○ (default: annotation=Union[float, NoneType] required=False default=None alias='min_assets' description='Minimum assets filter' json_schema_extra={})
- `max_assets` (typing.Optional[float]) ○ (default: annotation=Union[float, NoneType] required=False default=None alias='max_assets' description='Maximum assets filter' json_schema_extra={})
- `sort_by` (<class 'str'>) ○ (default: annotation=str required=False default='name' alias='sort_by' description='Sort by field' json_schema_extra={})
- `sort_order` (<class 'str'>) ○ (default: annotation=str required=False default='asc' alias='sort_order' description='Sort order (asc/desc)' json_schema_extra={})
- `page` (<class 'int'>) ○ (default: annotation=int required=False default=1 alias='page' description='Page number' json_schema_extra={} metadata=[Ge(ge=1)])
- `limit` (<class 'int'>) ○ (default: annotation=int required=False default=20 alias='limit' description='Items per page' json_schema_extra={} metadata=[Ge(ge=1), Le(le=100)])

---

#### GET /api/banks/

**Get all banks**

**Parameters:**

- `skip` (<class 'int'>) ○ (default: annotation=int required=False default=0 alias='skip' json_schema_extra={} metadata=[Ge(ge=0)])
- `limit` (<class 'int'>) ○ (default: annotation=int required=False default=100 alias='limit' json_schema_extra={} metadata=[Ge(ge=1), Le(le=1000)])

---

#### GET /api/banks/{bank_id}

**Get a specific bank by ID**

**Parameters:**

- `bank_id` (<class 'int'>) ✓

---

#### POST /api/banks/

**Create a new bank**

**Parameters:**

- `bank` (<class 'schemas.banks.BanksCreate'>) ✓

---

#### PUT /api/banks/{bank_id}

**Update a bank**

**Parameters:**

- `bank_id` (<class 'int'>) ✓
- `bank` (<class 'schemas.banks.BanksUpdate'>) ✓

---

#### DELETE /api/banks/{bank_id}

**Delete a bank (soft delete)**

**Parameters:**

- `bank_id` (<class 'int'>) ✓

---

#### GET /api/banks/stats/overview

**Get banks statistics**

---

#### GET /api/banks/{bank_id}/analytics

**Get analytics for a specific bank**

**Parameters:**

- `bank_id` (<class 'int'>) ✓

---

#### GET /api/banks/{bank_id}/case-statistics

**Get case statistics for a specific bank**

**Parameters:**

- `bank_id` (<class 'int'>) ✓

---

#### POST /api/banks/{bank_id}/generate-analytics

**Generate analytics and statistics for a bank**

**Parameters:**

- `bank_id` (<class 'int'>) ✓

---

#### GET /api/banks/{bank_id}/related-cases

**Get cases related to a specific bank**

**Parameters:**

- `bank_id` (<class 'int'>) ✓
- `limit` (<class 'int'>) ○ (default: annotation=int required=False default=10 alias='limit' description='Maximum related cases' json_schema_extra={} metadata=[Ge(ge=1), Le(le=100)])

---

### Insurance

#### GET /api/insurance/search

**Search insurance companies with various filters**

**Parameters:**

- `query` (typing.Optional[str]) ○ (default: annotation=Union[str, NoneType] required=False default=None alias='query' description='General search query' json_schema_extra={})
- `name` (typing.Optional[str]) ○ (default: annotation=Union[str, NoneType] required=False default=None alias='name' description='Insurance name filter' json_schema_extra={})
- `city` (typing.Optional[str]) ○ (default: annotation=Union[str, NoneType] required=False default=None alias='city' description='City filter' json_schema_extra={})
- `region` (typing.Optional[str]) ○ (default: annotation=Union[str, NoneType] required=False default=None alias='region' description='Region filter' json_schema_extra={})
- `insurance_type` (typing.Optional[str]) ○ (default: annotation=Union[str, NoneType] required=False default=None alias='insurance_type' description='Insurance type filter' json_schema_extra={})
- `ownership_type` (typing.Optional[str]) ○ (default: annotation=Union[str, NoneType] required=False default=None alias='ownership_type' description='Ownership type filter' json_schema_extra={})
- `has_mobile_app` (typing.Optional[bool]) ○ (default: annotation=Union[bool, NoneType] required=False default=None alias='has_mobile_app' description='Has mobile app filter' json_schema_extra={})
- `has_online_portal` (typing.Optional[bool]) ○ (default: annotation=Union[bool, NoneType] required=False default=None alias='has_online_portal' description='Has online portal filter' json_schema_extra={})
- `has_online_claims` (typing.Optional[bool]) ○ (default: annotation=Union[bool, NoneType] required=False default=None alias='has_online_claims' description='Has online claims filter' json_schema_extra={})
- `has_24_7_support` (typing.Optional[bool]) ○ (default: annotation=Union[bool, NoneType] required=False default=None alias='has_24_7_support' description='Has 24/7 support filter' json_schema_extra={})
- `rating` (typing.Optional[str]) ○ (default: annotation=Union[str, NoneType] required=False default=None alias='rating' description='Rating filter' json_schema_extra={})
- `target_market` (typing.Optional[str]) ○ (default: annotation=Union[str, NoneType] required=False default=None alias='target_market' description='Target market filter' json_schema_extra={})
- `min_assets` (typing.Optional[float]) ○ (default: annotation=Union[float, NoneType] required=False default=None alias='min_assets' description='Minimum assets filter' json_schema_extra={})
- `max_assets` (typing.Optional[float]) ○ (default: annotation=Union[float, NoneType] required=False default=None alias='max_assets' description='Maximum assets filter' json_schema_extra={})
- `sort_by` (<class 'str'>) ○ (default: annotation=str required=False default='name' alias='sort_by' description='Sort by field' json_schema_extra={})
- `sort_order` (<class 'str'>) ○ (default: annotation=str required=False default='asc' alias='sort_order' description='Sort order (asc/desc)' json_schema_extra={})
- `page` (<class 'int'>) ○ (default: annotation=int required=False default=1 alias='page' description='Page number' json_schema_extra={} metadata=[Ge(ge=1)])
- `limit` (<class 'int'>) ○ (default: annotation=int required=False default=20 alias='limit' description='Items per page' json_schema_extra={} metadata=[Ge(ge=1), Le(le=100)])

---

#### GET /api/insurance/

**Get all insurance companies**

**Parameters:**

- `skip` (<class 'int'>) ○ (default: annotation=int required=False default=0 alias='skip' json_schema_extra={} metadata=[Ge(ge=0)])
- `limit` (<class 'int'>) ○ (default: annotation=int required=False default=100 alias='limit' json_schema_extra={} metadata=[Ge(ge=1), Le(le=1000)])

---

#### GET /api/insurance/{insurance_id}

**Get a specific insurance company by ID**

**Parameters:**

- `insurance_id` (<class 'int'>) ✓

---

#### POST /api/insurance/

**Create a new insurance company**

**Parameters:**

- `insurance` (<class 'schemas.insurance.InsuranceCreate'>) ✓

---

#### PUT /api/insurance/{insurance_id}

**Update an insurance company**

**Parameters:**

- `insurance_id` (<class 'int'>) ✓
- `insurance` (<class 'schemas.insurance.InsuranceUpdate'>) ✓

---

#### DELETE /api/insurance/{insurance_id}

**Delete an insurance company (soft delete)**

**Parameters:**

- `insurance_id` (<class 'int'>) ✓

---

#### GET /api/insurance/stats/overview

**Get insurance statistics**

---

#### GET /api/insurance/{insurance_id}/analytics

**Get analytics for a specific insurance company**

**Parameters:**

- `insurance_id` (<class 'int'>) ✓

---

#### GET /api/insurance/{insurance_id}/case-statistics

**Get case statistics for a specific insurance company**

**Parameters:**

- `insurance_id` (<class 'int'>) ✓

---

#### GET /api/insurance/{insurance_id}/related-cases

**Get related cases for a specific insurance company**

**Parameters:**

- `insurance_id` (<class 'int'>) ✓
- `limit` (<class 'int'>) ○ (default: annotation=int required=False default=10 alias='limit' description='Maximum related cases' json_schema_extra={} metadata=[Ge(ge=1), Le(le=100)])

---

### Companies

#### GET /api/companies/

**Get all companies with pagination**

**Parameters:**

- `skip` (<class 'int'>) ○ (default: 0)
- `limit` (<class 'int'>) ○ (default: 100)

---

#### GET /api/companies/search

**Search companies with filters and pagination**

**Parameters:**

- `query` (typing.Optional[str]) ○ (default: annotation=Union[str, NoneType] required=False default=None alias='query' description='Search term for company name, industry, or activities' json_schema_extra={})
- `city` (typing.Optional[str]) ○ (default: annotation=Union[str, NoneType] required=False default=None alias='city' description='Filter by city' json_schema_extra={})
- `region` (typing.Optional[str]) ○ (default: annotation=Union[str, NoneType] required=False default=None alias='region' description='Filter by region' json_schema_extra={})
- `company_type` (typing.Optional[str]) ○ (default: annotation=Union[str, NoneType] required=False default=None alias='company_type' description='Filter by company type' json_schema_extra={})
- `industry` (typing.Optional[str]) ○ (default: annotation=Union[str, NoneType] required=False default=None alias='industry' description='Filter by industry' json_schema_extra={})
- `is_active` (typing.Optional[bool]) ○ (default: annotation=Union[bool, NoneType] required=False default=True alias='is_active' description='Filter by active status' json_schema_extra={})
- `page` (<class 'int'>) ○ (default: annotation=int required=False default=1 alias='page' description='Page number' json_schema_extra={} metadata=[Ge(ge=1)])
- `limit` (<class 'int'>) ○ (default: annotation=int required=False default=10 alias='limit' description='Items per page' json_schema_extra={} metadata=[Ge(ge=1), Le(le=100)])

---

#### GET /api/companies/{company_id}

**Get a specific company by ID**

**Parameters:**

- `company_id` (<class 'int'>) ✓

---

#### POST /api/companies/

**Create a new company**

**Parameters:**

- `company` (<class 'schemas.companies.CompaniesCreate'>) ✓

---

#### PUT /api/companies/{company_id}

**Update a company**

**Parameters:**

- `company_id` (<class 'int'>) ✓
- `company` (<class 'schemas.companies.CompaniesUpdate'>) ✓

---

#### DELETE /api/companies/{company_id}

**Delete a company**

**Parameters:**

- `company_id` (<class 'int'>) ✓

---

#### GET /api/companies/stats/overview

**Get companies statistics overview**

---

#### GET /api/companies/{company_id}/analytics

**Get analytics for a specific company**

**Parameters:**

- `company_id` (<class 'int'>) ✓

---

#### GET /api/companies/{company_id}/case-statistics

**Get case statistics for a specific company**

**Parameters:**

- `company_id` (<class 'int'>) ✓

---

#### GET /api/companies/{company_id}/related-cases

**Get related cases for a specific company**

**Parameters:**

- `company_id` (<class 'int'>) ✓
- `limit` (<class 'int'>) ○ (default: annotation=int required=False default=10 alias='limit' description='Maximum related cases' json_schema_extra={} metadata=[Ge(ge=1), Le(le=100)])

---

### Search

#### GET /api/search/unified

**Unified search across people, banks, and insurance**

**Parameters:**

- `query` (typing.Optional[str]) ○ (default: annotation=Union[str, NoneType] required=False default=None alias='query' description='General search query' json_schema_extra={})
- `search_type` (<class 'str'>) ○ (default: annotation=str required=False default='all' alias='search_type' description='Type of search (all, people, banks, insurance, companies)' json_schema_extra={})
- `page` (<class 'int'>) ○ (default: annotation=int required=False default=1 alias='page' description='Page number' json_schema_extra={} metadata=[Ge(ge=1)])
- `limit` (<class 'int'>) ○ (default: annotation=int required=False default=1000 alias='limit' description='Items per page' json_schema_extra={} metadata=[Ge(ge=1), Le(le=5000)])

---

#### GET /api/search/quick

**Quick search for suggestions and autocomplete**

**Parameters:**

- `query` (<class 'str'>) ○ (default: annotation=str required=True alias='query' description='Search query' json_schema_extra={} metadata=[MinLen(min_length=1)])
- `limit` (<class 'int'>) ○ (default: annotation=int required=False default=10 alias='limit' description='Maximum results' json_schema_extra={} metadata=[Ge(ge=1), Le(le=50)])

---

#### POST /api/search/advanced

**Advanced search with detailed filters**

**Parameters:**

- `request` (<class 'schemas.search.AdvancedSearchRequest'>) ✓

---

#### GET /api/search/stats

**Get search statistics**

---

### Reported_Cases

#### GET /api/cases/search

**Search reported cases with filters and pagination**

**Parameters:**

- `query` (typing.Optional[str]) ○ (default: annotation=Union[str, NoneType] required=False default=None alias='query' description='Search query for title, antagonist, protagonist, or citation' json_schema_extra={})
- `year` (typing.Optional[str]) ○ (default: annotation=Union[str, NoneType] required=False default=None alias='year' description='Filter by year' json_schema_extra={})
- `court_type` (typing.Optional[str]) ○ (default: annotation=Union[str, NoneType] required=False default=None alias='court_type' description='Filter by court type (SC, CA, HC)' json_schema_extra={})
- `region` (typing.Optional[str]) ○ (default: annotation=Union[str, NoneType] required=False default=None alias='region' description='Filter by region' json_schema_extra={})
- `area_of_law` (typing.Optional[str]) ○ (default: annotation=Union[str, NoneType] required=False default=None alias='area_of_law' description='Filter by area of law' json_schema_extra={})
- `page` (<class 'int'>) ○ (default: annotation=int required=False default=1 alias='page' description='Page number' json_schema_extra={} metadata=[Ge(ge=1)])
- `limit` (<class 'int'>) ○ (default: annotation=int required=False default=20 alias='limit' description='Number of results per page' json_schema_extra={} metadata=[Ge(ge=1), Le(le=100)])
- `sort_by` (<class 'str'>) ○ (default: annotation=str required=False default='date' alias='sort_by' description='Sort by field' json_schema_extra={})
- `sort_order` (<class 'str'>) ○ (default: annotation=str required=False default='desc' alias='sort_order' description='Sort order' json_schema_extra={})

---

#### GET /api/cases/{case_id}

**Get detailed information about a specific case**

**Parameters:**

- `case_id` (<class 'int'>) ✓

---

#### GET /api/cases/

**Get recent cases with pagination**

**Parameters:**

- `page` (<class 'int'>) ○ (default: annotation=int required=False default=1 alias='page' description='Page number' json_schema_extra={} metadata=[Ge(ge=1)])
- `limit` (<class 'int'>) ○ (default: annotation=int required=False default=20 alias='limit' description='Number of results per page' json_schema_extra={} metadata=[Ge(ge=1), Le(le=100)])

---

#### GET /api/cases/stats/overview

**Get overview statistics of reported cases**

---

### Legal_History

#### GET /api/legal-history/search/{entity_type}/{entity_id}

**Get legal history for a specific entity (person, bank, or insurance)**

**Parameters:**

- `entity_type` (<class 'str'>) ✓
- `entity_id` (<class 'int'>) ✓

---

#### GET /api/legal-history/cases/{entity_type}/{entity_id}

**Get paginated list of cases for an entity**

**Parameters:**

- `entity_type` (<class 'str'>) ✓
- `entity_id` (<class 'int'>) ✓
- `page` (<class 'int'>) ○ (default: annotation=int required=False default=1 alias='page' description='Page number' json_schema_extra={} metadata=[Ge(ge=1)])
- `limit` (<class 'int'>) ○ (default: annotation=int required=False default=20 alias='limit' description='Number of results per page' json_schema_extra={} metadata=[Ge(ge=1), Le(le=100)])
- `mention_type` (typing.Optional[str]) ○ (default: annotation=Union[str, NoneType] required=False default=None alias='mention_type' description='Filter by mention type' json_schema_extra={})
- `min_relevance_score` (typing.Optional[float]) ○ (default: annotation=Union[float, NoneType] required=False default=None alias='min_relevance_score' description='Minimum relevance score' json_schema_extra={})

---

#### GET /api/legal-history/mentions/{entity_type}/{entity_id}

**Get detailed mention information for an entity**

**Parameters:**

- `entity_type` (<class 'str'>) ✓
- `entity_id` (<class 'int'>) ✓

---

#### POST /api/legal-history/rebuild-index/{entity_type}/{entity_id}

**Rebuild legal history index for an entity**

**Parameters:**

- `entity_type` (<class 'str'>) ✓
- `entity_id` (<class 'int'>) ✓

---

### Case_Search

#### GET /api/case-search/search

**Search cases by person name, title, or content**

**Parameters:**

- `query` (<class 'str'>) ○ (default: annotation=str required=True alias='query' description='Search query' json_schema_extra={} metadata=[MinLen(min_length=2)])
- `page` (<class 'int'>) ○ (default: annotation=int required=False default=1 alias='page' description='Page number' json_schema_extra={} metadata=[Ge(ge=1)])
- `limit` (<class 'int'>) ○ (default: annotation=int required=False default=20 alias='limit' description='Items per page' json_schema_extra={} metadata=[Ge(ge=1), Le(le=100)])
- `case_type` (typing.Optional[str]) ○ (default: annotation=Union[str, NoneType] required=False default=None alias='case_type' description='Filter by case type' json_schema_extra={})
- `area_of_law` (typing.Optional[str]) ○ (default: annotation=Union[str, NoneType] required=False default=None alias='area_of_law' description='Filter by area of law' json_schema_extra={})
- `court_type` (typing.Optional[str]) ○ (default: annotation=Union[str, NoneType] required=False default=None alias='court_type' description='Filter by court type' json_schema_extra={})
- `status` (typing.Optional[str]) ○ (default: annotation=Union[str, NoneType] required=False default=None alias='status' description='Filter by case status' json_schema_extra={})

---

#### GET /api/case-search/person/{person_name}

**Get all cases for a specific person**

**Parameters:**

- `person_name` (<class 'str'>) ✓
- `page` (<class 'int'>) ○ (default: annotation=int required=False default=1 alias='page' description='Page number' json_schema_extra={} metadata=[Ge(ge=1)])
- `limit` (<class 'int'>) ○ (default: annotation=int required=False default=20 alias='limit' description='Items per page' json_schema_extra={} metadata=[Ge(ge=1), Le(le=100)])

---

#### GET /api/case-search/suggestions

**Get case search suggestions for autocomplete**

**Parameters:**

- `query` (<class 'str'>) ○ (default: annotation=str required=True alias='query' description='Search query' json_schema_extra={} metadata=[MinLen(min_length=2)])
- `limit` (<class 'int'>) ○ (default: annotation=int required=False default=10 alias='limit' description='Maximum suggestions' json_schema_extra={} metadata=[Ge(ge=1), Le(le=50)])

---

#### GET /api/case-search/{case_id}/details

**Get detailed information about a specific case including all metadata**

**Parameters:**

- `case_id` (<class 'int'>) ✓

---

#### GET /api/case-search/{case_id}/related-cases

**Get cases related to the people involved in the current case**

**Parameters:**

- `case_id` (<class 'int'>) ✓
- `limit` (<class 'int'>) ○ (default: annotation=int required=False default=10 alias='limit' description='Maximum related cases' json_schema_extra={} metadata=[Ge(ge=1), Le(le=50)])

---

### Enhanced_Search

#### GET /api/enhanced-search/search

**Enhanced search across all entities with progress indication**

**Parameters:**

- `q` (<class 'str'>) ○ (default: annotation=str required=True alias='q' description='Search query' json_schema_extra={})
- `page` (<class 'int'>) ○ (default: annotation=int required=False default=1 alias='page' description='Page number' json_schema_extra={} metadata=[Ge(ge=1)])
- `limit` (<class 'int'>) ○ (default: annotation=int required=False default=20 alias='limit' description='Items per page' json_schema_extra={} metadata=[Ge(ge=1), Le(le=100)])
- `court_type` (typing.Optional[str]) ○ (default: annotation=Union[str, NoneType] required=False default=None alias='court_type' description='Filter by court type' json_schema_extra={})
- `risk_level` (typing.Optional[str]) ○ (default: annotation=Union[str, NoneType] required=False default=None alias='risk_level' description='Filter by risk level' json_schema_extra={})
- `region` (typing.Optional[str]) ○ (default: annotation=Union[str, NoneType] required=False default=None alias='region' description='Filter by region' json_schema_extra={})
- `case_type` (typing.Optional[str]) ○ (default: annotation=Union[str, NoneType] required=False default=None alias='case_type' description='Filter by case type' json_schema_extra={})
- `sort_by` (<class 'str'>) ○ (default: annotation=str required=False default='relevance' alias='sort_by' description='Sort field' json_schema_extra={})
- `sort_order` (<class 'str'>) ○ (default: annotation=str required=False default='desc' alias='sort_order' description='Sort order' json_schema_extra={} metadata=[_PydanticGeneralMetadata(pattern='^(asc|desc)$')])

---

### Case_Hearings

#### GET /api/cases/{case_id}/hearings

**Get all hearings for a specific case**

**Parameters:**

- `case_id` (<class 'int'>) ✓

---

#### POST /api/cases/{case_id}/hearings

**Create a new hearing for a case**

**Parameters:**

- `case_id` (<class 'int'>) ✓
- `hearing` (<class 'schemas.case_hearings.CaseHearingCreate'>) ✓

---

#### PUT /api/hearings/{hearing_id}

**Update a case hearing**

**Parameters:**

- `hearing_id` (<class 'int'>) ✓
- `hearing` (<class 'schemas.case_hearings.CaseHearingUpdate'>) ✓

---

#### DELETE /api/hearings/{hearing_id}

**Delete a case hearing**

**Parameters:**

- `hearing_id` (<class 'int'>) ✓

---

### Person_Case_Statistics

#### GET /api/person-case-statistics/

**Get all person case statistics with pagination.**

**Parameters:**

- `skip` (<class 'int'>) ○ (default: annotation=int required=False default=0 alias='skip' description='Number of records to skip' json_schema_extra={} metadata=[Ge(ge=0)])
- `limit` (<class 'int'>) ○ (default: annotation=int required=False default=100 alias='limit' description='Number of records to return' json_schema_extra={} metadata=[Ge(ge=1), Le(le=1000)])

---

#### GET /api/person-case-statistics/person/{person_id}

**Get case statistics for a specific person.**

**Parameters:**

- `person_id` (<class 'int'>) ✓

---

#### GET /api/person-case-statistics/summary/{person_id}

**Get case statistics summary for a specific person.**

**Parameters:**

- `person_id` (<class 'int'>) ✓

---

#### POST /api/person-case-statistics/

**Create new person case statistics.**

**Parameters:**

- `stats_data` (<class 'schemas.person_case_statistics.PersonCaseStatisticsCreate'>) ✓

---

#### PUT /api/person-case-statistics/person/{person_id}

**Update person case statistics.**

**Parameters:**

- `person_id` (<class 'int'>) ✓
- `stats_data` (<class 'schemas.person_case_statistics.PersonCaseStatisticsUpdate'>) ✓

---

#### DELETE /api/person-case-statistics/person/{person_id}

**Delete person case statistics.**

**Parameters:**

- `person_id` (<class 'int'>) ✓

---

#### GET /api/person-case-statistics/top-cases

**Get people with the most cases.**

**Parameters:**

- `limit` (<class 'int'>) ○ (default: annotation=int required=False default=10 alias='limit' description='Number of top people to return' json_schema_extra={} metadata=[Ge(ge=1), Le(le=100)])

---

#### GET /api/person-case-statistics/high-risk

**Get people with high unresolved cases (potential high risk).**

**Parameters:**

- `unresolved_threshold` (<class 'int'>) ○ (default: annotation=int required=False default=5 alias='unresolved_threshold' description='Minimum unresolved cases to be considered high risk' json_schema_extra={} metadata=[Ge(ge=0)])
- `limit` (<class 'int'>) ○ (default: annotation=int required=False default=20 alias='limit' description='Number of people to return' json_schema_extra={} metadata=[Ge(ge=1), Le(le=100)])

---

### Person-Case-Statistics

#### GET /api/person-case-statistics/

**Get all person case statistics with pagination.**

**Parameters:**

- `skip` (<class 'int'>) ○ (default: annotation=int required=False default=0 alias='skip' description='Number of records to skip' json_schema_extra={} metadata=[Ge(ge=0)])
- `limit` (<class 'int'>) ○ (default: annotation=int required=False default=100 alias='limit' description='Number of records to return' json_schema_extra={} metadata=[Ge(ge=1), Le(le=1000)])

---

#### GET /api/person-case-statistics/person/{person_id}

**Get case statistics for a specific person.**

**Parameters:**

- `person_id` (<class 'int'>) ✓

---

#### GET /api/person-case-statistics/summary/{person_id}

**Get case statistics summary for a specific person.**

**Parameters:**

- `person_id` (<class 'int'>) ✓

---

#### POST /api/person-case-statistics/

**Create new person case statistics.**

**Parameters:**

- `stats_data` (<class 'schemas.person_case_statistics.PersonCaseStatisticsCreate'>) ✓

---

#### PUT /api/person-case-statistics/person/{person_id}

**Update person case statistics.**

**Parameters:**

- `person_id` (<class 'int'>) ✓
- `stats_data` (<class 'schemas.person_case_statistics.PersonCaseStatisticsUpdate'>) ✓

---

#### DELETE /api/person-case-statistics/person/{person_id}

**Delete person case statistics.**

**Parameters:**

- `person_id` (<class 'int'>) ✓

---

#### GET /api/person-case-statistics/top-cases

**Get people with the most cases.**

**Parameters:**

- `limit` (<class 'int'>) ○ (default: annotation=int required=False default=10 alias='limit' description='Number of top people to return' json_schema_extra={} metadata=[Ge(ge=1), Le(le=100)])

---

#### GET /api/person-case-statistics/high-risk

**Get people with high unresolved cases (potential high risk).**

**Parameters:**

- `unresolved_threshold` (<class 'int'>) ○ (default: annotation=int required=False default=5 alias='unresolved_threshold' description='Minimum unresolved cases to be considered high risk' json_schema_extra={} metadata=[Ge(ge=0)])
- `limit` (<class 'int'>) ○ (default: annotation=int required=False default=20 alias='limit' description='Number of people to return' json_schema_extra={} metadata=[Ge(ge=1), Le(le=100)])

---

### Person_Analytics

#### GET /api/person/{person_id}/analytics

**Get analytics for a specific person**

**Parameters:**

- `person_id` (<class 'int'>) ✓

---

#### POST /api/person/{person_id}/analytics/generate

**Generate or regenerate analytics for a specific person**

**Parameters:**

- `person_id` (<class 'int'>) ✓

---

#### GET /api/analytics/risk-level/{risk_level}

**Get all persons with a specific risk level**

**Parameters:**

- `risk_level` (<class 'str'>) ✓

---

#### GET /api/analytics/financial-risk/{risk_level}

**Get all persons with a specific financial risk level**

**Parameters:**

- `risk_level` (<class 'str'>) ✓

---

#### GET /api/analytics/high-risk

**Get all high-risk persons (High or Critical risk level)**

---

#### GET /api/analytics/stats

**Get overall analytics statistics**

---

### Banking_Summary

#### POST /api/banking-summary/generate/{case_id}

**Generate and save AI-powered banking summary for a case.**

**Parameters:**

- `case_id` (<class 'int'>) ✓

---

#### GET /api/banking-summary/{case_id}

**Get existing banking summary for a case.**

**Parameters:**

- `case_id` (<class 'int'>) ✓

---

#### POST /api/banking-summary/generate-batch

**Generate banking summaries for multiple cases.**

**Parameters:**

- `case_ids` (list[int]) ✓

---

#### GET /api/banking-summary/stats/summary

**Get statistics about generated banking summaries.**

---

### Banking-Summary

#### POST /api/banking-summary/generate/{case_id}

**Generate and save AI-powered banking summary for a case.**

**Parameters:**

- `case_id` (<class 'int'>) ✓

---

#### GET /api/banking-summary/{case_id}

**Get existing banking summary for a case.**

**Parameters:**

- `case_id` (<class 'int'>) ✓

---

#### POST /api/banking-summary/generate-batch

**Generate banking summaries for multiple cases.**

**Parameters:**

- `case_ids` (list[int]) ✓

---

#### GET /api/banking-summary/stats/summary

**Get statistics about generated banking summaries.**

---

### Request_Details

#### POST /api/request-details/submit

**Submit a new request for details or information**

**Parameters:**

- `request_data` (<class 'schemas.request_details.RequestDetailsCreate'>) ✓
- `request` (<class 'starlette.requests.Request'>) ✓

---

#### POST /api/request-details/submit-case-request

**Submit a quick case request**

**Parameters:**

- `request_data` (<class 'schemas.request_details.QuickCaseRequest'>) ✓
- `request` (<class 'starlette.requests.Request'>) ✓

---

#### POST /api/request-details/submit-profile-request

**Submit a quick profile request**

**Parameters:**

- `request_data` (<class 'schemas.request_details.QuickProfileRequest'>) ✓
- `request` (<class 'starlette.requests.Request'>) ✓

---

#### GET /api/request-details/

**Get all requests with optional filtering**

**Parameters:**

- `skip` (<class 'int'>) ○ (default: annotation=int required=False default=0 alias='skip' json_schema_extra={} metadata=[Ge(ge=0)])
- `limit` (<class 'int'>) ○ (default: annotation=int required=False default=100 alias='limit' json_schema_extra={} metadata=[Ge(ge=1), Le(le=1000)])
- `status` (typing.Optional[models.request_details.RequestStatus]) ○
- `entity_type` (typing.Optional[models.request_details.EntityType]) ○
- `request_type` (typing.Optional[models.request_details.RequestType]) ○
- `priority` (typing.Optional[models.request_details.Priority]) ○
- `is_urgent` (typing.Optional[bool]) ○
- `assigned_to` (typing.Optional[str]) ○

---

#### GET /api/request-details/stats

**Get request statistics**

---

#### GET /api/request-details/{request_id}

**Get a specific request by ID**

**Parameters:**

- `request_id` (<class 'int'>) ✓

---

#### PUT /api/request-details/{request_id}

**Update a request (admin/staff only)**

**Parameters:**

- `request_id` (<class 'int'>) ✓
- `request_data` (<class 'schemas.request_details.RequestDetailsUpdate'>) ✓

---

#### DELETE /api/request-details/{request_id}

**Delete a request (admin only)**

**Parameters:**

- `request_id` (<class 'int'>) ✓

---

#### GET /api/request-details/entity/{entity_type}/{entity_id}

**Get all requests for a specific entity**

**Parameters:**

- `entity_type` (<enum 'EntityType'>) ✓
- `entity_id` (<class 'int'>) ✓

---

#### GET /api/request-details/recent/{days}

**Get recent requests from the last N days**

**Parameters:**

- `days` (<class 'int'>) ○ (default: annotation=int required=True alias='days' json_schema_extra={} metadata=[Ge(ge=1), Le(le=30)])

---

### Request-Details

#### POST /api/request-details/submit

**Submit a new request for details or information**

**Parameters:**

- `request_data` (<class 'schemas.request_details.RequestDetailsCreate'>) ✓
- `request` (<class 'starlette.requests.Request'>) ✓

---

#### POST /api/request-details/submit-case-request

**Submit a quick case request**

**Parameters:**

- `request_data` (<class 'schemas.request_details.QuickCaseRequest'>) ✓
- `request` (<class 'starlette.requests.Request'>) ✓

---

#### POST /api/request-details/submit-profile-request

**Submit a quick profile request**

**Parameters:**

- `request_data` (<class 'schemas.request_details.QuickProfileRequest'>) ✓
- `request` (<class 'starlette.requests.Request'>) ✓

---

#### GET /api/request-details/

**Get all requests with optional filtering**

**Parameters:**

- `skip` (<class 'int'>) ○ (default: annotation=int required=False default=0 alias='skip' json_schema_extra={} metadata=[Ge(ge=0)])
- `limit` (<class 'int'>) ○ (default: annotation=int required=False default=100 alias='limit' json_schema_extra={} metadata=[Ge(ge=1), Le(le=1000)])
- `status` (typing.Optional[models.request_details.RequestStatus]) ○
- `entity_type` (typing.Optional[models.request_details.EntityType]) ○
- `request_type` (typing.Optional[models.request_details.RequestType]) ○
- `priority` (typing.Optional[models.request_details.Priority]) ○
- `is_urgent` (typing.Optional[bool]) ○
- `assigned_to` (typing.Optional[str]) ○

---

#### GET /api/request-details/stats

**Get request statistics**

---

#### GET /api/request-details/{request_id}

**Get a specific request by ID**

**Parameters:**

- `request_id` (<class 'int'>) ✓

---

#### PUT /api/request-details/{request_id}

**Update a request (admin/staff only)**

**Parameters:**

- `request_id` (<class 'int'>) ✓
- `request_data` (<class 'schemas.request_details.RequestDetailsUpdate'>) ✓

---

#### DELETE /api/request-details/{request_id}

**Delete a request (admin only)**

**Parameters:**

- `request_id` (<class 'int'>) ✓

---

#### GET /api/request-details/entity/{entity_type}/{entity_id}

**Get all requests for a specific entity**

**Parameters:**

- `entity_type` (<enum 'EntityType'>) ✓
- `entity_id` (<class 'int'>) ✓

---

#### GET /api/request-details/recent/{days}

**Get recent requests from the last N days**

**Parameters:**

- `days` (<class 'int'>) ○ (default: annotation=int required=True alias='days' json_schema_extra={} metadata=[Ge(ge=1), Le(le=30)])

---

### Subscription

#### GET /api/subscription/plans

**Get available subscription plans**

---

#### GET /api/subscription/current

**Get current user's subscription with usage data**

---

#### POST /api/subscription/upgrade

**Upgrade user's subscription plan**

**Parameters:**

- `plan` (<class 'str'>) ✓

---

#### POST /api/subscription/cancel

**Cancel user's subscription**

---

#### GET /api/subscription/usage

**Get user's usage history**

**Parameters:**

- `limit` (<class 'int'>) ○ (default: annotation=int required=False default=50 alias='limit' json_schema_extra={} metadata=[Le(le=100)])
- `offset` (<class 'int'>) ○ (default: annotation=int required=False default=0 alias='offset' json_schema_extra={} metadata=[Ge(ge=0)])

---

#### POST /api/subscription/usage

**Record usage for a specific resource**

**Parameters:**

- `resource_type` (<class 'str'>) ✓
- `count` (<class 'int'>) ○ (default: 1)
- `metadata` (typing.Optional[dict]) ○

---

### Notifications

#### GET /api/notifications/

**Get paginated list of notifications**

**Parameters:**

- `page` (<class 'int'>) ○ (default: annotation=int required=False default=1 alias='page' json_schema_extra={} metadata=[Ge(ge=1)])
- `limit` (<class 'int'>) ○ (default: annotation=int required=False default=20 alias='limit' json_schema_extra={} metadata=[Ge(ge=1), Le(le=100)])
- `status` (typing.Optional[str]) ○ (default: annotation=Union[str, NoneType] required=False default=None alias='status' json_schema_extra={})
- `type` (typing.Optional[str]) ○ (default: annotation=Union[str, NoneType] required=False default=None alias='type' json_schema_extra={})
- `category` (typing.Optional[str]) ○ (default: annotation=Union[str, NoneType] required=False default=None alias='category' json_schema_extra={})
- `search` (typing.Optional[str]) ○ (default: annotation=Union[str, NoneType] required=False default=None alias='search' json_schema_extra={})
- `user_id` (typing.Optional[int]) ○ (default: annotation=Union[int, NoneType] required=False default=None alias='user_id' json_schema_extra={})

---

#### GET /api/notifications/stats

**Get notification statistics**

**Parameters:**

- `user_id` (typing.Optional[int]) ○ (default: annotation=Union[int, NoneType] required=False default=None alias='user_id' json_schema_extra={})

---

#### POST /api/notifications/

**Create a new notification**

**Parameters:**

- `notification_data` (<class 'schemas.notification.NotificationCreateRequest'>) ✓

---

#### GET /api/notifications/{notification_id}

**Get a specific notification by ID**

**Parameters:**

- `notification_id` (<class 'int'>) ✓

---

#### PUT /api/notifications/{notification_id}

**Update a notification**

**Parameters:**

- `notification_id` (<class 'int'>) ✓
- `notification_data` (<class 'schemas.notification.NotificationUpdateRequest'>) ✓

---

#### PUT /api/notifications/{notification_id}/read

**Mark a notification as read**

**Parameters:**

- `notification_id` (<class 'int'>) ✓

---

#### PUT /api/notifications/{notification_id}/unread

**Mark a notification as unread**

**Parameters:**

- `notification_id` (<class 'int'>) ✓

---

#### PUT /api/notifications/mark-all-read

**Mark all notifications as read for a user**

**Parameters:**

- `user_id` (<class 'int'>) ✓

---

#### DELETE /api/notifications/{notification_id}

**Delete a notification**

**Parameters:**

- `notification_id` (<class 'int'>) ✓

---

#### DELETE /api/notifications/bulk

**Delete multiple notifications**

**Parameters:**

- `notification_ids` (typing.List[int]) ✓

---

### Security

#### GET /api/security/events

**Get user's security events**

**Parameters:**

- `limit` (<class 'int'>) ○ (default: annotation=int required=False default=50 alias='limit' json_schema_extra={} metadata=[Le(le=100)])
- `offset` (<class 'int'>) ○ (default: annotation=int required=False default=0 alias='offset' json_schema_extra={} metadata=[Ge(ge=0)])

---

#### POST /api/security/change-password

**Change user's password**

**Parameters:**

- `password_data` (<class 'schemas.security.PasswordChangeRequest'>) ✓
- `request` (<class 'starlette.requests.Request'>) ✓

---

#### GET /api/security/2fa

**Get user's 2FA status**

---

#### POST /api/security/2fa/setup

**Setup two-factor authentication**

**Parameters:**

- `setup_data` (<class 'schemas.security.TwoFactorAuthSetup'>) ✓
- `request` (<class 'starlette.requests.Request'>) ✓

---

#### POST /api/security/2fa/verify

**Verify two-factor authentication setup**

**Parameters:**

- `verify_data` (<class 'schemas.security.TwoFactorAuthVerify'>) ✓
- `request` (<class 'starlette.requests.Request'>) ✓

---

#### POST /api/security/2fa/disable

**Disable two-factor authentication**

**Parameters:**

- `request` (<class 'starlette.requests.Request'>) ✓

---

#### GET /api/security/api-keys

**Get user's API keys**

---

#### POST /api/security/api-keys

**Create a new API key**

**Parameters:**

- `key_data` (<class 'schemas.security.ApiKeyCreate'>) ✓
- `request` (<class 'starlette.requests.Request'>) ✓

---

#### DELETE /api/security/api-keys/{key_id}

**Revoke an API key**

**Parameters:**

- `key_id` (<class 'int'>) ✓
- `request` (<class 'starlette.requests.Request'>) ✓

---

#### GET /api/security/sessions

**Get user's active login sessions**

---

#### DELETE /api/security/sessions/{session_id}

**Terminate a specific login session**

**Parameters:**

- `session_id` (<class 'int'>) ✓

---

#### GET /api/security/settings

**Get comprehensive security settings**

---

### Admin

#### GET /api/admin/stats

**Get overall dashboard statistics**

---

#### GET /api/admin/stats

**Get overall dashboard statistics**

---

#### GET /api/admin/users

**Get paginated list of users with filtering**

**Parameters:**

- `page` (<class 'int'>) ○ (default: annotation=int required=False default=1 alias='page' json_schema_extra={} metadata=[Ge(ge=1)])
- `limit` (<class 'int'>) ○ (default: annotation=int required=False default=10 alias='limit' json_schema_extra={} metadata=[Ge(ge=1), Le(le=100)])
- `search` (typing.Optional[str]) ○
- `role` (typing.Optional[str]) ○
- `status` (typing.Optional[str]) ○

---

#### GET /api/admin/users

**Get paginated list of users with filtering**

**Parameters:**

- `page` (<class 'int'>) ○ (default: annotation=int required=False default=1 alias='page' json_schema_extra={} metadata=[Ge(ge=1)])
- `limit` (<class 'int'>) ○ (default: annotation=int required=False default=10 alias='limit' json_schema_extra={} metadata=[Ge(ge=1), Le(le=100)])
- `search` (typing.Optional[str]) ○
- `role` (typing.Optional[str]) ○
- `status` (typing.Optional[str]) ○

---

#### GET /api/admin/users/stats

**Get user statistics for admin dashboard**

---

#### GET /api/admin/users/stats

**Get user statistics for admin dashboard**

---

#### GET /api/admin/users/{user_id}

**Get detailed user information**

**Parameters:**

- `user_id` (<class 'int'>) ✓

---

#### GET /api/admin/users/{user_id}

**Get detailed user information**

**Parameters:**

- `user_id` (<class 'int'>) ✓

---

#### POST /api/admin/users

**Create a new user**

**Parameters:**

- `user_data` (<class 'schemas.admin.UserCreateRequest'>) ✓

---

#### POST /api/admin/users

**Create a new user**

**Parameters:**

- `user_data` (<class 'schemas.admin.UserCreateRequest'>) ✓

---

#### PUT /api/admin/users/{user_id}

**Update user information**

**Parameters:**

- `user_id` (<class 'int'>) ✓
- `user_data` (<class 'schemas.admin.UserUpdateRequest'>) ✓

---

#### PUT /api/admin/users/{user_id}

**Update user information**

**Parameters:**

- `user_id` (<class 'int'>) ✓
- `user_data` (<class 'schemas.admin.UserUpdateRequest'>) ✓

---

#### DELETE /api/admin/users/{user_id}

**Delete a user**

**Parameters:**

- `user_id` (<class 'int'>) ✓

---

#### DELETE /api/admin/users/{user_id}

**Delete a user**

**Parameters:**

- `user_id` (<class 'int'>) ✓

---

#### POST /api/admin/users/{user_id}/reset-password

**Reset a user's password (admin only)**

**Parameters:**

- `user_id` (<class 'int'>) ✓
- `password_data` (<class 'schemas.user.AdminPasswordReset'>) ✓

---

#### POST /api/admin/users/{user_id}/reset-password

**Reset a user's password (admin only)**

**Parameters:**

- `user_id` (<class 'int'>) ✓
- `password_data` (<class 'schemas.user.AdminPasswordReset'>) ✓

---

#### GET /api/admin/api-keys

**Get API keys with optional user filtering**

**Parameters:**

- `user_id` (typing.Optional[int]) ○
- `page` (<class 'int'>) ○ (default: annotation=int required=False default=1 alias='page' json_schema_extra={} metadata=[Ge(ge=1)])
- `limit` (<class 'int'>) ○ (default: annotation=int required=False default=10 alias='limit' json_schema_extra={} metadata=[Ge(ge=1), Le(le=100)])

---

#### GET /api/admin/api-keys

**Get API keys with optional user filtering**

**Parameters:**

- `user_id` (typing.Optional[int]) ○
- `page` (<class 'int'>) ○ (default: annotation=int required=False default=1 alias='page' json_schema_extra={} metadata=[Ge(ge=1)])
- `limit` (<class 'int'>) ○ (default: annotation=int required=False default=10 alias='limit' json_schema_extra={} metadata=[Ge(ge=1), Le(le=100)])

---

#### POST /api/admin/api-keys

**Create a new API key for a user**

**Parameters:**

- `api_key_data` (<class 'schemas.admin.ApiKeyCreateRequest'>) ✓

---

#### POST /api/admin/api-keys

**Create a new API key for a user**

**Parameters:**

- `api_key_data` (<class 'schemas.admin.ApiKeyCreateRequest'>) ✓

---

#### DELETE /api/admin/api-keys/{key_id}

**Delete an API key**

**Parameters:**

- `key_id` (<class 'int'>) ✓

---

#### DELETE /api/admin/api-keys/{key_id}

**Delete an API key**

**Parameters:**

- `key_id` (<class 'int'>) ✓

---

#### GET /api/admin/cases

**Get paginated list of cases with filtering**

**Parameters:**

- `page` (<class 'int'>) ○ (default: annotation=int required=False default=1 alias='page' json_schema_extra={} metadata=[Ge(ge=1)])
- `limit` (<class 'int'>) ○ (default: annotation=int required=False default=10 alias='limit' json_schema_extra={} metadata=[Ge(ge=1), Le(le=100)])
- `search` (typing.Optional[str]) ○
- `court_type` (typing.Optional[str]) ○
- `status` (typing.Optional[str]) ○

---

#### GET /api/admin/cases

**Get paginated list of cases with filtering**

**Parameters:**

- `page` (<class 'int'>) ○ (default: annotation=int required=False default=1 alias='page' json_schema_extra={} metadata=[Ge(ge=1)])
- `limit` (<class 'int'>) ○ (default: annotation=int required=False default=10 alias='limit' json_schema_extra={} metadata=[Ge(ge=1), Le(le=100)])
- `search` (typing.Optional[str]) ○
- `court_type` (typing.Optional[str]) ○
- `status` (typing.Optional[str]) ○

---

#### GET /api/admin/cases/stats

**Get comprehensive case statistics for admin dashboard**

---

#### GET /api/admin/cases/stats

**Get comprehensive case statistics for admin dashboard**

---

#### GET /api/admin/cases/{case_id}

**Get a specific case by ID**

**Parameters:**

- `case_id` (<class 'int'>) ✓

---

#### GET /api/admin/cases/{case_id}

**Get a specific case by ID**

**Parameters:**

- `case_id` (<class 'int'>) ✓

---

#### POST /api/admin/cases

**Create a new case**

**Parameters:**

- `case_data` (<class 'schemas.admin.CaseCreateRequest'>) ✓

---

#### POST /api/admin/cases

**Create a new case**

**Parameters:**

- `case_data` (<class 'schemas.admin.CaseCreateRequest'>) ✓

---

#### PUT /api/admin/cases/{case_id}

**Update a case**

**Parameters:**

- `case_id` (<class 'int'>) ✓
- `case_data` (<class 'schemas.admin.CaseUpdateRequest'>) ✓

---

#### PUT /api/admin/cases/{case_id}

**Update a case**

**Parameters:**

- `case_id` (<class 'int'>) ✓
- `case_data` (<class 'schemas.admin.CaseUpdateRequest'>) ✓

---

#### DELETE /api/admin/cases/{case_id}

**Delete a case**

**Parameters:**

- `case_id` (<class 'int'>) ✓

---

#### DELETE /api/admin/cases/{case_id}

**Delete a case**

**Parameters:**

- `case_id` (<class 'int'>) ✓

---

#### POST /api/admin/cases/upload

**Upload a case document and create a case record with AI analysis**

**Parameters:**

- `file` (<class 'fastapi.datastructures.UploadFile'>) ○ (default: annotation=UploadFile required=True alias='file' json_schema_extra={})

---

#### POST /api/admin/cases/upload

**Upload a case document and create a case record with AI analysis**

**Parameters:**

- `file` (<class 'fastapi.datastructures.UploadFile'>) ○ (default: annotation=UploadFile required=True alias='file' json_schema_extra={})

---

#### GET /api/admin/payments

**Get paginated list of payments with filtering**

**Parameters:**

- `page` (<class 'int'>) ○ (default: annotation=int required=False default=1 alias='page' json_schema_extra={} metadata=[Ge(ge=1)])
- `limit` (<class 'int'>) ○ (default: annotation=int required=False default=10 alias='limit' json_schema_extra={} metadata=[Ge(ge=1), Le(le=100)])
- `status` (typing.Optional[str]) ○

---

#### GET /api/admin/payments

**Get paginated list of payments with filtering**

**Parameters:**

- `page` (<class 'int'>) ○ (default: annotation=int required=False default=1 alias='page' json_schema_extra={} metadata=[Ge(ge=1)])
- `limit` (<class 'int'>) ○ (default: annotation=int required=False default=10 alias='limit' json_schema_extra={} metadata=[Ge(ge=1), Le(le=100)])
- `status` (typing.Optional[str]) ○

---

#### GET /api/admin/subscriptions

**Get paginated list of subscriptions with filtering**

**Parameters:**

- `page` (<class 'int'>) ○ (default: annotation=int required=False default=1 alias='page' json_schema_extra={} metadata=[Ge(ge=1)])
- `limit` (<class 'int'>) ○ (default: annotation=int required=False default=10 alias='limit' json_schema_extra={} metadata=[Ge(ge=1), Le(le=100)])
- `status` (typing.Optional[str]) ○

---

#### GET /api/admin/subscriptions

**Get paginated list of subscriptions with filtering**

**Parameters:**

- `page` (<class 'int'>) ○ (default: annotation=int required=False default=1 alias='page' json_schema_extra={} metadata=[Ge(ge=1)])
- `limit` (<class 'int'>) ○ (default: annotation=int required=False default=10 alias='limit' json_schema_extra={} metadata=[Ge(ge=1), Le(le=100)])
- `status` (typing.Optional[str]) ○

---

#### POST /api/admin/cases/{case_id}/process-metadata

**Process metadata for a specific case**

**Parameters:**

- `case_id` (<class 'int'>) ✓

---

#### POST /api/admin/cases/{case_id}/process-metadata

**Process metadata for a specific case**

**Parameters:**

- `case_id` (<class 'int'>) ✓

---

#### POST /api/admin/cases/process-all-metadata

**Process metadata for all cases**

---

#### POST /api/admin/cases/process-all-metadata

**Process metadata for all cases**

---

#### POST /api/admin/cases/{case_id}/process-enhanced

**Process case with analytics and entity extraction**

**Parameters:**

- `case_id` (<class 'int'>) ✓

---

#### POST /api/admin/cases/{case_id}/process-enhanced

**Process case with analytics and entity extraction**

**Parameters:**

- `case_id` (<class 'int'>) ✓

---

#### GET /api/admin/google-maps-api-key

**Get Google Maps API key for frontend use**

---

#### GET /api/admin/google-maps-api-key

**Get Google Maps API key for frontend use**

---

#### GET /api/admin/logs/access

**Get access logs with filtering**

**Parameters:**

- `user_id` (typing.Optional[int]) ○ (default: annotation=Union[int, NoneType] required=False default=None alias='user_id' json_schema_extra={})
- `limit` (<class 'int'>) ○ (default: annotation=int required=False default=100 alias='limit' json_schema_extra={} metadata=[Ge(ge=1), Le(le=1000)])
- `offset` (<class 'int'>) ○ (default: annotation=int required=False default=0 alias='offset' json_schema_extra={} metadata=[Ge(ge=0)])
- `start_date` (typing.Optional[str]) ○ (default: annotation=Union[str, NoneType] required=False default=None alias='start_date' json_schema_extra={})
- `end_date` (typing.Optional[str]) ○ (default: annotation=Union[str, NoneType] required=False default=None alias='end_date' json_schema_extra={})

---

#### GET /api/admin/logs/access

**Get access logs with filtering**

**Parameters:**

- `user_id` (typing.Optional[int]) ○ (default: annotation=Union[int, NoneType] required=False default=None alias='user_id' json_schema_extra={})
- `limit` (<class 'int'>) ○ (default: annotation=int required=False default=100 alias='limit' json_schema_extra={} metadata=[Ge(ge=1), Le(le=1000)])
- `offset` (<class 'int'>) ○ (default: annotation=int required=False default=0 alias='offset' json_schema_extra={} metadata=[Ge(ge=0)])
- `start_date` (typing.Optional[str]) ○ (default: annotation=Union[str, NoneType] required=False default=None alias='start_date' json_schema_extra={})
- `end_date` (typing.Optional[str]) ○ (default: annotation=Union[str, NoneType] required=False default=None alias='end_date' json_schema_extra={})

---

#### GET /api/admin/logs/activity

**Get activity logs with filtering**

**Parameters:**

- `user_id` (typing.Optional[int]) ○ (default: annotation=Union[int, NoneType] required=False default=None alias='user_id' json_schema_extra={})
- `activity_type` (typing.Optional[str]) ○ (default: annotation=Union[str, NoneType] required=False default=None alias='activity_type' json_schema_extra={})
- `limit` (<class 'int'>) ○ (default: annotation=int required=False default=100 alias='limit' json_schema_extra={} metadata=[Ge(ge=1), Le(le=1000)])
- `offset` (<class 'int'>) ○ (default: annotation=int required=False default=0 alias='offset' json_schema_extra={} metadata=[Ge(ge=0)])
- `start_date` (typing.Optional[str]) ○ (default: annotation=Union[str, NoneType] required=False default=None alias='start_date' json_schema_extra={})
- `end_date` (typing.Optional[str]) ○ (default: annotation=Union[str, NoneType] required=False default=None alias='end_date' json_schema_extra={})

---

#### GET /api/admin/logs/activity

**Get activity logs with filtering**

**Parameters:**

- `user_id` (typing.Optional[int]) ○ (default: annotation=Union[int, NoneType] required=False default=None alias='user_id' json_schema_extra={})
- `activity_type` (typing.Optional[str]) ○ (default: annotation=Union[str, NoneType] required=False default=None alias='activity_type' json_schema_extra={})
- `limit` (<class 'int'>) ○ (default: annotation=int required=False default=100 alias='limit' json_schema_extra={} metadata=[Ge(ge=1), Le(le=1000)])
- `offset` (<class 'int'>) ○ (default: annotation=int required=False default=0 alias='offset' json_schema_extra={} metadata=[Ge(ge=0)])
- `start_date` (typing.Optional[str]) ○ (default: annotation=Union[str, NoneType] required=False default=None alias='start_date' json_schema_extra={})
- `end_date` (typing.Optional[str]) ○ (default: annotation=Union[str, NoneType] required=False default=None alias='end_date' json_schema_extra={})

---

#### GET /api/admin/logs/audit

**Get audit logs with filtering**

**Parameters:**

- `user_id` (typing.Optional[int]) ○ (default: annotation=Union[int, NoneType] required=False default=None alias='user_id' json_schema_extra={})
- `table_name` (typing.Optional[str]) ○ (default: annotation=Union[str, NoneType] required=False default=None alias='table_name' json_schema_extra={})
- `limit` (<class 'int'>) ○ (default: annotation=int required=False default=100 alias='limit' json_schema_extra={} metadata=[Ge(ge=1), Le(le=1000)])
- `offset` (<class 'int'>) ○ (default: annotation=int required=False default=0 alias='offset' json_schema_extra={} metadata=[Ge(ge=0)])
- `start_date` (typing.Optional[str]) ○ (default: annotation=Union[str, NoneType] required=False default=None alias='start_date' json_schema_extra={})
- `end_date` (typing.Optional[str]) ○ (default: annotation=Union[str, NoneType] required=False default=None alias='end_date' json_schema_extra={})

---

#### GET /api/admin/logs/audit

**Get audit logs with filtering**

**Parameters:**

- `user_id` (typing.Optional[int]) ○ (default: annotation=Union[int, NoneType] required=False default=None alias='user_id' json_schema_extra={})
- `table_name` (typing.Optional[str]) ○ (default: annotation=Union[str, NoneType] required=False default=None alias='table_name' json_schema_extra={})
- `limit` (<class 'int'>) ○ (default: annotation=int required=False default=100 alias='limit' json_schema_extra={} metadata=[Ge(ge=1), Le(le=1000)])
- `offset` (<class 'int'>) ○ (default: annotation=int required=False default=0 alias='offset' json_schema_extra={} metadata=[Ge(ge=0)])
- `start_date` (typing.Optional[str]) ○ (default: annotation=Union[str, NoneType] required=False default=None alias='start_date' json_schema_extra={})
- `end_date` (typing.Optional[str]) ○ (default: annotation=Union[str, NoneType] required=False default=None alias='end_date' json_schema_extra={})

---

#### GET /api/admin/logs/errors

**Get error logs with filtering**

**Parameters:**

- `user_id` (typing.Optional[int]) ○ (default: annotation=Union[int, NoneType] required=False default=None alias='user_id' json_schema_extra={})
- `severity` (typing.Optional[str]) ○ (default: annotation=Union[str, NoneType] required=False default=None alias='severity' json_schema_extra={})
- `resolved` (typing.Optional[bool]) ○ (default: annotation=Union[bool, NoneType] required=False default=None alias='resolved' json_schema_extra={})
- `limit` (<class 'int'>) ○ (default: annotation=int required=False default=100 alias='limit' json_schema_extra={} metadata=[Ge(ge=1), Le(le=1000)])
- `offset` (<class 'int'>) ○ (default: annotation=int required=False default=0 alias='offset' json_schema_extra={} metadata=[Ge(ge=0)])
- `start_date` (typing.Optional[str]) ○ (default: annotation=Union[str, NoneType] required=False default=None alias='start_date' json_schema_extra={})
- `end_date` (typing.Optional[str]) ○ (default: annotation=Union[str, NoneType] required=False default=None alias='end_date' json_schema_extra={})

---

#### GET /api/admin/logs/errors

**Get error logs with filtering**

**Parameters:**

- `user_id` (typing.Optional[int]) ○ (default: annotation=Union[int, NoneType] required=False default=None alias='user_id' json_schema_extra={})
- `severity` (typing.Optional[str]) ○ (default: annotation=Union[str, NoneType] required=False default=None alias='severity' json_schema_extra={})
- `resolved` (typing.Optional[bool]) ○ (default: annotation=Union[bool, NoneType] required=False default=None alias='resolved' json_schema_extra={})
- `limit` (<class 'int'>) ○ (default: annotation=int required=False default=100 alias='limit' json_schema_extra={} metadata=[Ge(ge=1), Le(le=1000)])
- `offset` (<class 'int'>) ○ (default: annotation=int required=False default=0 alias='offset' json_schema_extra={} metadata=[Ge(ge=0)])
- `start_date` (typing.Optional[str]) ○ (default: annotation=Union[str, NoneType] required=False default=None alias='start_date' json_schema_extra={})
- `end_date` (typing.Optional[str]) ○ (default: annotation=Union[str, NoneType] required=False default=None alias='end_date' json_schema_extra={})

---

#### GET /api/admin/logs/security

**Get security logs with filtering**

**Parameters:**

- `user_id` (typing.Optional[int]) ○ (default: annotation=Union[int, NoneType] required=False default=None alias='user_id' json_schema_extra={})
- `event_type` (typing.Optional[str]) ○ (default: annotation=Union[str, NoneType] required=False default=None alias='event_type' json_schema_extra={})
- `severity` (typing.Optional[str]) ○ (default: annotation=Union[str, NoneType] required=False default=None alias='severity' json_schema_extra={})
- `blocked` (typing.Optional[bool]) ○ (default: annotation=Union[bool, NoneType] required=False default=None alias='blocked' json_schema_extra={})
- `limit` (<class 'int'>) ○ (default: annotation=int required=False default=100 alias='limit' json_schema_extra={} metadata=[Ge(ge=1), Le(le=1000)])
- `offset` (<class 'int'>) ○ (default: annotation=int required=False default=0 alias='offset' json_schema_extra={} metadata=[Ge(ge=0)])
- `start_date` (typing.Optional[str]) ○ (default: annotation=Union[str, NoneType] required=False default=None alias='start_date' json_schema_extra={})
- `end_date` (typing.Optional[str]) ○ (default: annotation=Union[str, NoneType] required=False default=None alias='end_date' json_schema_extra={})

---

#### GET /api/admin/logs/security

**Get security logs with filtering**

**Parameters:**

- `user_id` (typing.Optional[int]) ○ (default: annotation=Union[int, NoneType] required=False default=None alias='user_id' json_schema_extra={})
- `event_type` (typing.Optional[str]) ○ (default: annotation=Union[str, NoneType] required=False default=None alias='event_type' json_schema_extra={})
- `severity` (typing.Optional[str]) ○ (default: annotation=Union[str, NoneType] required=False default=None alias='severity' json_schema_extra={})
- `blocked` (typing.Optional[bool]) ○ (default: annotation=Union[bool, NoneType] required=False default=None alias='blocked' json_schema_extra={})
- `limit` (<class 'int'>) ○ (default: annotation=int required=False default=100 alias='limit' json_schema_extra={} metadata=[Ge(ge=1), Le(le=1000)])
- `offset` (<class 'int'>) ○ (default: annotation=int required=False default=0 alias='offset' json_schema_extra={} metadata=[Ge(ge=0)])
- `start_date` (typing.Optional[str]) ○ (default: annotation=Union[str, NoneType] required=False default=None alias='start_date' json_schema_extra={})
- `end_date` (typing.Optional[str]) ○ (default: annotation=Union[str, NoneType] required=False default=None alias='end_date' json_schema_extra={})

---

#### GET /api/admin/logs/stats

**Get logging statistics**

**Parameters:**

- `start_date` (typing.Optional[str]) ○ (default: annotation=Union[str, NoneType] required=False default=None alias='start_date' json_schema_extra={})
- `end_date` (typing.Optional[str]) ○ (default: annotation=Union[str, NoneType] required=False default=None alias='end_date' json_schema_extra={})

---

#### GET /api/admin/logs/stats

**Get logging statistics**

**Parameters:**

- `start_date` (typing.Optional[str]) ○ (default: annotation=Union[str, NoneType] required=False default=None alias='start_date' json_schema_extra={})
- `end_date` (typing.Optional[str]) ○ (default: annotation=Union[str, NoneType] required=False default=None alias='end_date' json_schema_extra={})

---

#### GET /api/admin/people/stats

**Get people statistics for admin dashboard**

---

#### GET /api/admin/people/stats

**Get people statistics for admin dashboard**

---

#### GET /api/admin/banks/stats

**Get banks statistics for admin dashboard**

---

#### GET /api/admin/banks/stats

**Get banks statistics for admin dashboard**

---

#### GET /api/admin/insurance/stats

**Get insurance statistics for admin dashboard**

---

#### GET /api/admin/insurance/stats

**Get insurance statistics for admin dashboard**

---

#### GET /api/admin/companies/stats

**Get companies statistics for admin dashboard**

---

#### GET /api/admin/companies/stats

**Get companies statistics for admin dashboard**

---

#### GET /api/admin/payments/stats

**Get payments statistics for admin dashboard**

---

#### GET /api/admin/payments/stats

**Get payments statistics for admin dashboard**

---

#### GET /api/admin/people/stats

**Get comprehensive people statistics for admin dashboard**

---

#### GET /api/admin/people/stats

**Get comprehensive people statistics for admin dashboard**

---

#### GET /api/admin/people/

**Get paginated list of people with optional filtering**

**Parameters:**

- `page` (<class 'int'>) ○ (default: annotation=int required=False default=1 alias='page' json_schema_extra={} metadata=[Ge(ge=1)])
- `limit` (<class 'int'>) ○ (default: annotation=int required=False default=10 alias='limit' json_schema_extra={} metadata=[Ge(ge=1), Le(le=100)])
- `search` (typing.Optional[str]) ○ (default: annotation=Union[str, NoneType] required=False default=None alias='search' json_schema_extra={})
- `risk_level` (typing.Optional[str]) ○ (default: annotation=Union[str, NoneType] required=False default=None alias='risk_level' json_schema_extra={})

---

#### GET /api/admin/people/

**Get paginated list of people with optional filtering**

**Parameters:**

- `page` (<class 'int'>) ○ (default: annotation=int required=False default=1 alias='page' json_schema_extra={} metadata=[Ge(ge=1)])
- `limit` (<class 'int'>) ○ (default: annotation=int required=False default=10 alias='limit' json_schema_extra={} metadata=[Ge(ge=1), Le(le=100)])
- `search` (typing.Optional[str]) ○ (default: annotation=Union[str, NoneType] required=False default=None alias='search' json_schema_extra={})
- `risk_level` (typing.Optional[str]) ○ (default: annotation=Union[str, NoneType] required=False default=None alias='risk_level' json_schema_extra={})

---

#### GET /api/admin/people/{person_id}

**Get detailed information about a specific person**

**Parameters:**

- `person_id` (<class 'int'>) ✓

---

#### GET /api/admin/people/{person_id}

**Get detailed information about a specific person**

**Parameters:**

- `person_id` (<class 'int'>) ✓

---

#### POST /api/admin/people/

**Create a new person record**

**Parameters:**

- `person_data` (<class 'dict'>) ✓

---

#### POST /api/admin/people/

**Create a new person record**

**Parameters:**

- `person_data` (<class 'dict'>) ✓

---

#### PUT /api/admin/people/{person_id}

**Update an existing person record**

**Parameters:**

- `person_id` (<class 'int'>) ✓
- `person_data` (<class 'dict'>) ✓

---

#### PUT /api/admin/people/{person_id}

**Update an existing person record**

**Parameters:**

- `person_id` (<class 'int'>) ✓
- `person_data` (<class 'dict'>) ✓

---

#### DELETE /api/admin/people/{person_id}

**Delete a person and all associated data**

**Parameters:**

- `person_id` (<class 'int'>) ✓

---

#### DELETE /api/admin/people/{person_id}

**Delete a person and all associated data**

**Parameters:**

- `person_id` (<class 'int'>) ✓

---

#### GET /api/admin/banks/stats

**Get comprehensive bank statistics for admin dashboard**

---

#### GET /api/admin/banks/stats

**Get comprehensive bank statistics for admin dashboard**

---

#### GET /api/admin/banks/

**Get paginated list of banks with optional filtering**

**Parameters:**

- `page` (<class 'int'>) ○ (default: annotation=int required=False default=1 alias='page' json_schema_extra={} metadata=[Ge(ge=1)])
- `limit` (<class 'int'>) ○ (default: annotation=int required=False default=10 alias='limit' json_schema_extra={} metadata=[Ge(ge=1), Le(le=100)])
- `search` (typing.Optional[str]) ○ (default: annotation=Union[str, NoneType] required=False default=None alias='search' json_schema_extra={})
- `bank_type` (typing.Optional[str]) ○ (default: annotation=Union[str, NoneType] required=False default=None alias='bank_type' json_schema_extra={})

---

#### GET /api/admin/banks/

**Get paginated list of banks with optional filtering**

**Parameters:**

- `page` (<class 'int'>) ○ (default: annotation=int required=False default=1 alias='page' json_schema_extra={} metadata=[Ge(ge=1)])
- `limit` (<class 'int'>) ○ (default: annotation=int required=False default=10 alias='limit' json_schema_extra={} metadata=[Ge(ge=1), Le(le=100)])
- `search` (typing.Optional[str]) ○ (default: annotation=Union[str, NoneType] required=False default=None alias='search' json_schema_extra={})
- `bank_type` (typing.Optional[str]) ○ (default: annotation=Union[str, NoneType] required=False default=None alias='bank_type' json_schema_extra={})

---

#### GET /api/admin/banks/{bank_id}

**Get detailed information about a specific bank**

**Parameters:**

- `bank_id` (<class 'int'>) ✓

---

#### GET /api/admin/banks/{bank_id}

**Get detailed information about a specific bank**

**Parameters:**

- `bank_id` (<class 'int'>) ✓

---

#### POST /api/admin/banks/

**Create a new bank**

**Parameters:**

- `bank_data` (<class 'schemas.admin.BankCreateRequest'>) ✓

---

#### POST /api/admin/banks/

**Create a new bank**

**Parameters:**

- `bank_data` (<class 'schemas.admin.BankCreateRequest'>) ✓

---

#### PUT /api/admin/banks/{bank_id}

**Update an existing bank**

**Parameters:**

- `bank_id` (<class 'int'>) ✓
- `bank_data` (<class 'schemas.admin.BankUpdateRequest'>) ✓

---

#### PUT /api/admin/banks/{bank_id}

**Update an existing bank**

**Parameters:**

- `bank_id` (<class 'int'>) ✓
- `bank_data` (<class 'schemas.admin.BankUpdateRequest'>) ✓

---

#### DELETE /api/admin/banks/{bank_id}

**Delete a bank and all associated data**

**Parameters:**

- `bank_id` (<class 'int'>) ✓

---

#### DELETE /api/admin/banks/{bank_id}

**Delete a bank and all associated data**

**Parameters:**

- `bank_id` (<class 'int'>) ✓

---

#### GET /api/admin/insurance/stats

**Get comprehensive insurance statistics for admin dashboard**

---

#### GET /api/admin/insurance/stats

**Get comprehensive insurance statistics for admin dashboard**

---

#### GET /api/admin/insurance/

**Get paginated list of insurance companies with optional filtering**

**Parameters:**

- `page` (<class 'int'>) ○ (default: annotation=int required=False default=1 alias='page' json_schema_extra={} metadata=[Ge(ge=1)])
- `limit` (<class 'int'>) ○ (default: annotation=int required=False default=10 alias='limit' json_schema_extra={} metadata=[Ge(ge=1), Le(le=100)])
- `search` (typing.Optional[str]) ○ (default: annotation=Union[str, NoneType] required=False default=None alias='search' json_schema_extra={})
- `insurance_type` (typing.Optional[str]) ○ (default: annotation=Union[str, NoneType] required=False default=None alias='insurance_type' json_schema_extra={})

---

#### GET /api/admin/insurance/

**Get paginated list of insurance companies with optional filtering**

**Parameters:**

- `page` (<class 'int'>) ○ (default: annotation=int required=False default=1 alias='page' json_schema_extra={} metadata=[Ge(ge=1)])
- `limit` (<class 'int'>) ○ (default: annotation=int required=False default=10 alias='limit' json_schema_extra={} metadata=[Ge(ge=1), Le(le=100)])
- `search` (typing.Optional[str]) ○ (default: annotation=Union[str, NoneType] required=False default=None alias='search' json_schema_extra={})
- `insurance_type` (typing.Optional[str]) ○ (default: annotation=Union[str, NoneType] required=False default=None alias='insurance_type' json_schema_extra={})

---

#### GET /api/admin/insurance/{insurance_id}

**Get detailed information about a specific insurance company**

**Parameters:**

- `insurance_id` (<class 'int'>) ✓

---

#### GET /api/admin/insurance/{insurance_id}

**Get detailed information about a specific insurance company**

**Parameters:**

- `insurance_id` (<class 'int'>) ✓

---

#### POST /api/admin/insurance/

**Create a new insurance company**

**Parameters:**

- `insurance_data` (<class 'schemas.admin.InsuranceCreateRequest'>) ✓

---

#### POST /api/admin/insurance/

**Create a new insurance company**

**Parameters:**

- `insurance_data` (<class 'schemas.admin.InsuranceCreateRequest'>) ✓

---

#### PUT /api/admin/insurance/{insurance_id}

**Update an existing insurance company**

**Parameters:**

- `insurance_id` (<class 'int'>) ✓
- `insurance_data` (<class 'schemas.admin.InsuranceUpdateRequest'>) ✓

---

#### PUT /api/admin/insurance/{insurance_id}

**Update an existing insurance company**

**Parameters:**

- `insurance_id` (<class 'int'>) ✓
- `insurance_data` (<class 'schemas.admin.InsuranceUpdateRequest'>) ✓

---

#### DELETE /api/admin/insurance/{insurance_id}

**Delete an insurance company and all associated data**

**Parameters:**

- `insurance_id` (<class 'int'>) ✓

---

#### DELETE /api/admin/insurance/{insurance_id}

**Delete an insurance company and all associated data**

**Parameters:**

- `insurance_id` (<class 'int'>) ✓

---

#### GET /api/admin/companies/stats

**Get comprehensive company statistics for admin dashboard**

---

#### GET /api/admin/companies/stats

**Get comprehensive company statistics for admin dashboard**

---

#### GET /api/admin/companies/

**Get paginated list of companies with optional filtering**

**Parameters:**

- `page` (<class 'int'>) ○ (default: annotation=int required=False default=1 alias='page' json_schema_extra={} metadata=[Ge(ge=1)])
- `limit` (<class 'int'>) ○ (default: annotation=int required=False default=10 alias='limit' json_schema_extra={} metadata=[Ge(ge=1), Le(le=100)])
- `search` (typing.Optional[str]) ○ (default: annotation=Union[str, NoneType] required=False default=None alias='search' json_schema_extra={})
- `company_type` (typing.Optional[str]) ○ (default: annotation=Union[str, NoneType] required=False default=None alias='company_type' json_schema_extra={})

---

#### GET /api/admin/companies/

**Get paginated list of companies with optional filtering**

**Parameters:**

- `page` (<class 'int'>) ○ (default: annotation=int required=False default=1 alias='page' json_schema_extra={} metadata=[Ge(ge=1)])
- `limit` (<class 'int'>) ○ (default: annotation=int required=False default=10 alias='limit' json_schema_extra={} metadata=[Ge(ge=1), Le(le=100)])
- `search` (typing.Optional[str]) ○ (default: annotation=Union[str, NoneType] required=False default=None alias='search' json_schema_extra={})
- `company_type` (typing.Optional[str]) ○ (default: annotation=Union[str, NoneType] required=False default=None alias='company_type' json_schema_extra={})

---

#### GET /api/admin/companies/{company_id}

**Get detailed information about a specific company**

**Parameters:**

- `company_id` (<class 'int'>) ✓

---

#### GET /api/admin/companies/{company_id}

**Get detailed information about a specific company**

**Parameters:**

- `company_id` (<class 'int'>) ✓

---

#### POST /api/admin/companies/

**Create a new company**

**Parameters:**

- `company_data` (<class 'schemas.admin.CompanyCreateRequest'>) ✓

---

#### POST /api/admin/companies/

**Create a new company**

**Parameters:**

- `company_data` (<class 'schemas.admin.CompanyCreateRequest'>) ✓

---

#### PUT /api/admin/companies/{company_id}

**Update an existing company**

**Parameters:**

- `company_id` (<class 'int'>) ✓
- `company_data` (<class 'schemas.admin.CompanyUpdateRequest'>) ✓

---

#### PUT /api/admin/companies/{company_id}

**Update an existing company**

**Parameters:**

- `company_id` (<class 'int'>) ✓
- `company_data` (<class 'schemas.admin.CompanyUpdateRequest'>) ✓

---

#### DELETE /api/admin/companies/{company_id}

**Delete a company and all associated data**

**Parameters:**

- `company_id` (<class 'int'>) ✓

---

#### DELETE /api/admin/companies/{company_id}

**Delete a company and all associated data**

**Parameters:**

- `company_id` (<class 'int'>) ✓

---

#### GET /api/admin/payments/stats

**Get comprehensive payment statistics for admin dashboard**

---

#### GET /api/admin/payments/stats

**Get comprehensive payment statistics for admin dashboard**

---

#### GET /api/admin/payments/

**Get paginated list of payments with optional filtering**

**Parameters:**

- `page` (<class 'int'>) ○ (default: annotation=int required=False default=1 alias='page' json_schema_extra={} metadata=[Ge(ge=1)])
- `limit` (<class 'int'>) ○ (default: annotation=int required=False default=10 alias='limit' json_schema_extra={} metadata=[Ge(ge=1), Le(le=100)])
- `search` (typing.Optional[str]) ○ (default: annotation=Union[str, NoneType] required=False default=None alias='search' json_schema_extra={})
- `status` (typing.Optional[str]) ○ (default: annotation=Union[str, NoneType] required=False default=None alias='status' json_schema_extra={})

---

#### GET /api/admin/payments/

**Get paginated list of payments with optional filtering**

**Parameters:**

- `page` (<class 'int'>) ○ (default: annotation=int required=False default=1 alias='page' json_schema_extra={} metadata=[Ge(ge=1)])
- `limit` (<class 'int'>) ○ (default: annotation=int required=False default=10 alias='limit' json_schema_extra={} metadata=[Ge(ge=1), Le(le=100)])
- `search` (typing.Optional[str]) ○ (default: annotation=Union[str, NoneType] required=False default=None alias='search' json_schema_extra={})
- `status` (typing.Optional[str]) ○ (default: annotation=Union[str, NoneType] required=False default=None alias='status' json_schema_extra={})

---

#### GET /api/admin/payments/{payment_id}

**Get detailed information about a specific payment**

**Parameters:**

- `payment_id` (<class 'int'>) ✓

---

#### GET /api/admin/payments/{payment_id}

**Get detailed information about a specific payment**

**Parameters:**

- `payment_id` (<class 'int'>) ✓

---

#### DELETE /api/admin/payments/{payment_id}

**Delete a payment record**

**Parameters:**

- `payment_id` (<class 'int'>) ✓

---

#### DELETE /api/admin/payments/{payment_id}

**Delete a payment record**

**Parameters:**

- `payment_id` (<class 'int'>) ✓

---

#### POST /api/admin/payments/

**Create a new payment record**

**Parameters:**

- `payment_data` (<class 'schemas.admin.PaymentCreateRequest'>) ✓

---

#### POST /api/admin/payments/

**Create a new payment record**

**Parameters:**

- `payment_data` (<class 'schemas.admin.PaymentCreateRequest'>) ✓

---

#### PUT /api/admin/payments/{payment_id}

**Update an existing payment record**

**Parameters:**

- `payment_id` (<class 'int'>) ✓
- `payment_data` (<class 'schemas.admin.PaymentUpdateRequest'>) ✓

---

#### PUT /api/admin/payments/{payment_id}

**Update an existing payment record**

**Parameters:**

- `payment_id` (<class 'int'>) ✓
- `payment_data` (<class 'schemas.admin.PaymentUpdateRequest'>) ✓

---

#### GET /api/admin/settings/stats

**Get comprehensive settings statistics for admin dashboard**

---

#### GET /api/admin/settings/stats

**Get comprehensive settings statistics for admin dashboard**

---

#### GET /api/admin/settings

**Get paginated list of settings with optional filtering**

**Parameters:**

- `page` (<class 'int'>) ○ (default: annotation=int required=False default=1 alias='page' json_schema_extra={} metadata=[Ge(ge=1)])
- `limit` (<class 'int'>) ○ (default: annotation=int required=False default=10 alias='limit' json_schema_extra={} metadata=[Ge(ge=1), Le(le=100)])
- `search` (typing.Optional[str]) ○ (default: annotation=Union[str, NoneType] required=False default=None alias='search' json_schema_extra={})
- `category` (typing.Optional[str]) ○ (default: annotation=Union[str, NoneType] required=False default=None alias='category' json_schema_extra={})
- `is_public` (typing.Optional[bool]) ○ (default: annotation=Union[bool, NoneType] required=False default=None alias='is_public' json_schema_extra={})
- `is_editable` (typing.Optional[bool]) ○ (default: annotation=Union[bool, NoneType] required=False default=None alias='is_editable' json_schema_extra={})

---

#### GET /api/admin/settings

**Get paginated list of settings with optional filtering**

**Parameters:**

- `page` (<class 'int'>) ○ (default: annotation=int required=False default=1 alias='page' json_schema_extra={} metadata=[Ge(ge=1)])
- `limit` (<class 'int'>) ○ (default: annotation=int required=False default=10 alias='limit' json_schema_extra={} metadata=[Ge(ge=1), Le(le=100)])
- `search` (typing.Optional[str]) ○ (default: annotation=Union[str, NoneType] required=False default=None alias='search' json_schema_extra={})
- `category` (typing.Optional[str]) ○ (default: annotation=Union[str, NoneType] required=False default=None alias='category' json_schema_extra={})
- `is_public` (typing.Optional[bool]) ○ (default: annotation=Union[bool, NoneType] required=False default=None alias='is_public' json_schema_extra={})
- `is_editable` (typing.Optional[bool]) ○ (default: annotation=Union[bool, NoneType] required=False default=None alias='is_editable' json_schema_extra={})

---

#### GET /api/admin/settings/{setting_id}

**Get detailed information about a specific setting**

**Parameters:**

- `setting_id` (<class 'int'>) ✓

---

#### GET /api/admin/settings/{setting_id}

**Get detailed information about a specific setting**

**Parameters:**

- `setting_id` (<class 'int'>) ✓

---

#### GET /api/admin/settings/key/{key}

**Get setting by key**

**Parameters:**

- `key` (<class 'str'>) ✓

---

#### GET /api/admin/settings/key/{key}

**Get setting by key**

**Parameters:**

- `key` (<class 'str'>) ✓

---

#### POST /api/admin/settings

**Create a new setting**

**Parameters:**

- `setting_data` (<class 'schemas.admin.SettingsCreateRequest'>) ✓

---

#### POST /api/admin/settings

**Create a new setting**

**Parameters:**

- `setting_data` (<class 'schemas.admin.SettingsCreateRequest'>) ✓

---

#### PUT /api/admin/settings/{setting_id}

**Update an existing setting**

**Parameters:**

- `setting_id` (<class 'int'>) ✓
- `setting_data` (<class 'schemas.admin.SettingsUpdateRequest'>) ✓

---

#### PUT /api/admin/settings/{setting_id}

**Update an existing setting**

**Parameters:**

- `setting_id` (<class 'int'>) ✓
- `setting_data` (<class 'schemas.admin.SettingsUpdateRequest'>) ✓

---

#### PUT /api/admin/settings/key/{key}

**Update setting by key**

**Parameters:**

- `key` (<class 'str'>) ✓
- `setting_data` (<class 'schemas.admin.SettingsUpdateRequest'>) ✓

---

#### PUT /api/admin/settings/key/{key}

**Update setting by key**

**Parameters:**

- `key` (<class 'str'>) ✓
- `setting_data` (<class 'schemas.admin.SettingsUpdateRequest'>) ✓

---

#### DELETE /api/admin/settings/{setting_id}

**Delete a setting record**

**Parameters:**

- `setting_id` (<class 'int'>) ✓

---

#### DELETE /api/admin/settings/{setting_id}

**Delete a setting record**

**Parameters:**

- `setting_id` (<class 'int'>) ✓

---

#### GET /api/admin/settings/category/{category}

**Get all settings in a specific category**

**Parameters:**

- `category` (<class 'str'>) ✓
- `page` (<class 'int'>) ○ (default: annotation=int required=False default=1 alias='page' json_schema_extra={} metadata=[Ge(ge=1)])
- `limit` (<class 'int'>) ○ (default: annotation=int required=False default=10 alias='limit' json_schema_extra={} metadata=[Ge(ge=1), Le(le=100)])

---

#### GET /api/admin/settings/category/{category}

**Get all settings in a specific category**

**Parameters:**

- `category` (<class 'str'>) ✓
- `page` (<class 'int'>) ○ (default: annotation=int required=False default=1 alias='page' json_schema_extra={} metadata=[Ge(ge=1)])
- `limit` (<class 'int'>) ○ (default: annotation=int required=False default=10 alias='limit' json_schema_extra={} metadata=[Ge(ge=1), Le(le=100)])

---

#### GET /api/admin/roles/permissions

**Get paginated list of permissions with filtering**

**Parameters:**

- `page` (<class 'int'>) ○ (default: annotation=int required=False default=1 alias='page' json_schema_extra={} metadata=[Ge(ge=1)])
- `limit` (<class 'int'>) ○ (default: annotation=int required=False default=10 alias='limit' json_schema_extra={} metadata=[Ge(ge=1), Le(le=100)])
- `search` (typing.Optional[str]) ○ (default: annotation=Union[str, NoneType] required=False default=None alias='search' json_schema_extra={})
- `category` (typing.Optional[str]) ○ (default: annotation=Union[str, NoneType] required=False default=None alias='category' json_schema_extra={})
- `is_active` (typing.Optional[bool]) ○ (default: annotation=Union[bool, NoneType] required=False default=None alias='is_active' json_schema_extra={})

---

#### GET /api/admin/roles/permissions

**Get paginated list of permissions with filtering**

**Parameters:**

- `page` (<class 'int'>) ○ (default: annotation=int required=False default=1 alias='page' json_schema_extra={} metadata=[Ge(ge=1)])
- `limit` (<class 'int'>) ○ (default: annotation=int required=False default=10 alias='limit' json_schema_extra={} metadata=[Ge(ge=1), Le(le=100)])
- `search` (typing.Optional[str]) ○ (default: annotation=Union[str, NoneType] required=False default=None alias='search' json_schema_extra={})
- `category` (typing.Optional[str]) ○ (default: annotation=Union[str, NoneType] required=False default=None alias='category' json_schema_extra={})
- `is_active` (typing.Optional[bool]) ○ (default: annotation=Union[bool, NoneType] required=False default=None alias='is_active' json_schema_extra={})

---

#### POST /api/admin/roles/permissions

**Create a new permission**

**Parameters:**

- `permission_data` (<class 'schemas.role.PermissionCreateRequest'>) ✓

---

#### POST /api/admin/roles/permissions

**Create a new permission**

**Parameters:**

- `permission_data` (<class 'schemas.role.PermissionCreateRequest'>) ✓

---

#### GET /api/admin/roles/permissions/{permission_id}

**Get a specific permission by ID**

**Parameters:**

- `permission_id` (<class 'int'>) ✓

---

#### GET /api/admin/roles/permissions/{permission_id}

**Get a specific permission by ID**

**Parameters:**

- `permission_id` (<class 'int'>) ✓

---

#### PUT /api/admin/roles/permissions/{permission_id}

**Update a permission**

**Parameters:**

- `permission_id` (<class 'int'>) ✓
- `permission_data` (<class 'schemas.role.PermissionUpdateRequest'>) ✓

---

#### PUT /api/admin/roles/permissions/{permission_id}

**Update a permission**

**Parameters:**

- `permission_id` (<class 'int'>) ✓
- `permission_data` (<class 'schemas.role.PermissionUpdateRequest'>) ✓

---

#### DELETE /api/admin/roles/permissions/{permission_id}

**Delete a permission**

**Parameters:**

- `permission_id` (<class 'int'>) ✓

---

#### DELETE /api/admin/roles/permissions/{permission_id}

**Delete a permission**

**Parameters:**

- `permission_id` (<class 'int'>) ✓

---

#### GET /api/admin/roles/roles

**Get paginated list of roles with filtering**

**Parameters:**

- `page` (<class 'int'>) ○ (default: annotation=int required=False default=1 alias='page' json_schema_extra={} metadata=[Ge(ge=1)])
- `limit` (<class 'int'>) ○ (default: annotation=int required=False default=10 alias='limit' json_schema_extra={} metadata=[Ge(ge=1), Le(le=100)])
- `search` (typing.Optional[str]) ○ (default: annotation=Union[str, NoneType] required=False default=None alias='search' json_schema_extra={})
- `is_active` (typing.Optional[bool]) ○ (default: annotation=Union[bool, NoneType] required=False default=None alias='is_active' json_schema_extra={})

---

#### GET /api/admin/roles/roles

**Get paginated list of roles with filtering**

**Parameters:**

- `page` (<class 'int'>) ○ (default: annotation=int required=False default=1 alias='page' json_schema_extra={} metadata=[Ge(ge=1)])
- `limit` (<class 'int'>) ○ (default: annotation=int required=False default=10 alias='limit' json_schema_extra={} metadata=[Ge(ge=1), Le(le=100)])
- `search` (typing.Optional[str]) ○ (default: annotation=Union[str, NoneType] required=False default=None alias='search' json_schema_extra={})
- `is_active` (typing.Optional[bool]) ○ (default: annotation=Union[bool, NoneType] required=False default=None alias='is_active' json_schema_extra={})

---

#### POST /api/admin/roles/roles

**Create a new role**

**Parameters:**

- `role_data` (<class 'schemas.role.RoleCreateRequest'>) ✓

---

#### POST /api/admin/roles/roles

**Create a new role**

**Parameters:**

- `role_data` (<class 'schemas.role.RoleCreateRequest'>) ✓

---

#### GET /api/admin/roles/roles/{role_id}

**Get a specific role by ID with permissions**

**Parameters:**

- `role_id` (<class 'int'>) ✓

---

#### GET /api/admin/roles/roles/{role_id}

**Get a specific role by ID with permissions**

**Parameters:**

- `role_id` (<class 'int'>) ✓

---

#### PUT /api/admin/roles/roles/{role_id}

**Update a role**

**Parameters:**

- `role_id` (<class 'int'>) ✓
- `role_data` (<class 'schemas.role.RoleUpdateRequest'>) ✓

---

#### PUT /api/admin/roles/roles/{role_id}

**Update a role**

**Parameters:**

- `role_id` (<class 'int'>) ✓
- `role_data` (<class 'schemas.role.RoleUpdateRequest'>) ✓

---

#### DELETE /api/admin/roles/roles/{role_id}

**Delete a role**

**Parameters:**

- `role_id` (<class 'int'>) ✓

---

#### DELETE /api/admin/roles/roles/{role_id}

**Delete a role**

**Parameters:**

- `role_id` (<class 'int'>) ✓

---

#### GET /api/admin/roles/user-roles

**Get paginated list of user role assignments with filtering**

**Parameters:**

- `page` (<class 'int'>) ○ (default: annotation=int required=False default=1 alias='page' json_schema_extra={} metadata=[Ge(ge=1)])
- `limit` (<class 'int'>) ○ (default: annotation=int required=False default=10 alias='limit' json_schema_extra={} metadata=[Ge(ge=1), Le(le=100)])
- `user_id` (typing.Optional[int]) ○ (default: annotation=Union[int, NoneType] required=False default=None alias='user_id' json_schema_extra={})
- `role_id` (typing.Optional[int]) ○ (default: annotation=Union[int, NoneType] required=False default=None alias='role_id' json_schema_extra={})
- `is_active` (typing.Optional[bool]) ○ (default: annotation=Union[bool, NoneType] required=False default=None alias='is_active' json_schema_extra={})

---

#### GET /api/admin/roles/user-roles

**Get paginated list of user role assignments with filtering**

**Parameters:**

- `page` (<class 'int'>) ○ (default: annotation=int required=False default=1 alias='page' json_schema_extra={} metadata=[Ge(ge=1)])
- `limit` (<class 'int'>) ○ (default: annotation=int required=False default=10 alias='limit' json_schema_extra={} metadata=[Ge(ge=1), Le(le=100)])
- `user_id` (typing.Optional[int]) ○ (default: annotation=Union[int, NoneType] required=False default=None alias='user_id' json_schema_extra={})
- `role_id` (typing.Optional[int]) ○ (default: annotation=Union[int, NoneType] required=False default=None alias='role_id' json_schema_extra={})
- `is_active` (typing.Optional[bool]) ○ (default: annotation=Union[bool, NoneType] required=False default=None alias='is_active' json_schema_extra={})

---

#### POST /api/admin/roles/user-roles

**Assign a role to a user**

**Parameters:**

- `user_role_data` (<class 'schemas.role.UserRoleCreateRequest'>) ✓

---

#### POST /api/admin/roles/user-roles

**Assign a role to a user**

**Parameters:**

- `user_role_data` (<class 'schemas.role.UserRoleCreateRequest'>) ✓

---

#### PUT /api/admin/roles/user-roles/{user_role_id}

**Update a user role assignment**

**Parameters:**

- `user_role_id` (<class 'int'>) ✓
- `user_role_data` (<class 'schemas.role.UserRoleUpdateRequest'>) ✓

---

#### PUT /api/admin/roles/user-roles/{user_role_id}

**Update a user role assignment**

**Parameters:**

- `user_role_id` (<class 'int'>) ✓
- `user_role_data` (<class 'schemas.role.UserRoleUpdateRequest'>) ✓

---

#### DELETE /api/admin/roles/user-roles/{user_role_id}

**Remove a role from a user**

**Parameters:**

- `user_role_id` (<class 'int'>) ✓

---

#### DELETE /api/admin/roles/user-roles/{user_role_id}

**Remove a role from a user**

**Parameters:**

- `user_role_id` (<class 'int'>) ✓

---

#### GET /api/admin/roles/stats

**Get roles and permissions statistics**

---

#### GET /api/admin/roles/stats

**Get roles and permissions statistics**

---

### Admin-People

#### GET /api/admin/people/stats

**Get comprehensive people statistics for admin dashboard**

---

#### GET /api/admin/people/

**Get paginated list of people with optional filtering**

**Parameters:**

- `page` (<class 'int'>) ○ (default: annotation=int required=False default=1 alias='page' json_schema_extra={} metadata=[Ge(ge=1)])
- `limit` (<class 'int'>) ○ (default: annotation=int required=False default=10 alias='limit' json_schema_extra={} metadata=[Ge(ge=1), Le(le=100)])
- `search` (typing.Optional[str]) ○ (default: annotation=Union[str, NoneType] required=False default=None alias='search' json_schema_extra={})
- `risk_level` (typing.Optional[str]) ○ (default: annotation=Union[str, NoneType] required=False default=None alias='risk_level' json_schema_extra={})

---

#### GET /api/admin/people/{person_id}

**Get detailed information about a specific person**

**Parameters:**

- `person_id` (<class 'int'>) ✓

---

#### POST /api/admin/people/

**Create a new person record**

**Parameters:**

- `person_data` (<class 'dict'>) ✓

---

#### PUT /api/admin/people/{person_id}

**Update an existing person record**

**Parameters:**

- `person_id` (<class 'int'>) ✓
- `person_data` (<class 'dict'>) ✓

---

#### DELETE /api/admin/people/{person_id}

**Delete a person and all associated data**

**Parameters:**

- `person_id` (<class 'int'>) ✓

---

### Admin-Banks

#### GET /api/admin/banks/stats

**Get comprehensive bank statistics for admin dashboard**

---

#### GET /api/admin/banks/

**Get paginated list of banks with optional filtering**

**Parameters:**

- `page` (<class 'int'>) ○ (default: annotation=int required=False default=1 alias='page' json_schema_extra={} metadata=[Ge(ge=1)])
- `limit` (<class 'int'>) ○ (default: annotation=int required=False default=10 alias='limit' json_schema_extra={} metadata=[Ge(ge=1), Le(le=100)])
- `search` (typing.Optional[str]) ○ (default: annotation=Union[str, NoneType] required=False default=None alias='search' json_schema_extra={})
- `bank_type` (typing.Optional[str]) ○ (default: annotation=Union[str, NoneType] required=False default=None alias='bank_type' json_schema_extra={})

---

#### GET /api/admin/banks/{bank_id}

**Get detailed information about a specific bank**

**Parameters:**

- `bank_id` (<class 'int'>) ✓

---

#### POST /api/admin/banks/

**Create a new bank**

**Parameters:**

- `bank_data` (<class 'schemas.admin.BankCreateRequest'>) ✓

---

#### PUT /api/admin/banks/{bank_id}

**Update an existing bank**

**Parameters:**

- `bank_id` (<class 'int'>) ✓
- `bank_data` (<class 'schemas.admin.BankUpdateRequest'>) ✓

---

#### DELETE /api/admin/banks/{bank_id}

**Delete a bank and all associated data**

**Parameters:**

- `bank_id` (<class 'int'>) ✓

---

### Admin-Insurance

#### GET /api/admin/insurance/stats

**Get comprehensive insurance statistics for admin dashboard**

---

#### GET /api/admin/insurance/

**Get paginated list of insurance companies with optional filtering**

**Parameters:**

- `page` (<class 'int'>) ○ (default: annotation=int required=False default=1 alias='page' json_schema_extra={} metadata=[Ge(ge=1)])
- `limit` (<class 'int'>) ○ (default: annotation=int required=False default=10 alias='limit' json_schema_extra={} metadata=[Ge(ge=1), Le(le=100)])
- `search` (typing.Optional[str]) ○ (default: annotation=Union[str, NoneType] required=False default=None alias='search' json_schema_extra={})
- `insurance_type` (typing.Optional[str]) ○ (default: annotation=Union[str, NoneType] required=False default=None alias='insurance_type' json_schema_extra={})

---

#### GET /api/admin/insurance/{insurance_id}

**Get detailed information about a specific insurance company**

**Parameters:**

- `insurance_id` (<class 'int'>) ✓

---

#### POST /api/admin/insurance/

**Create a new insurance company**

**Parameters:**

- `insurance_data` (<class 'schemas.admin.InsuranceCreateRequest'>) ✓

---

#### PUT /api/admin/insurance/{insurance_id}

**Update an existing insurance company**

**Parameters:**

- `insurance_id` (<class 'int'>) ✓
- `insurance_data` (<class 'schemas.admin.InsuranceUpdateRequest'>) ✓

---

#### DELETE /api/admin/insurance/{insurance_id}

**Delete an insurance company and all associated data**

**Parameters:**

- `insurance_id` (<class 'int'>) ✓

---

### Admin-Companies

#### GET /api/admin/companies/stats

**Get comprehensive company statistics for admin dashboard**

---

#### GET /api/admin/companies/

**Get paginated list of companies with optional filtering**

**Parameters:**

- `page` (<class 'int'>) ○ (default: annotation=int required=False default=1 alias='page' json_schema_extra={} metadata=[Ge(ge=1)])
- `limit` (<class 'int'>) ○ (default: annotation=int required=False default=10 alias='limit' json_schema_extra={} metadata=[Ge(ge=1), Le(le=100)])
- `search` (typing.Optional[str]) ○ (default: annotation=Union[str, NoneType] required=False default=None alias='search' json_schema_extra={})
- `company_type` (typing.Optional[str]) ○ (default: annotation=Union[str, NoneType] required=False default=None alias='company_type' json_schema_extra={})

---

#### GET /api/admin/companies/{company_id}

**Get detailed information about a specific company**

**Parameters:**

- `company_id` (<class 'int'>) ✓

---

#### POST /api/admin/companies/

**Create a new company**

**Parameters:**

- `company_data` (<class 'schemas.admin.CompanyCreateRequest'>) ✓

---

#### PUT /api/admin/companies/{company_id}

**Update an existing company**

**Parameters:**

- `company_id` (<class 'int'>) ✓
- `company_data` (<class 'schemas.admin.CompanyUpdateRequest'>) ✓

---

#### DELETE /api/admin/companies/{company_id}

**Delete a company and all associated data**

**Parameters:**

- `company_id` (<class 'int'>) ✓

---

### Admin-Payments

#### GET /api/admin/payments/stats

**Get comprehensive payment statistics for admin dashboard**

---

#### GET /api/admin/payments/

**Get paginated list of payments with optional filtering**

**Parameters:**

- `page` (<class 'int'>) ○ (default: annotation=int required=False default=1 alias='page' json_schema_extra={} metadata=[Ge(ge=1)])
- `limit` (<class 'int'>) ○ (default: annotation=int required=False default=10 alias='limit' json_schema_extra={} metadata=[Ge(ge=1), Le(le=100)])
- `search` (typing.Optional[str]) ○ (default: annotation=Union[str, NoneType] required=False default=None alias='search' json_schema_extra={})
- `status` (typing.Optional[str]) ○ (default: annotation=Union[str, NoneType] required=False default=None alias='status' json_schema_extra={})

---

#### GET /api/admin/payments/{payment_id}

**Get detailed information about a specific payment**

**Parameters:**

- `payment_id` (<class 'int'>) ✓

---

#### DELETE /api/admin/payments/{payment_id}

**Delete a payment record**

**Parameters:**

- `payment_id` (<class 'int'>) ✓

---

#### POST /api/admin/payments/

**Create a new payment record**

**Parameters:**

- `payment_data` (<class 'schemas.admin.PaymentCreateRequest'>) ✓

---

#### PUT /api/admin/payments/{payment_id}

**Update an existing payment record**

**Parameters:**

- `payment_id` (<class 'int'>) ✓
- `payment_data` (<class 'schemas.admin.PaymentUpdateRequest'>) ✓

---

### Admin-Settings

#### GET /api/admin/settings/stats

**Get comprehensive settings statistics for admin dashboard**

---

#### GET /api/admin/settings

**Get paginated list of settings with optional filtering**

**Parameters:**

- `page` (<class 'int'>) ○ (default: annotation=int required=False default=1 alias='page' json_schema_extra={} metadata=[Ge(ge=1)])
- `limit` (<class 'int'>) ○ (default: annotation=int required=False default=10 alias='limit' json_schema_extra={} metadata=[Ge(ge=1), Le(le=100)])
- `search` (typing.Optional[str]) ○ (default: annotation=Union[str, NoneType] required=False default=None alias='search' json_schema_extra={})
- `category` (typing.Optional[str]) ○ (default: annotation=Union[str, NoneType] required=False default=None alias='category' json_schema_extra={})
- `is_public` (typing.Optional[bool]) ○ (default: annotation=Union[bool, NoneType] required=False default=None alias='is_public' json_schema_extra={})
- `is_editable` (typing.Optional[bool]) ○ (default: annotation=Union[bool, NoneType] required=False default=None alias='is_editable' json_schema_extra={})

---

#### GET /api/admin/settings/{setting_id}

**Get detailed information about a specific setting**

**Parameters:**

- `setting_id` (<class 'int'>) ✓

---

#### GET /api/admin/settings/key/{key}

**Get setting by key**

**Parameters:**

- `key` (<class 'str'>) ✓

---

#### POST /api/admin/settings

**Create a new setting**

**Parameters:**

- `setting_data` (<class 'schemas.admin.SettingsCreateRequest'>) ✓

---

#### PUT /api/admin/settings/{setting_id}

**Update an existing setting**

**Parameters:**

- `setting_id` (<class 'int'>) ✓
- `setting_data` (<class 'schemas.admin.SettingsUpdateRequest'>) ✓

---

#### PUT /api/admin/settings/key/{key}

**Update setting by key**

**Parameters:**

- `key` (<class 'str'>) ✓
- `setting_data` (<class 'schemas.admin.SettingsUpdateRequest'>) ✓

---

#### DELETE /api/admin/settings/{setting_id}

**Delete a setting record**

**Parameters:**

- `setting_id` (<class 'int'>) ✓

---

#### GET /api/admin/settings/category/{category}

**Get all settings in a specific category**

**Parameters:**

- `category` (<class 'str'>) ✓
- `page` (<class 'int'>) ○ (default: annotation=int required=False default=1 alias='page' json_schema_extra={} metadata=[Ge(ge=1)])
- `limit` (<class 'int'>) ○ (default: annotation=int required=False default=10 alias='limit' json_schema_extra={} metadata=[Ge(ge=1), Le(le=100)])

---

### Admin-Roles

#### GET /api/admin/roles/permissions

**Get paginated list of permissions with filtering**

**Parameters:**

- `page` (<class 'int'>) ○ (default: annotation=int required=False default=1 alias='page' json_schema_extra={} metadata=[Ge(ge=1)])
- `limit` (<class 'int'>) ○ (default: annotation=int required=False default=10 alias='limit' json_schema_extra={} metadata=[Ge(ge=1), Le(le=100)])
- `search` (typing.Optional[str]) ○ (default: annotation=Union[str, NoneType] required=False default=None alias='search' json_schema_extra={})
- `category` (typing.Optional[str]) ○ (default: annotation=Union[str, NoneType] required=False default=None alias='category' json_schema_extra={})
- `is_active` (typing.Optional[bool]) ○ (default: annotation=Union[bool, NoneType] required=False default=None alias='is_active' json_schema_extra={})

---

#### POST /api/admin/roles/permissions

**Create a new permission**

**Parameters:**

- `permission_data` (<class 'schemas.role.PermissionCreateRequest'>) ✓

---

#### GET /api/admin/roles/permissions/{permission_id}

**Get a specific permission by ID**

**Parameters:**

- `permission_id` (<class 'int'>) ✓

---

#### PUT /api/admin/roles/permissions/{permission_id}

**Update a permission**

**Parameters:**

- `permission_id` (<class 'int'>) ✓
- `permission_data` (<class 'schemas.role.PermissionUpdateRequest'>) ✓

---

#### DELETE /api/admin/roles/permissions/{permission_id}

**Delete a permission**

**Parameters:**

- `permission_id` (<class 'int'>) ✓

---

#### GET /api/admin/roles/roles

**Get paginated list of roles with filtering**

**Parameters:**

- `page` (<class 'int'>) ○ (default: annotation=int required=False default=1 alias='page' json_schema_extra={} metadata=[Ge(ge=1)])
- `limit` (<class 'int'>) ○ (default: annotation=int required=False default=10 alias='limit' json_schema_extra={} metadata=[Ge(ge=1), Le(le=100)])
- `search` (typing.Optional[str]) ○ (default: annotation=Union[str, NoneType] required=False default=None alias='search' json_schema_extra={})
- `is_active` (typing.Optional[bool]) ○ (default: annotation=Union[bool, NoneType] required=False default=None alias='is_active' json_schema_extra={})

---

#### POST /api/admin/roles/roles

**Create a new role**

**Parameters:**

- `role_data` (<class 'schemas.role.RoleCreateRequest'>) ✓

---

#### GET /api/admin/roles/roles/{role_id}

**Get a specific role by ID with permissions**

**Parameters:**

- `role_id` (<class 'int'>) ✓

---

#### PUT /api/admin/roles/roles/{role_id}

**Update a role**

**Parameters:**

- `role_id` (<class 'int'>) ✓
- `role_data` (<class 'schemas.role.RoleUpdateRequest'>) ✓

---

#### DELETE /api/admin/roles/roles/{role_id}

**Delete a role**

**Parameters:**

- `role_id` (<class 'int'>) ✓

---

#### GET /api/admin/roles/user-roles

**Get paginated list of user role assignments with filtering**

**Parameters:**

- `page` (<class 'int'>) ○ (default: annotation=int required=False default=1 alias='page' json_schema_extra={} metadata=[Ge(ge=1)])
- `limit` (<class 'int'>) ○ (default: annotation=int required=False default=10 alias='limit' json_schema_extra={} metadata=[Ge(ge=1), Le(le=100)])
- `user_id` (typing.Optional[int]) ○ (default: annotation=Union[int, NoneType] required=False default=None alias='user_id' json_schema_extra={})
- `role_id` (typing.Optional[int]) ○ (default: annotation=Union[int, NoneType] required=False default=None alias='role_id' json_schema_extra={})
- `is_active` (typing.Optional[bool]) ○ (default: annotation=Union[bool, NoneType] required=False default=None alias='is_active' json_schema_extra={})

---

#### POST /api/admin/roles/user-roles

**Assign a role to a user**

**Parameters:**

- `user_role_data` (<class 'schemas.role.UserRoleCreateRequest'>) ✓

---

#### PUT /api/admin/roles/user-roles/{user_role_id}

**Update a user role assignment**

**Parameters:**

- `user_role_id` (<class 'int'>) ✓
- `user_role_data` (<class 'schemas.role.UserRoleUpdateRequest'>) ✓

---

#### DELETE /api/admin/roles/user-roles/{user_role_id}

**Remove a role from a user**

**Parameters:**

- `user_role_id` (<class 'int'>) ✓

---

#### GET /api/admin/roles/stats

**Get roles and permissions statistics**

---

### Admin_Payments

#### GET /api/admin/payments/stats

**Get comprehensive payment statistics for admin dashboard**

---

#### GET /api/admin/payments/

**Get paginated list of payments with optional filtering**

**Parameters:**

- `page` (<class 'int'>) ○ (default: annotation=int required=False default=1 alias='page' json_schema_extra={} metadata=[Ge(ge=1)])
- `limit` (<class 'int'>) ○ (default: annotation=int required=False default=10 alias='limit' json_schema_extra={} metadata=[Ge(ge=1), Le(le=100)])
- `search` (typing.Optional[str]) ○ (default: annotation=Union[str, NoneType] required=False default=None alias='search' json_schema_extra={})
- `status` (typing.Optional[str]) ○ (default: annotation=Union[str, NoneType] required=False default=None alias='status' json_schema_extra={})

---

#### GET /api/admin/payments/{payment_id}

**Get detailed information about a specific payment**

**Parameters:**

- `payment_id` (<class 'int'>) ✓

---

#### DELETE /api/admin/payments/{payment_id}

**Delete a payment record**

**Parameters:**

- `payment_id` (<class 'int'>) ✓

---

#### POST /api/admin/payments/

**Create a new payment record**

**Parameters:**

- `payment_data` (<class 'schemas.admin.PaymentCreateRequest'>) ✓

---

#### PUT /api/admin/payments/{payment_id}

**Update an existing payment record**

**Parameters:**

- `payment_id` (<class 'int'>) ✓
- `payment_data` (<class 'schemas.admin.PaymentUpdateRequest'>) ✓

---

### Admin_Case_Hearings

#### GET /api/admin/case-hearings/test

**Test endpoint without authentication**

---

#### GET /api/admin/case-hearings/search/cases

**Search cases by suit reference number or title for hearing creation**

**Parameters:**

- `q` (<class 'str'>) ○ (default: annotation=str required=False default='' alias='q' json_schema_extra={} metadata=[MinLen(min_length=0)])
- `limit` (<class 'int'>) ○ (default: annotation=int required=False default=1000 alias='limit' json_schema_extra={} metadata=[Ge(ge=1), Le(le=10000)])

---

#### GET /api/admin/case-hearings/courts

**Get courts for hearing creation/editing**

**Parameters:**

- `court_type` (typing.Optional[str]) ○ (default: annotation=Union[str, NoneType] required=False default=None alias='court_type' json_schema_extra={})

---

#### GET /api/admin/case-hearings/judges

**Get judges for hearing creation/editing**

---

#### GET /api/admin/case-hearings

**Get all case hearings with filtering and pagination for admin**

**Parameters:**

- `page` (<class 'int'>) ○ (default: annotation=int required=False default=1 alias='page' json_schema_extra={} metadata=[Ge(ge=1)])
- `limit` (<class 'int'>) ○ (default: annotation=int required=False default=50 alias='limit' json_schema_extra={} metadata=[Ge(ge=1), Le(le=100)])
- `search` (typing.Optional[str]) ○ (default: annotation=Union[str, NoneType] required=False default=None alias='search' json_schema_extra={})
- `court_type` (typing.Optional[str]) ○ (default: annotation=Union[str, NoneType] required=False default=None alias='court_type' json_schema_extra={})
- `remark` (typing.Optional[str]) ○ (default: annotation=Union[str, NoneType] required=False default=None alias='remark' json_schema_extra={})
- `group_by_case` (<class 'bool'>) ○ (default: annotation=bool required=False default=False alias='group_by_case' json_schema_extra={})

---

#### GET /api/admin/case-hearings/{hearing_id}

**Get a specific case hearing by ID**

**Parameters:**

- `hearing_id` (<class 'int'>) ✓

---

#### POST /api/admin/case-hearings

**Create a new case hearing record**

**Parameters:**

- `hearing_data` (<class 'dict'>) ✓

---

#### PUT /api/admin/case-hearings/{hearing_id}

**Update a case hearing record**

**Parameters:**

- `hearing_id` (<class 'int'>) ✓
- `hearing_data` (<class 'dict'>) ✓

---

#### DELETE /api/admin/case-hearings/{hearing_id}

**Delete a case hearing record**

**Parameters:**

- `hearing_id` (<class 'int'>) ✓

---

#### GET /api/admin/case-hearings/search/cases

**Search cases by suit reference number or title for hearing creation**

**Parameters:**

- `q` (<class 'str'>) ○ (default: annotation=str required=False default='' alias='q' json_schema_extra={} metadata=[MinLen(min_length=0)])
- `limit` (<class 'int'>) ○ (default: annotation=int required=False default=1000 alias='limit' json_schema_extra={} metadata=[Ge(ge=1), Le(le=10000)])

---

#### GET /api/all-cases

**Get ALL cases from the database for hearing creation**

---

#### GET /api/admin/case-hearings/courts

**Get courts for hearing creation/editing**

**Parameters:**

- `court_type` (typing.Optional[str]) ○ (default: annotation=Union[str, NoneType] required=False default=None alias='court_type' json_schema_extra={})

---

#### GET /api/admin/case-hearings/judges

**Get judges for hearing creation/editing**

---

#### GET /api/admin/case-hearings/stats

**Get hearing statistics for admin dashboard**

---

### Judges

#### GET /api/admin/judges

**Get list of judges with filtering and pagination**

**Parameters:**

- `page` (<class 'int'>) ○ (default: annotation=int required=False default=1 alias='page' description='Page number' json_schema_extra={} metadata=[Ge(ge=1)])
- `limit` (<class 'int'>) ○ (default: annotation=int required=False default=20 alias='limit' description='Items per page' json_schema_extra={} metadata=[Ge(ge=1), Le(le=100)])
- `search` (typing.Optional[str]) ○ (default: annotation=Union[str, NoneType] required=False default=None alias='search' description='Search term for name, title, or court type' json_schema_extra={})
- `status` (typing.Optional[models.judges.JudgeStatus]) ○ (default: annotation=Union[JudgeStatus, NoneType] required=False default=None alias='status' description='Filter by status' json_schema_extra={})
- `court_type` (typing.Optional[str]) ○ (default: annotation=Union[str, NoneType] required=False default=None alias='court_type' description='Filter by court type' json_schema_extra={})
- `region` (typing.Optional[str]) ○ (default: annotation=Union[str, NoneType] required=False default=None alias='region' description='Filter by region' json_schema_extra={})

---

#### GET /api/admin/judges/{judge_id}

**Get a specific judge by ID**

**Parameters:**

- `judge_id` (<class 'int'>) ✓

---

#### POST /api/admin/judges

**Create a new judge**

**Parameters:**

- `judge_data` (<class 'schemas.judges.JudgeCreate'>) ✓

---

#### PUT /api/admin/judges/{judge_id}

**Update a judge**

**Parameters:**

- `judge_id` (<class 'int'>) ✓
- `judge_data` (<class 'schemas.judges.JudgeUpdate'>) ✓

---

#### DELETE /api/admin/judges/{judge_id}

**Delete a judge (soft delete)**

**Parameters:**

- `judge_id` (<class 'int'>) ✓

---

#### GET /api/admin/judges/search/active

**Search active judges for dropdowns**

**Parameters:**

- `query` (<class 'str'>) ○ (default: annotation=str required=False default='' alias='query' description='Search query' json_schema_extra={})
- `limit` (<class 'int'>) ○ (default: annotation=int required=False default=50 alias='limit' description='Maximum results' json_schema_extra={} metadata=[Ge(ge=1), Le(le=100)])

---

### Court_Types

#### GET /api/admin/court-types

**Get list of court types with filtering and pagination**

**Parameters:**

- `page` (<class 'int'>) ○ (default: annotation=int required=False default=1 alias='page' description='Page number' json_schema_extra={} metadata=[Ge(ge=1)])
- `limit` (<class 'int'>) ○ (default: annotation=int required=False default=20 alias='limit' description='Items per page' json_schema_extra={} metadata=[Ge(ge=1), Le(le=100)])
- `search` (typing.Optional[str]) ○ (default: annotation=Union[str, NoneType] required=False default=None alias='search' description='Search term for name or code' json_schema_extra={})
- `level` (typing.Optional[models.court_types.CourtLevel]) ○ (default: annotation=Union[CourtLevel, NoneType] required=False default=None alias='level' description='Filter by court level' json_schema_extra={})
- `region` (typing.Optional[str]) ○ (default: annotation=Union[str, NoneType] required=False default=None alias='region' description='Filter by region' json_schema_extra={})

---

#### GET /api/admin/court-types/{court_type_id}

**Get a specific court type by ID**

**Parameters:**

- `court_type_id` (<class 'int'>) ✓

---

#### POST /api/admin/court-types

**Create a new court type**

**Parameters:**

- `court_type_data` (<class 'schemas.court_types.CourtTypeCreate'>) ✓

---

#### PUT /api/admin/court-types/{court_type_id}

**Update a court type**

**Parameters:**

- `court_type_id` (<class 'int'>) ✓
- `court_type_data` (<class 'schemas.court_types.CourtTypeUpdate'>) ✓

---

#### DELETE /api/admin/court-types/{court_type_id}

**Delete a court type (soft delete)**

**Parameters:**

- `court_type_id` (<class 'int'>) ✓

---

#### GET /api/admin/court-types/search/active

**Search active court types for dropdowns**

**Parameters:**

- `query` (<class 'str'>) ○ (default: annotation=str required=False default='' alias='query' description='Search query' json_schema_extra={})
- `limit` (<class 'int'>) ○ (default: annotation=int required=False default=50 alias='limit' description='Maximum results' json_schema_extra={} metadata=[Ge(ge=1), Le(le=100)])

---

### Tenant

#### GET /api/tenant/tenants/stats

**Get tenant statistics**

---

#### GET /api/tenant/tenants

**Get paginated list of tenants with filtering**

**Parameters:**

- `page` (<class 'int'>) ○ (default: annotation=int required=False default=1 alias='page' json_schema_extra={} metadata=[Ge(ge=1)])
- `limit` (<class 'int'>) ○ (default: annotation=int required=False default=10 alias='limit' json_schema_extra={} metadata=[Ge(ge=1), Le(le=100)])
- `search` (typing.Optional[str]) ○ (default: annotation=Union[str, NoneType] required=False default=None alias='search' json_schema_extra={})
- `status` (typing.Optional[str]) ○ (default: annotation=Union[str, NoneType] required=False default=None alias='status' json_schema_extra={})
- `is_approved` (typing.Optional[bool]) ○ (default: annotation=Union[bool, NoneType] required=False default=None alias='is_approved' json_schema_extra={})

---

#### GET /api/tenant/tenants/{tenant_id}

**Get tenant by ID**

**Parameters:**

- `tenant_id` (<class 'int'>) ✓

---

#### POST /api/tenant/tenants

**Create a new tenant**

**Parameters:**

- `tenant_data` (<class 'schemas.tenant.TenantCreateRequest'>) ✓

---

#### PUT /api/tenant/tenants/{tenant_id}

**Update tenant**

**Parameters:**

- `tenant_id` (<class 'int'>) ✓
- `tenant_data` (<class 'schemas.tenant.TenantUpdateRequest'>) ✓

---

#### DELETE /api/tenant/tenants/{tenant_id}

**Delete tenant (soft delete by setting is_active to False)**

**Parameters:**

- `tenant_id` (<class 'int'>) ✓

---

#### GET /api/tenant/plans

**Get paginated list of subscription plans**

**Parameters:**

- `page` (<class 'int'>) ○ (default: annotation=int required=False default=1 alias='page' json_schema_extra={} metadata=[Ge(ge=1)])
- `limit` (<class 'int'>) ○ (default: annotation=int required=False default=10 alias='limit' json_schema_extra={} metadata=[Ge(ge=1), Le(le=100)])
- `is_active` (typing.Optional[bool]) ○ (default: annotation=Union[bool, NoneType] required=False default=None alias='is_active' json_schema_extra={})

---

#### GET /api/tenant/plans/{plan_id}

**Get subscription plan by ID**

**Parameters:**

- `plan_id` (<class 'int'>) ✓

---

#### GET /api/tenant/subscription-requests

**Get paginated list of subscription requests**

**Parameters:**

- `page` (<class 'int'>) ○ (default: annotation=int required=False default=1 alias='page' json_schema_extra={} metadata=[Ge(ge=1)])
- `limit` (<class 'int'>) ○ (default: annotation=int required=False default=10 alias='limit' json_schema_extra={} metadata=[Ge(ge=1), Le(le=100)])
- `status` (typing.Optional[str]) ○ (default: annotation=Union[str, NoneType] required=False default=None alias='status' json_schema_extra={})
- `tenant_id` (typing.Optional[int]) ○ (default: annotation=Union[int, NoneType] required=False default=None alias='tenant_id' json_schema_extra={})

---

#### POST /api/tenant/subscription-requests

**Create a new subscription request**

**Parameters:**

- `request_data` (<class 'schemas.tenant.SubscriptionRequestCreateRequest'>) ✓

---

#### PUT /api/tenant/subscription-requests/{request_id}/approve

**Approve a subscription request**

**Parameters:**

- `request_id` (<class 'int'>) ✓
- `admin_notes` (typing.Optional[str]) ○

---

#### PUT /api/tenant/subscription-requests/{request_id}/reject

**Reject a subscription request**

**Parameters:**

- `request_id` (<class 'int'>) ✓
- `admin_notes` (<class 'str'>) ✓

---

#### GET /api/tenant/tenants/{tenant_id}/settings

**Get tenant settings**

**Parameters:**

- `tenant_id` (<class 'int'>) ✓

---

#### POST /api/tenant/tenants/{tenant_id}/settings

**Create tenant setting**

**Parameters:**

- `tenant_id` (<class 'int'>) ✓
- `setting_data` (<class 'schemas.tenant.TenantSettingCreateRequest'>) ✓

---

#### PUT /api/tenant/tenants/{tenant_id}/settings/{setting_id}

**Update tenant setting**

**Parameters:**

- `tenant_id` (<class 'int'>) ✓
- `setting_id` (<class 'int'>) ✓
- `setting_data` (<class 'schemas.tenant.TenantSettingUpdateRequest'>) ✓

---

#### GET /api/tenant/tenants

**Get all tenants with filtering and pagination**

**Parameters:**

- `page` (<class 'int'>) ○ (default: annotation=int required=False default=1 alias='page' json_schema_extra={} metadata=[Ge(ge=1)])
- `limit` (<class 'int'>) ○ (default: annotation=int required=False default=10 alias='limit' json_schema_extra={} metadata=[Ge(ge=1), Le(le=100)])
- `search` (<class 'str'>) ○ (default: annotation=str required=False default='' alias='search' json_schema_extra={})
- `status` (<class 'str'>) ○ (default: annotation=str required=False default='' alias='status' json_schema_extra={})
- `plan` (<class 'str'>) ○ (default: annotation=str required=False default='' alias='plan' json_schema_extra={})

---

#### GET /api/tenant/tenants/{tenant_id}

**Get a specific tenant by ID**

**Parameters:**

- `tenant_id` (<class 'int'>) ✓

---

#### POST /api/tenant/tenants

**Create a new tenant**

**Parameters:**

- `tenant_data` (<class 'schemas.tenant.TenantCreateRequest'>) ✓

---

#### PUT /api/tenant/tenants/{tenant_id}

**Update a tenant**

**Parameters:**

- `tenant_id` (<class 'int'>) ✓
- `tenant_data` (<class 'schemas.tenant.TenantUpdateRequest'>) ✓

---

#### DELETE /api/tenant/tenants/{tenant_id}

**Delete a tenant**

**Parameters:**

- `tenant_id` (<class 'int'>) ✓

---

### Courts

#### GET /api/courts/

**Get all courts with optional filtering**

**Parameters:**

- `page` (<class 'int'>) ○ (default: annotation=int required=False default=1 alias='page' description='Page number' json_schema_extra={} metadata=[Ge(ge=1)])
- `limit` (<class 'int'>) ○ (default: annotation=int required=False default=20 alias='limit' description='Number of results per page' json_schema_extra={} metadata=[Ge(ge=1), Le(le=100)])
- `court_type` (typing.Optional[schemas.court.CourtType]) ○ (default: annotation=Union[CourtType, NoneType] required=False default=None alias='court_type' description='Filter by court type' json_schema_extra={})
- `region` (typing.Optional[str]) ○ (default: annotation=Union[str, NoneType] required=False default=None alias='region' description='Filter by region' json_schema_extra={})
- `city` (typing.Optional[str]) ○ (default: annotation=Union[str, NoneType] required=False default=None alias='city' description='Filter by city' json_schema_extra={})
- `is_active` (typing.Optional[bool]) ○ (default: annotation=Union[bool, NoneType] required=False default=None alias='is_active' description='Filter by active status' json_schema_extra={})

---

#### GET /api/courts/search

**Search courts with various filters**

**Parameters:**

- `query` (typing.Optional[str]) ○ (default: annotation=Union[str, NoneType] required=False default=None alias='query' description='Search query' json_schema_extra={})
- `court_type` (typing.Optional[schemas.court.CourtType]) ○ (default: annotation=Union[CourtType, NoneType] required=False default=None alias='court_type' description='Filter by court type' json_schema_extra={})
- `region` (typing.Optional[str]) ○ (default: annotation=Union[str, NoneType] required=False default=None alias='region' description='Filter by region' json_schema_extra={})
- `city` (typing.Optional[str]) ○ (default: annotation=Union[str, NoneType] required=False default=None alias='city' description='Filter by city' json_schema_extra={})
- `district` (typing.Optional[str]) ○ (default: annotation=Union[str, NoneType] required=False default=None alias='district' description='Filter by district' json_schema_extra={})
- `is_active` (typing.Optional[bool]) ○ (default: annotation=Union[bool, NoneType] required=False default=None alias='is_active' description='Filter by active status' json_schema_extra={})
- `page` (<class 'int'>) ○ (default: annotation=int required=False default=1 alias='page' description='Page number' json_schema_extra={} metadata=[Ge(ge=1)])
- `limit` (<class 'int'>) ○ (default: annotation=int required=False default=20 alias='limit' description='Number of results per page' json_schema_extra={} metadata=[Ge(ge=1), Le(le=100)])

---

#### GET /api/courts/regions

**Get all unique regions**

---

#### GET /api/courts/cities

**Get all unique cities, optionally filtered by region**

**Parameters:**

- `region` (typing.Optional[str]) ○ (default: annotation=Union[str, NoneType] required=False default=None alias='region' description='Filter cities by region' json_schema_extra={})

---

#### GET /api/courts/types

**Get all unique court types**

---

#### GET /api/courts/map

**Get courts for map display with optional proximity search**

**Parameters:**

- `court_type` (typing.Optional[schemas.court.CourtType]) ○ (default: annotation=Union[CourtType, NoneType] required=False default=None alias='court_type' description='Filter by court type' json_schema_extra={})
- `region` (typing.Optional[str]) ○ (default: annotation=Union[str, NoneType] required=False default=None alias='region' description='Filter by region' json_schema_extra={})
- `city` (typing.Optional[str]) ○ (default: annotation=Union[str, NoneType] required=False default=None alias='city' description='Filter by city' json_schema_extra={})
- `latitude` (typing.Optional[float]) ○ (default: annotation=Union[float, NoneType] required=False default=None alias='latitude' description='Latitude for proximity search' json_schema_extra={} metadata=[Ge(ge=-90), Le(le=90)])
- `longitude` (typing.Optional[float]) ○ (default: annotation=Union[float, NoneType] required=False default=None alias='longitude' description='Longitude for proximity search' json_schema_extra={} metadata=[Ge(ge=-180), Le(le=180)])
- `radius_km` (typing.Optional[float]) ○ (default: annotation=Union[float, NoneType] required=False default=None alias='radius_km' description='Search radius in kilometers' json_schema_extra={} metadata=[Gt(gt=0), Le(le=1000)])
- `is_active` (typing.Optional[bool]) ○ (default: annotation=Union[bool, NoneType] required=False default=True alias='is_active' description='Filter by active status' json_schema_extra={})

---

#### GET /api/courts/{court_id}

**Get a specific court by ID**

**Parameters:**

- `court_id` (<class 'int'>) ✓

---

#### POST /api/courts/

**Create a new court**

**Parameters:**

- `court` (<class 'schemas.court.CourtCreate'>) ✓

---

#### PUT /api/courts/{court_id}

**Update a court**

**Parameters:**

- `court_id` (<class 'int'>) ✓
- `court` (<class 'schemas.court.CourtUpdate'>) ✓

---

#### DELETE /api/courts/{court_id}

**Delete a court**

**Parameters:**

- `court_id` (<class 'int'>) ✓

---

### Ai-Chat

#### POST /api/ai-chat/sessions

**Create a new AI chat session for a case**

**Parameters:**

- `session_data` (<class 'schemas.ai_chat.ChatSessionCreate'>) ✓

---

#### POST /api/ai-chat/sessions

**Create a new AI chat session for a case**

**Parameters:**

- `session_data` (<class 'schemas.ai_chat.ChatSessionCreate'>) ✓

---

#### GET /api/ai-chat/sessions

**Get chat sessions with optional filtering**

**Parameters:**

- `case_id` (typing.Optional[int]) ○ (default: annotation=Union[int, NoneType] required=False default=None alias='case_id' description='Filter by case ID' json_schema_extra={})
- `user_id` (typing.Optional[int]) ○ (default: annotation=Union[int, NoneType] required=False default=None alias='user_id' description='Filter by user ID' json_schema_extra={})
- `page` (<class 'int'>) ○ (default: annotation=int required=False default=1 alias='page' description='Page number' json_schema_extra={} metadata=[Ge(ge=1)])
- `limit` (<class 'int'>) ○ (default: annotation=int required=False default=20 alias='limit' description='Items per page' json_schema_extra={} metadata=[Ge(ge=1), Le(le=100)])

---

#### GET /api/ai-chat/sessions

**Get chat sessions with optional filtering**

**Parameters:**

- `case_id` (typing.Optional[int]) ○ (default: annotation=Union[int, NoneType] required=False default=None alias='case_id' description='Filter by case ID' json_schema_extra={})
- `user_id` (typing.Optional[int]) ○ (default: annotation=Union[int, NoneType] required=False default=None alias='user_id' description='Filter by user ID' json_schema_extra={})
- `page` (<class 'int'>) ○ (default: annotation=int required=False default=1 alias='page' description='Page number' json_schema_extra={} metadata=[Ge(ge=1)])
- `limit` (<class 'int'>) ○ (default: annotation=int required=False default=20 alias='limit' description='Items per page' json_schema_extra={} metadata=[Ge(ge=1), Le(le=100)])

---

#### GET /api/ai-chat/sessions/{session_id}

**Get a specific chat session by ID**

**Parameters:**

- `session_id` (<class 'str'>) ✓

---

#### GET /api/ai-chat/sessions/{session_id}

**Get a specific chat session by ID**

**Parameters:**

- `session_id` (<class 'str'>) ✓

---

#### POST /api/ai-chat/sessions/{session_id}/messages

**Send a message to an AI chat session**

**Parameters:**

- `session_id` (<class 'str'>) ✓
- `message_data` (<class 'schemas.ai_chat.ChatMessageRequest'>) ✓

---

#### POST /api/ai-chat/sessions/{session_id}/messages

**Send a message to an AI chat session**

**Parameters:**

- `session_id` (<class 'str'>) ✓
- `message_data` (<class 'schemas.ai_chat.ChatMessageRequest'>) ✓

---

#### POST /api/ai-chat/sessions/{case_id}/start

**Start a new chat session and send the first message**

**Parameters:**

- `case_id` (<class 'int'>) ✓
- `message_data` (<class 'schemas.ai_chat.ChatMessageRequest'>) ✓

---

#### POST /api/ai-chat/sessions/{case_id}/start

**Start a new chat session and send the first message**

**Parameters:**

- `case_id` (<class 'int'>) ✓
- `message_data` (<class 'schemas.ai_chat.ChatMessageRequest'>) ✓

---

#### POST /api/ai-chat/case-summary

**Generate a comprehensive AI summary of a case**

**Parameters:**

- `summary_data` (<class 'schemas.ai_chat.CaseSummaryRequest'>) ✓

---

#### POST /api/ai-chat/case-summary

**Generate a comprehensive AI summary of a case**

**Parameters:**

- `summary_data` (<class 'schemas.ai_chat.CaseSummaryRequest'>) ✓

---

#### DELETE /api/ai-chat/sessions/{session_id}

**Delete a chat session (soft delete)**

**Parameters:**

- `session_id` (<class 'str'>) ✓

---

#### DELETE /api/ai-chat/sessions/{session_id}

**Delete a chat session (soft delete)**

**Parameters:**

- `session_id` (<class 'str'>) ✓

---

#### GET /api/ai-chat/analytics/usage

**Get AI chat usage analytics for reporting**

**Parameters:**

- `days` (<class 'int'>) ○ (default: annotation=int required=False default=30 alias='days' description='Number of days to analyze' json_schema_extra={} metadata=[Ge(ge=1), Le(le=365)])

---

#### GET /api/ai-chat/analytics/usage

**Get AI chat usage analytics for reporting**

**Parameters:**

- `days` (<class 'int'>) ○ (default: annotation=int required=False default=30 alias='days' description='Number of days to analyze' json_schema_extra={} metadata=[Ge(ge=1), Le(le=365)])

---

#### GET /api/ai-chat/analytics/session/{session_id}

**Get detailed analytics for a specific chat session**

**Parameters:**

- `session_id` (<class 'str'>) ✓

---

#### GET /api/ai-chat/analytics/session/{session_id}

**Get detailed analytics for a specific chat session**

**Parameters:**

- `session_id` (<class 'str'>) ✓

---

#### GET /api/ai-chat/analytics/users

**Get user-specific AI chat analytics and token usage for billing**

**Parameters:**

- `days` (<class 'int'>) ○ (default: annotation=int required=False default=30 alias='days' description='Number of days to analyze' json_schema_extra={} metadata=[Ge(ge=1), Le(le=365)])

---

#### GET /api/ai-chat/analytics/users

**Get user-specific AI chat analytics and token usage for billing**

**Parameters:**

- `days` (<class 'int'>) ○ (default: annotation=int required=False default=30 alias='days' description='Number of days to analyze' json_schema_extra={} metadata=[Ge(ge=1), Le(le=365)])

---

