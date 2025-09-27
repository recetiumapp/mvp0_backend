# recetium backend/src/core/config.py
#
# Recetium MVP 0 
# Author: Rob Palencia / Sept.2025 
#
# Database configuration loader for Supabase Postgres.
#

from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    db_user: str
    db_password: str
    db_host: str
    db_port: str
    db_name: str

    class Config:
        env_file = ".env"

settings = Settings()

DATABASE_URL = (
    f"postgresql://{settings.db_user}:{settings.db_password}"
    f"@{settings.db_host}:{settings.db_port}/{settings.db_name}"
)
