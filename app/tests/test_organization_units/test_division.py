"""Department endpoints tests module."""
import uuid
from typing import Final

import pytest
from fastapi import status
from httpx import AsyncClient
from sqlmodel.ext.asyncio.session import AsyncSession

from app.models import DivisionDB

ENDPOINT: Final = "divisions"
USER_ID: Final = "38eb651b-bd33-4f9a-beb2-0f9d52d7acc6"


@pytest.mark.asyncio
async def test_can_create_division(client: AsyncClient):
    response = await client.post(
        f"/{ENDPOINT}",
        json={"name": "division 1"},
    )

    assert response.status_code == status.HTTP_201_CREATED, response.json()
    assert response.json()["name"] == "division 1"
    assert response.json()["date_created"]
    assert response.json()["date_modified"]


@pytest.mark.asyncio
async def test_division_names_are_lower_cased(client: AsyncClient):
    response = await client.post(
        f"/{ENDPOINT}",
        json={"name": "CamiCeria"},
    )

    assert response.status_code == status.HTTP_201_CREATED, response.json()
    assert response.json()["name"] == "camiceria"


@pytest.mark.asyncio
async def test_can_not_create_duplicate_division_name(
    client: AsyncClient, session: AsyncSession
):
    division = DivisionDB(
        name="hr", created_by=uuid.UUID(USER_ID), modified_by=uuid.UUID(USER_ID)
    )
    session.add(division)
    await session.commit()

    response = await client.post(
        f"/{ENDPOINT}",
        json={"name": "HR"},
    )
    assert response.status_code == status.HTTP_400_BAD_REQUEST, response.json()
    assert response.json()["detail"] == "duplicate division name."


@pytest.mark.asyncio
async def test_can_get_divisions_list(client: AsyncClient, session: AsyncSession):
    divisions = [
        DivisionDB(
            name="hr", created_by=uuid.UUID(USER_ID), modified_by=uuid.UUID(USER_ID)
        ),
        DivisionDB(
            name="camiceria",
            created_by=uuid.UUID(USER_ID),
            modified_by=uuid.UUID(USER_ID),
        ),
        DivisionDB(
            name="store", created_by=uuid.UUID(USER_ID), modified_by=uuid.UUID(USER_ID)
        ),
    ]
    for dep in divisions:
        session.add(dep)
    await session.commit()

    response = await client.get(f"/{ENDPOINT}")

    assert response.status_code == status.HTTP_200_OK, response.json()
    assert response.json()["count"] == 3
    assert len(response.json()["result"]) == 3
    assert isinstance(response.json()["result"], list)


@pytest.mark.asyncio
async def test_can_get_division_by_id(client: AsyncClient, session: AsyncSession):
    division = DivisionDB(
        name="hr", created_by=uuid.UUID(USER_ID), modified_by=uuid.UUID(USER_ID)
    )
    session.add(division)
    await session.commit()
    await session.refresh(division)

    response = await client.get(f"/{ENDPOINT}/{division.uid}")

    assert response.status_code == status.HTTP_200_OK, response.json()
    assert response.json()["uid"] == str(division.uid)
    assert response.json()["name"] == "hr"


@pytest.mark.asyncio
async def test_division_not_found(client: AsyncClient):
    response = await client.get(f"/{ENDPOINT}/{uuid.uuid4()}")

    assert response.status_code == status.HTTP_404_NOT_FOUND, response.json()
    assert response.json()["detail"] == "division not found."


@pytest.mark.asyncio
async def test_can_update_division(client: AsyncClient, session: AsyncSession):
    division = DivisionDB(
        name="sales", created_by=uuid.UUID(USER_ID), modified_by=uuid.UUID(USER_ID)
    )
    session.add(division)
    await session.commit()
    await session.refresh(division)

    response = await client.patch(
        f"/{ENDPOINT}/{division.uid}",
        json={"name": "finance"},
    )

    assert response.status_code == status.HTTP_200_OK, response.json()
    assert response.json()["uid"] == str(division.uid)
    assert response.json()["name"] == "finance"
    assert response.json()["date_created"] == division.date_created.isoformat()
    assert response.json()["date_modified"] != division.date_modified.isoformat()
    assert response.json()["modified_by"] == USER_ID


@pytest.mark.asyncio
async def test_delete_division(client: AsyncClient, session: AsyncSession):
    division = DivisionDB(
        name="hr", created_by=uuid.UUID(USER_ID), modified_by=uuid.UUID(USER_ID)
    )
    session.add(division)
    await session.commit()
    await session.refresh(division)

    response = await client.delete(f"/{ENDPOINT}/{division.uid}")
    assert response.status_code == status.HTTP_204_NO_CONTENT, response.json()
