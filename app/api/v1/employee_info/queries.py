"""Employee related queries module."""
from uuid import UUID

from sqlmodel import select

from app.models import (
    CountryDB,
    DepartmentDB,
    DesignationDB,
    DivisionDB,
    EducationalLevelDB,
    EmployeeDB,
    NationalityDB,
    SectionDB,
    UnitDB,
)

pass


def get_employee_relationships_query():
    """Create employee and related tables join queries."""
    statement = (
        select(
            EmployeeDB.uid,
            EmployeeDB.badge_number,
            EmployeeDB.first_name,
            EmployeeDB.last_name,
            EmployeeDB.grandfather_name,
            EmployeeDB.gender,
            EmployeeDB.birth_date,
            EmployeeDB.birth_place,
            EmployeeDB.origin_of_birth,
            EmployeeDB.mother_first_name,
            EmployeeDB.mother_last_name,
            EmployeeDB.mother_grandfather_name,
            EmployeeDB.section_uid,
            EmployeeDB.educational_level_uid,
            EmployeeDB.country_uid,
            EmployeeDB.nationality_uid,
            EmployeeDB.designation_uid,
            EmployeeDB.current_hire_date,
            EmployeeDB.current_salary,
            EmployeeDB.marital_status,
            EmployeeDB.national_id,
            EmployeeDB.phone_number,
            EmployeeDB.apprenticeship_from_date,
            EmployeeDB.apprenticeship_to_date,
            EmployeeDB.contract_type,
            EmployeeDB.national_service,
            EmployeeDB.is_active,
            EmployeeDB.is_terminated,
            EmployeeDB.created_by,
            EmployeeDB.modified_by,
            EmployeeDB.date_created,
            EmployeeDB.date_modified,
            DivisionDB.name.label("division"),
            DepartmentDB.name.label("department"),
            UnitDB.name.label("unit"),
            SectionDB.name.label("section"),
            EducationalLevelDB.level.label("educational_level"),
            DesignationDB.title.label("designation"),
            NationalityDB.name.label("nationality"),
            CountryDB.name.label("country"),
        )
        .join(SectionDB, SectionDB.uid == EmployeeDB.section_uid)
        .join(UnitDB, SectionDB.unit_uid == UnitDB.uid)
        .join(DepartmentDB, UnitDB.department_uid == DepartmentDB.uid)
        .join(DivisionDB, DepartmentDB.division_uid == DivisionDB.uid)
        .join(
            EducationalLevelDB,
            EducationalLevelDB.uid == EmployeeDB.educational_level_uid,
        )
        .join(DesignationDB, DesignationDB.uid == EmployeeDB.designation_uid)
        .join(NationalityDB, NationalityDB.uid == EmployeeDB.nationality_uid)
        .join(CountryDB, CountryDB.uid == EmployeeDB.country_uid)
    )
    return statement


def get_full_emp_info_by_uid_query(employee_uid: UUID):
    """Create single employee and related tables join queries."""
    statement = get_employee_relationships_query().where(EmployeeDB.uid == employee_uid)

    return statement
