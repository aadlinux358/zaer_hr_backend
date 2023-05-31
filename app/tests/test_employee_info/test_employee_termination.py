"""Employee termination api tests module."""
import copy
from typing import Final
from uuid import UUID, uuid4

import pytest
from fastapi import status
from httpx import AsyncClient
from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession

from app.models import EmployeeDB
from app.models.employee_info.termination import TerminationDB
from app.tests.test_employee_info.employee_related_data import (
    EMPLOYEE_TEST_DATA,
    initialize_related_tables,
)

ENDPOINT: Final = "terminations"
USER_ID: Final = "38eb651b-bd33-4f9a-beb2-0f9d52d7acc6"


@pytest.mark.asyncio
async def test_create_employee_termination(client: AsyncClient, session: AsyncSession):
    related = await initialize_related_tables(session)
    values = copy.deepcopy(EMPLOYEE_TEST_DATA)
    values.update(is_active=False)
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
            "employee_uid": str(employee.uid),
            "termination_date": "2023-05-29",
        },
    )
    await session.refresh(employee)
    assert response.status_code == status.HTTP_201_CREATED
    assert response.json()["hire_date"] == str(employee.current_hire_date)
    assert employee.is_terminated is True


@pytest.mark.asyncio
async def test_can_not_terminate_active_employee(
    client: AsyncClient, session: AsyncSession
):
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
            "employee_uid": str(employee.uid),
            "termination_date": "2023-05-29",
        },
    )
    await session.refresh(employee)

    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.json()["detail"] == "can not terminate active employee."


@pytest.mark.asyncio
async def test_can_get_terminiation_by_id(client: AsyncClient, session: AsyncSession):
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

    termination = TerminationDB(
        employee_uid=employee.uid,
        hire_date=employee.current_hire_date,
        termination_date="2023-03-01",
        created_by=UUID(USER_ID),
        modified_by=UUID(USER_ID),
    )
    session.add(termination)
    await session.commit()
    await session.refresh(termination)

    response = await client.get(f"{ENDPOINT}/{termination.uid}")

    assert response.status_code == status.HTTP_200_OK
    assert response.json()["uid"] == str(termination.uid)


@pytest.mark.asyncio
async def test_termination_not_found(client: AsyncClient, session: AsyncSession):
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

    termination = TerminationDB(
        employee_uid=employee.uid,
        hire_date=employee.current_hire_date,
        termination_date="2023-03-01",
        created_by=UUID(USER_ID),
        modified_by=UUID(USER_ID),
    )
    session.add(termination)
    await session.commit()
    await session.refresh(termination)

    response = await client.get(f"{ENDPOINT}/{uuid4()}")

    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json()["detail"] == "termination not found."


@pytest.mark.asyncio
async def test_can_read_many_terminations(client: AsyncClient, session: AsyncSession):
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

    termination = TerminationDB(
        employee_uid=employee.uid,
        hire_date=employee.current_hire_date,
        termination_date="2023-03-01",
        created_by=UUID(USER_ID),
        modified_by=UUID(USER_ID),
    )
    session.add(termination)
    await session.commit()
    await session.refresh(termination)

    response = await client.get(f"{ENDPOINT}")

    assert response.status_code == status.HTTP_200_OK
    assert response.json()["count"] == 1
    assert isinstance(response.json()["result"], list)


@pytest.mark.asyncio
async def test_can_update_termination(client: AsyncClient, session: AsyncSession):
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

    termination = TerminationDB(
        employee_uid=employee.uid,
        hire_date=employee.current_hire_date,
        termination_date="2023-03-01",
        created_by=UUID(USER_ID),
        modified_by=UUID(USER_ID),
    )
    session.add(termination)
    await session.commit()
    await session.refresh(termination)

    response = await client.patch(
        f"{ENDPOINT}/{termination.uid}", json={"termination_date": "2023-04-22"}
    )
    await session.refresh(termination)

    assert response.status_code == status.HTTP_200_OK
    assert response.json()["uid"] == str(termination.uid)
    assert response.json()["termination_date"] == str(termination.termination_date)


@pytest.mark.asyncio
async def test_can_delete_termination(client: AsyncClient, session: AsyncSession):
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

    termination = TerminationDB(
        employee_uid=employee.uid,
        hire_date=employee.current_hire_date,
        termination_date="2023-03-01",
        created_by=UUID(USER_ID),
        modified_by=UUID(USER_ID),
    )
    session.add(termination)
    await session.commit()
    await session.refresh(termination)

    response = await client.delete(f"{ENDPOINT}/{termination.uid}")
    stmt = select(TerminationDB).where(TerminationDB.uid == termination.uid)
    result = await session.exec(stmt)  # type: ignore
    termination_db = result.one_or_none()

    assert response.status_code == status.HTTP_204_NO_CONTENT
    assert termination_db is None
