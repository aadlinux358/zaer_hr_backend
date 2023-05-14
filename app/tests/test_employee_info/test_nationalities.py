"""Nationality endpoints tests module."""
import uuid
from typing import Final

import pytest
from fastapi import status
from httpx import AsyncClient
from sqlmodel.ext.asyncio.session import AsyncSession

from app.models import NationalityDB

ENDPOINT: Final = "nationalities"
USER_ID: Final = "38eb651b-bd33-4f9a-beb2-0f9d52d7acc6"


@pytest.mark.asyncio
async def test_can_create_nationality(client: AsyncClient):
    response = await client.post(
        f"/{ENDPOINT}",
        json={"name": "eritrean"},
    )

    assert response.status_code == status.HTTP_201_CREATED, response.json()
    assert response.json()["name"] == "eritrean"
    assert response.json()["date_created"]
    assert response.json()["date_modified"]


@pytest.mark.asyncio
async def test_nationality_names_are_lower_cased(client: AsyncClient):
    response = await client.post(
        f"/{ENDPOINT}",
        json={"name": "AMEriCan"},
    )

    assert response.status_code == status.HTTP_201_CREATED, response.json()
    assert response.json()["name"] == "american"


@pytest.mark.asyncio
async def test_can_not_create_duplicate_nationality_name(
    client: AsyncClient, session: AsyncSession
):
    nationality = NationalityDB(
        name="eritrean", created_by=uuid.UUID(USER_ID), modified_by=uuid.UUID(USER_ID)
    )
    session.add(nationality)
    await session.commit()

    response = await client.post(
        f"/{ENDPOINT}",
        json={
            "name": "eritrean",
        },
    )
    assert response.status_code == status.HTTP_400_BAD_REQUEST, response.json()
    assert response.json()["detail"] == "duplicate nationality name."


@pytest.mark.asyncio
async def test_can_get_nationalities_list(client: AsyncClient, session: AsyncSession):
    nationalities = [
        NationalityDB(
            name="ethiopian",
            created_by=uuid.UUID(USER_ID),
            modified_by=uuid.UUID(USER_ID),
        ),
        NationalityDB(
            name="british",
            created_by=uuid.UUID(USER_ID),
            modified_by=uuid.UUID(USER_ID),
        ),
        NationalityDB(
            name="mexican",
            created_by=uuid.UUID(USER_ID),
            modified_by=uuid.UUID(USER_ID),
        ),
    ]
    for dep in nationalities:
        session.add(dep)
    await session.commit()

    response = await client.get(f"/{ENDPOINT}")

    assert response.status_code == status.HTTP_200_OK, response.json()
    assert response.json()["count"] == 3
    assert len(response.json()["result"]) == 3
    assert isinstance(response.json()["result"], list)


@pytest.mark.asyncio
async def test_can_get_nationality_by_id(client: AsyncClient, session: AsyncSession):
    nationality = NationalityDB(
        name="eritrean", created_by=uuid.UUID(USER_ID), modified_by=uuid.UUID(USER_ID)
    )
    session.add(nationality)
    await session.commit()
    await session.refresh(nationality)

    response = await client.get(f"/{ENDPOINT}/{nationality.uid}")

    assert response.status_code == status.HTTP_200_OK, response.json()
    assert response.json()["uid"] == str(nationality.uid)
    assert response.json()["name"] == "eritrean"


@pytest.mark.asyncio
async def test_nationality_not_found(client: AsyncClient):
    response = await client.get(f"/{ENDPOINT}/{uuid.uuid4()}")

    assert response.status_code == status.HTTP_404_NOT_FOUND, response.json()
    assert response.json()["detail"] == "nationality not found."


@pytest.mark.asyncio
async def test_can_update_nationality(client: AsyncClient, session: AsyncSession):
    nationality = NationalityDB(
        name="brazilian", created_by=uuid.UUID(USER_ID), modified_by=uuid.UUID(USER_ID)
    )
    session.add(nationality)
    await session.commit()
    await session.refresh(nationality)

    response = await client.patch(
        f"/{ENDPOINT}/{nationality.uid}",
        json={"name": "german"},
    )

    assert response.status_code == status.HTTP_200_OK, response.json()
    assert response.json()["uid"] == str(nationality.uid)
    assert response.json()["name"] == "german"
    assert response.json()["date_created"] == nationality.date_created.isoformat()
    assert response.json()["date_modified"] != nationality.date_modified.isoformat()
    assert response.json()["modified_by"] == USER_ID


@pytest.mark.asyncio
async def test_delete_nationality(client: AsyncClient, session: AsyncSession):
    nationality = NationalityDB(
        name="somali", created_by=uuid.UUID(USER_ID), modified_by=uuid.UUID(USER_ID)
    )
    session.add(nationality)
    await session.commit()
    await session.refresh(nationality)

    response = await client.delete(f"/{ENDPOINT}/{nationality.uid}")
    assert response.status_code == status.HTTP_204_NO_CONTENT, response.json()
