"""Department endpoints tests module."""
import uuid
from typing import Final

import pytest
from fastapi import status
from httpx import AsyncClient
from sqlmodel.ext.asyncio.session import AsyncSession

from app.models.organization_units.department import DepartmentDB
from app.tests.test_organization_units.utils import create_test_model

ENDPOINT: Final = "departments"
USER_ID: Final = "38eb651b-bd33-4f9a-beb2-0f9d52d7acc6"


@pytest.mark.asyncio
async def test_create_department(client: AsyncClient, session: AsyncSession):
    division = await create_test_model("division", session)

    response = await client.post(
        f"/{ENDPOINT}",
        json={
            "name": "shirt division",
            "division_uid": str(division.uid),
        },
    )

    assert response.status_code == status.HTTP_201_CREATED, response.json()
    assert response.json()["name"] == "shirt division"


@pytest.mark.asyncio
async def test_department_names_are_lower_cased(
    client: AsyncClient, session: AsyncSession
):
    division = await create_test_model("division", session)

    response = await client.post(
        f"/{ENDPOINT}",
        json={
            "name": "UPPERCASE",
            "division_uid": str(division.uid),
        },
    )

    assert response.status_code == status.HTTP_201_CREATED, response.json()
    assert response.json()["name"] == "uppercase"


@pytest.mark.asyncio
async def test_can_not_create_duplicate_department_name(
    client: AsyncClient, session: AsyncSession
):
    division = await create_test_model("division", session)

    department = DepartmentDB(
        name="shirt division",
        division_uid=division.uid,
        created_by=uuid.UUID(USER_ID),
        modified_by=uuid.UUID(USER_ID),
    )
    session.add(department)
    await session.commit()
    await session.refresh(department)

    response = await client.post(
        f"/{ENDPOINT}",
        json={
            "name": "shirt division",
            "division_uid": str(division.uid),
        },
    )

    assert response.status_code == status.HTTP_400_BAD_REQUEST, response.json()
    assert response.json()["detail"] == "duplicate department name."


@pytest.mark.asyncio
async def test_can_get_department_list(client: AsyncClient, session: AsyncSession):
    division = await create_test_model("division", session)

    departments = [
        DepartmentDB(
            name="shirt division",
            division_uid=division.uid,
            created_by=uuid.UUID(USER_ID),
            modified_by=uuid.UUID(USER_ID),
        ),
        DepartmentDB(
            name="garment division",
            division_uid=division.uid,
            created_by=uuid.UUID(USER_ID),
            modified_by=uuid.UUID(USER_ID),
        ),
    ]

    for department in departments:
        session.add(department)

    await session.commit()

    response = await client.get(f"{ENDPOINT}")

    assert response.status_code == status.HTTP_200_OK, response.json()
    assert response.json()["count"] == 2
    assert len(response.json()["result"]) == 2
    assert isinstance(response.json()["result"], list)


@pytest.mark.asyncio
async def test_can_get_department_by_uid(client: AsyncClient, session: AsyncSession):
    division = await create_test_model("division", session)

    department = DepartmentDB(
        name="shirt division",
        division_uid=division.uid,
        created_by=uuid.UUID(USER_ID),
        modified_by=uuid.UUID(USER_ID),
    )
    session.add(department)
    await session.commit()
    await session.refresh(department)

    response = await client.get(f"/{ENDPOINT}/{department.uid}")

    assert response.status_code == status.HTTP_200_OK, response.json()
    assert response.json()["uid"] == str(department.uid)
    assert response.json()["name"] == "shirt division"


@pytest.mark.asyncio
async def test_department_not_fount(client: AsyncClient):
    response = await client.get(f"/{ENDPOINT}/{uuid.uuid4()}")

    assert response.status_code == status.HTTP_404_NOT_FOUND, response.json()
    assert response.json()["detail"] == "department not found."


@pytest.mark.asyncio
async def test_can_update_department(client: AsyncClient, session: AsyncSession):
    division = await create_test_model("division", session)

    department = DepartmentDB(
        name="shirt division",
        division_uid=division.uid,
        created_by=uuid.UUID(USER_ID),
        modified_by=uuid.UUID(USER_ID),
    )
    session.add(department)
    await session.commit()
    await session.refresh(department)

    response = await client.patch(
        f"{ENDPOINT}/{department.uid}",
        json={"name": "garment division"},
    )

    assert response.status_code == status.HTTP_200_OK, response.json()
    assert response.json()["uid"] == str(department.uid)
    assert response.json()["name"] == "garment division"
    assert response.json()["modified_by"] == USER_ID


@pytest.mark.asyncio
async def test_delete_department(client: AsyncClient, session: AsyncSession):
    division = await create_test_model("division", session)

    department = DepartmentDB(
        name="shirt division",
        division_uid=division.uid,
        created_by=uuid.UUID(USER_ID),
        modified_by=uuid.UUID(USER_ID),
    )
    session.add(department)
    await session.commit()
    await session.refresh(department)

    response = await client.delete(f"/{ENDPOINT}/{department.uid}")
    assert response.status_code == status.HTTP_204_NO_CONTENT, response.json()


@pytest.mark.asyncio
async def test_download_csv(client: AsyncClient):
    response = await client.get(f"{ENDPOINT}/download/csv")

    assert response.status_code == status.HTTP_200_OK
    assert "text/csv" in response.headers["Content-Type"]


@pytest.mark.asyncio
async def test_download_excel(client: AsyncClient):
    response = await client.get(f"{ENDPOINT}/download/xlsx")

    assert response.status_code == status.HTTP_200_OK
    assert (
        "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        in response.headers["Content-Type"]
    )
