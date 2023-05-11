"""Department crud operations module."""
from typing import Optional
from uuid import UUID

from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession

from app.models import DivisionDB
from app.models.organization_units.department import (
    DepartmentCreate,
    DepartmentDB,
    DepartmentReadMany,
    DepartmentReadManyPrintFormat,
    DepartmentReadPrintFormat,
    DepartmentUpdate,
)


class DepartmentCRUD:
    """Department's database operations."""

    def __init__(self, session: AsyncSession):
        """Database operations initializer."""
        self.session = session

    async def create(self, payload: DepartmentCreate) -> DepartmentDB:
        """Create database department."""
        values = payload.dict()

        department = DepartmentDB(**values)
        self.session.add(department)
        await self.session.commit()
        await self.session.refresh(department)

        return department

    async def read_many(self) -> DepartmentReadMany:
        """Fetch all departments."""
        statement = select(DepartmentDB)
        result = await self.session.exec(statement)  # type: ignore
        all_result = result.all()
        return DepartmentReadMany(count=len(all_result), result=all_result)

    async def read_many_print_format(self) -> DepartmentReadManyPrintFormat:
        """Fetch all departments in print format."""
        statement = select(
            DepartmentDB.uid,
            DepartmentDB.name,
            DivisionDB.name.label("division"),  # type: ignore
            DepartmentDB.created_by,
            DepartmentDB.modified_by,
            DepartmentDB.date_created,
            DepartmentDB.date_modified,
        ).join(
            DivisionDB
        )  # type: ignore
        result = await self.session.execute(statement)
        all_result = result.mappings().all()
        return DepartmentReadManyPrintFormat(count=len(all_result), result=all_result)

    async def read_by_uid(self, department_uid: UUID) -> Optional[DepartmentDB]:
        """Read department by id."""
        statement = select(DepartmentDB).where(DepartmentDB.uid == department_uid)
        result = await self.session.exec(statement)  # type: ignore
        department = result.one_or_none()

        return department

    async def read_by_uid_print_format(
        self, department_uid: UUID
    ) -> Optional[DepartmentReadPrintFormat]:
        """Read department by id for printing."""
        statement = (
            select(
                DepartmentDB.uid,
                DepartmentDB.name,
                DivisionDB.name.label("division"),  # type: ignore
                DepartmentDB.created_by,
                DepartmentDB.modified_by,
                DepartmentDB.date_created,
                DepartmentDB.date_modified,
            )
            .join(DivisionDB)
            .where(DepartmentDB.uid == department_uid)
        )  # type: ignore
        result = await self.session.execute(statement)
        department = result.mappings().one_or_none()
        return department  # type: ignore

    async def update_department(
        self, department_uid: UUID, payload: DepartmentUpdate
    ) -> Optional[DepartmentDB]:
        """Update department."""
        department = await self.read_by_uid(department_uid)
        if not department:
            return None

        values = payload.dict(exclude_unset=True)
        for k, v in values.items():
            setattr(department, k, v)

        self.session.add(department)
        await self.session.commit()
        await self.session.refresh(department)

        return department

    async def delete_department(self, department_uid: UUID) -> bool:
        """Delete department."""
        department = await self.read_by_uid(department_uid)
        if not department:
            return False
        await self.session.delete(department)
        await self.session.commit()

        return True
