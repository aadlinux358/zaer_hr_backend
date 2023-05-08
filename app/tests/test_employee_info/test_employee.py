"""Employee api tests module."""
import copy
import uuid
from typing import Final

import pytest
from fastapi import status
from httpx import AsyncClient
from sqlmodel.ext.asyncio.session import AsyncSession

from app.models import EmployeeDB

from .employee_related_data import initialize_related_tables

ENDPOINT: Final = "employees"
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
async def test_create_employee(client: AsyncClient, session: AsyncSession):
    related = await initialize_related_tables(session)
    payload = copy.deepcopy(EMPLOYEE_TEST_DATA)
    payload.update(
        designation_uid=str(related["designation"].uid),
        nationality_uid=str(related["nationality"].uid),
        unit_uid=str(related["unit"].uid),
        educational_level_uid=str(related["educational_level"].uid),
    )
    response = await client.post(f"/{ENDPOINT}", json=payload)

    assert response.status_code == status.HTTP_201_CREATED, response.json()
    response_json = response.json()
    for k, v in EMPLOYEE_TEST_DATA.items():
        if isinstance(v, str):
            v = v.lower().strip()
        assert response_json[k] == v


@pytest.mark.asyncio
async def test_duplicate_violation(client: AsyncClient, session: AsyncSession):
    related = await initialize_related_tables(session)
    values = copy.deepcopy(EMPLOYEE_TEST_DATA)
    employee = EmployeeDB(
        **values,
        designation_uid=related["designation"].uid,
        nationality_uid=related["nationality"].uid,
        unit_uid=related["unit"].uid,
        educational_level_uid=related["educational_level"].uid,
    )
    session.add(employee)
    await session.commit()

    payload = copy.deepcopy(EMPLOYEE_TEST_DATA)
    payload.update(
        designation_uid=str(related["designation"].uid),
        nationality_uid=str(related["nationality"].uid),
        unit_uid=str(related["unit"].uid),
        educational_level_uid=str(related["educational_level"].uid),
    )
    response = await client.post(f"/{ENDPOINT}", json=payload)

    assert response.status_code == status.HTTP_400_BAD_REQUEST, response.json()
    assert (
        response.json()["detail"]
        == "integrity error. eg. duplicate field or invalid field value."
    )


@pytest.mark.asyncio
async def test_get_employees_list(client: AsyncClient, session: AsyncSession):
    related = await initialize_related_tables(session)
    emp_one = copy.deepcopy(EMPLOYEE_TEST_DATA)
    emp_one.update(badge_number=1, phone_number="07112244", national_id="7654321`")
    emp_two = copy.deepcopy(EMPLOYEE_TEST_DATA)
    emp_two.update(badge_number=2, phone_number="07112255", national_id="1234567")
    emp_three = copy.deepcopy(EMPLOYEE_TEST_DATA)
    emp_three.update(badge_number=3, phone_number="07112266", national_id="9988776")
    employees = [
        EmployeeDB(
            **emp_one,
            designation_uid=related["designation"].uid,
            nationality_uid=related["nationality"].uid,
            unit_uid=related["unit"].uid,
            educational_level_uid=related["educational_level"].uid,
        ),
        EmployeeDB(
            **emp_two,
            designation_uid=related["designation"].uid,
            nationality_uid=related["nationality"].uid,
            unit_uid=related["unit"].uid,
            educational_level_uid=related["educational_level"].uid,
        ),
        EmployeeDB(
            **emp_three,
            designation_uid=related["designation"].uid,
            nationality_uid=related["nationality"].uid,
            unit_uid=related["unit"].uid,
            educational_level_uid=related["educational_level"].uid,
        ),
    ]
    for employee in employees:
        session.add(employee)
    await session.commit()

    response = await client.get(f"{ENDPOINT}")

    assert response.status_code == status.HTTP_200_OK, response.json()
    assert response.json()["count"] == 3
    assert len(response.json()["result"]) == 3
    assert isinstance(response.json()["result"], list)


@pytest.mark.asyncio
async def test_get_employee_by_uid(client: AsyncClient, session: AsyncSession):
    related = await initialize_related_tables(session)
    values = copy.deepcopy(EMPLOYEE_TEST_DATA)
    employee = EmployeeDB(
        **values,
        designation_uid=related["designation"].uid,
        nationality_uid=related["nationality"].uid,
        unit_uid=related["unit"].uid,
        educational_level_uid=related["educational_level"].uid,
    )
    session.add(employee)
    await session.commit()
    await session.refresh(employee)

    response = await client.get(f"{ENDPOINT}/{employee.uid}")
    assert response.status_code == status.HTTP_200_OK, response.json()
    assert response.json()["uid"] == str(employee.uid)


@pytest.mark.asyncio
async def test_employee_not_found(client: AsyncClient, session: AsyncSession):
    response = await client.get(f"{ENDPOINT}/{uuid.uuid4()}")

    assert response.status_code == status.HTTP_404_NOT_FOUND, response.json()
    assert response.json()["detail"] == "employee not found."


@pytest.mark.asyncio
async def test_can_update_employee(client: AsyncClient, session: AsyncSession):
    related = await initialize_related_tables(session)
    values = copy.deepcopy(EMPLOYEE_TEST_DATA)
    employee = EmployeeDB(
        **values,
        designation_uid=related["designation"].uid,
        nationality_uid=related["nationality"].uid,
        unit_uid=related["unit"].uid,
        educational_level_uid=related["educational_level"].uid,
    )
    session.add(employee)
    await session.commit()
    await session.refresh(employee)

    payload = {"first_name": "john", "phone_number": "07222222", "modified_by": USER_ID}

    response = await client.patch(f"{ENDPOINT}/{employee.uid}", json=payload)

    assert response.status_code == status.HTTP_200_OK, response.json()
    assert response.json()["uid"] == str(employee.uid)
    assert response.json()["first_name"] == "john"
    assert response.json()["phone_number"] == "07222222"
