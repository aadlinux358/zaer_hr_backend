"""API endpoints exception responses module."""
from typing import Optional

from fastapi import HTTPException, status


async def superuser_or_error(user_claims: Optional[dict]) -> None:
    """Check if user is superuser."""
    if user_claims is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="invalid token claim."
        )

    if not user_claims.get("is_superuser"):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="insufficient privileges."
        )

    if not user_claims.get("is_active"):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="inactive user."
        )


async def staff_user_or_error(user_claims: Optional[dict]) -> None:
    """Check if user is staff member."""
    if user_claims is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="invalid token claim."
        )

    if not user_claims.get("is_staff"):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="insufficient privileges."
        )

    if not user_claims.get("is_active"):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="inactive user."
        )
