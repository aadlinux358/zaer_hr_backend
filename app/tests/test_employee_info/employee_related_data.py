"""Setup employee's related tables."""
import uuid
from typing import Any, Final

from sqlmodel.ext.asyncio.session import AsyncSession

from app.models import (
    DepartmentDB,
    DesignationDB,
    DivisionDB,
    EducationalLevelDB,
    NationalityDB,
    SectionDB,
    UnitDB,
)

USER_ID: Final = "38eb651b-bd33-4f9a-beb2-0f9d52d7acc6"


async def initialize_related_tables(session: AsyncSession) -> dict[str, Any]:
    """Initialize employee table related tables."""
    division = DivisionDB(
        name="division one",
        created_by=uuid.UUID(USER_ID),
        modified_by=uuid.UUID(USER_ID),
    )
    session.add(division)
    await session.commit()
    await session.refresh(division)

    department = DepartmentDB(
        name="section one",
        division_uid=division.uid,
        created_by=uuid.UUID(USER_ID),
        modified_by=uuid.UUID(USER_ID),
    )
    session.add(department)
    await session.commit()
    await session.refresh(department)

    section = SectionDB(
        name="section one",
        department_uid=department.uid,
        created_by=uuid.UUID(USER_ID),
        modified_by=uuid.UUID(USER_ID),
    )
    session.add(section)
    await session.commit()
    await session.refresh(section)

    unit = UnitDB(
        name="unit one",
        section_uid=section.uid,
        created_by=uuid.UUID(USER_ID),
        modified_by=uuid.UUID(USER_ID),
    )
    session.add(unit)
    await session.commit()
    await session.refresh(unit)

    designation = DesignationDB(
        title="designation one",
        created_by=uuid.UUID(USER_ID),
        modified_by=uuid.UUID(USER_ID),
    )
    session.add(designation)
    await session.commit()
    await session.refresh(designation)

    nationality = NationalityDB(
        name="eritrean", created_by=uuid.UUID(USER_ID), modified_by=uuid.UUID(USER_ID)
    )
    session.add(nationality)
    await session.commit()
    await session.refresh(nationality)

    educational_level = EducationalLevelDB(
        level="10th", created_by=uuid.UUID(USER_ID), modified_by=uuid.UUID(USER_ID)
    )
    session.add(educational_level)
    await session.commit()
    await session.refresh(educational_level)

    return {
        "division": division,
        "department": department,
        "section": section,
        "unit": unit,
        "designation": designation,
        "nationality": nationality,
        "educational_level": educational_level,
    }
