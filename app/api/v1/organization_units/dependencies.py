"""API dependencies module."""
from fastapi import Depends
from sqlmodel.ext.asyncio.session import AsyncSession

from app.api.v1.organization_units.department_crud import DepartmentCRUD
from app.api.v1.organization_units.designation_crud import DesignationCRUD
from app.api.v1.organization_units.division_crud import DivisionCRUD
from app.api.v1.organization_units.section_crud import SectionCRUD
from app.api.v1.organization_units.unit_crud import UnitCRUD
from app.core.db import get_async_session


async def get_divisions_crud(
    session: AsyncSession = Depends(get_async_session),
) -> DivisionCRUD:
    """Dependency function that initialize division crud operations class."""
    return DivisionCRUD(session=session)


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


async def get_units_crud(
    session: AsyncSession = Depends(get_async_session),
) -> UnitCRUD:
    """Dependency function that initialize unit crud operations class."""
    return UnitCRUD(session=session)


async def get_designation_crud(
    session: AsyncSession = Depends(get_async_session),
) -> DesignationCRUD:
    """Dependency function that initialize designation crud operations class."""
    return DesignationCRUD(session=session)
