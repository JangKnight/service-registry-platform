from pydantic_settings import BaseSettings
from typing import Optional

class Settings(BaseSettings):
    database_url: str


    app_env: str = "development"
    debug: bool = True
    log_level: str = "INFO"


    secret_key: str


    sentry_dsn: Optional[str] = None
    aws_region: Optional[str] = "us-east-1"

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = False

settings = Settings()