"""Country crud operations module."""
from typing import Optional
from uuid import UUID

from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession

from app.models.employee_info.country import (
    CountryCreate,
    CountryDB,
    CountryReadMany,
    CountryUpdate,
)


class CountryCRUD:
    """Class defining all database related operations."""

    def __init__(self, session: AsyncSession):
        """Database operations class initializer."""
        self.session = session

    async def create(self, payload: CountryCreate) -> CountryDB:
        """Create database country."""
        values = payload.dict()

        country = CountryDB(**values)
        self.session.add(country)
        await self.session.commit()
        await self.session.refresh(country)

        return country

    async def read_many(self) -> CountryReadMany:
        """Fetch all countries."""
        statement = select(CountryDB)
        result = await self.session.exec(statement=statement)  # type: ignore
        all_result = result.all()
        return CountryReadMany(count=len(all_result), result=all_result)

    async def read_by_uid(self, country_uid: UUID) -> Optional[CountryDB]:
        """Read country by id."""
        statement = select(CountryDB).where(CountryDB.uid == country_uid)
        result = await self.session.exec(statement)  # type: ignore
        country = result.one_or_none()

        return country

    async def update_country(
        self, country_uid: UUID, payload: CountryUpdate
    ) -> Optional[CountryDB]:
        """Update country."""
        country = await self.read_by_uid(country_uid)
        if not country:
            return None

        values = payload.dict(exclude_unset=True)
        for k, v in values.items():
            setattr(country, k, v)

        self.session.add(country)
        await self.session.commit()
        await self.session.refresh(country)

        return country

    async def delete_country(self, country_uid: UUID) -> bool:
        """Delete country."""
        country = await self.read_by_uid(country_uid)
        if not country:
            return False
        await self.session.delete(country)
        await self.session.commit()

        return True
