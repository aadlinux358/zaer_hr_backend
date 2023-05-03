"""Educational level endpoints tests module."""
import uuid
from typing import Final

import pytest
from fastapi import status
from httpx import AsyncClient
from sqlmodel.ext.asyncio.session import AsyncSession

from app.models import EducationalLevelDB

ENDPOINT: Final = "educational-levels"
USER_ID: Final = "38eb651b-bd33-4f9a-beb2-0f9d52d7acc6"


@pytest.mark.asyncio
async def test_can_create_educational_level(client: AsyncClient):
    response = await client.post(
        f"/{ENDPOINT}",
        json={"level": "10th", "created_by": USER_ID, "modified_by": USER_ID},
    )

    assert response.status_code == status.HTTP_201_CREATED, response.json()
    assert response.json()["level"] == "10th"
    assert response.json()["date_created"]
    assert response.json()["date_modified"]


@pytest.mark.asyncio
async def test_educational_level_levels_are_lower_cased(client: AsyncClient):
    response = await client.post(
        f"/{ENDPOINT}",
        json={"level": "7th", "created_by": USER_ID, "modified_by": USER_ID},
    )

    assert response.status_code == status.HTTP_201_CREATED, response.json()
    assert response.json()["level"] == "7th"


@pytest.mark.asyncio
async def test_can_not_create_duplicate_educational_level_level(
    client: AsyncClient, session: AsyncSession
):
    educational_level = EducationalLevelDB(
        level="8th", created_by=uuid.UUID(USER_ID), modified_by=uuid.UUID(USER_ID)
    )
    session.add(educational_level)
    await session.commit()

    response = await client.post(
        f"/{ENDPOINT}",
        json={"level": "8th", "created_by": USER_ID, "modified_by": USER_ID},
    )
    assert response.status_code == status.HTTP_400_BAD_REQUEST, response.json()
    assert response.json()["detail"] == "duplicate educational level."


@pytest.mark.asyncio
async def test_can_get_educational_levels_list(
    client: AsyncClient, session: AsyncSession
):
    educational_levels = [
        EducationalLevelDB(
            level="1st",
            created_by=uuid.UUID(USER_ID),
            modified_by=uuid.UUID(USER_ID),
        ),
        EducationalLevelDB(
            level="2nd",
            created_by=uuid.UUID(USER_ID),
            modified_by=uuid.UUID(USER_ID),
        ),
        EducationalLevelDB(
            level="3rd",
            created_by=uuid.UUID(USER_ID),
            modified_by=uuid.UUID(USER_ID),
        ),
    ]
    for dep in educational_levels:
        session.add(dep)
    await session.commit()

    response = await client.get(f"/{ENDPOINT}")

    assert response.status_code == status.HTTP_200_OK, response.json()
    assert response.json()["count"] == 3
    assert len(response.json()["result"]) == 3
    assert isinstance(response.json()["result"], list)


@pytest.mark.asyncio
async def test_can_get_educational_level_by_id(
    client: AsyncClient, session: AsyncSession
):
    educational_level = EducationalLevelDB(
        level="10th", created_by=uuid.UUID(USER_ID), modified_by=uuid.UUID(USER_ID)
    )
    session.add(educational_level)
    await session.commit()
    await session.refresh(educational_level)

    response = await client.get(f"/{ENDPOINT}/{educational_level.uid}")

    assert response.status_code == status.HTTP_200_OK, response.json()
    assert response.json()["uid"] == str(educational_level.uid)
    assert response.json()["level"] == "10th"


@pytest.mark.asyncio
async def test_educational_level_not_found(client: AsyncClient):
    response = await client.get(f"/{ENDPOINT}/{uuid.uuid4()}")

    assert response.status_code == status.HTTP_404_NOT_FOUND, response.json()
    assert response.json()["detail"] == "educational level not found."


@pytest.mark.asyncio
async def test_can_update_educational_level(client: AsyncClient, session: AsyncSession):
    educational_level = EducationalLevelDB(
        level="10th", created_by=uuid.UUID(USER_ID), modified_by=uuid.UUID(USER_ID)
    )
    session.add(educational_level)
    await session.commit()
    await session.refresh(educational_level)

    response = await client.patch(
        f"/{ENDPOINT}/{educational_level.uid}",
        json={"level": "12th", "modified_by": USER_ID},
    )

    assert response.status_code == status.HTTP_200_OK, response.json()
    assert response.json()["uid"] == str(educational_level.uid)
    assert response.json()["level"] == "12th"
    assert response.json()["date_created"] == educational_level.date_created.isoformat()
    assert (
        response.json()["date_modified"] != educational_level.date_modified.isoformat()
    )


@pytest.mark.asyncio
async def test_delete_educational_level(client: AsyncClient, session: AsyncSession):
    educational_level = EducationalLevelDB(
        level="10th", created_by=uuid.UUID(USER_ID), modified_by=uuid.UUID(USER_ID)
    )
    session.add(educational_level)
    await session.commit()
    await session.refresh(educational_level)

    response = await client.delete(f"/{ENDPOINT}/{educational_level.uid}")
    assert response.status_code == status.HTTP_204_NO_CONTENT, response.json()
