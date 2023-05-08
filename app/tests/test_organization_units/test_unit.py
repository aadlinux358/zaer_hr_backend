"""Unit endpoints tests module."""
import uuid
from typing import Final

import pytest
from fastapi import status
from httpx import AsyncClient
from sqlmodel.ext.asyncio.session import AsyncSession

from app.models import DepartmentDB, DivisionDB, SectionDB, UnitDB

ENDPOINT: Final = "units"
USER_ID: Final = "38eb651b-bd33-4f9a-beb2-0f9d52d7acc6"


@pytest.mark.asyncio
async def test_create_unit(client: AsyncClient, session: AsyncSession):
    division = DivisionDB(
        name="operations", created_by=uuid.UUID(USER_ID), modified_by=uuid.UUID(USER_ID)
    )
    session.add(division)
    await session.commit()
    await session.refresh(division)
    department = DepartmentDB(
        name="shirt division",
        division_uid=division.uid,
        created_by=uuid.UUID(USER_ID),
        modified_by=uuid.UUID(USER_ID),
    )
    session.add(department)
    await session.commit()
    await session.refresh(department)
    section = SectionDB(
        name="section one",
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
        },
    )

    assert response.status_code == status.HTTP_201_CREATED, response.json()
    assert response.json()["name"] == "cutting"
    assert response.json()["section_uid"] == str(section.uid)
    assert response.json()["modified_by"] == USER_ID
    assert response.json()["created_by"] == USER_ID


@pytest.mark.asyncio
async def test_can_not_create_duplicate_unit_name(
    client: AsyncClient, session: AsyncSession
):
    division = DivisionDB(
        name="operations", created_by=uuid.UUID(USER_ID), modified_by=uuid.UUID(USER_ID)
    )
    session.add(division)
    await session.commit()
    await session.refresh(division)
    department = DepartmentDB(
        name="shirt division",
        division_uid=division.uid,
        created_by=uuid.UUID(USER_ID),
        modified_by=uuid.UUID(USER_ID),
    )
    session.add(department)
    await session.commit()
    await session.refresh(department)
    section = SectionDB(
        name="cutting",
        department_uid=department.uid,
        created_by=uuid.UUID(USER_ID),
        modified_by=uuid.UUID(USER_ID),
    )
    session.add(section)
    await session.commit()
    await session.refresh(section)

    unit = UnitDB(
        name="unit one",
        section_uid=section.uid,
        created_by=uuid.UUID(USER_ID),
        modified_by=uuid.UUID(USER_ID),
    )
    session.add(unit)
    await session.commit()
    await session.refresh(unit)

    response = await client.post(
        f"{ENDPOINT}",
        json={
            "name": "unit one",
            "section_uid": str(section.uid),
        },
    )

    assert response.status_code == status.HTTP_400_BAD_REQUEST, response.json()
    assert response.json()["detail"] == "duplicate unit name."


@pytest.mark.asyncio
async def test_can_get_unit_list(client: AsyncClient, session: AsyncSession):
    division = DivisionDB(
        name="operations", created_by=uuid.UUID(USER_ID), modified_by=uuid.UUID(USER_ID)
    )
    session.add(division)
    await session.commit()
    await session.refresh(division)
    department = DepartmentDB(
        name="shirt division",
        division_uid=division.uid,
        created_by=uuid.UUID(USER_ID),
        modified_by=uuid.UUID(USER_ID),
    )
    session.add(department)
    await session.commit()
    await session.refresh(department)
    section = SectionDB(
        name="cutting",
        department_uid=department.uid,
        created_by=uuid.UUID(USER_ID),
        modified_by=uuid.UUID(USER_ID),
    )

    session.add(section)
    await session.commit()
    await session.refresh(section)
    units = [
        UnitDB(
            name="unit one",
            section_uid=section.uid,
            created_by=uuid.UUID(USER_ID),
            modified_by=uuid.UUID(USER_ID),
        ),
        UnitDB(
            name="unit two",
            section_uid=section.uid,
            created_by=uuid.UUID(USER_ID),
            modified_by=uuid.UUID(USER_ID),
        ),
    ]
    for unit in units:
        session.add(unit)
    await session.commit()

    response = await client.get(f"{ENDPOINT}")

    assert response.status_code == status.HTTP_200_OK, response.json()
    assert response.json()["count"] == 2
    assert len(response.json()["result"]) == 2
    assert isinstance(response.json()["result"], list)


