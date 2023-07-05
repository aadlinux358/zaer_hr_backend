"""Employee crud operations module."""
from typing import Optional
from uuid import UUID

from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession

from app.api.v1.employee_info.queries import (
    get_employee_relationships_query,
    get_full_emp_info_by_badge_number_query,
    get_full_emp_info_by_uid_query,
)
from app.models.employee_info.employee import (
    EmployeeCreate,
    EmployeeDB,
    EmployeeReadFull,
    EmployeeReadMany,
    EmployeeReadManyFull,
    EmployeeUpdate,
)


class EmployeeCRUD:
    """Class defining all database related operations."""

    def __init__(self, session: AsyncSession) -> None:
        """Database operations class initializer."""
        self.session = session

    async def create_employee(self, payload: EmployeeCreate) -> EmployeeDB:
        """Create employee in the database."""
        values = payload.dict()
        employee = EmployeeDB(**values)
        self.session.add(employee)
        await self.session.commit()
        await self.session.refresh(employee)

        return employee

    async def read_many(self) -> EmployeeReadMany:
        """Read many employee records."""
        statement = select(EmployeeDB)
        result = await self.session.exec(statement)  # type: ignore
        all_result = result.all()

        return EmployeeReadMany(count=len(all_result), result=all_result)

    async def read_many_full_info(self) -> EmployeeReadManyFull:
        """Read many full employee records."""
        statement = get_employee_relationships_query()
        result = await self.session.exec(statement)
        all_result = result.all()

        return EmployeeReadManyFull(count=len(all_result), result=all_result)

    async def read_by_uid(self, employee_uid: UUID) -> Optional[EmployeeDB]:
        """Read employee by uid."""
        statement = select(EmployeeDB).where(EmployeeDB.uid == employee_uid)
        result = await self.session.exec(statement)  # type: ignore
        employee = result.one_or_none()

        return employee

    async def read_full_by_uid(self, employee_uid: UUID) -> Optional[EmployeeReadFull]:
        """Read full employee info by uid."""
        statement = get_full_emp_info_by_uid_query(employee_uid=employee_uid)
        result = await self.session.exec(statement)
        employee = result.one_or_none()
        if employee:
            return EmployeeReadFull(**employee._mapping)
        return employee

    async def read_full_by_badge_number(
        self, badge_number: int
    ) -> Optional[EmployeeReadFull]:
        """Read full employee info by badge number."""
        statement = get_full_emp_info_by_badge_number_query(badge_number=badge_number)
        result = await self.session.exec(statement)
        employee = result.one_or_none()
        if employee:
            return EmployeeReadFull(**employee._mapping)
        return employee

    async def update_employee(
        self, employee_uid: UUID, payload: EmployeeUpdate
    ) -> Optional[EmployeeDB]:
        """Update employee."""
        employee = await self.read_by_uid(employee_uid)
        if employee is None:
            return None

        values = payload.dict(exclude_unset=True)
        for k, v in values.items():
            setattr(employee, k, v)

        self.session.add(employee)
        await self.session.commit()
        await self.session.refresh(employee)

        return employee

    async def delete_employee(self, employee_uid: UUID) -> bool:
        """
        Delete employee.

        Note that this method does not remove the employee from
        the database, instead it marks it as inactive.
        """
        employee = await self.read_by_uid(employee_uid)
        if employee is None:
            return False
        setattr(employee, "is_active", False)

        self.session.add(employee)
        await self.session.commit()

        return True
