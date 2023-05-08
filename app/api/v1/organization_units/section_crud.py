"""Section crud operations module."""
from typing import Optional
from uuid import UUID

from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession

from app.models.organization_units.section import (
    SectionCreate,
    SectionDB,
    SectionReadMany,
    SectionUpdate,
)


class SectionCRUD:
    """Section's database operations."""

    def __init__(self, session: AsyncSession):
        """Database operations initializer."""
        self.session = session

    async def create(self, payload: SectionCreate) -> SectionDB:
        """Create database section."""
        values = payload.dict()

        section = SectionDB(**values)
        self.session.add(section)
        await self.session.commit()
        await self.session.refresh(section)

        return section

    async def read_many(self) -> SectionReadMany:
        """Fetch all sections."""
        statement = select(SectionDB)
        result = await self.session.exec(statement)  # type: ignore
        all_result = result.all()
        return SectionReadMany(count=len(all_result), result=all_result)

    async def read_by_uid(self, section_uid: UUID) -> Optional[SectionDB]:
        """Read section by uid."""
        statement = select(SectionDB).where(SectionDB.uid == section_uid)
        result = await self.session.exec(statement)  # type: ignore
        section = result.one_or_none()

        return section

    async def update_section(
        self, section_uid: UUID, payload: SectionUpdate
    ) -> Optional[SectionDB]:
        """Update section."""
        section = await self.read_by_uid(section_uid)
        if not section:
            return None

        values = payload.dict(exclude_unset=True)
        for k, v in values.items():
            setattr(section, k, v)

        self.session.add(section)
        await self.session.commit()
        await self.session.refresh(section)

        return section

    async def delete_section(self, section_uid: UUID) -> bool:
        """Delete section."""
        section = await self.read_by_uid(section_uid)
        if not section:
            return False
        await self.session.delete(section)
        await self.session.commit()

        return True