@pytest.mark.asyncio
async def test_can_get_unit_by_uid(client: AsyncClient, session: AsyncSession):
    division = DivisionDB(
        name="operations", created_by=uuid.UUID(USER_ID), modified_by=uuid.UUID(USER_ID)
    )
    session.add(division)
    await session.commit()
    await session.refresh(division)
    department = DepartmentDB(
        name="shirt division",
        division_uid=division.uid,
        created_by=uuid.UUID(USER_ID),
        modified_by=uuid.UUID(USER_ID),
    )
    session.add(department)
    await session.commit()
    await session.refresh(department)
    section = SectionDB(
        name="preparation 1",
        department_uid=department.uid,
        created_by=uuid.UUID(USER_ID),
        modified_by=uuid.UUID(USER_ID),
    )
    session.add(section)
    await session.commit()
    await session.refresh(section)
    unit = UnitDB(
        name="unit one",
        section_uid=section.uid,
        created_by=uuid.UUID(USER_ID),
        modified_by=uuid.UUID(USER_ID),
    )
    session.add(unit)
    await session.commit()
    await session.refresh(unit)

    response = await client.get(f"{ENDPOINT}/{unit.uid}")

    assert response.status_code == status.HTTP_200_OK, response.json()
    assert response.json()["uid"] == str(unit.uid)
    assert response.json()["name"] == "unit one"


@pytest.mark.asyncio
async def test_unit_not_found(client: AsyncClient, session: AsyncSession):
    response = await client.get(f"{ENDPOINT}/{uuid.uuid4()}")

    assert response.status_code == status.HTTP_404_NOT_FOUND, response.json()
    assert response.json()["detail"] == "unit not found."


@pytest.mark.asyncio
async def test_can_update_unit(client: AsyncClient, session: AsyncSession):
    division = DivisionDB(
        name="operations", created_by=uuid.UUID(USER_ID), modified_by=uuid.UUID(USER_ID)
    )
    session.add(division)
    await session.commit()
    await session.refresh(division)
    department = DepartmentDB(
        name="shirt division",
        division_uid=division.uid,
        created_by=uuid.UUID(USER_ID),
        modified_by=uuid.UUID(USER_ID),
    )
    session.add(department)
    await session.commit()
    await session.refresh(department)
    section = SectionDB(
        name="preparation 1",
        department_uid=department.uid,
        created_by=uuid.UUID(USER_ID),
        modified_by=uuid.UUID(USER_ID),
    )
    session.add(section)
    await session.commit()
    await session.refresh(section)
    unit = UnitDB(
        name="unit one",
        section_uid=section.uid,
        created_by=uuid.UUID(USER_ID),
        modified_by=uuid.UUID(USER_ID),
    )
    session.add(unit)
    await session.commit()
    await session.refresh(unit)

    response = await client.patch(
        f"{ENDPOINT}/{unit.uid}",
        json={"name": "preparation 2"},
    )

    assert response.status_code == status.HTTP_200_OK, response.json()
    assert response.json()["uid"] == str(unit.uid)
    assert response.json()["name"] == "preparation 2"
    assert response.json()["modified_by"] == USER_ID


@pytest.mark.asyncio
async def test_delete_unit(client: AsyncClient, session: AsyncSession):
    division = DivisionDB(
        name="operations", created_by=uuid.UUID(USER_ID), modified_by=uuid.UUID(USER_ID)
    )
    session.add(division)
    await session.commit()
    await session.refresh(division)
    department = DepartmentDB(
        name="shirt division",
        division_uid=division.uid,
        created_by=uuid.UUID(USER_ID),
        modified_by=uuid.UUID(USER_ID),
    )
    session.add(department)
    await session.commit()
    await session.refresh(department)
    section = SectionDB(
        name="preparation 1",
        department_uid=department.uid,
        created_by=uuid.UUID(USER_ID),
        modified_by=uuid.UUID(USER_ID),
    )
    session.add(section)
    await session.commit()
    await session.refresh(section)
    unit = UnitDB(
        name="unit one",
        section_uid=section.uid,
        created_by=uuid.UUID(USER_ID),
        modified_by=uuid.UUID(USER_ID),
    )
    session.add(unit)
    await session.commit()
    await session.refresh(unit)

    response = await client.delete(f"/{ENDPOINT}/{unit.uid}")
    assert response.status_code == status.HTTP_204_NO_CONTENT, response.json()
