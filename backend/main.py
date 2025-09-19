from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles
# from middleware.logging_middleware import LoggingMiddleware
from contextlib import asynccontextmanager
import uvicorn

from database import create_tables
from routes import auth
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
from routes import tenant
from routes import courts
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
app.include_router(tenant.router, prefix="/api/tenant", tags=["tenant"])
app.include_router(courts.router, prefix="/api/courts", tags=["courts"])

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
