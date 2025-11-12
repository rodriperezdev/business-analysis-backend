"""
Configuration management for the Business Analytics API.
Handles environment variables, settings, and application configuration.
"""

from pydantic_settings import BaseSettings
from typing import List


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""
    
    # API Settings
    api_title: str = "Business Analytics API"
    api_version: str = "1.0.0"
    api_description: str = "API for business metrics analysis, benchmarking, and insights"
    
    # Server Settings
    host: str = "0.0.0.0"
    port: int = 8004
    reload: bool = False
    
    # CORS Settings
    cors_origins: List[str] = [
        "https://perezrodri.vercel.app",  # Production frontend
        "http://localhost:3000",  # Local development
        "http://localhost:3001",  # Alternative local port
    ]
    cors_allow_credentials: bool = True
    cors_allow_methods: List[str] = ["*"]
    cors_allow_headers: List[str] = ["*"]
    
    # Logging
    log_level: str = "INFO"
    
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = False


# Global settings instance
settings = Settings()


