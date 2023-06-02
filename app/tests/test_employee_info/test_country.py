"""Country endpoints tests module."""
import uuid
from typing import Final

import pytest
from fastapi import status
from httpx import AsyncClient
from sqlmodel.ext.asyncio.session import AsyncSession

from app.models import CountryDB

ENDPOINT: Final = "countries"
USER_ID: Final = "38eb651b-bd33-4f9a-beb2-0f9d52d7acc6"


@pytest.mark.asyncio
async def test_can_create_country(client: AsyncClient):
    response = await client.post(
        f"/{ENDPOINT}",
        json={"name": "eritrea"},
    )

    assert response.status_code == status.HTTP_201_CREATED, response.json()
    assert response.json()["name"] == "eritrea"
    assert response.json()["date_created"]
    assert response.json()["date_modified"]


@pytest.mark.asyncio
async def test_country_names_are_lower_cased(client: AsyncClient):
    response = await client.post(
        f"/{ENDPOINT}",
        json={"name": "AmeRicA"},
    )

    assert response.status_code == status.HTTP_201_CREATED, response.json()
    assert response.json()["name"] == "america"


@pytest.mark.asyncio
async def test_can_not_create_duplicate_country_name(
    client: AsyncClient, session: AsyncSession
):
    country = CountryDB(
        name="eritrea", created_by=uuid.UUID(USER_ID), modified_by=uuid.UUID(USER_ID)
    )
    session.add(country)
    await session.commit()

    response = await client.post(
        f"/{ENDPOINT}",
        json={
            "name": "eritrea",
        },
    )
    assert response.status_code == status.HTTP_400_BAD_REQUEST, response.json()
    assert response.json()["detail"] == "duplicate country name."


@pytest.mark.asyncio
async def test_can_get_countries_list(client: AsyncClient, session: AsyncSession):
    countries = [
        CountryDB(
            name="ethiopia",
            created_by=uuid.UUID(USER_ID),
            modified_by=uuid.UUID(USER_ID),
        ),
        CountryDB(
            name="england",
            created_by=uuid.UUID(USER_ID),
            modified_by=uuid.UUID(USER_ID),
        ),
        CountryDB(
            name="mexico",
            created_by=uuid.UUID(USER_ID),
            modified_by=uuid.UUID(USER_ID),
        ),
    ]
    for dep in countries:
        session.add(dep)
    await session.commit()

    response = await client.get(f"/{ENDPOINT}")

    assert response.status_code == status.HTTP_200_OK, response.json()
    assert response.json()["count"] == 3
    assert len(response.json()["result"]) == 3
    assert isinstance(response.json()["result"], list)


@pytest.mark.asyncio
async def test_can_get_country_by_id(client: AsyncClient, session: AsyncSession):
    country = CountryDB(
        name="eritrea", created_by=uuid.UUID(USER_ID), modified_by=uuid.UUID(USER_ID)
    )
    session.add(country)
    await session.commit()
    await session.refresh(country)

    response = await client.get(f"/{ENDPOINT}/{country.uid}")

    assert response.status_code == status.HTTP_200_OK, response.json()
    assert response.json()["uid"] == str(country.uid)
    assert response.json()["name"] == "eritrea"


@pytest.mark.asyncio
async def test_country_not_found(client: AsyncClient):
    response = await client.get(f"/{ENDPOINT}/{uuid.uuid4()}")

    assert response.status_code == status.HTTP_404_NOT_FOUND, response.json()
    assert response.json()["detail"] == "country not found."


@pytest.mark.asyncio
async def test_can_update_country(client: AsyncClient, session: AsyncSession):
    country = CountryDB(
        name="brazil", created_by=uuid.UUID(USER_ID), modified_by=uuid.UUID(USER_ID)
    )
    session.add(country)
    await session.commit()
    await session.refresh(country)

    response = await client.patch(
        f"/{ENDPOINT}/{country.uid}",
        json={"name": "canada"},
    )

    assert response.status_code == status.HTTP_200_OK, response.json()
    assert response.json()["uid"] == str(country.uid)
    assert response.json()["name"] == "canada"
    assert response.json()["date_created"] == country.date_created.isoformat()
    assert response.json()["date_modified"] != country.date_modified.isoformat()
    assert response.json()["modified_by"] == USER_ID


@pytest.mark.asyncio
async def test_delete_country(client: AsyncClient, session: AsyncSession):
    country = CountryDB(
        name="somal", created_by=uuid.UUID(USER_ID), modified_by=uuid.UUID(USER_ID)
    )
    session.add(country)
    await session.commit()
    await session.refresh(country)

    response = await client.delete(f"/{ENDPOINT}/{country.uid}")
    assert response.status_code == status.HTTP_204_NO_CONTENT, response.json()
