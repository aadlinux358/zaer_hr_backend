"""Designation crud operations module."""
from typing import Optional
from uuid import UUID

from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession

from app.models.organization_units.designation import (
    DesignationCreate,
    DesignationDB,
    DesignationReadMany,
    DesignationUpdate,
)


class DesignationCRUD:
    """Class defining all database related operations."""

    def __init__(self, session: AsyncSession) -> None:
        """Database operations class initializer."""
        self.session = session

    async def create(self, payload: DesignationCreate) -> DesignationDB:
        """Create designation."""
        values = payload.dict()

        designation = DesignationDB(**values)
        self.session.add(designation)
        await self.session.commit()
        await self.session.refresh(designation)

        return designation

    async def read_many(self) -> DesignationReadMany:
        """Fetch all designations."""
        statement = select(DesignationDB)
        result = await self.session.exec(statement)  # type: ignore
        all_result = result.all()
        return DesignationReadMany(count=len(all_result), result=all_result)

    async def read_by_uid(self, designation_uid: UUID) -> Optional[DesignationDB]:
        """Read designation by uid."""
        statement = select(DesignationDB).where(DesignationDB.uid == designation_uid)
        result = await self.session.exec(statement)  # type: ignore
        designation = result.one_or_none()

        return designation

    async def update_designation(
        self, designation_uid: UUID, payload: DesignationUpdate
    ) -> Optional[DesignationDB]:
        """Update designation."""
        designation = await self.read_by_uid(designation_uid)
        if not designation:
            return None

        values = payload.dict(exclude_unset=True)
        for k, v in values.items():
            setattr(designation, k, v)

        self.session.add(designation)
        await self.session.commit()
        await self.session.refresh(designation)

        return designation

    async def delete_designation(self, designation_uid: UUID) -> bool:
        """Delete designation."""
        designation = await self.read_by_uid(designation_uid)
        if not designation:
            return False

        await self.session.delete(designation)
        await self.session.commit()

        return True
