"""Human resources application models package."""
from app.models.employee_info.address import AddressDB
from app.models.employee_info.child import ChildDB
from app.models.employee_info.contact_person import ContactPersonDB
from app.models.employee_info.educational_level import EducationalLevelDB
from app.models.employee_info.employee import EmployeeDB
from app.models.employee_info.nationalities import NationalityDB
from app.models.employee_info.termination import TerminationDB
from app.models.organization_units.department import DepartmentDB
from app.models.organization_units.designation import DesignationDB
from app.models.organization_units.division import DivisionDB
from app.models.organization_units.section import SectionDB
from app.models.organization_units.unit import UnitDB

__all__ = (
    "DivisionDB",
    "DepartmentDB",
    "SectionDB",
    "UnitDB",
    "DesignationDB",
    "NationalityDB",
    "EducationalLevelDB",
    "EmployeeDB",
    "ChildDB",
    "AddressDB",
    "ContactPersonDB",
    "TerminationDB",
)
