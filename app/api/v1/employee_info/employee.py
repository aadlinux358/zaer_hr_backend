"""Employee api endpoints module."""
from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi_jwt_auth import AuthJWT  # type: ignore
from sqlalchemy.exc import IntegrityError

from app.api.v1.employee_info.dependencies import get_employee_crud
from app.api.v1.employee_info.employee_crud import EmployeeCRUD
from app.api.v1.utils.exception_responses import staff_user_or_error
from app.models.employee_info.employee import (
    EmployeeBase,
    EmployeeCreate,
    EmployeeRead,
    EmployeeReadMany,
    EmployeeUpdate,
    EmployeeUpdateBase,
)
from app.utils.lower_case_attrs import lower_str_attrs

router = APIRouter(prefix="/employees", tags=["employee"])

EmployeeCRUDDep = Annotated[EmployeeCRUD, Depends(get_employee_crud)]
AuthJWTDep = Annotated[AuthJWT, Depends()]


@router.post("", response_model=EmployeeRead, status_code=status.HTTP_201_CREATED)
async def create_employee(
    payload: EmployeeBase, employees: EmployeeCRUDDep, Authorize: AuthJWTDep
):
    """Create Employee."""
    Authorize.jwt_required()
    user_claims = Authorize.get_raw_jwt()
    await staff_user_or_error(user_claims=user_claims)
    subject = UUID(Authorize.get_jwt_subject())  # type: ignore
    lower_str_attrs(payload)
    create_payload = EmployeeCreate(
        **payload.dict(), created_by=subject, modified_by=subject
    )
    try:
        employee = await employees.create_employee(create_payload)
    except IntegrityError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="integrity error. eg. duplicate field or invalid field value.",
        )
    return employee


@router.get("", response_model=EmployeeReadMany)
async def read_many(employees: EmployeeCRUDDep, Authorize: AuthJWTDep):
    """Read many employees."""
    Authorize.jwt_required()
    employee_list = await employees.read_many()

    return employee_list


@router.get("/{employee_uid}", response_model=EmployeeRead)
async def read_by_uid(
    employee_uid: UUID, employees: EmployeeCRUDDep, Authorize: AuthJWTDep
):
    """Read employee by uid."""
    Authorize.jwt_required()
    employee = await employees.read_by_uid(employee_uid)
    if employee is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="employee not found."
        )
    return employee


@router.patch("/{employee_uid}", response_model=EmployeeRead)
async def update_employee(
    employee_uid: UUID,
    payload: EmployeeUpdateBase,
    employees: EmployeeCRUDDep,
    Authorize: AuthJWTDep,
):
    """Update employee."""
    Authorize.jwt_required()
    user_claims = Authorize.get_raw_jwt()
    await staff_user_or_error(user_claims=user_claims)
    subject = UUID(Authorize.get_jwt_subject())  # type: ignore
    lower_str_attrs(payload)
    update_payload = EmployeeUpdate(
        **payload.dict(exclude_unset=True), modified_by=subject
    )
    employee = await employees.update_employee(employee_uid, update_payload)
    if employee is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="employee not found."
        )
    return employee
