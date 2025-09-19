# Local Development Setup

## 1. Install PostgreSQL

Make sure PostgreSQL is installed and running locally:
- **Port**: 5432
- **Username**: postgres
- **Password**: 62579011
- **Database**: juridence

## 2. Create Database

Connect to PostgreSQL and create the database:

```sql
CREATE DATABASE juridence;
```

## 3. Environment Variables

Create a `.env` file in the backend directory with:

```env
# Database Configuration
POSTGRES_HOST=localhost
POSTGRES_PORT=5432
POSTGRES_USER=postgres
POSTGRES_PASSWORD=62579011
POSTGRES_DATABASE=juridence

# JWT Configuration
SECRET_KEY=your-local-development-secret-key
ACCESS_TOKEN_EXPIRE_MINUTES=30

# CORS Configuration
CORS_ORIGINS=["http://localhost:3000"]

# Application Configuration
DEBUG=true
ENVIRONMENT=development
```

## 4. Install Dependencies

```bash
cd backend
pip install -r requirements.txt
```

## 5. Run Backend

```bash
cd backend
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

## 6. Run Frontend

```bash
npm install
npm start
```

Your application should now be running locally with PostgreSQL!
