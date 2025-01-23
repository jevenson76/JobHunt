from pydantic import BaseSettings, PostgresDsn, SecretStr
from typing import Optional

class Settings(BaseSettings):
    # API Keys
    OPENAI_API_KEY: SecretStr
    SUPABASE_URL: str
    SUPABASE_KEY: SecretStr

    # Database
    DATABASE_URL: PostgresDsn

    # Application Settings
    API_HOST: str = "0.0.0.0"
    API_PORT: int = 8000
    DEBUG: bool = False
    LOG_LEVEL: str = "INFO"

    # Job Search Settings
    MAX_JOBS_PER_SEARCH: int = 100
    DEFAULT_SEARCH_TIMEOUT: int = 300
    MAX_CONCURRENT_SEARCHES: int = 5

    # Rate Limiting
    DEFAULT_RATE_LIMIT: int = 60
    RATE_LIMIT_WINDOW: int = 60

    class Config:
        env_file = ".env"
        case_sensitive = True