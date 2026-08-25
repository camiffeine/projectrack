'''Centralized application settings and configuration management'''

import os
from functools import lru_cache
from pydantic import BaseModel, Field
from dotenv import load_dotenv

load_dotenv()

class Settings(BaseModel):
    '''Application settings model with environment variable fallbacks'''
    # App metadata
    APP_NAME: str = "ProjecTrack"
    APP_VERSION: str = "0.0.5"
    DEBUG: bool = Field(default_factory=lambda: os.getenv("DEBUG", "False").lower() in ("true", "1", "yes"))

    # Database Configuration (NFR-005, NFR-006)
    MONGO_URI: str = Field(default_factory=lambda: os.getenv("MONGO_URI", "mongodb://localhost:27017/"))
    MONGO_DB_NAME: str = Field(default_factory=lambda: os.getenv("MONGO_DB", os.getenv("MONGO_DB_NAME", "ProjecTrack_dev")))
    MIN_POOL_SIZE: int = Field(default_factory=lambda: int(os.getenv("MIN_POOL_SIZE", "10")))
    MAX_POOL_SIZE: int = Field(default_factory=lambda: int(os.getenv("MAX_POOL_SIZE", "50")))
    MAX_IDLE_TIME_MS: int = Field(default_factory=lambda: int(os.getenv("MAX_IDLE_TIME_MS", "45000")))
    CONNECT_TIMEOUT_MS: int = Field(default_factory=lambda: int(os.getenv("CONNECT_TIMEOUT_MS", "3000")))
    SERVER_SELECTION_TIMEOUT_MS: int = Field(default_factory=lambda: int(os.getenv("SERVER_SELECTION_TIMEOUT_MS", "3000")))

    # Security & JWT Configuration (NFR-003, NFR-004)
    SECRET_KEY: str = Field(default_factory=lambda: os.getenv("SECRET_KEY", "default-insecure-dev-secret-key-change-in-production"))
    ALGORITHM: str = Field(default_factory=lambda: os.getenv("ALGORITHM", "HS256"))
    ACCESS_TOKEN_EXPIRE_MINUTES: int = Field(default_factory=lambda: int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "60")))

@lru_cache()
def get_settings() -> Settings:
    '''Returns cached application settings instance'''
    return Settings()

settings = get_settings()
