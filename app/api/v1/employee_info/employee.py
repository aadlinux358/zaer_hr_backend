"""Employee api endpoints module."""
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.exc import IntegrityError

from app.api.v1.employee_info.dependencies import get_employee_crud
from app.api.v1.employee_info.employee_crud import EmployeeCRUD
from app.models.employee_info.employee import (
    EmployeeCreate,
    EmployeeRead,
    EmployeeReadMany,
    EmployeeUpdate,
)
from app.utils.lower_case_attrs import lower_str_attrs

router = APIRouter(prefix="/employees", tags=["employee"])


@router.post("", response_model=EmployeeRead, status_code=status.HTTP_201_CREATED)
async def create_employee(
    payload: EmployeeCreate, employees: EmployeeCRUD = Depends(get_employee_crud)
):
    """Create Employee."""
    lower_str_attrs(payload)
    try:
        employee = await employees.create_employee(payload)
    except IntegrityError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="integrity error. eg. duplicate field or invalid field value.",
        )
    return employee


@router.get("", response_model=EmployeeReadMany)
async def read_many(employees: EmployeeCRUD = Depends(get_employee_crud)):
    """Read many employees."""
    employee_list = await employees.read_many()

    return employee_list


@router.get("/{employee_uid}", response_model=EmployeeRead)
async def read_by_uid(
    employee_uid: UUID, employees: EmployeeCRUD = Depends(get_employee_crud)
):
    """Read employee by uid."""
    employee = await employees.read_by_uid(employee_uid)
    if employee is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="employee not found."
        )
    return employee


@router.patch("/{employee_uid}", response_model=EmployeeRead)
async def update_employee(
    employee_uid: UUID,
    payload: EmployeeUpdate,
    employees: EmployeeCRUD = Depends(get_employee_crud),
):
    """Update employee."""
    lower_str_attrs(payload)
    employee = await employees.update_employee(employee_uid, payload)
    if employee is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="employee not found."
        )
    return employee
