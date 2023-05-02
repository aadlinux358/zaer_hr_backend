"""API dependencies module."""
from fastapi import Depends
from sqlmodel.ext.asyncio.session import AsyncSession

from app.api.v1.organization_units.current_job_crud import CurrentJobCRUD
from app.api.v1.organization_units.department_crud import DepartmentCRUD
from app.api.v1.organization_units.section_crud import SectionCRUD
from app.api.v1.organization_units.sub_section_crud import SubSectionCRUD
from app.core.db import get_async_session


async def get_departments_crud(
    session: AsyncSession = Depends(get_async_session),
) -> DepartmentCRUD:
    """Dependency function that initialize department crud operations class."""
    return DepartmentCRUD(session=session)


async def get_sections_crud(
    session: AsyncSession = Depends(get_async_session),
) -> SectionCRUD:
    """Dependency function that initialize section crud operations class."""
    return SectionCRUD(session=session)


async def get_sub_sections_crud(
    session: AsyncSession = Depends(get_async_session),
) -> SubSectionCRUD:
    """Dependency function that initialize sub section crud operations class."""
    return SubSectionCRUD(session=session)


async def get_current_job_crud(
    session: AsyncSession = Depends(get_async_session),
) -> CurrentJobCRUD:
    """Dependency function that initialize current job crud operations class."""
    return CurrentJobCRUD(session=session)
