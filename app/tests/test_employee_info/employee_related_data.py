"""Setup employee's related tables."""
import uuid
from typing import Any, Final

from sqlmodel.ext.asyncio.session import AsyncSession

from app.models import (
    CountryDB,
    DepartmentDB,
    DesignationDB,
    DivisionDB,
    EducationalLevelDB,
    NationalityDB,
    SectionDB,
    UnitDB,
)

USER_ID: Final = "38eb651b-bd33-4f9a-beb2-0f9d52d7acc6"

EMPLOYEE_TEST_DATA: Final = {
    "first_name": "Semere",
    "last_name": "Tewelde",
    "grandfather_name": "Kidane",
    "gender": "m",
    "birth_date": "1980-02-22",
    "current_salary": 3000,
    "current_hire_date": "2015-04-21",
    "birth_place": "asmara",
    "mother_first_name": "abeba",
    "mother_last_name": "mebrahtu",
    "phone_number": "07112233",
    "national_id": "2345677",
    "created_by": USER_ID,
    "modified_by": USER_ID,
}


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

    unit = UnitDB(
        name="unit one",
        department_uid=department.uid,
        created_by=uuid.UUID(USER_ID),
        modified_by=uuid.UUID(USER_ID),
    )
    session.add(unit)
    await session.commit()
    await session.refresh(unit)

    section = SectionDB(
        name="section one",
        unit_uid=unit.uid,
        created_by=uuid.UUID(USER_ID),
        modified_by=uuid.UUID(USER_ID),
    )
    session.add(section)
    await session.commit()
    await session.refresh(section)

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

    country = CountryDB(
        name="eritrea", created_by=uuid.UUID(USER_ID), modified_by=uuid.UUID(USER_ID)
    )
    session.add(country)
    await session.commit()
    await session.refresh(country)

    educational_level = EducationalLevelDB(
        level="10th",
        level_order=10,
        created_by=uuid.UUID(USER_ID),
        modified_by=uuid.UUID(USER_ID),
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
        "country": country,
        "educational_level": educational_level,
    }
