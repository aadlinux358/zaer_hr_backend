"""Employee termination api tests module."""
from typing import Final

import pytest
from httpx import AsyncClient
from sqlmodel.ext.asyncio.session import AsyncSession

ENDPOINT: Final = "terminate"
USER_ID: Final = "38eb651b-bd33-4f9a-beb2-0f9d52d7acc6"


@pytest.mark.asyncio
async def test_create_employee_termination(client: AsyncClient, session: AsyncSession):
    assert True
