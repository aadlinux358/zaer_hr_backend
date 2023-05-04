"""Human resources application settings module."""
import os
import sys
from typing import Union

from pydantic import BaseSettings, PostgresDsn
import requests
from requests.exceptions import ConnectionError
from dotenv import load_dotenv

load_dotenv()

def get_public_key() -> str:
    auth_api = os.environ.get('auth_api')
    if auth_api is None:
        print('auth_api environment variable not set.')
        sys.exit(1)
    try:
        response = requests.get(f"{auth_api}/api/v1/auth/public-key")
    except ConnectionError as e:
        print('Can not obtain public key. Check Auth service.')
        sys.exit(1)

    return response.json()['public_key']

class Settings(BaseSettings):
    """Settings configuration class."""
    # fastapi_jwt_auth
    authjwt_public_key: str = get_public_key()
    authjwt_algorithm: str = 'RS256'

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
