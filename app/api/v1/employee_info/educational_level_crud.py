"""Educational level crud operations module."""
from typing import Optional
from uuid import UUID

from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession

from app.models.employee_info.educational_level import (
    EducationalLevelCreate,
    EducationalLevelDB,
    EducationalLevelReadMany,
    EducationalLevelUpdate,
)


class EducationalLevelCRUD:
    """Class defining all database related operations."""

    def __init__(self, session: AsyncSession):
        """Database operations class initializer."""
        self.session = session

    async def create(self, payload: EducationalLevelCreate) -> EducationalLevelDB:
        """Create database educational_level."""
        values = payload.dict()

        educational_level = EducationalLevelDB(**values)
        self.session.add(educational_level)
        await self.session.commit()
        await self.session.refresh(educational_level)

        return educational_level

    async def read_many(self) -> EducationalLevelReadMany:
        """Fetch all educational levels."""
        statement = select(EducationalLevelDB)
        result = await self.session.exec(statement=statement)  # type: ignore
        return EducationalLevelReadMany(count=len(result.all()), result=result.all())

    async def read_by_uid(
        self, educational_level_uid: UUID
    ) -> Optional[EducationalLevelDB]:
        """Read educational level by uid."""
        statement = select(EducationalLevelDB).where(
            EducationalLevelDB.uid == educational_level_uid
        )
        result = await self.session.exec(statement)  # type: ignore
        educational_level = result.one_or_none()

        return educational_level

    async def update_educational_level(
        self, educational_level_uid: UUID, payload: EducationalLevelUpdate
    ) -> Optional[EducationalLevelDB]:
        """Update educational level."""
        educational_level = await self.read_by_uid(educational_level_uid)
        if not educational_level:
            return None

        values = payload.dict(exclude_unset=True)
        for k, v in values.items():
            setattr(educational_level, k, v)

        self.session.add(educational_level)
        await self.session.commit()
        await self.session.refresh(educational_level)

        return educational_level

    async def delete_educational_level(self, educational_level_uid: UUID) -> bool:
        """Delete educational level."""
        educational_level = await self.read_by_uid(educational_level_uid)
        if not educational_level:
            return False
        await self.session.delete(educational_level)
        await self.session.commit()

        return True
