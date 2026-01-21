from pydantic_settings import BaseSettings
from typing import Optional

class Settings(BaseSettings):
    db_user: str
    db_password: str
    db_name: str
    db_host: str = "db"
    db_port: int = 5432

    @property
    def database_url(self) -> str:
        return f"postgresql://{self.db_user}:{self.db_password}@{self.db_host}:{self.db_port}/{self.db_name}"



    app_env: str = "development"
    debug: bool = True
    log_level: str = "INFO"


    secret_key: str


    sentry_dsn: Optional[str] = None
    aws_region: Optional[str] = "us-east-1"

    class Config:
        env_file = ".env"
        extra = "ignore"
        case_sensitive = False

settings = Settings()