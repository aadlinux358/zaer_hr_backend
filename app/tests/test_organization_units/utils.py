"""Organizational units testing utility functions module."""
import uuid
from typing import Final

from sqlalchemy.ext.asyncio.session import AsyncSession

from app.models import DepartmentDB, DivisionDB, UnitDB

USER_ID: Final = "38eb651b-bd33-4f9a-beb2-0f9d52d7acc6"


async def create_test_model(
    model_name: str, session: AsyncSession
) -> DivisionDB | DepartmentDB | UnitDB:
    """Create test models."""
    division = DivisionDB(
        name="operations", created_by=uuid.UUID(USER_ID), modified_by=uuid.UUID(USER_ID)
    )
    session.add(division)
    await session.commit()
    await session.refresh(division)

    if model_name == "division":
        return division

    department = DepartmentDB(
        name="shirt division",
        division_uid=division.uid,
        created_by=uuid.UUID(USER_ID),
        modified_by=uuid.UUID(USER_ID),
    )
    session.add(department)
    await session.commit()
    await session.refresh(department)

    if model_name == "department":
        return department

    unit = UnitDB(
        name="unit one",
        department_uid=department.uid,
        created_by=uuid.UUID(USER_ID),
        modified_by=uuid.UUID(USER_ID),
    )
    session.add(unit)
    await session.commit()
    await session.refresh(unit)

    if model_name == "unit":
        return unit

    raise ValueError("invalid model name")
