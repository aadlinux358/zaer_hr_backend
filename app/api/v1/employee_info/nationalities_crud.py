"""Nationality crud operations module."""
from typing import Optional
from uuid import UUID

from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession

from app.models.employee_info.nationalities import (
    NationalityCreate,
    NationalityDB,
    NationalityReadMany,
    NationalityUpdate,
)


class NationalityCRUD:
    """Class defining all database related operations."""

    def __init__(self, session: AsyncSession):
        """Database operations class initializer."""
        self.session = session

    async def create(self, payload: NationalityCreate) -> NationalityDB:
        """Create database nationality."""
        values = payload.dict()

        nationality = NationalityDB(**values)
        self.session.add(nationality)
        await self.session.commit()
        await self.session.refresh(nationality)

        return nationality

    async def read_many(self) -> NationalityReadMany:
        """Fetch all nationalities."""
        statement = select(NationalityDB)
        result = await self.session.exec(statement=statement)  # type: ignore
        all_result = result.all()
        return NationalityReadMany(count=len(all_result), result=all_result)

    async def read_by_uid(self, nationality_uid: UUID) -> Optional[NationalityDB]:
        """Read nationality by id."""
        statement = select(NationalityDB).where(NationalityDB.uid == nationality_uid)
        result = await self.session.exec(statement)  # type: ignore
        nationality = result.one_or_none()

        return nationality

    async def update_nationality(
        self, nationality_uid: UUID, payload: NationalityUpdate
    ) -> Optional[NationalityDB]:
        """Update nationality."""
        nationality = await self.read_by_uid(nationality_uid)
        if not nationality:
            return None

        values = payload.dict(exclude_unset=True)
        for k, v in values.items():
            setattr(nationality, k, v)

        self.session.add(nationality)
        await self.session.commit()
        await self.session.refresh(nationality)

        return nationality

    async def delete_nationality(self, nationality_uid: UUID) -> bool:
        """Delete nationality."""
        nationality = await self.read_by_uid(nationality_uid)
        if not nationality:
            return False
        await self.session.delete(nationality)
        await self.session.commit()

        return True
