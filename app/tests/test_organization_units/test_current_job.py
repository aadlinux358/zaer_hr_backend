"""Current job endpoints tests module."""
import uuid
from typing import Final

import pytest
from fastapi import status
from httpx import AsyncClient
from sqlmodel.ext.asyncio.session import AsyncSession

from app.models import CurrentJobDB

ENDPOINT: Final = "current-jobs"
USER_ID: Final = "38eb651b-bd33-4f9a-beb2-0f9d52d7acc6"


@pytest.mark.asyncio
async def test_create_current_job(client: AsyncClient, session: AsyncSession):
    response = await client.post(
        f"/{ENDPOINT}",
        json={
            "title": "machine OPERATOR",
            "created_by": USER_ID,
            "modified_by": USER_ID,
        },
    )

    assert response.status_code == status.HTTP_201_CREATED, response.json()
    assert response.json()["title"] == "machine operator"


@pytest.mark.asyncio
async def test_duplicate_current_job_title(client: AsyncClient, session: AsyncSession):
    current_job = CurrentJobDB(
        title="cutter", created_by=uuid.UUID(USER_ID), modified_by=uuid.UUID(USER_ID)
    )
    session.add(current_job)
    await session.commit()

    response = await client.post(
        f"{ENDPOINT}",
        json={"title": "cutter", "created_by": USER_ID, "modified_by": USER_ID},
    )

    assert response.status_code == status.HTTP_400_BAD_REQUEST, response.json()
    assert response.json()["detail"] == "duplicate current job title."


@pytest.mark.asyncio
async def test_can_get_current_job_list(client: AsyncClient, session: AsyncSession):
    current_jobs = [
        CurrentJobDB(
            title="machine operator",
            created_by=uuid.UUID(USER_ID),
            modified_by=uuid.UUID(USER_ID),
        ),
        CurrentJobDB(
            title="cutter",
            created_by=uuid.UUID(USER_ID),
            modified_by=uuid.UUID(USER_ID),
        ),
    ]
    for current_job in current_jobs:
        session.add(current_job)
    await session.commit()

    response = await client.get(f"{ENDPOINT}")

    assert response.status_code == status.HTTP_200_OK, response.json()
    assert response.json()["count"] == 2
    assert len(response.json()["result"]) == 2
    assert isinstance(response.json()["result"], list)


@pytest.mark.asyncio
async def test_get_current_job_by_id(client: AsyncClient, session: AsyncSession):
    current_job = CurrentJobDB(
        title="cutter", created_by=uuid.UUID(USER_ID), modified_by=uuid.UUID(USER_ID)
    )
    session.add(current_job)
    await session.commit()
    await session.refresh(current_job)

    response = await client.get(f"{ENDPOINT}/{current_job.uid}")

    assert response.status_code == status.HTTP_200_OK, response.json()
    assert response.json()["uid"] == str(current_job.uid)
    assert response.json()["title"] == "cutter"


@pytest.mark.asyncio
async def test_current_job_not_found(client: AsyncClient, session: AsyncSession):
    response = await client.get(f"{ENDPOINT}/{uuid.uuid4()}")

    assert response.status_code == status.HTTP_404_NOT_FOUND, response.json()
    assert response.json()["detail"] == "current job not found."


@pytest.mark.asyncio
async def test_update_current_job(client: AsyncClient, session: AsyncSession):
    current_job = CurrentJobDB(
        title="cutter", created_by=uuid.UUID(USER_ID), modified_by=uuid.UUID(USER_ID)
    )
    session.add(current_job)
    await session.commit()
    await session.refresh(current_job)

    response = await client.patch(
        f"{ENDPOINT}/{current_job.uid}", json={"title": "other", "modified_by": USER_ID}
    )

    assert response.status_code == status.HTTP_200_OK, response.json()
    assert response.json()["uid"] == str(current_job.uid)
    assert response.json()["title"] == "other"
    assert response.json()["modified_by"] == USER_ID


@pytest.mark.asyncio
async def test_delete_current_job(client: AsyncClient, session: AsyncSession):
    current_job = CurrentJobDB(
        title="cutter", created_by=uuid.UUID(USER_ID), modified_by=uuid.UUID(USER_ID)
    )
    session.add(current_job)
    await session.commit()
    await session.refresh(current_job)

    response = await client.delete(f"/{ENDPOINT}/{current_job.uid}")
    assert response.status_code == status.HTTP_204_NO_CONTENT, response.json()
