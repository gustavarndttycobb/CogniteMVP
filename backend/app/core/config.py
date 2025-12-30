"""Configuration settings for the Cognite MVP API."""

from pydantic_settings import BaseSettings
from functools import lru_cache


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""
    """Pydantic gets the values from environment variables even if here is lowercase and in .env is uppercase"""
    
    # Cognite configuration
    cognite_project: str
    cognite_cluster: str
    cognite_base_url: str
    
    # Data model configuration
    data_model_space: str
    data_model_name: str
    data_model_version: str
    
    # API configuration
    api_title: str = "Cognite MVP API"
    api_version: str = "1.0.0"
    
    class Config:
        """setting the environment variables file"""
        env_file = ".env"
        env_file_encoding = "utf-8"


@lru_cache
def get_settings() -> Settings:
    """Get cached settings instance."""
    return Settings()
