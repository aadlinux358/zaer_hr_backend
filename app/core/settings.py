"""Human resources application settings module."""
import os
import sys
from urllib.parse import quote_plus

import requests
from dotenv import load_dotenv
from pydantic import BaseSettings, validator
from requests.exceptions import ConnectionError

load_dotenv()


def get_pytest_keys() -> dict:
    """Generate keys for testing."""
    from cryptography.hazmat.primitives import serialization
    from cryptography.hazmat.primitives.asymmetric import rsa

    key = rsa.generate_private_key(public_exponent=65537, key_size=2048)
    private_key_bytes = key.private_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.PKCS8,
        encryption_algorithm=serialization.NoEncryption(),
    )
    public_key = key.public_key()
    public_key_bytes = public_key.public_bytes(
        encoding=serialization.Encoding.PEM, format=serialization.PublicFormat.PKCS1
    )
    public_key_str = public_key_bytes.decode()
    private_key_str = private_key_bytes.decode()
    return dict(private_key=private_key_str, public_key=public_key_str)


_pytest_private_key = None
_pytest_public_key = None

if "pytest" in sys.modules:
    keys = get_pytest_keys()
    _pytest_private_key = keys.get("private_key")
    _pytest_public_key = keys.get("public_key")


def get_public_key() -> str | None:
    """Get public key."""
    # TODO clean up this check for pytest
    if "pytest" in sys.modules:
        return _pytest_public_key

    auth_api = os.environ.get("auth_api")
    if auth_api is None:
        print("auth_api environment variable not set.")
        return None
    try:
        response = requests.get(f"{auth_api}/api/v1/auth/public-key")
    except ConnectionError:
        print("Can not obtain public key. Check Auth service.")
        return None

    return response.json()["public_key"]


class Settings(BaseSettings):
    """Settings configuration class."""

    # fastapi_jwt_auth
    authjwt_private_key: str | None = _pytest_private_key
    authjwt_public_key: str | None = get_public_key()
    authjwt_algorithm: str = "RS256"

    # Base
    api_v1_prefix: str
    app_name: str
    debug: bool
    version: str
    description: str

    # Database
    pg_user: str
    pg_password: str
    pg_server: str
    pg_db: str
    pg_port: int
    pg_test_db: str
    pg_test_port: int

    @validator("pg_user", "pg_password", "pg_db", "pg_test_db")
    def url_encode(cls, v):
        """Url quote strings."""
        v = quote_plus(v)
        return v

    class Config:
        """Further settings customization config class."""

        env_file = ".env"


settings = Settings()
