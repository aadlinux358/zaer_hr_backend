"""Employee information api dependencies module."""
from fastapi import Depends
from sqlmodel.ext.asyncio.session import AsyncSession

from app.api.v1.employee_info.address_crud import AddressCRUD
from app.api.v1.employee_info.child_crud import ChildCRUD
from app.api.v1.employee_info.contact_person_crud import ContactPersonCRUD
from app.api.v1.employee_info.educational_level_crud import EducationalLevelCRUD
from app.api.v1.employee_info.employee_crud import EmployeeCRUD
from app.api.v1.employee_info.nationalities_crud import NationalityCRUD
from app.api.v1.employee_info.termination_crud import TerminationCRUD
from app.core.db import get_async_session


async def get_employee_crud(
    session: AsyncSession = Depends(get_async_session),
) -> EmployeeCRUD:
    """Dependency function that initialize employee crud operations class."""
    return EmployeeCRUD(session=session)


async def get_child_crud(
    session: AsyncSession = Depends(get_async_session),
) -> ChildCRUD:
    """Initialize child crud operation class."""
    return ChildCRUD(session=session)


async def get_nationality_crud(
    session: AsyncSession = Depends(get_async_session),
) -> NationalityCRUD:
    """Initialize nationality crud operation class."""
    return NationalityCRUD(session=session)


async def get_educational_level_crud(
    session: AsyncSession = Depends(get_async_session),
) -> EducationalLevelCRUD:
    """Initialize nationality crud operation class."""
    return EducationalLevelCRUD(session=session)


async def get_address_crud(
    session: AsyncSession = Depends(get_async_session),
) -> AddressCRUD:
    """Initialize address crud operations class."""
    return AddressCRUD(session=session)


async def get_contact_person_crud(
    session: AsyncSession = Depends(get_async_session),
) -> ContactPersonCRUD:
    """Initialize contact person crud operations class."""
    return ContactPersonCRUD(session=session)


async def get_termination_crud(
    session: AsyncSession = Depends(get_async_session),
) -> TerminationCRUD:
    """Initialize termination crud operations class."""
    return TerminationCRUD(session=session)
