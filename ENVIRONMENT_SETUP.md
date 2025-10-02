# Environment Setup Guide

## Local Development

Create a `.env` file in the root directory and `backend/.env` file with your local credentials:

### Root `.env`:
```
REACT_APP_API_URL=http://localhost:8000
```

### Backend `.env`:
```
# Database Configuration
DATABASE_URL=postgresql://your_local_user:your_local_password@localhost:5432/your_local_db

# JWT Configuration
SECRET_KEY=your-local-secret-key
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

# CORS Configuration
CORS_ORIGINS=["http://localhost:3000"]

# Application Configuration
PROJECT_NAME=Juridence Legal Search Platform
VERSION=1.0.0
DESCRIPTION=Advanced legal case search and analytics platform

# Server Configuration
HOST=0.0.0.0
PORT=8000
DEBUG=True

# Security Configuration
BCRYPT_ROUNDS=12
JWT_SECRET_KEY=your-local-jwt-secret-key

# Admin Configuration
ADMIN_EMAIL=admin@juridence.com
ADMIN_PASSWORD=admin123
```

## Server Production

The server uses different credentials and is configured separately. The server `.env` file should contain:

```
# Database Configuration
DATABASE_URL=postgresql://juridence_user:juridence_password123@localhost:5432/juridence_db

# JWT Configuration
SECRET_KEY=your-server-secret-key
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

# CORS Configuration
CORS_ORIGINS=["http://localhost:3000", "http://62.171.137.28", "http://62.171.137.28:3000"]

# Application Configuration
PROJECT_NAME=Juridence Legal Search Platform
VERSION=1.0.0
DESCRIPTION=Advanced legal case search and analytics platform

# Server Configuration
HOST=0.0.0.0
PORT=8000
DEBUG=True

# Security Configuration
BCRYPT_ROUNDS=12
JWT_SECRET_KEY=your-server-jwt-secret-key

# Admin Configuration
ADMIN_EMAIL=admin@juridence.com
ADMIN_PASSWORD=admin123
```

## Important Notes

- **NEVER commit `.env` files to the repository**
- Each environment (local, staging, production) should have its own `.env` file
- The `.gitignore` file is configured to exclude all `.env` files
- Use strong, unique secrets for production environments
