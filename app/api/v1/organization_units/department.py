"""Department api endpoints module."""
from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.exc import IntegrityError

from app.api.v1.organization_units.department_crud import DepartmentCRUD
from app.api.v1.organization_units.dependencies import get_departments_crud
from app.models.organization_units.department import (
    DepartmentCreate,
    DepartmentRead,
    DepartmentReadMany,
    DepartmentUpdate,
)
from app.utils.lower_case_attrs import lower_str_attrs

router = APIRouter(prefix="/departments", tags=["department"])

DepartmentCRUDDep = Annotated[DepartmentCRUD, Depends(get_departments_crud)]


@router.post("", response_model=DepartmentRead, status_code=status.HTTP_201_CREATED)
async def create_department(
    payload: DepartmentCreate,
    departments: DepartmentCRUDDep,
):
    """Create department endpoint."""
    lower_str_attrs(payload)
    try:
        department = await departments.create(payload=payload)
    except IntegrityError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="duplicate department name."
        )

    return department


@router.get("", response_model=DepartmentReadMany)
async def read_many(departments: DepartmentCRUDDep):
    """Read many departments."""
    department_list = await departments.read_many()

    return department_list


@router.get("/{department_uid}", response_model=DepartmentRead)
async def read_by_uid(department_uid: UUID, departments: DepartmentCRUDDep):
    """Read department by uid."""
    department = await departments.read_by_uid(department_uid)
    if department is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="department not found."
        )
    return department


@router.patch("/{department_uid}", response_model=DepartmentRead)
async def updated_department(
    department_uid: UUID,
    payload: DepartmentUpdate,
    departments: DepartmentCRUDDep,
):
    """Update department."""
    lower_str_attrs(payload)
    department = await departments.update_department(department_uid, payload)
    if department is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="department not found."
        )
    return department


@router.delete("/{department_uid}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_department(department_uid: UUID, departments: DepartmentCRUDDep):
    """Delete department."""
    deleted = await departments.delete_department(department_uid)
    if not deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="department not found."
        )
