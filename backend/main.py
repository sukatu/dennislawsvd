from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles
# from middleware.logging_middleware import LoggingMiddleware
from contextlib import asynccontextmanager
import uvicorn

from database import create_tables
from routes import auth
from auth import get_current_user
from models.user import User
from routes import profile
from routes import people
from routes import banks
from routes import insurance
from routes import companies
from routes import search
from routes import reported_cases
from routes import legal_history
from routes import case_search
from routes import enhanced_search
from routes import case_hearings
from routes import person_case_statistics
from routes import person_analytics
from routes import banking_summary
from routes import request_details
from routes import subscription
from routes import notifications
from routes import security
from routes import admin
from routes import admin_payments
from routes import admin_case_hearings
from routes import judges
from routes import court_types
from routes import tenant
from routes import courts
from routes import ai_chat
from routes import employees
from routes import file_upload
from routes import file_repository
from config import settings

# Application lifespan
@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    print("Starting juridence Backend...")
    create_tables()
    print("Database tables created successfully")
    yield
    # Shutdown
    print("Shutting down juridence Backend...")

# Create FastAPI app
app = FastAPI(
    title="juridence API",
    description="Backend API for juridence Services - Court Search, Document Verification & Document Request",
    version="1.0.0",
    lifespan=lifespan
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,  # Use settings for CORS origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Logging middleware
# app.add_middleware(LoggingMiddleware)

# Temporarily override authentication for testing - using real database user
async def get_real_admin_user():
    """Get real admin user from database - bypasses authentication"""
    from database import get_db
    from datetime import datetime
    
    db = next(get_db())
    # Get the real admin user from database
    admin_user = db.query(User).filter(User.email == "admin@juridence.com").first()
    if not admin_user:
        db.close()
        raise HTTPException(status_code=404, detail="Admin user not found")
    
    # Update last login without committing (let the profile endpoint handle commits)
    admin_user.last_login = datetime.utcnow()
    
    # Don't close the session here - let the endpoint handle it
    return admin_user

app.dependency_overrides[get_current_user] = get_real_admin_user

# Mount static files
app.mount("/uploads", StaticFiles(directory="uploads"), name="uploads")

# Include routers
app.include_router(auth.router)
app.include_router(profile.router, prefix="/api", tags=["profile"])
app.include_router(people.router, prefix="/api/people", tags=["people"])
app.include_router(banks.router, prefix="/api/banks", tags=["banks"])
app.include_router(insurance.router, prefix="/api/insurance", tags=["insurance"])
app.include_router(companies.router, prefix="/api/companies", tags=["companies"])
app.include_router(search.router, prefix="/api/search", tags=["search"])
app.include_router(reported_cases.router, prefix="/api/cases", tags=["reported_cases"])
app.include_router(legal_history.router, prefix="/api/legal-history", tags=["legal_history"])
app.include_router(case_search.router, prefix="/api/case-search", tags=["case_search"])
app.include_router(enhanced_search.router, prefix="/api/enhanced-search", tags=["enhanced_search"])
app.include_router(case_hearings.router, prefix="/api", tags=["case_hearings"])
app.include_router(person_case_statistics.router, tags=["person_case_statistics"])
app.include_router(person_analytics.router, prefix="/api", tags=["person_analytics"])
app.include_router(banking_summary.router, tags=["banking_summary"])
app.include_router(request_details.router, tags=["request_details"])
app.include_router(subscription.router, prefix="/api/subscription", tags=["subscription"])
app.include_router(notifications.router, prefix="/api/notifications", tags=["notifications"])
app.include_router(security.router, prefix="/api/security", tags=["security"])
app.include_router(admin.router, tags=["admin"])
app.include_router(admin_payments.router, prefix="/api/admin/payments", tags=["admin_payments"])
app.include_router(admin_case_hearings.router, prefix="/api", tags=["admin_case_hearings"])
app.include_router(judges.router, prefix="/api", tags=["judges"])
app.include_router(court_types.router, prefix="/api", tags=["court_types"])
app.include_router(tenant.router, prefix="/api/tenant", tags=["tenant"])
app.include_router(courts.router, prefix="/api/courts", tags=["courts"])
app.include_router(ai_chat.router, prefix="/api", tags=["ai-chat"])
app.include_router(employees.router, tags=["employees"])
app.include_router(file_upload.router, prefix="/api/files", tags=["file_upload"])
app.include_router(file_repository.router, tags=["file-repository"])

# Root endpoint
@app.get("/")
async def root():
    return {
        "message": "Welcome to juridence API",
        "version": "1.0.0",
        "docs": "/docs",
        "status": "running"
    }

# Health check endpoint
@app.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "service": "juridence-api",
        "version": "1.0.0"
    }

# Global exception handler
@app.exception_handler(Exception)
async def global_exception_handler(request, exc):
    return JSONResponse(
        status_code=500,
        content={
            "message": "Internal server error",
            "detail": str(exc) if settings.debug else "An error occurred"
        }
    )

if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host=settings.host,
        port=settings.port,
        reload=settings.debug
    )
