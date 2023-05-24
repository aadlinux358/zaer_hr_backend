"""Child endpoints tests module."""
import copy
import uuid
from datetime import date
from typing import Final

import pytest
from fastapi import status
from httpx import AsyncClient
from sqlmodel.ext.asyncio.session import AsyncSession

from app.models.employee_info.child import ChildDB
from app.models.employee_info.employee import EmployeeDB
from app.tests.test_employee_info.employee_related_data import initialize_related_tables

ENDPOINT: Final = "/employee/children"
USER_ID: Final = "38eb651b-bd33-4f9a-beb2-0f9d52d7acc6"
EMPLOYEE_TEST_DATA: Final = {
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
async def test_create_child(client: AsyncClient, session: AsyncSession):
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

    response = await client.post(
        f"{ENDPOINT}",
        json={
            "parent_uid": str(employee.uid),
            "first_name": "SENAY",
            "gender": "m",
            "birth_date": "2015-03-07",
        },
    )

    assert response.status_code == status.HTTP_201_CREATED, response.json()
    assert response.json()["parent_uid"] == str(employee.uid)
    assert response.json()["first_name"] == "senay"
    assert response.json()["gender"] == "m"
    assert response.json()["birth_date"] == "2015-03-07"
    assert response.json()["created_by"] == USER_ID
    assert response.json()["modified_by"] == USER_ID


@pytest.mark.asyncio
async def test_duplicate_child(client: AsyncClient, session: AsyncSession):
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

    child = ChildDB(
        parent_uid=employee.uid,
        first_name="senay",
        birth_date=date(2016, 7, 21),
        gender="m",
        created_by=uuid.UUID(USER_ID),
        modified_by=uuid.UUID(USER_ID),
    )
    session.add(child)
    await session.commit()
    await session.refresh(child)

    child_payload = {
        "parent_uid": str(employee.uid),
        "first_name": "senay",
        "gender": "m",
        "birth_date": "2016-03-07",
    }
    response = await client.post(f"{ENDPOINT}", json=child_payload)

    assert response.status_code == status.HTTP_400_BAD_REQUEST, response.json()
    assert response.json()["detail"] == "duplicate or invalid field information."


@pytest.mark.asyncio
async def test_can_get_employee_children(client: AsyncClient, session: AsyncSession):
    related = await initialize_related_tables(session)
    values = copy.deepcopy(EMPLOYEE_TEST_DATA)
    other_values = copy.deepcopy(EMPLOYEE_TEST_DATA)
    other_values.update(phone_number="22328832", national_id="9923322")
    employee = EmployeeDB(
        **values,
        designation_uid=related["designation"].uid,
        nationality_uid=related["nationality"].uid,
        unit_uid=related["unit"].uid,
        educational_level_uid=related["educational_level"].uid,
    )
    other_employee = EmployeeDB(
        **other_values,
        designation_uid=related["designation"].uid,
        nationality_uid=related["nationality"].uid,
        unit_uid=related["unit"].uid,
        educational_level_uid=related["educational_level"].uid,
    )
    session.add(employee)
    session.add(other_employee)
    await session.commit()
    await session.refresh(employee)
    await session.refresh(other_employee)

    children = [
        ChildDB(
            parent_uid=employee.uid,
            first_name="senay",
            birth_date=date(2016, 7, 21),
            gender="m",
            created_by=uuid.UUID(USER_ID),
            modified_by=uuid.UUID(USER_ID),
        ),
        ChildDB(
            parent_uid=employee.uid,
            first_name="awet",
            birth_date=date(2017, 7, 21),
            gender="m",
            created_by=uuid.UUID(USER_ID),
            modified_by=uuid.UUID(USER_ID),
        ),
        ChildDB(
            parent_uid=employee.uid,
            first_name="yohana",
            birth_date=date(2019, 9, 21),
            gender="f",
            created_by=uuid.UUID(USER_ID),
            modified_by=uuid.UUID(USER_ID),
        ),
        ChildDB(
            parent_uid=other_employee.uid,
            first_name="zemen",
            birth_date=date(2019, 9, 21),
            gender="f",
            created_by=uuid.UUID(USER_ID),
            modified_by=uuid.UUID(USER_ID),
        ),
    ]
    for child in children:
        session.add(child)
    await session.commit()

    response = await client.get(f"{ENDPOINT}/employee-id/{employee.uid}")

    assert response.status_code == status.HTTP_200_OK, response.json()
    assert response.json()["count"] == 3
    assert len(response.json()["result"]) == 3
    assert isinstance(response.json()["result"], list)


@pytest.mark.asyncio
async def test_can_get_child_by_uid(client: AsyncClient, session: AsyncSession):
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

    child = ChildDB(
        parent_uid=employee.uid,
        first_name="meron",
        birth_date=date(2016, 7, 21),
        gender="m",
        created_by=uuid.UUID(USER_ID),
        modified_by=uuid.UUID(USER_ID),
    )
    session.add(child)
    await session.commit()
    await session.refresh(child)

    response = await client.get(f"{ENDPOINT}/child-id/{child.uid}")

    assert response.status_code == status.HTTP_200_OK, response.json()
    assert response.json()["uid"] == str(child.uid)
    assert response.json()["first_name"] == "meron"


@pytest.mark.asyncio
async def test_child_not_found(client: AsyncClient, session: AsyncSession):
    response = await client.get(f"{ENDPOINT}/child-id/{uuid.uuid4()}")

    assert response.status_code == status.HTTP_404_NOT_FOUND, response.json()
    assert response.json()["detail"] == "child not found."


@pytest.mark.asyncio
async def test_update_child(client: AsyncClient, session: AsyncSession):
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

    child = ChildDB(
        parent_uid=employee.uid,
        first_name="meron",
        birth_date=date(2016, 7, 21),
        gender="m",
        created_by=uuid.UUID(USER_ID),
        modified_by=uuid.UUID(USER_ID),
    )
    session.add(child)
    await session.commit()
    await session.refresh(child)

    uuid.uuid4()
    payload = {
        "first_name": "TEMESGEN",
    }

    response = await client.patch(f"{ENDPOINT}/{child.uid}", json=payload)

    assert response.status_code == status.HTTP_200_OK, response.json()
    assert response.json()["uid"] == str(child.uid)
    assert response.json()["first_name"] == "temesgen"
    assert response.json()["modified_by"] == USER_ID


@pytest.mark.asyncio
async def test_delete_child(client: AsyncClient, session: AsyncSession):
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

    child = ChildDB(
        parent_uid=employee.uid,
        first_name="meron",
        birth_date=date(2016, 7, 21),
        gender="m",
        created_by=uuid.UUID(USER_ID),
        modified_by=uuid.UUID(USER_ID),
    )
    session.add(child)
    await session.commit()
    await session.refresh(child)

    response = await client.delete(f"{ENDPOINT}/{child.uid}")

    assert response.status_code == status.HTTP_204_NO_CONTENT, response.json()
