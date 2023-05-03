"""Sub section crud operations module."""
from typing import Optional
from uuid import UUID

from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession

from app.models.organization_units.sub_section import (
    SubSectionCreate,
    SubSectionDB,
    SubSectionReadMany,
    SubSectionUpdate,
)


class SubSectionCRUD:
    """Sub section's database operations."""

    def __init__(self, session: AsyncSession):
        """Database operations initializer."""
        self.session = session

    async def create(self, payload: SubSectionCreate) -> SubSectionDB:
        """Create database sub section."""
        values = payload.dict()

        sub_section = SubSectionDB(**values)
        self.session.add(sub_section)
        await self.session.commit()
        await self.session.refresh(sub_section)

        return sub_section

    async def read_many(self) -> SubSectionReadMany:
        """Fetch all sub sections."""
        statement = select(SubSectionDB)
        result = await self.session.exec(statement)  # type: ignore
        all_result = result.all()
        return SubSectionReadMany(count=len(all_result), result=all_result)

    async def read_by_uid(self, sub_section_uid: UUID) -> Optional[SubSectionDB]:
        """Read sub_section by uid."""
        statement = select(SubSectionDB).where(SubSectionDB.uid == sub_section_uid)
        result = await self.session.exec(statement)  # type: ignore
        sub_section = result.one_or_none()

        return sub_section

    async def update_sub_section(
        self, sub_section_uid: UUID, payload: SubSectionUpdate
    ) -> Optional[SubSectionDB]:
        """Update sub section."""
        sub_section = await self.read_by_uid(sub_section_uid)
        if not sub_section:
            return None

        values = payload.dict(exclude_unset=True)
        for k, v in values.items():
            setattr(sub_section, k, v)

        self.session.add(sub_section)
        await self.session.commit()
        await self.session.refresh(sub_section)

        return sub_section

    async def delete_sub_section(self, sub_section_uid: UUID) -> bool:
        """Delete sub section."""
        sub_section = await self.read_by_uid(sub_section_uid)
        if not sub_section:
            return False
        await self.session.delete(sub_section)
        await self.session.commit()

        return True
