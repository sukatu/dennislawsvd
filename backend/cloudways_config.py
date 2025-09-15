#!/usr/bin/env python3
"""
Cloudways-specific configuration for DennisLaw SVD Backend
Update these settings for your Cloudways deployment
"""

import os

class CloudwaysSettings:
    # Database Configuration
    # Get these from Cloudways Dashboard > Application Management > Database
    DATABASE_HOST = "localhost"  # Usually localhost on Cloudways
    DATABASE_PORT = 3306
    DATABASE_NAME = "your_database_name"  # Update this
    DATABASE_USER = "your_database_user"  # Update this
    DATABASE_PASSWORD = "your_database_password"  # Update this
    
    # Construct database URL
    DATABASE_URL = f"mysql+pymysql://{DATABASE_USER}:{DATABASE_PASSWORD}@{DATABASE_HOST}:{DATABASE_PORT}/{DATABASE_NAME}"
    
    # API Configuration
    API_HOST = "0.0.0.0"  # Listen on all interfaces
    API_PORT = 8000
    DEBUG = False  # Set to False for production
    
    # CORS Settings
    # Update these with your actual domain
    ALLOWED_ORIGINS = [
        "https://yourdomain.com",
        "https://www.yourdomain.com",
        "https://api.yourdomain.com",
        "http://localhost:3000",  # For development
    ]
    
    # Security Settings
    SECRET_KEY = "your-secret-key-here"  # Generate a strong secret key
    ACCESS_TOKEN_EXPIRE_MINUTES = 30
    
    # File Upload Settings
    MAX_FILE_SIZE = 10 * 1024 * 1024  # 10MB
    UPLOAD_FOLDER = "/home/master/applications/your-app/backend/uploads"
    
    # Logging Configuration
    LOG_LEVEL = "INFO"
    LOG_FILE = "/home/master/applications/your-app/backend/logs/app.log"
    
    # Email Configuration (if needed)
    SMTP_HOST = "smtp.gmail.com"
    SMTP_PORT = 587
    SMTP_USERNAME = "your-email@gmail.com"
    SMTP_PASSWORD = "your-app-password"
    
    # Redis Configuration (if available)
    REDIS_HOST = "localhost"
    REDIS_PORT = 6379
    REDIS_DB = 0
    
    @classmethod
    def get_database_url(cls):
        """Get the database URL for SQLAlchemy"""
        return cls.DATABASE_URL
    
    @classmethod
    def get_cors_origins(cls):
        """Get CORS allowed origins"""
        return cls.ALLOWED_ORIGINS
    
    @classmethod
    def is_production(cls):
        """Check if running in production"""
        return not cls.DEBUG

# Example usage in your main.py:
# from cloudways_config import CloudwaysSettings
# 
# # Update your existing config.py or main.py to use these settings
# database_url = CloudwaysSettings.get_database_url()
# cors_origins = CloudwaysSettings.get_cors_origins()
