"""Sub section endpoints tests module."""
import uuid
from typing import Final

import pytest
from fastapi import status
from httpx import AsyncClient
from sqlmodel.ext.asyncio.session import AsyncSession

from app.models import DepartmentDB, SectionDB
from app.models.organization_units.sub_section import SubSectionDB

ENDPOINT: Final = "sub-sections"
USER_ID: Final = "38eb651b-bd33-4f9a-beb2-0f9d52d7acc6"


@pytest.mark.asyncio
async def test_create_sub_section(client: AsyncClient, session: AsyncSession):
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
        f"{ENDPOINT}",
        json={
            "name": "CuTTing",
            "section_uid": str(section.uid),
            "created_by": USER_ID,
            "modified_by": USER_ID,
        },
    )

    assert response.status_code == status.HTTP_201_CREATED, response.json()
    assert response.json()["name"] == "cutting"
    assert response.json()["section_uid"] == str(section.uid)


@pytest.mark.asyncio
async def test_can_not_create_duplicate_sub_section_name(
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
    sub_section = SubSectionDB(
        name="cutting",
        section_uid=section.uid,
        created_by=uuid.UUID(USER_ID),
        modified_by=uuid.UUID(USER_ID),
    )
    session.add(sub_section)
    await session.commit()
    await session.refresh(sub_section)

    response = await client.post(
        f"{ENDPOINT}",
        json={
            "name": "cutting",
            "section_uid": str(section.uid),
            "created_by": USER_ID,
            "modified_by": USER_ID,
        },
    )

    assert response.status_code == status.HTTP_400_BAD_REQUEST, response.json()
    assert response.json()["detail"] == "duplicate sub section name."


@pytest.mark.asyncio
async def test_can_get_sub_section_list(client: AsyncClient, session: AsyncSession):
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
    sub_sections = [
        SubSectionDB(
            name="cutting",
            section_uid=section.uid,
            created_by=uuid.UUID(USER_ID),
            modified_by=uuid.UUID(USER_ID),
        ),
        SubSectionDB(
            name="assembly line 1",
            section_uid=section.uid,
            created_by=uuid.UUID(USER_ID),
            modified_by=uuid.UUID(USER_ID),
        ),
    ]
    for sub_section in sub_sections:
        session.add(sub_section)
    await session.commit()

    response = await client.get(f"{ENDPOINT}")

    assert response.status_code == status.HTTP_200_OK, response.json()
    assert response.json()["count"] == 2
    assert len(response.json()["result"]) == 2
    assert isinstance(response.json()["result"], list)


@pytest.mark.asyncio
async def test_can_get_sub_section_by_uid(client: AsyncClient, session: AsyncSession):
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
    sub_section = SubSectionDB(
        name="preparation 1",
        section_uid=section.uid,
        created_by=uuid.UUID(USER_ID),
        modified_by=uuid.UUID(USER_ID),
    )
    session.add(sub_section)
    await session.commit()
    await session.refresh(sub_section)

    response = await client.get(f"{ENDPOINT}/{sub_section.uid}")

    assert response.status_code == status.HTTP_200_OK, response.json()
    assert response.json()["uid"] == str(sub_section.uid)
    assert response.json()["name"] == "preparation 1"


@pytest.mark.asyncio
async def test_sub_section_not_found(client: AsyncClient, session: AsyncSession):
    response = await client.get(f"{ENDPOINT}/{uuid.uuid4()}")

    assert response.status_code == status.HTTP_404_NOT_FOUND, response.json()
    assert response.json()["detail"] == "sub section not found."


@pytest.mark.asyncio
async def test_can_update_sub_section(client: AsyncClient, session: AsyncSession):
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
    sub_section = SubSectionDB(
        name="preparation 1",
        section_uid=section.uid,
        created_by=uuid.UUID(USER_ID),
        modified_by=uuid.UUID(USER_ID),
    )
    session.add(sub_section)
    await session.commit()
    await session.refresh(sub_section)

    response = await client.patch(
        f"{ENDPOINT}/{sub_section.uid}",
        json={"name": "preparation 2", "modified_by": USER_ID},
    )

    assert response.status_code == status.HTTP_200_OK, response.json()
    assert response.json()["uid"] == str(sub_section.uid)
    assert response.json()["name"] == "preparation 2"
    assert response.json()["modified_by"] == USER_ID


@pytest.mark.asyncio
async def test_delete_sub_section(client: AsyncClient, session: AsyncSession):
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
    sub_section = SubSectionDB(
        name="preparation 1",
        section_uid=section.uid,
        created_by=uuid.UUID(USER_ID),
        modified_by=uuid.UUID(USER_ID),
    )
    session.add(sub_section)
    await session.commit()
    await session.refresh(sub_section)

    response = await client.delete(f"/{ENDPOINT}/{sub_section.uid}")
    assert response.status_code == status.HTTP_204_NO_CONTENT, response.json()
