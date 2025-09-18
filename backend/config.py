from pydantic_settings import BaseSettings
from typing import Optional
import os

class Settings(BaseSettings):
    # Database Configuration
    render_database_url: Optional[str] = None
    mysql_host: str = "localhost"
    mysql_port: int = 3306
    mysql_user: str = "root"
    mysql_password: str = "Hausawi@2025"
    mysql_database: str = "dennislaw_svd"
    
    # JWT Configuration
    secret_key: str = "your-secret-key-change-this-in-production"
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 30
    
    # CORS Configuration
    cors_origins: list = [
        "http://localhost:3000", 
        "https://case-search-frontend.ondigitalocean.app",
        "https://your-domain.com"
    ]
    
    # Google OAuth
    google_client_id: Optional[str] = None
    google_client_secret: Optional[str] = None
    
    # Email Configuration
    mail_username: Optional[str] = None
    mail_password: Optional[str] = None
    mail_from: Optional[str] = None
    mail_port: int = 587
    mail_server: str = "smtp.gmail.com"
    mail_tls: bool = True
    mail_ssl: bool = False
    
    # OpenAI Configuration
    openai_api_key: Optional[str] = None
    
    # Google Maps Configuration
    react_app_google_maps_api_key: Optional[str] = None
    
    # Application Configuration
    debug: bool = True
    host: str = "0.0.0.0"
    port: int = 8000
    
    @property
    def database_url(self) -> str:
        if self.render_database_url:
            return self.render_database_url
        from urllib.parse import quote_plus
        password = quote_plus(self.mysql_password)
        return f"mysql+pymysql://{self.mysql_user}:{password}@{self.mysql_host}:{self.mysql_port}/{self.mysql_database}"
    
    class Config:
        env_file = ".env"
        case_sensitive = False

# Create settings instance
settings = Settings()
