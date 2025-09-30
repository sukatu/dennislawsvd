# Juridence Legal Database System - System Overview

## Table of Contents
1. [System Architecture](#system-architecture)
2. [Database Schema](#database-schema)
3. [API Structure](#api-structure)
4. [Frontend Components](#frontend-components)
5. [Authentication & Security](#authentication--security)
6. [AI Integration](#ai-integration)
7. [Employee Management System](#employee-management-system)
8. [File Repository System](#file-repository-system)
9. [Analytics & Reporting](#analytics--reporting)
10. [Deployment Architecture](#deployment-architecture)
11. [Performance Metrics](#performance-metrics)
12. [Monitoring & Logging](#monitoring--logging)

## System Architecture

### High-Level Architecture

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Frontend      │    │   Backend       │    │   Database      │
│   (React.js)    │◄──►│   (FastAPI)     │◄──►│   (PostgreSQL)  │
└─────────────────┘    └─────────────────┘    └─────────────────┘
         │                       │                       │
         │                       │                       │
         ▼                       ▼                       ▼
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   CDN/Static    │    │   AI Service    │    │   File Storage  │
│   Assets        │    │   (OpenAI)      │    │   (Local/Cloud) │
└─────────────────┘    └─────────────────┘    └─────────────────┘
```

### Technology Stack

#### Frontend
- **Framework**: React.js 18+
- **Routing**: React Router v6
- **State Management**: React Context API
- **Styling**: Tailwind CSS
- **Charts**: Chart.js with React-Chartjs-2
- **Icons**: Lucide React
- **HTTP Client**: Fetch API

#### Backend
- **Framework**: FastAPI (Python 3.9+)
- **ASGI Server**: Uvicorn
- **ORM**: SQLAlchemy
- **Database**: PostgreSQL 13+
- **Authentication**: JWT + API Keys
- **Validation**: Pydantic
- **AI Integration**: OpenAI GPT-4

#### Infrastructure
- **Web Server**: Nginx (production)
- **Process Manager**: PM2 (Node.js)
- **Database**: PostgreSQL with connection pooling
- **File Storage**: Local filesystem (configurable for cloud)
- **Monitoring**: Built-in logging and analytics

## Database Schema

### Core Entities

#### 1. Users & Authentication
```sql
-- Users table
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    email VARCHAR(255) UNIQUE NOT NULL,
    hashed_password VARCHAR(255) NOT NULL,
    first_name VARCHAR(100),
    last_name VARCHAR(100),
    role VARCHAR(50) DEFAULT 'user',
    is_admin BOOLEAN DEFAULT FALSE,
    is_verified BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- API Keys table
CREATE TABLE api_keys (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users(id),
    key_name VARCHAR(255) NOT NULL,
    key_hash VARCHAR(255) UNIQUE NOT NULL,
    permissions JSONB DEFAULT '["read"]',
    is_active BOOLEAN DEFAULT TRUE,
    expires_at TIMESTAMP,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

#### 2. Legal Cases
```sql
-- Cases table
CREATE TABLE cases (
    id SERIAL PRIMARY KEY,
    title TEXT NOT NULL,
    suit_reference_number VARCHAR(255),
    date DATE,
    presiding_judge TEXT,
    court_type VARCHAR(50),
    area_of_law VARCHAR(100),
    status VARCHAR(50),
    protagonist TEXT,
    antagonist TEXT,
    case_summary TEXT,
    judges JSONB,
    lawyers JSONB,
    related_people JSONB,
    organizations JSONB,
    banks_involved JSONB,
    insurance_involved JSONB,
    statutes_cited JSONB,
    cases_cited JSONB,
    resolution_status VARCHAR(50),
    outcome VARCHAR(50),
    decision_type VARCHAR(50),
    monetary_amount DECIMAL(15,2),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

#### 3. People
```sql
-- People table
CREATE TABLE people (
    id SERIAL PRIMARY KEY,
    first_name VARCHAR(100),
    last_name VARCHAR(100),
    full_name VARCHAR(200),
    date_of_birth DATE,
    phone_number VARCHAR(20),
    email VARCHAR(255),
    address TEXT,
    city VARCHAR(100),
    region VARCHAR(50),
    country VARCHAR(100),
    occupation VARCHAR(100),
    employer VARCHAR(255),
    organization VARCHAR(255),
    risk_level VARCHAR(20),
    risk_score DECIMAL(5,2),
    case_count INTEGER DEFAULT 0,
    case_types JSONB,
    court_records JSONB,
    is_verified BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

#### 4. Banks
```sql
-- Banks table
CREATE TABLE banks (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    short_name VARCHAR(100),
    bank_code VARCHAR(20) UNIQUE,
    license_number VARCHAR(50),
    established_date DATE,
    bank_type VARCHAR(50),
    ownership_type VARCHAR(50),
    services JSONB,
    previous_names JSONB,
    branches_count INTEGER DEFAULT 0,
    total_assets DECIMAL(20,2),
    net_worth DECIMAL(20,2),
    rating VARCHAR(10),
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

#### 5. Companies
```sql
-- Companies table
CREATE TABLE companies (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    short_name VARCHAR(100),
    registration_number VARCHAR(50) UNIQUE,
    type_of_company VARCHAR(100),
    nature_of_business TEXT,
    date_of_incorporation DATE,
    directors JSONB,
    secretary JSONB,
    auditor JSONB,
    shareholders JSONB,
    authorized_shares BIGINT,
    stated_capital DECIMAL(20,2),
    business_activities JSONB,
    previous_names JSONB,
    board_of_directors JSONB,
    key_personnel JSONB,
    subsidiaries JSONB,
    annual_revenue DECIMAL(20,2),
    net_worth DECIMAL(20,2),
    employee_count INTEGER,
    rating VARCHAR(10),
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

#### 6. Insurance Companies
```sql
-- Insurance table
CREATE TABLE insurance (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    short_name VARCHAR(100),
    license_number VARCHAR(50) UNIQUE,
    registration_number VARCHAR(50),
    established_date DATE,
    insurance_type VARCHAR(100),
    ownership_type VARCHAR(50),
    services JSONB,
    previous_names JSONB,
    coverage_areas JSONB,
    branches_count INTEGER DEFAULT 0,
    agents_count INTEGER DEFAULT 0,
    total_assets DECIMAL(20,2),
    net_worth DECIMAL(20,2),
    premium_income DECIMAL(20,2),
    claims_paid DECIMAL(20,2),
    rating VARCHAR(10),
    specializes_in JSONB,
    target_market VARCHAR(100),
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

### Analytics & Tracking Tables

#### Usage Tracking
```sql
-- Usage tracking table
CREATE TABLE usage_tracking (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users(id),
    session_id VARCHAR(255),
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    resource_type VARCHAR(50),
    resource_id INTEGER,
    endpoint VARCHAR(255),
    query TEXT,
    tokens_used INTEGER DEFAULT 0,
    cost_estimate DECIMAL(10,4) DEFAULT 0,
    response_time_ms INTEGER,
    metadata JSONB
);

-- AI Chat Sessions
CREATE TABLE ai_chat_sessions (
    id SERIAL PRIMARY KEY,
    session_id VARCHAR(255) UNIQUE NOT NULL,
    case_id INTEGER REFERENCES cases(id),
    user_id INTEGER REFERENCES users(id),
    title VARCHAR(255),
    messages JSONB,
    total_messages INTEGER DEFAULT 0,
    is_active BOOLEAN DEFAULT TRUE,
    ai_model_used VARCHAR(50),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

## API Structure

### API Organization

```
/api/
├── auth/                    # Authentication endpoints
│   ├── login
│   ├── register
│   ├── refresh
│   └── me
├── search/                  # Search endpoints
│   ├── unified
│   └── quick
├── cases/                   # Case management
│   ├── search
│   ├── {id}
│   └── {id}/related
├── people/                  # People management
│   ├── search
│   ├── {id}
│   └── {id}/analytics
├── banks/                   # Bank management
│   ├── search
│   ├── {id}
│   ├── POST /
│   ├── PUT /{id}
│   └── DELETE /{id}
├── companies/               # Company management
│   ├── search
│   ├── {id}
│   ├── POST /
│   ├── PUT /{id}
│   └── DELETE /{id}
├── insurance/               # Insurance management
│   ├── search
│   ├── {id}
│   ├── POST /
│   ├── PUT /{id}
│   └── DELETE /{id}
├── ai-chat/                 # AI integration
│   ├── message
│   ├── case-summary
│   ├── sessions/{id}
│   └── analytics
├── admin/                   # Admin endpoints
│   ├── stats
│   ├── users
│   ├── api-keys
│   └── logs
└── profile/                 # User profile
    ├── me
    ├── change-password
    └── upload-avatar
```

### API Response Format

#### Success Response
```json
{
  "results": [...],
  "total": 100,
  "page": 1,
  "limit": 20,
  "total_pages": 5,
  "has_next": true,
  "has_prev": false,
  "search_time_ms": 45.2
}
```

#### Error Response
```json
{
  "detail": "Error message",
  "error_code": "ERROR_CODE",
  "timestamp": "2025-09-28T15:30:00Z",
  "request_id": "req_123456789"
}
```

## Frontend Components

### Component Architecture

```
src/
├── components/
│   ├── admin/               # Admin dashboard components
│   │   ├── UserManagement.js
│   │   ├── ApiKeyManagement.js
│   │   ├── CaseManagement.js
│   │   ├── BankManagement.js
│   │   ├── CompanyManagement.js
│   │   ├── InsuranceManagement.js
│   │   ├── AIAnalytics.js
│   │   └── Documentation.js
│   ├── common/              # Shared components
│   │   ├── Header.js
│   │   ├── Sidebar.js
│   │   ├── SearchBar.js
│   │   └── Toast.js
│   └── ui/                  # UI components
│       ├── Button.js
│       ├── Modal.js
│       ├── Table.js
│       └── Chart.js
├── pages/                   # Page components
│   ├── Home.js
│   ├── SearchResults.js
│   ├── CaseDetails.js
│   ├── PersonProfile.js
│   ├── BankDetail.js
│   ├── CompanyProfile.js
│   ├── InsuranceProfile.js
│   ├── AdminDashboard.js
│   └── Settings.js
├── contexts/                # React contexts
│   ├── AuthContext.js
│   └── ThemeContext.js
├── hooks/                   # Custom hooks
│   ├── useAuth.js
│   └── useApi.js
└── utils/                   # Utility functions
    ├── api.js
    ├── auth.js
    └── helpers.js
```

### State Management

#### Context Providers
- **AuthContext**: User authentication state
- **ThemeContext**: UI theme and preferences
- **ToastContext**: Notification system

#### Custom Hooks
- **useAuth**: Authentication operations
- **useApi**: API request handling
- **useToast**: Notification management

## Authentication & Security

### Authentication Methods

#### 1. JWT Tokens
- **Access Token**: Short-lived (1 hour)
- **Refresh Token**: Long-lived (7 days)
- **Algorithm**: HS256
- **Storage**: HTTP-only cookies (preferred) or localStorage

#### 2. API Keys
- **Format**: `jrd_` + 32 random characters
- **Hashing**: SHA-256
- **Storage**: Database with salt
- **Permissions**: Read, Write, Admin

### Security Features

#### 1. Password Security
- **Hashing**: bcrypt with salt rounds 12
- **Requirements**: Minimum 8 characters
- **Validation**: Server-side validation

#### 2. API Security
- **Rate Limiting**: Per API key and IP
- **CORS**: Configured for specific origins
- **Input Validation**: Pydantic models
- **SQL Injection**: SQLAlchemy ORM protection

#### 3. Data Protection
- **Encryption**: HTTPS in production
- **Sensitive Data**: Encrypted at rest
- **Audit Logs**: All operations logged
- **Access Control**: Role-based permissions

## AI Integration

### OpenAI Integration

#### Models Used
- **GPT-4**: Primary model for complex analysis
- **GPT-3.5-turbo**: Fallback for simple queries
- **Model Selection**: Dynamic based on query complexity

#### AI Features

##### 1. Case Analysis
```python
# Case summary generation
def generate_case_summary(case_id: int, user_id: int):
    case = get_case_details(case_id)
    prompt = build_case_prompt(case)
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[{"role": "user", "content": prompt}],
        max_tokens=600
    )
    return response.choices[0].message.content
```

##### 2. Legal Chat
```python
# AI chat for case discussion
def generate_ai_response(message: str, case_id: int, session_id: str):
    context = get_case_context(case_id)
    prompt = build_chat_prompt(message, context)
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[{"role": "user", "content": prompt}],
        max_tokens=800
    )
    return response.choices[0].message.content
```

#### AI Analytics
- **Token Usage**: Tracked per user and session
- **Cost Estimation**: Real-time cost calculation
- **Usage Patterns**: Analytics for optimization
- **Model Performance**: Response time and quality metrics

## Employee Management System

### Overview
The Employee Management System provides LinkedIn-style employee profiles with comprehensive tracking of employment history, skills, education, and legal cases.

### Key Features

#### Employee Profiles
- **Personal Information**: Name, contact details, demographics
- **Professional Data**: Job title, department, employment status
- **Employment History**: Dynamic tracking of career progression
- **Education History**: Academic qualifications and certifications
- **Skills & Languages**: Comprehensive skill tracking
- **CV Management**: File upload and storage system
- **Legal Cases**: Associated legal proceedings

#### Data Synchronization
- **Automatic People Sync**: Employees automatically added to people database
- **Real-time Updates**: Changes sync immediately across systems
- **Data Integrity**: 100% synchronization rate maintained
- **Bidirectional Updates**: Changes in either system reflect in both

#### File Management
- **CV Upload**: Support for PDF, DOC, DOCX, TXT files
- **File Validation**: Size and type restrictions
- **Secure Storage**: Organized file structure with unique naming
- **Download Access**: Secure file retrieval system

### Database Schema

#### Employee Table
```sql
CREATE TABLE employees (
    id SERIAL PRIMARY KEY,
    first_name VARCHAR(100) NOT NULL,
    last_name VARCHAR(100) NOT NULL,
    email VARCHAR(255) UNIQUE,
    job_title VARCHAR(200),
    current_employer_name VARCHAR(200),
    current_employer_type VARCHAR(20),
    employment_status VARCHAR(20) DEFAULT 'active',
    employee_type VARCHAR(20) DEFAULT 'full_time',
    skills JSON,
    languages JSON,
    cv_file VARCHAR(500),
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);
```

#### Employment History Table
```sql
CREATE TABLE employment_history (
    id SERIAL PRIMARY KEY,
    employee_id INTEGER REFERENCES employees(id),
    company_name VARCHAR(200) NOT NULL,
    job_title VARCHAR(200),
    start_date DATE,
    end_date DATE,
    description TEXT,
    created_at TIMESTAMP DEFAULT NOW()
);
```

### API Endpoints

#### Employee Management
- `GET /api/employees/` - List employees with pagination
- `POST /api/employees/` - Create new employee
- `GET /api/employees/{id}` - Get employee details
- `PUT /api/employees/{id}` - Update employee
- `DELETE /api/employees/{id}` - Delete employee

#### File Management
- `POST /api/employees/{id}/upload-cv` - Upload CV file
- `GET /api/files/download-cv/{filename}` - Download CV file
- `DELETE /api/files/{filename}` - Delete file

#### Analytics
- `GET /api/employees/analytics/overview` - Employee statistics
- `GET /api/employees/analytics/employer/{type}/{name}` - Employer-specific analytics

## File Repository System

### Overview
The File Repository System provides comprehensive file management capabilities for the entire application, including upload, download, organization, and analytics.

### Key Features

#### File Management
- **Multi-format Support**: PDF, DOC, DOCX, TXT, images
- **Organized Storage**: Folder-based file organization
- **File Validation**: Size and type restrictions
- **Secure Access**: Authentication-based file access
- **Metadata Tracking**: File information and usage analytics

#### Repository Structure
```
uploads/
├── cvs/                    # Employee CV files
├── cases/                  # Legal case documents
├── avatars/               # User profile pictures
└── general/               # General file uploads
```

#### File Operations
- **Upload**: Drag-and-drop or click-to-upload interface
- **Download**: Secure file retrieval with proper headers
- **Delete**: Safe file removal with confirmation
- **Organize**: Folder creation and file organization
- **Search**: File search by name, type, and metadata

### API Endpoints

#### File Operations
- `POST /api/files/upload` - Upload file
- `GET /api/files/download/{filename}` - Download file
- `DELETE /api/files/{filename}` - Delete file
- `GET /api/files/list` - List files with pagination
- `POST /api/files/create-folder` - Create folder

#### Repository Management
- `GET /api/file-repository/` - Get repository structure
- `GET /api/file-repository/folder/{path}` - Get folder contents
- `POST /api/file-repository/folder` - Create new folder
- `DELETE /api/file-repository/folder/{path}` - Delete folder

### Frontend Components

#### File Repository Interface
- **Folder Navigation**: Tree-like folder structure
- **File Grid**: Visual file display with thumbnails
- **Upload Interface**: Drag-and-drop file upload
- **Search & Filter**: File search and filtering capabilities
- **Bulk Operations**: Multi-file selection and operations

## Analytics & Reporting

### Analytics Categories

#### 1. User Analytics
- **Active Users**: Daily, weekly, monthly
- **Usage Patterns**: Peak hours, popular features
- **Geographic Distribution**: User locations
- **Device Types**: Desktop, mobile, tablet

#### 2. Search Analytics
- **Popular Queries**: Most searched terms
- **Search Success Rate**: Query to result ratio
- **Response Times**: Average search performance
- **Filter Usage**: Most used search filters

#### 3. Content Analytics
- **Entity Popularity**: Most viewed cases, people, companies
- **Content Performance**: Engagement metrics
- **Data Quality**: Completeness and accuracy
- **Update Frequency**: Content freshness

#### 4. AI Analytics
- **Token Usage**: Per user and system-wide
- **Cost Analysis**: AI usage costs
- **Model Performance**: Response quality and speed
- **User Satisfaction**: AI interaction feedback

### Reporting Features

#### 1. Real-time Dashboards
- **Admin Dashboard**: System overview and metrics
- **User Dashboard**: Personal usage statistics
- **AI Analytics**: AI usage and performance
- **Financial Reports**: Cost and billing analysis

#### 2. Scheduled Reports
- **Daily Reports**: System health and usage
- **Weekly Reports**: User engagement and trends
- **Monthly Reports**: Comprehensive analytics
- **Custom Reports**: Configurable reporting

## Deployment Architecture

### Production Environment

#### 1. Web Server (Nginx)
```nginx
server {
    listen 80;
    server_name api.juridence.com;
    
    location / {
        proxy_pass http://localhost:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
    
    location /static/ {
        alias /var/www/static/;
        expires 1y;
    }
}
```

#### 2. Application Server
- **Backend**: Uvicorn with multiple workers
- **Frontend**: React build served by Nginx
- **Process Management**: PM2 for Node.js processes
- **Load Balancing**: Nginx upstream configuration

#### 3. Database
- **PostgreSQL**: Primary database
- **Connection Pooling**: SQLAlchemy pool configuration
- **Backup Strategy**: Daily automated backups
- **Monitoring**: Query performance tracking

### Development Environment

#### 1. Local Development
```bash
# Backend
cd backend
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
uvicorn main:app --reload

# Frontend
cd frontend
npm install
npm start
```

#### 2. Docker Development
```dockerfile
# Backend Dockerfile
FROM python:3.9-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
```

## Performance Metrics

### System Performance

#### 1. Response Times
- **API Endpoints**: < 200ms average
- **Search Queries**: < 100ms average
- **Database Queries**: < 50ms average
- **AI Responses**: < 5s average

#### 2. Throughput
- **Concurrent Users**: 100+ supported
- **Requests per Second**: 50+ RPS
- **Database Connections**: 20 max pool size
- **Memory Usage**: < 2GB per instance

#### 3. Scalability
- **Horizontal Scaling**: Multiple app instances
- **Database Scaling**: Read replicas support
- **Caching**: Redis integration ready
- **CDN**: Static asset optimization

### Optimization Strategies

#### 1. Database Optimization
- **Indexing**: Strategic indexes on search fields
- **Query Optimization**: Efficient SQL queries
- **Connection Pooling**: Reuse database connections
- **Caching**: Query result caching

#### 2. API Optimization
- **Pagination**: Limit result sets
- **Filtering**: Reduce data transfer
- **Compression**: Gzip compression
- **Rate Limiting**: Prevent abuse

#### 3. Frontend Optimization
- **Code Splitting**: Lazy load components
- **Bundle Optimization**: Minimize bundle size
- **Image Optimization**: Compress and lazy load
- **Caching**: Browser caching strategies

## Monitoring & Logging

### Logging System

#### 1. Application Logs
```python
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('app.log'),
        logging.StreamHandler()
    ]
)
```

#### 2. Log Categories
- **Access Logs**: HTTP requests and responses
- **Error Logs**: Application errors and exceptions
- **Security Logs**: Authentication and authorization
- **Performance Logs**: Response times and metrics
- **AI Logs**: AI usage and costs

#### 3. Log Management
- **Log Rotation**: Daily log file rotation
- **Log Aggregation**: Centralized log collection
- **Log Analysis**: Automated log analysis
- **Alerting**: Error and performance alerts

### Monitoring Tools

#### 1. System Monitoring
- **CPU Usage**: Real-time CPU monitoring
- **Memory Usage**: Memory consumption tracking
- **Disk Usage**: Storage space monitoring
- **Network Usage**: Network traffic analysis

#### 2. Application Monitoring
- **Response Times**: API endpoint performance
- **Error Rates**: Error frequency tracking
- **User Activity**: User behavior analytics
- **Database Performance**: Query performance

#### 3. Business Metrics
- **User Growth**: User registration trends
- **Usage Patterns**: Feature usage analytics
- **Revenue Metrics**: Subscription and billing
- **Content Metrics**: Data quality and completeness

---

**System Version**: 1.0.0  
**Last Updated**: September 28, 2025  
**Documentation Version**: 1.0.0
