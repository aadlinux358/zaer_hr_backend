"""Section endpoints tests module."""
import uuid
from typing import Final

import pytest
from fastapi import status
from httpx import AsyncClient
from sqlmodel.ext.asyncio.session import AsyncSession

from app.models.organization_units.department import DepartmentDB
from app.models.organization_units.section import SectionDB

ENDPOINT: Final = "sections"
USER_ID: Final = "38eb651b-bd33-4f9a-beb2-0f9d52d7acc6"


@pytest.mark.asyncio
async def test_create_section(client: AsyncClient, session: AsyncSession):
    department = DepartmentDB(
        name="operations", created_by=uuid.UUID(USER_ID), modified_by=uuid.UUID(USER_ID)
    )
    session.add(department)
    await session.commit()
    await session.refresh(department)

    response = await client.post(
        f"/{ENDPOINT}",
        json={
            "name": "shirt department",
            "department_uid": str(department.uid),
            "created_by": USER_ID,
            "modified_by": USER_ID,
        },
    )

    assert response.status_code == status.HTTP_201_CREATED, response.json()
    assert response.json()["name"] == "shirt department"


@pytest.mark.asyncio
async def test_section_names_are_lower_cased(
    client: AsyncClient, session: AsyncSession
):
    department = DepartmentDB(
        name="operations", created_by=uuid.UUID(USER_ID), modified_by=uuid.UUID(USER_ID)
    )
    session.add(department)
    await session.commit()
    await session.refresh(department)

    response = await client.post(
        f"/{ENDPOINT}",
        json={
            "name": "UPPERCASE",
            "department_uid": str(department.uid),
            "created_by": USER_ID,
            "modified_by": USER_ID,
        },
    )

    assert response.status_code == status.HTTP_201_CREATED, response.json()
    assert response.json()["name"] == "uppercase"


@pytest.mark.asyncio
async def test_can_not_create_duplicate_section_name(
    client: AsyncClient, session: AsyncSession
):
    department = DepartmentDB(
        name="operations", created_by=uuid.UUID(USER_ID), modified_by=uuid.UUID(USER_ID)
    )
    session.add(department)
    await session.commit()
    await session.refresh(department)
    section = SectionDB(
        name="shirt department",
        department_uid=department.uid,
        created_by=uuid.UUID(USER_ID),
        modified_by=uuid.UUID(USER_ID),
    )
    session.add(section)
    await session.commit()
    await session.refresh(section)

    response = await client.post(
        f"/{ENDPOINT}",
        json={
            "name": "shirt department",
            "department_uid": str(department.uid),
            "created_by": USER_ID,
            "modified_by": USER_ID,
        },
    )

    assert response.status_code == status.HTTP_400_BAD_REQUEST, response.json()
    assert response.json()["detail"] == "duplicate section name."


@pytest.mark.asyncio
async def test_can_get_section_list(client: AsyncClient, session: AsyncSession):
    department = DepartmentDB(
        name="operations", created_by=uuid.UUID(USER_ID), modified_by=uuid.UUID(USER_ID)
    )
    session.add(department)
    await session.commit()
    await session.refresh(department)
    sections = [
        SectionDB(
            name="shirt department",
            department_uid=department.uid,
            created_by=uuid.UUID(USER_ID),
            modified_by=uuid.UUID(USER_ID),
        ),
        SectionDB(
            name="garment department",
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
    department = DepartmentDB(
        name="operations", created_by=uuid.UUID(USER_ID), modified_by=uuid.UUID(USER_ID)
    )
    session.add(department)
    await session.commit()
    await session.refresh(department)
    section = SectionDB(
        name="shirt department",
        department_uid=department.uid,
        created_by=uuid.UUID(USER_ID),
        modified_by=uuid.UUID(USER_ID),
    )
    session.add(section)
    await session.commit()
    await session.refresh(section)

    response = await client.get(f"/{ENDPOINT}/{section.uid}")

    assert response.status_code == status.HTTP_200_OK, response.json()
    assert response.json()["uid"] == str(section.uid)
    assert response.json()["name"] == "shirt department"


@pytest.mark.asyncio
async def test_section_not_fount(client: AsyncClient):
    response = await client.get(f"/{ENDPOINT}/{uuid.uuid4()}")

    assert response.status_code == status.HTTP_404_NOT_FOUND, response.json()
    assert response.json()["detail"] == "section not found."


@pytest.mark.asyncio
async def test_can_update_section(client: AsyncClient, session: AsyncSession):
    department = DepartmentDB(
        name="operations", created_by=uuid.UUID(USER_ID), modified_by=uuid.UUID(USER_ID)
    )
    session.add(department)
    await session.commit()
    await session.refresh(department)
    section = SectionDB(
        name="shirt department",
        department_uid=department.uid,
        created_by=uuid.UUID(USER_ID),
        modified_by=uuid.UUID(USER_ID),
    )
    session.add(section)
    await session.commit()
    await session.refresh(section)

    response = await client.patch(
        f"{ENDPOINT}/{section.uid}",
        json={"name": "garment department", "modified_by": USER_ID},
    )

    assert response.status_code == status.HTTP_200_OK, response.json()
    assert response.json()["uid"] == str(section.uid)
    assert response.json()["name"] == "garment department"
    assert response.json()["modified_by"] == USER_ID


@pytest.mark.asyncio
async def test_delete_section(client: AsyncClient, session: AsyncSession):
    department = DepartmentDB(
        name="operations", created_by=uuid.UUID(USER_ID), modified_by=uuid.UUID(USER_ID)
    )
    session.add(department)
    await session.commit()
    await session.refresh(department)
    section = SectionDB(
        name="shirt department",
        department_uid=department.uid,
        created_by=uuid.UUID(USER_ID),
        modified_by=uuid.UUID(USER_ID),
    )
    session.add(section)
    await session.commit()
    await session.refresh(section)

    response = await client.delete(f"/{ENDPOINT}/{section.uid}")
    assert response.status_code == status.HTTP_204_NO_CONTENT, response.json()
