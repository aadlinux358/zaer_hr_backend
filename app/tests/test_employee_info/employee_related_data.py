"""Setup employee's related tables."""
import uuid
from typing import Any, Final

from sqlmodel.ext.asyncio.session import AsyncSession

from app.models.employee_info.educational_level import EducationalLevelDB
from app.models.employee_info.nationalities import NationalityDB
from app.models.organization_units.current_job import CurrentJobDB
from app.models.organization_units.department import DepartmentDB
from app.models.organization_units.section import SectionDB
from app.models.organization_units.sub_section import SubSectionDB

USER_ID: Final = "38eb651b-bd33-4f9a-beb2-0f9d52d7acc6"


async def initialize_related_tables(session: AsyncSession) -> dict[str, Any]:
    """Initialize employee table related tables."""
    department = DepartmentDB(
        name="department one",
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

    sub_section = SubSectionDB(
        name="sub section one",
        section_uid=section.uid,
        created_by=uuid.UUID(USER_ID),
        modified_by=uuid.UUID(USER_ID),
    )
    session.add(sub_section)
    await session.commit()
    await session.refresh(sub_section)

    current_job = CurrentJobDB(
        title="current job one",
        created_by=uuid.UUID(USER_ID),
        modified_by=uuid.UUID(USER_ID),
    )
    session.add(current_job)
    await session.commit()
    await session.refresh(current_job)

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
        "department": department,
        "section": section,
        "sub_section": sub_section,
        "current_job": current_job,
        "nationality": nationality,
        "educational_level": educational_level,
    }
