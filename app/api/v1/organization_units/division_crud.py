"""Division crud operations module."""
from typing import Optional
from uuid import UUID

from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession

from app.models.organization_units.division import (
    DivisionCreate,
    DivisionDB,
    DivisionReadMany,
    DivisionUpdate,
)


class DivisionCRUD:
    """Class defining all database related operations."""

    def __init__(self, session: AsyncSession):
        """Database operations class initializer."""
        self.session = session

    async def create(self, payload: DivisionCreate) -> DivisionDB:
        """Create database division."""
        values = payload.dict()

        division = DivisionDB(**values)
        self.session.add(division)
        await self.session.commit()
        await self.session.refresh(division)

        return division

    async def read_many(self) -> DivisionReadMany:
        """Fetch all divisions."""
        statement = select(DivisionDB)
        result = await self.session.exec(statement=statement)  # type: ignore
        all_result = result.all()
        return DivisionReadMany(count=len(all_result), result=all_result)

    async def read_by_uid(self, division_uid: UUID) -> Optional[DivisionDB]:
        """Read division by id."""
        statement = select(DivisionDB).where(DivisionDB.uid == division_uid)
        result = await self.session.exec(statement)  # type: ignore
        division = result.one_or_none()

        return division

    async def update_division(
        self, division_uid: UUID, payload: DivisionUpdate
    ) -> Optional[DivisionDB]:
        """Update division."""
        division = await self.read_by_uid(division_uid)
        if not division:
            return None

        values = payload.dict(exclude_unset=True)
        for k, v in values.items():
            setattr(division, k, v)

        self.session.add(division)
        await self.session.commit()
        await self.session.refresh(division)

        return division

    async def delete_division(self, division_uid: UUID) -> bool:
        """Delete division."""
        division = await self.read_by_uid(division_uid)
        if not division:
            return False
        await self.session.delete(division)
        await self.session.commit()

        return True
