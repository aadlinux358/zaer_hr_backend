"""Child database operations module."""
from typing import Optional
from uuid import UUID

from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession

from app.models.employee_info.child import (
    ChildCreate,
    ChildDB,
    ChildReadMany,
    ChildUpdate,
)


class ChildCRUD:
    """Database operations handler class."""

    def __init__(self, session: AsyncSession) -> None:
        """DB operations class initializer."""
        self.session = session

    async def create_child(self, payload: ChildCreate) -> ChildDB:
        """Create database child."""
        values = payload.dict()

        child = ChildDB(**values)
        self.session.add(child)
        await self.session.commit()
        await self.session.refresh(child)

        return child

    async def read_many(self) -> ChildReadMany:
        """Fetch all child records."""
        statement = select(ChildDB)
        result = await self.session.exec(statement)  # type: ignore
        return ChildReadMany(count=len(result.all()), result=result.all())

    async def read_by_uid(self, child_uid: UUID) -> Optional[ChildDB]:
        """Read child by uid."""
        statement = select(ChildDB).where(ChildDB.uid == child_uid)
        result = await self.session.exec(statement)  # type: ignore
        child = result.one_or_none()

        return child

    async def update_child(
        self, child_uid: UUID, payload: ChildUpdate
    ) -> Optional[ChildDB]:
        """Update child."""
        child = await self.read_by_uid(child_uid)
        if child is None:
            return None

        values = payload.dict(exclude_unset=True)
        for k, v in values.items():
            setattr(child, k, v)

        self.session.add(child)
        await self.session.commit()
        await self.session.refresh(child)

        return child

    async def delete_child(self, child_uid: UUID) -> bool:
        """Delete child."""
        child = await self.read_by_uid(child_uid)
        if child is None:
            return False
        await self.session.delete(child)
        await self.session.commit()

        return True
