"""Human resources application settings module."""
from typing import Union

from pydantic import BaseSettings, PostgresDsn


class Settings(BaseSettings):
    """Settings configuration class."""

    # Base
    api_v1_prefix: str
    app_name: str
    debug: bool
    version: str
    description: str

    # Database
    async_db_connection_string: Union[PostgresDsn, str]
    async_test_db_connection_string: Union[PostgresDsn, str]
    pg_user: str
    pg_password: str
    pg_server: str
    pg_db: str

    class Config:
        """Further settings customization config class."""

        env_file = ".env"


settings = Settings()
