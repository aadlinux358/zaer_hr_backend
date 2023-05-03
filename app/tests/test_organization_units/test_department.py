"""Department endpoints tests module."""
import uuid
from typing import Final

import pytest
from fastapi import status
from httpx import AsyncClient
from sqlmodel.ext.asyncio.session import AsyncSession

from app.models import DepartmentDB

ENDPOINT: Final = "departments"
USER_ID: Final = "38eb651b-bd33-4f9a-beb2-0f9d52d7acc6"


@pytest.mark.asyncio
async def test_can_create_department(client: AsyncClient):
    response = await client.post(
        f"/{ENDPOINT}",
        json={"name": "department 1", "created_by": USER_ID, "modified_by": USER_ID},
    )

    assert response.status_code == status.HTTP_201_CREATED, response.json()
    assert response.json()["name"] == "department 1"
    assert response.json()["date_created"]
    assert response.json()["date_modified"]


@pytest.mark.asyncio
async def test_department_names_are_lower_cased(client: AsyncClient):
    response = await client.post(
        f"/{ENDPOINT}",
        json={"name": "CamiCeria", "created_by": USER_ID, "modified_by": USER_ID},
    )

    assert response.status_code == status.HTTP_201_CREATED, response.json()
    assert response.json()["name"] == "camiceria"


@pytest.mark.asyncio
async def test_can_not_create_duplicate_department_name(
    client: AsyncClient, session: AsyncSession
):
    department = DepartmentDB(
        name="hr", created_by=uuid.UUID(USER_ID), modified_by=uuid.UUID(USER_ID)
    )
    session.add(department)
    await session.commit()

    response = await client.post(
        f"/{ENDPOINT}",
        json={"name": "HR", "created_by": USER_ID, "modified_by": USER_ID},
    )
    assert response.status_code == status.HTTP_400_BAD_REQUEST, response.json()
    assert response.json()["detail"] == "duplicate department name."


@pytest.mark.asyncio
async def test_can_get_departments_list(client: AsyncClient, session: AsyncSession):
    departments = [
        DepartmentDB(
            name="hr", created_by=uuid.UUID(USER_ID), modified_by=uuid.UUID(USER_ID)
        ),
        DepartmentDB(
            name="camiceria",
            created_by=uuid.UUID(USER_ID),
            modified_by=uuid.UUID(USER_ID),
        ),
        DepartmentDB(
            name="store", created_by=uuid.UUID(USER_ID), modified_by=uuid.UUID(USER_ID)
        ),
    ]
    for dep in departments:
        session.add(dep)
    await session.commit()

    response = await client.get(f"/{ENDPOINT}")

    assert response.status_code == status.HTTP_200_OK, response.json()
    assert response.json()["count"] == 3
    assert len(response.json()["result"]) == 3
    assert isinstance(response.json()["result"], list)


@pytest.mark.asyncio
async def test_can_get_department_by_id(client: AsyncClient, session: AsyncSession):
    department = DepartmentDB(
        name="hr", created_by=uuid.UUID(USER_ID), modified_by=uuid.UUID(USER_ID)
    )
    session.add(department)
    await session.commit()
    await session.refresh(department)

    response = await client.get(f"/{ENDPOINT}/{department.uid}")

    assert response.status_code == status.HTTP_200_OK, response.json()
    assert response.json()["uid"] == str(department.uid)
    assert response.json()["name"] == "hr"


@pytest.mark.asyncio
async def test_department_not_found(client: AsyncClient):
    response = await client.get(f"/{ENDPOINT}/{uuid.uuid4()}")

    assert response.status_code == status.HTTP_404_NOT_FOUND, response.json()
    assert response.json()["detail"] == "department not found."


@pytest.mark.asyncio
async def test_can_update_department(client: AsyncClient, session: AsyncSession):
    department = DepartmentDB(
        name="sales", created_by=uuid.UUID(USER_ID), modified_by=uuid.UUID(USER_ID)
    )
    session.add(department)
    await session.commit()
    await session.refresh(department)

    response = await client.patch(
        f"/{ENDPOINT}/{department.uid}",
        json={"name": "finance", "modified_by": USER_ID},
    )

    assert response.status_code == status.HTTP_200_OK, response.json()
    assert response.json()["uid"] == str(department.uid)
    assert response.json()["name"] == "finance"
    assert response.json()["date_created"] == department.date_created.isoformat()
    assert response.json()["date_modified"] != department.date_modified.isoformat()


@pytest.mark.asyncio
async def test_delete_department(client: AsyncClient, session: AsyncSession):
    department = DepartmentDB(
        name="hr", created_by=uuid.UUID(USER_ID), modified_by=uuid.UUID(USER_ID)
    )
    session.add(department)
    await session.commit()
    await session.refresh(department)

    response = await client.delete(f"/{ENDPOINT}/{department.uid}")
    assert response.status_code == status.HTTP_204_NO_CONTENT, response.json()
