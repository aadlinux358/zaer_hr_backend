"""Department api endpoints module."""
from typing import Annotated
from uuid import UUID

import pandas as pd
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import FileResponse
from fastapi_jwt_auth import AuthJWT  # type: ignore
from sqlalchemy.exc import IntegrityError

from app.api.v1.organization_units.department_crud import DepartmentCRUD
from app.api.v1.organization_units.dependencies import get_departments_crud
from app.api.v1.utils import superuser_or_error
from app.models.organization_units.department import (
    DepartmentBase,
    DepartmentCreate,
    DepartmentRead,
    DepartmentReadMany,
    DepartmentReadManyPrintFormat,
    DepartmentReadPrintFormat,
    DepartmentUpdate,
    DepartmentUpdateBase,
)
from app.utils.lower_case_attrs import lower_str_attrs

router = APIRouter(prefix="/departments", tags=["department"])

DepartmentCRUDDep = Annotated[DepartmentCRUD, Depends(get_departments_crud)]
AuthJWTDep = Annotated[AuthJWT, Depends()]


@router.post("", response_model=DepartmentRead, status_code=status.HTTP_201_CREATED)
async def create_department(
    payload: DepartmentBase, departments: DepartmentCRUDDep, Authorize: AuthJWTDep
):
    """Create department."""
    Authorize.jwt_required()
    user_claims = Authorize.get_raw_jwt()
    await superuser_or_error(user_claims)
    subject = UUID(Authorize.get_jwt_subject())  # type: ignore
    lower_str_attrs(payload)
    create_payload = DepartmentCreate(
        **payload.dict(), created_by=subject, modified_by=subject
    )
    try:
        department = await departments.create(payload=create_payload)
    except IntegrityError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="duplicate department name."
        )

    return department


@router.get("", response_model=DepartmentReadMany)
async def read_many(departments: DepartmentCRUDDep, Authorize: AuthJWTDep):
    """Read many departments."""
    Authorize.jwt_required()
    department_list = await departments.read_many()

    return department_list


@router.get("/for/print", response_model=DepartmentReadManyPrintFormat)
async def read_many_print_format(departments: DepartmentCRUDDep, Authorize: AuthJWTDep):
    """Read many departments."""
    Authorize.jwt_required()
    department_list = await departments.read_many_print_format()

    return department_list


@router.get("/{department_uid}", response_model=DepartmentRead)
async def read_by_uid(
    department_uid: UUID, departments: DepartmentCRUDDep, Authorize: AuthJWTDep
):
    """Read department by uid."""
    Authorize.jwt_required()
    department = await departments.read_by_uid(department_uid)
    if department is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="department not found."
        )
    return department


@router.get("/{department_uid}/for/print", response_model=DepartmentReadPrintFormat)
async def read_by_uid_print_format(
    department_uid: UUID, departments: DepartmentCRUDDep, Authorize: AuthJWTDep
):
    """Read department by uid."""
    Authorize.jwt_required()
    department = await departments.read_by_uid_print_format(department_uid)
    if department is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="department not found."
        )
    return department


@router.patch("/{department_uid}", response_model=DepartmentRead)
async def update_department(
    department_uid: UUID,
    payload: DepartmentUpdateBase,
    departments: DepartmentCRUDDep,
    Authorize: AuthJWTDep,
):
    """Update department."""
    Authorize.jwt_required()
    user_claims = Authorize.get_raw_jwt()
    await superuser_or_error(user_claims)
    subject = UUID(Authorize.get_jwt_subject())  # type: ignore
    lower_str_attrs(payload)
    update_payload = DepartmentUpdate(
        **payload.dict(exclude_unset=True), modified_by=subject
    )
    department = await departments.update_department(department_uid, update_payload)
    if department is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="department not found."
        )

    return department


@router.delete("/{department_uid}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_department(
    department_uid: UUID, departments: DepartmentCRUDDep, Authorize: AuthJWTDep
):
    """Delete department."""
    Authorize.jwt_required()
    user_claims = Authorize.get_raw_jwt()
    await superuser_or_error(user_claims)
    deleted = await departments.delete_department(department_uid)
    if not deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="department not found."
        )


@router.get("/download/csv", response_class=FileResponse)
async def download_csv(departments: DepartmentCRUDDep, Authorize: AuthJWTDep):
    """Download departments as csv."""
    Authorize.jwt_required()
    department_list = await departments.read_many_print_format()
    df = pd.DataFrame([d.dict() for d in department_list.result])
    df.to_csv("hr_tmp/departments.csv", index=False)
    return FileResponse("hr_tmp/departments.csv")


@router.get("/download/xlsx", response_class=FileResponse)
async def download_excel(
    departments: DepartmentCRUDDep, Authorize: AuthJWTDep
) -> FileResponse:
    """Download departments as excel."""
    Authorize.jwt_required()
    department_list = await departments.read_many()
    df = pd.DataFrame([d.dict() for d in department_list.result])
    df.to_excel("hr_tmp/departments.xlsx", index=False)
    return FileResponse("hr_tmp/departments.xlsx")
