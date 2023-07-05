"""Employee api endpoints module."""
import base64
import os
import pathlib
from typing import Annotated
from uuid import UUID

import pandas as pd
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import FileResponse, Response
from fastapi_jwt_auth import AuthJWT  # type: ignore
from sqlalchemy.exc import IntegrityError

from app.api.v1.employee_info.dependencies import (
    get_employee_crud,
    get_termination_crud,
)
from app.api.v1.employee_info.employee_crud import EmployeeCRUD
from app.api.v1.employee_info.termination_crud import TerminationCRUD
from app.api.v1.utils.exception_responses import staff_user_or_error
from app.models.employee_info.employee import (
    EmployeeBase,
    EmployeeCreate,
    EmployeeRead,
    EmployeeReadFull,
    EmployeeReadMany,
    EmployeeReadManyFull,
    EmployeeSeverancePay,
    EmployeeUpdate,
    EmployeeUpdateBase,
)
from app.models.employee_info.termination import TerminationRead
from app.reports.severance_pay import SeverancePayReport
from app.utils.lower_case_attrs import lower_str_attrs

router = APIRouter(prefix="/employees", tags=["employee"])

EmployeeCRUDDep = Annotated[EmployeeCRUD, Depends(get_employee_crud)]
AuthJWTDep = Annotated[AuthJWT, Depends()]
TerminationCRUDDep = Annotated[TerminationCRUD, Depends(get_termination_crud)]


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


@router.get("/full", response_model=EmployeeReadManyFull)
async def read_many_full(employees: EmployeeCRUDDep, Authorize: AuthJWTDep):
    """Read many full employee info."""
    Authorize.jwt_required()
    employee_list = await employees.read_many_full_info()

    return employee_list


@router.get("", response_model=EmployeeReadMany)
async def read_many(employees: EmployeeCRUDDep, Authorize: AuthJWTDep):
    """Read many employees."""
    Authorize.jwt_required()
    employee_list = await employees.read_many()

    return employee_list


@router.get("/{employee_uid}/full", response_model=EmployeeReadFull)
async def read_full_info_by_id(
    employee_uid: UUID, employees: EmployeeCRUDDep, Authorize: AuthJWTDep
) -> EmployeeReadFull:
    """Read full employee info by uid."""
    Authorize.jwt_required()
    employee = await employees.read_full_by_uid(employee_uid)
    if employee is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="employee not found."
        )
    return employee


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
    db_employee = await employees.read_by_uid(employee_uid)
    if db_employee:
        if db_employee.is_active is False:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="can not update inactive employee",
            )
    employee = await employees.update_employee(employee_uid, update_payload)
    if employee is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="employee not found."
        )
    return employee


@router.post(
    "/deactivate/{employee_uid}",
    response_model=EmployeeRead,
    status_code=status.HTTP_201_CREATED,
)
async def deactivate_employee(
    employee_uid: UUID, employees: EmployeeCRUDDep, Authorize: AuthJWTDep
):
    """Deactivate employee, not delete it from db."""
    Authorize.jwt_required()
    user_claims = Authorize.get_raw_jwt()
    await staff_user_or_error(user_claims=user_claims)
    subject = UUID(Authorize.get_jwt_subject())  # type: ignore
    # TODO: Log this action in to a db table
    employee = await employees.read_by_uid(employee_uid=employee_uid)
    if employee is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="employee not found."
        )
    if not employee.is_active:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="employee is already deactivated",
        )
    employee = await employees.update_employee(
        employee_uid=employee_uid,
        payload=EmployeeUpdate(is_active=False, modified_by=subject),
    )
    if employee is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="employee not found."
        )

    return employee


@router.post(
    "/activate/{employee_uid}",
    response_model=EmployeeRead,
    status_code=status.HTTP_201_CREATED,
)
async def activate_employee(
    employee_uid: UUID, employees: EmployeeCRUDDep, Authorize: AuthJWTDep
):
    """Activate employee."""
    Authorize.jwt_required()
    user_claims = Authorize.get_raw_jwt()
    await staff_user_or_error(user_claims=user_claims)
    subject = UUID(Authorize.get_jwt_subject())  # type: ignore
    # TODO: Log this action in to a db table
    employee = await employees.read_by_uid(employee_uid=employee_uid)
    if employee is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="employee not found."
        )
    if employee.is_active:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="employee is already activated",
        )
    employee = await employees.update_employee(
        employee_uid=employee_uid,
        payload=EmployeeUpdate(
            is_active=True, is_terminated=False, modified_by=subject
        ),
    )
    if employee is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="employee not found."
        )
    return employee


@router.get("/download/csv", response_class=FileResponse)
async def download_csv(
    employees: EmployeeCRUDDep, Authorize: AuthJWTDep
) -> FileResponse:
    """Download employees as csv."""
    Authorize.jwt_required()
    divisions_list = await employees.read_many_full_info()
    df = pd.DataFrame([d.dict() for d in divisions_list.result])
    # TODO remove this when app lifespan works with pytest and httpx
    p = pathlib.Path("hr_tmp")
    p.mkdir(exist_ok=True)
    df.to_csv("hr_tmp/employees.csv", index=False)
    return FileResponse("hr_tmp/employees.csv")


@router.get("/badge-number/{badge_number}", response_model=EmployeeReadFull)
async def read_by_badge_number(
    badge_number: int, employees: EmployeeCRUDDep, Authorize: AuthJWTDep
) -> EmployeeReadFull:
    """Read employee by badge number."""
    Authorize.jwt_required()
    employee = await employees.read_full_by_badge_number(badge_number=badge_number)
    if employee is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="employee not found."
        )
    return employee


@router.get("/severance-pay/{badge_number}", response_class=Response)
async def calculate_severance_pay(
    badge_number: int,
    employees: EmployeeCRUDDep,
    terminations: TerminationCRUDDep,
    Authorize: AuthJWTDep,
) -> Response:
    """Calculate employee severance pay."""
    Authorize.jwt_required()
    user_claims = Authorize.get_raw_jwt()
    await staff_user_or_error(user_claims=user_claims)

    employee = await employees.read_full_by_badge_number(badge_number=badge_number)
    if employee is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="employee not found."
        )
    if employee.is_terminated is False:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="employee is not terminated.",
        )
    emp_terminations = await terminations.read_many_by_employee(employee.uid)
    if not emp_terminations.count:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="no termination data found."
        )

    def filter_hire_date(t: TerminationRead) -> bool:
        if employee is None:
            return False
        return t.hire_date == employee.current_hire_date

    if emp_terminations.count > 1:
        termination = list(
            filter(  # type: ignore
                filter_hire_date,
                emp_terminations.result,
            )
        )[0]
    else:
        termination = emp_terminations.result[0]  # type: ignore

    emp_sev = EmployeeSeverancePay(
        **employee.dict(), termination_date=termination.termination_date
    )
    p = pathlib.Path("hr_tmp")
    p.mkdir(exist_ok=True)
    old_path = os.getcwd()
    os.chdir(p)
    sr = SeverancePayReport(emp_sev)
    filename = sr.create_report()
    os.chdir(old_path)
    file_path = p / filename
    with open(file_path, "rb") as pdf_file:
        encoded_string = base64.b64encode(pdf_file.read())
        return Response(content=encoded_string, media_type="application/pdf")
