"""Termination database operations module."""
from typing import Optional
from uuid import UUID

from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession

from app.models.employee_info.termination import (
    TerminationCreate,
    TerminationDB,
    TerminationReadMany,
    TerminationUpdate,
)


class TerminationCRUD:
    """Database operations handler class."""

    def __init__(self, session: AsyncSession) -> None:
        """DB operations class initializer."""
        self.session = session

    async def create_termination(
        self, payload: TerminationCreate
    ) -> Optional[TerminationDB]:
        """Create database termination."""
        values = payload.dict()

        termination = TerminationDB(**values)
        self.session.add(termination)
        await self.session.commit()
        await self.session.refresh(termination)

        return termination

    async def read_many(self) -> TerminationReadMany:
        """Fetch all termination records."""
        statement = select(TerminationDB)
        result = await self.session.exec(statement)  # type: ignore
        all_result = result.all()
        return TerminationReadMany(count=len(all_result), result=all_result)

    async def read_many_by_employee(self, employee_uid: UUID) -> TerminationReadMany:
        """Fetch all termination records of an employee."""
        statement = select(TerminationDB).where(
            TerminationDB.employee_uid == employee_uid
        )
        result = await self.session.exec(statement)  # type: ignore
        all_result = result.all()
        return TerminationReadMany(count=len(all_result), result=all_result)

    async def read_by_uid(self, termination_uid: UUID) -> Optional[TerminationDB]:
        """Read termination by uid."""
        statement = select(TerminationDB).where(TerminationDB.uid == termination_uid)
        result = await self.session.exec(statement)  # type: ignore
        termination = result.one_or_none()

        return termination

    async def update_termination(
        self, termination_uid: UUID, payload: TerminationUpdate
    ) -> Optional[TerminationDB]:
        """Update termination."""
        termination = await self.read_by_uid(termination_uid)
        if termination is None:
            return None

        values = payload.dict(exclude_unset=True)
        for k, v in values.items():
            setattr(termination, k, v)

        self.session.add(termination)
        await self.session.commit()
        await self.session.refresh(termination)

        return termination

    async def delete_termination(self, termination_uid: UUID) -> bool:
        """Delete termination."""
        termination = await self.read_by_uid(termination_uid)
        if termination is None:
            return False
        await self.session.delete(termination)
        await self.session.commit()

        return True
