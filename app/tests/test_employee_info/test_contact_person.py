"""Employee contact person endpoints test module."""
import copy
import uuid
from typing import Final

import pytest
from fastapi import status
from httpx import AsyncClient
from sqlmodel.ext.asyncio.session import AsyncSession

from app.models.employee_info.contact_person import ContactPersonDB
from app.models.employee_info.employee import EmployeeDB
from app.tests.test_employee_info.employee_related_data import (
    EMPLOYEE_TEST_DATA,
    initialize_related_tables,
)

ENDPOINT: Final = "employee/contact-persons"
USER_ID: Final = "38eb651b-bd33-4f9a-beb2-0f9d52d7acc6"


@pytest.mark.asyncio
async def test_create_contact_person(client: AsyncClient, session: AsyncSession):
    related = await initialize_related_tables(session)
    values = copy.deepcopy(EMPLOYEE_TEST_DATA)
    employee = EmployeeDB(
        **values,
        designation_uid=related["designation"].uid,
        nationality_uid=related["nationality"].uid,
        section_uid=related["section"].uid,
        educational_level_uid=related["educational_level"].uid,
        country_uid=related["country"].uid,
    )
    session.add(employee)
    await session.commit()
    await session.refresh(employee)

    response = await client.post(
        f"{ENDPOINT}",
        json={
            "employee_uid": str(employee.uid),
            "first_name": "SAMUEL",
            "last_name": "TESFAY",
            "phone_number": "07999888",
            "relationship_to_employee": "brother",
        },
    )

    assert response.status_code == status.HTTP_201_CREATED, response.json()
    assert response.json()["employee_uid"] == str(employee.uid)
    assert response.json()["first_name"] == "samuel"
    assert response.json()["last_name"] == "tesfay"
    assert response.json()["phone_number"] == "07999888"
    assert response.json()["relationship_to_employee"] == "brother"
    assert response.json()["created_by"] == USER_ID
    assert response.json()["modified_by"] == USER_ID


@pytest.mark.asyncio
async def test_can_get_contact_person_by_uid(
    client: AsyncClient, session: AsyncSession
):
    related = await initialize_related_tables(session)
    values = copy.deepcopy(EMPLOYEE_TEST_DATA)
    employee = EmployeeDB(
        **values,
        designation_uid=related["designation"].uid,
        nationality_uid=related["nationality"].uid,
        section_uid=related["section"].uid,
        educational_level_uid=related["educational_level"].uid,
        country_uid=related["country"].uid,
    )
    session.add(employee)
    await session.commit()
    await session.refresh(employee)

    contact_person = ContactPersonDB(
        employee_uid=employee.uid,
        first_name="mikyas",
        last_name="yonas",
        phone_number="07323232",
        relationship_to_employee="brother",
        created_by=uuid.UUID(USER_ID),
        modified_by=uuid.UUID(USER_ID),
    )
    session.add(contact_person)
    await session.commit()
    await session.refresh(contact_person)

    response = await client.get(f"{ENDPOINT}/contact-id/{contact_person.uid}")

    assert response.status_code == status.HTTP_200_OK, response.json()
    assert response.json()["uid"] == str(contact_person.uid)
    assert response.json()["first_name"] == "mikyas"
    assert response.json()["last_name"] == "yonas"


@pytest.mark.asyncio
async def test_contact_person_not_found(client: AsyncClient, session: AsyncSession):
    response = await client.get(f"{ENDPOINT}/contact-id/{uuid.uuid4()}")

    assert response.status_code == status.HTTP_404_NOT_FOUND, response.json()
    assert response.json()["detail"] == "contact person not found."


@pytest.mark.asyncio
async def test_update_contact_person(client: AsyncClient, session: AsyncSession):
    related = await initialize_related_tables(session)
    values = copy.deepcopy(EMPLOYEE_TEST_DATA)
    employee = EmployeeDB(
        **values,
        designation_uid=related["designation"].uid,
        nationality_uid=related["nationality"].uid,
        section_uid=related["section"].uid,
        educational_level_uid=related["educational_level"].uid,
        country_uid=related["country"].uid,
    )
    session.add(employee)
    await session.commit()
    await session.refresh(employee)

    contact_person = ContactPersonDB(
        employee_uid=employee.uid,
        first_name="mikyas",
        last_name="yonas",
        phone_number="07323232",
        relationship_to_employee="brother",
        created_by=uuid.UUID(USER_ID),
        modified_by=uuid.UUID(USER_ID),
    )
    session.add(contact_person)
    await session.commit()
    await session.refresh(contact_person)

    response = await client.patch(
        f"{ENDPOINT}/{contact_person.uid}",
        json={
            "first_name": "AMILAK",
            "last_name": "mihretab",
        },
    )

    assert response.status_code == status.HTTP_200_OK, response.json()
    assert response.json()["uid"] == str(contact_person.uid)
    assert response.json()["first_name"] == "amilak"
    assert response.json()["last_name"] == "mihretab"
    assert response.json()["modified_by"] == USER_ID


@pytest.mark.asyncio
async def test_delete_contact_person(client: AsyncClient, session: AsyncSession):
    related = await initialize_related_tables(session)
    values = copy.deepcopy(EMPLOYEE_TEST_DATA)
    employee = EmployeeDB(
        **values,
        designation_uid=related["designation"].uid,
        nationality_uid=related["nationality"].uid,
        section_uid=related["section"].uid,
        educational_level_uid=related["educational_level"].uid,
        country_uid=related["country"].uid,
    )
    session.add(employee)
    await session.commit()
    await session.refresh(employee)

    contact_person = ContactPersonDB(
        employee_uid=employee.uid,
        first_name="mikyas",
        last_name="yonas",
        phone_number="07323232",
        relationship_to_employee="brother",
        created_by=uuid.UUID(USER_ID),
        modified_by=uuid.UUID(USER_ID),
    )
    session.add(contact_person)
    await session.commit()
    await session.refresh(contact_person)

    response = await client.delete(f"{ENDPOINT}/{contact_person.uid}")

    assert response.status_code == status.HTTP_204_NO_CONTENT, response.json()
