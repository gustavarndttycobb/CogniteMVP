"""Configuration settings for the Cognite MVP API."""

from pydantic_settings import BaseSettings
from functools import lru_cache


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""
    
    # Cognite configuration
    cognite_project: str = "radix-dev"
    cognite_cluster: str = "az-eastus-1.cognitedata.com"
    cognite_base_url: str = "https://az-eastus-1.cognitedata.com"
    
    # Data model configuration
    data_model_space: str = "ARNDT_SPACE_TEST"
    data_model_name: str = "ARNDT_TEST"
    data_model_version: str = "1"
    
    # API configuration
    api_title: str = "Cognite MVP API"
    api_version: str = "1.0.0"
    
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


@lru_cache
def get_settings() -> Settings:
    """Get cached settings instance."""
    return Settings()
