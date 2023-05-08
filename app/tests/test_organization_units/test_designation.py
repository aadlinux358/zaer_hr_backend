"""Designation endpoints tests module."""
import uuid
from typing import Final

import pytest
from fastapi import status
from httpx import AsyncClient
from sqlmodel.ext.asyncio.session import AsyncSession

from app.models import DesignationDB

ENDPOINT: Final = "designations"
USER_ID: Final = "38eb651b-bd33-4f9a-beb2-0f9d52d7acc6"


@pytest.mark.asyncio
async def test_create_designation(client: AsyncClient, session: AsyncSession):
    response = await client.post(
        f"/{ENDPOINT}",
        json={
            "title": "machine OPERATOR",
        },
    )

    assert response.status_code == status.HTTP_201_CREATED, response.json()
    assert response.json()["title"] == "machine operator"
    assert response.json()["created_by"] == USER_ID


@pytest.mark.asyncio
async def test_duplicate_designation_title(client: AsyncClient, session: AsyncSession):
    designation = DesignationDB(
        title="cutter", created_by=uuid.UUID(USER_ID), modified_by=uuid.UUID(USER_ID)
    )
    session.add(designation)
    await session.commit()

    response = await client.post(
        f"{ENDPOINT}",
        json={"title": "cutter", "created_by": USER_ID, "modified_by": USER_ID},
    )

    assert response.status_code == status.HTTP_400_BAD_REQUEST, response.json()
    assert response.json()["detail"] == "duplicate designation title."


@pytest.mark.asyncio
async def test_can_get_designation_list(client: AsyncClient, session: AsyncSession):
    designations = [
        DesignationDB(
            title="machine operator",
            created_by=uuid.UUID(USER_ID),
            modified_by=uuid.UUID(USER_ID),
        ),
        DesignationDB(
            title="cutter",
            created_by=uuid.UUID(USER_ID),
            modified_by=uuid.UUID(USER_ID),
        ),
    ]
    for designation in designations:
        session.add(designation)
    await session.commit()

    response = await client.get(f"{ENDPOINT}")

    assert response.status_code == status.HTTP_200_OK, response.json()
    assert response.json()["count"] == 2
    assert len(response.json()["result"]) == 2
    assert isinstance(response.json()["result"], list)


@pytest.mark.asyncio
async def test_get_designation_by_id(client: AsyncClient, session: AsyncSession):
    designation = DesignationDB(
        title="cutter", created_by=uuid.UUID(USER_ID), modified_by=uuid.UUID(USER_ID)
    )
    session.add(designation)
    await session.commit()
    await session.refresh(designation)

    response = await client.get(f"{ENDPOINT}/{designation.uid}")

    assert response.status_code == status.HTTP_200_OK, response.json()
    assert response.json()["uid"] == str(designation.uid)
    assert response.json()["title"] == "cutter"


@pytest.mark.asyncio
async def test_designation_not_found(client: AsyncClient, session: AsyncSession):
    response = await client.get(f"{ENDPOINT}/{uuid.uuid4()}")

    assert response.status_code == status.HTTP_404_NOT_FOUND, response.json()
    assert response.json()["detail"] == "designation not found."


@pytest.mark.asyncio
async def test_update_designation(client: AsyncClient, session: AsyncSession):
    designation = DesignationDB(
        title="cutter", created_by=uuid.UUID(USER_ID), modified_by=uuid.UUID(USER_ID)
    )
    session.add(designation)
    await session.commit()
    await session.refresh(designation)

    response = await client.patch(
        f"{ENDPOINT}/{designation.uid}", json={"title": "other"}
    )

    assert response.status_code == status.HTTP_200_OK, response.json()
    assert response.json()["uid"] == str(designation.uid)
    assert response.json()["title"] == "other"
    assert response.json()["modified_by"] == USER_ID


@pytest.mark.asyncio
async def test_delete_designation(client: AsyncClient, session: AsyncSession):
    designation = DesignationDB(
        title="cutter", created_by=uuid.UUID(USER_ID), modified_by=uuid.UUID(USER_ID)
    )
    session.add(designation)
    await session.commit()
    await session.refresh(designation)

    response = await client.delete(f"/{ENDPOINT}/{designation.uid}")
    assert response.status_code == status.HTTP_204_NO_CONTENT, response.json()
