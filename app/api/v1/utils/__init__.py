"""API endpoints exception responses package."""

from app.api.v1.utils.exception_responses import staff_user_or_error, superuser_or_error

__all__ = ["superuser_or_error", "staff_user_or_error"]
