"""Unit crud operations module."""
from typing import Optional
from uuid import UUID

from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession

from app.models.organization_units.unit import (
    UnitCreate,
    UnitDB,
    UnitReadMany,
    UnitUpdate,
)


class UnitCRUD:
    """Unit's database operations."""

    def __init__(self, session: AsyncSession):
        """Database operations initializer."""
        self.session = session

    async def create(self, payload: UnitCreate) -> UnitDB:
        """Create database unit."""
        values = payload.dict()

        unit = UnitDB(**values)
        self.session.add(unit)
        await self.session.commit()
        await self.session.refresh(unit)

        return unit

    async def read_many(self) -> UnitReadMany:
        """Fetch all units."""
        statement = select(UnitDB)
        result = await self.session.exec(statement)  # type: ignore
        all_result = result.all()
        return UnitReadMany(count=len(all_result), result=all_result)

    async def read_by_uid(self, unit_uid: UUID) -> Optional[UnitDB]:
        """Read unit by uid."""
        statement = select(UnitDB).where(UnitDB.uid == unit_uid)
        result = await self.session.exec(statement)  # type: ignore
        unit = result.one_or_none()

        return unit

    async def update_unit(
        self, unit_uid: UUID, payload: UnitUpdate
    ) -> Optional[UnitDB]:
        """Update unit."""
        unit = await self.read_by_uid(unit_uid)
        if not unit:
            return None

        values = payload.dict(exclude_unset=True)
        for k, v in values.items():
            setattr(unit, k, v)

        self.session.add(unit)
        await self.session.commit()
        await self.session.refresh(unit)

        return unit

    async def delete_unit(self, unit_uid: UUID) -> bool:
        """Delete unit."""
        unit = await self.read_by_uid(unit_uid)
        if not unit:
            return False
        await self.session.delete(unit)
        await self.session.commit()

        return True
