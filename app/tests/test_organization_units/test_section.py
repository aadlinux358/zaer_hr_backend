"""Section endpoints tests module."""
import uuid
from typing import Final

import pytest
from fastapi import status
from httpx import AsyncClient
from sqlmodel.ext.asyncio.session import AsyncSession

from app.models import DepartmentDB, DivisionDB, SectionDB
from app.tests.test_organization_units.utils import create_test_model

ENDPOINT: Final = "sections"
USER_ID: Final = "38eb651b-bd33-4f9a-beb2-0f9d52d7acc6"


@pytest.mark.asyncio
async def test_create_section(client: AsyncClient, session: AsyncSession):
    department = await create_test_model('department', session)

    response = await client.post(
        f"{ENDPOINT}",
        json={
            "name": "CuTTing",
            "department_uid": str(department.uid),
        },
    )

    assert response.status_code == status.HTTP_201_CREATED, response.json()
    assert response.json()["name"] == "cutting"
    assert response.json()["department_uid"] == str(department.uid)


@pytest.mark.asyncio
async def test_can_not_create_duplicate_section_name(
    client: AsyncClient, session: AsyncSession
):
    department = await create_test_model('department', session)

    section = SectionDB(
        name="cutting",
        department_uid=department.uid,
        created_by=uuid.UUID(USER_ID),
        modified_by=uuid.UUID(USER_ID),
    )
    session.add(section)
    await session.commit()
    await session.refresh(section)

    response = await client.post(
        f"{ENDPOINT}",
        json={
            "name": "cutting",
            "department_uid": str(department.uid),
        },
    )

    assert response.status_code == status.HTTP_400_BAD_REQUEST, response.json()
    assert response.json()["detail"] == "duplicate section name."


@pytest.mark.asyncio
async def test_can_get_section_list(client: AsyncClient, session: AsyncSession):
    department = await create_test_model('department', session)

    sections = [
        SectionDB(
            name="cutting",
            department_uid=department.uid,
            created_by=uuid.UUID(USER_ID),
            modified_by=uuid.UUID(USER_ID),
        ),
        SectionDB(
            name="assembly line 1",
            department_uid=department.uid,
            created_by=uuid.UUID(USER_ID),
            modified_by=uuid.UUID(USER_ID),
        ),
    ]
    for section in sections:
        session.add(section)
    await session.commit()

    response = await client.get(f"{ENDPOINT}")

    assert response.status_code == status.HTTP_200_OK, response.json()
    assert response.json()["count"] == 2
    assert len(response.json()["result"]) == 2
    assert isinstance(response.json()["result"], list)


@pytest.mark.asyncio
async def test_can_get_section_by_uid(client: AsyncClient, session: AsyncSession):
    department = await create_test_model('department', session)

    section = SectionDB(
        name="preparation 1",
        department_uid=department.uid,
        created_by=uuid.UUID(USER_ID),
        modified_by=uuid.UUID(USER_ID),
    )
    session.add(section)
    await session.commit()
    await session.refresh(section)

    response = await client.get(f"{ENDPOINT}/{section.uid}")

    assert response.status_code == status.HTTP_200_OK, response.json()
    assert response.json()["uid"] == str(section.uid)
    assert response.json()["name"] == "preparation 1"


@pytest.mark.asyncio
async def test_section_not_found(client: AsyncClient, session: AsyncSession):
    response = await client.get(f"{ENDPOINT}/{uuid.uuid4()}")

    assert response.status_code == status.HTTP_404_NOT_FOUND, response.json()
    assert response.json()["detail"] == "section not found."


@pytest.mark.asyncio
async def test_can_update_section(client: AsyncClient, session: AsyncSession):
    department = await create_test_model('department', session)

    section = SectionDB(
        name="preparation 1",
        department_uid=department.uid,
        created_by=uuid.UUID(USER_ID),
        modified_by=uuid.UUID(USER_ID),
    )
    session.add(section)
    await session.commit()
    await session.refresh(section)

    response = await client.patch(
        f"{ENDPOINT}/{section.uid}",
        json={"name": "preparation 2"},
    )

    assert response.status_code == status.HTTP_200_OK, response.json()
    assert response.json()["uid"] == str(section.uid)
    assert response.json()["name"] == "preparation 2"
    assert response.json()["modified_by"] == USER_ID


@pytest.mark.asyncio
async def test_delete_section(client: AsyncClient, session: AsyncSession):
    department = await create_test_model('department', session)

    section = SectionDB(
        name="preparation 1",
        department_uid=department.uid,
        created_by=uuid.UUID(USER_ID),
        modified_by=uuid.UUID(USER_ID),
    )
    session.add(section)
    await session.commit()
    await session.refresh(section)

    response = await client.delete(f"/{ENDPOINT}/{section.uid}")
    assert response.status_code == status.HTTP_204_NO_CONTENT, response.json()
