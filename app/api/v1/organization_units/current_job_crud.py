"""Current job crud operations module."""
from typing import Optional
from uuid import UUID

from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession

from app.models.organization_units.current_job import (
    CurrentJobCreate,
    CurrentJobDB,
    CurrentJobReadMany,
    CurrentJobUpdate,
)


class CurrentJobCRUD:
    """Class defining all database related operations."""

    def __init__(self, session: AsyncSession) -> None:
        """Database operations class initializer."""
        self.session = session

    async def create(self, payload: CurrentJobCreate) -> CurrentJobDB:
        """Create current job."""
        values = payload.dict()

        current_job = CurrentJobDB(**values)
        self.session.add(current_job)
        await self.session.commit()
        await self.session.refresh(current_job)

        return current_job

    async def read_many(self) -> CurrentJobReadMany:
        """Fetch all current jobs."""
        statement = select(CurrentJobDB)
        result = await self.session.exec(statement)  # type: ignore
        all_result = result.all()
        return CurrentJobReadMany(count=len(all_result), result=all_result)

    async def read_by_uid(self, current_job_uid: UUID) -> Optional[CurrentJobDB]:
        """Read current job by uid."""
        statement = select(CurrentJobDB).where(CurrentJobDB.uid == current_job_uid)
        result = await self.session.exec(statement)  # type: ignore
        current_job = result.one_or_none()

        return current_job

    async def update_current_job(
        self, current_job_uid: UUID, payload: CurrentJobUpdate
    ) -> Optional[CurrentJobDB]:
        """Update current job."""
        current_job = await self.read_by_uid(current_job_uid)
        if not current_job:
            return None

        values = payload.dict(exclude_unset=True)
        for k, v in values.items():
            setattr(current_job, k, v)

        self.session.add(current_job)
        await self.session.commit()
        await self.session.refresh(current_job)

        return current_job

    async def delete_current_job(self, current_job_uid: UUID) -> bool:
        """Delete current job."""
        current_job = await self.read_by_uid(current_job_uid)
        if not current_job:
            return False

        await self.session.delete(current_job)
        await self.session.commit()

        return True
