"""Employee address endpoints test module."""
import copy
import uuid
from typing import Final

import pytest
from fastapi import status
from httpx import AsyncClient
from sqlmodel.ext.asyncio.session import AsyncSession

from app.models.employee_info.address import AddressDB
from app.models.employee_info.employee import EmployeeDB
from app.tests.test_employee_info.employee_related_data import initialize_related_tables

ENDPOINT: Final = "addresses"
USER_ID: Final = "38eb651b-bd33-4f9a-beb2-0f9d52d7acc6"
EMPLOYEE_TEST_DATA: Final = {
    "badge_number": 1234,
    "first_name": "Semere",
    "last_name": "Tewelde",
    "grandfather_name": "Kidane",
    "gender": "m",
    "birth_date": "1980-02-22",
    "current_salary": 3000,
    "current_hire_date": "2015-04-21",
    "birth_place": "asmara",
    "mother_first_name": "abeba",
    "mother_last_name": "mebrahtu",
    "phone_number": "07112233",
    "national_id": "2345677",
    "created_by": USER_ID,
    "modified_by": USER_ID,
}


@pytest.mark.asyncio
async def test_create_address(client: AsyncClient, session: AsyncSession):
    related = await initialize_related_tables(session)
    values = copy.deepcopy(EMPLOYEE_TEST_DATA)
    employee = EmployeeDB(
        **values,
        designation_uid=related["designation"].uid,
        nationality_uid=related["nationality"].uid,
        sub_section_uid=related["sub_section"].uid,
        educational_level_uid=related["educational_level"].uid,
    )
    session.add(employee)
    await session.commit()
    await session.refresh(employee)

    response = await client.post(
        f"{ENDPOINT}",
        json={
            "employee_uid": str(employee.uid),
            "city": "ASMARA",
            "district": "GEZABANDA",
            "created_by": USER_ID,
            "modified_by": USER_ID,
        },
    )

    assert response.status_code == status.HTTP_201_CREATED, response.json()
    assert response.json()["employee_uid"] == str(employee.uid)
    assert response.json()["city"] == "asmara"
    assert response.json()["district"] == "gezabanda"


@pytest.mark.asyncio
async def test_can_get_address_by_uid(client: AsyncClient, session: AsyncSession):
    related = await initialize_related_tables(session)
    values = copy.deepcopy(EMPLOYEE_TEST_DATA)
    employee = EmployeeDB(
        **values,
        designation_uid=related["designation"].uid,
        nationality_uid=related["nationality"].uid,
        sub_section_uid=related["sub_section"].uid,
        educational_level_uid=related["educational_level"].uid,
    )
    session.add(employee)
    await session.commit()
    await session.refresh(employee)

    address = AddressDB(
        employee_uid=employee.uid,
        city="asmara",
        district="gejeret",
        created_by=uuid.UUID(USER_ID),
        modified_by=uuid.UUID(USER_ID),
    )
    session.add(address)
    await session.commit()
    await session.refresh(address)

    response = await client.get(f"{ENDPOINT}/{address.uid}")

    assert response.status_code == status.HTTP_200_OK, response.json()
    assert response.json()["uid"] == str(address.uid)
    assert response.json()["city"] == "asmara"
    assert response.json()["district"] == "gejeret"


@pytest.mark.asyncio
async def test_address_not_found(client: AsyncClient, session: AsyncSession):
    response = await client.get(f"{ENDPOINT}/{uuid.uuid4()}")

    assert response.status_code == status.HTTP_404_NOT_FOUND, response.json()
    assert response.json()["detail"] == "address not found."


@pytest.mark.asyncio
async def test_update_address(client: AsyncClient, session: AsyncSession):
    related = await initialize_related_tables(session)
    values = copy.deepcopy(EMPLOYEE_TEST_DATA)
    employee = EmployeeDB(
        **values,
        designation_uid=related["designation"].uid,
        nationality_uid=related["nationality"].uid,
        sub_section_uid=related["sub_section"].uid,
        educational_level_uid=related["educational_level"].uid,
    )
    session.add(employee)
    await session.commit()
    await session.refresh(employee)

    address = AddressDB(
        employee_uid=employee.uid,
        city="asmara",
        district="gejeret",
        created_by=uuid.UUID(USER_ID),
        modified_by=uuid.UUID(USER_ID),
    )
    session.add(address)
    await session.commit()
    await session.refresh(address)

    response = await client.patch(
        f"{ENDPOINT}/{address.uid}",
        json={"city": "KEREN", "district": "SHEFSHEFIT", "modified_by": USER_ID},
    )

    assert response.status_code == status.HTTP_200_OK, response.json()
    assert response.json()["uid"] == str(address.uid)
    assert response.json()["city"] == "keren"
    assert response.json()["district"] == "shefshefit"


@pytest.mark.asyncio
async def test_delete_address(client: AsyncClient, session: AsyncSession):
    related = await initialize_related_tables(session)
    values = copy.deepcopy(EMPLOYEE_TEST_DATA)
    employee = EmployeeDB(
        **values,
        designation_uid=related["designation"].uid,
        nationality_uid=related["nationality"].uid,
        sub_section_uid=related["sub_section"].uid,
        educational_level_uid=related["educational_level"].uid,
    )
    session.add(employee)
    await session.commit()
    await session.refresh(employee)

    address = AddressDB(
        employee_uid=employee.uid,
        city="asmara",
        district="gejeret",
        created_by=uuid.UUID(USER_ID),
        modified_by=uuid.UUID(USER_ID),
    )
    session.add(address)
    await session.commit()
    await session.refresh(address)

    response = await client.delete(f"{ENDPOINT}/{address.uid}")

    assert response.status_code == status.HTTP_204_NO_CONTENT, response.json()
