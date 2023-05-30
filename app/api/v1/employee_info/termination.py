"""Employee termination api endpoints module."""
from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi_jwt_auth import AuthJWT  # type: ignore
from sqlalchemy.exc import IntegrityError

from app.api.v1.employee_info.dependencies import (
    get_employee_crud,
    get_termination_crud,
)
from app.api.v1.employee_info.employee_crud import EmployeeCRUD
from app.api.v1.employee_info.termination_crud import TerminationCRUD
from app.api.v1.utils import staff_user_or_error
from app.models.employee_info.termination import (
    TerminationBase,
    TerminationCreate,
    TerminationRead,
    TerminationReadMany,
    TerminationUpdate,
    TerminationUpdateBase,
)

router = APIRouter(prefix="/terminations", tags=["terminate"])

TerminationCRUDDep = Annotated[TerminationCRUD, Depends(get_termination_crud)]
EmployeeCRUDDEp = Annotated[EmployeeCRUD, Depends(get_employee_crud)]
AuthJWTDep = Annotated[AuthJWT, Depends()]


@router.post("", response_model=TerminationRead, status_code=status.HTTP_201_CREATED)
async def create_termination(
    payload: TerminationBase,
    employees: EmployeeCRUDDEp,
    terminations: TerminationCRUDDep,
    Authorize: AuthJWTDep,
):
    """Create termination endpoint."""
    Authorize.jwt_required()
    user_claims = Authorize.get_raw_jwt()
    await staff_user_or_error(user_claims=user_claims)
    user = UUID(Authorize.get_jwt_subject())  # type: ignore
    employee = await employees.read_by_uid(payload.employee_uid)
    if employee is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="employee not found."
        )
    if employee.is_active:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="can not terminate active employee.",
        )

    create_payload = TerminationCreate(
        **payload.dict(),
        hire_date=employee.current_hire_date,
        created_by=user,
        modified_by=user
    )
    try:
        termination = await terminations.create_termination(create_payload)
    except IntegrityError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="duplicate or invalid field information.",
        )
    return termination


@router.get("/{termination_uid}", response_model=TerminationRead)
async def read_by_uid(
    termination_uid: UUID, terminations: TerminationCRUDDep, Authorize: AuthJWTDep
):
    """Read termination by uid."""
    Authorize.jwt_required()
    termination = await terminations.read_by_uid(termination_uid=termination_uid)

    if termination is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="termination not found."
        )

    return termination


@router.get("", response_model=TerminationReadMany)
async def read_many(terminations: TerminationCRUDDep, Authorize: AuthJWTDep):
    """Read many terminations."""
    Authorize.jwt_required()

    all_terminations = await terminations.read_many()

    return all_terminations


@router.patch("/{termination_uid}", response_model=TerminationRead)
async def update_termination(
    termination_uid: UUID,
    payload: TerminationUpdateBase,
    terminations: TerminationCRUDDep,
    Authorize: AuthJWTDep,
):
    """Update termination."""
    Authorize.jwt_required()
    user_claims = Authorize.get_raw_jwt()
    await staff_user_or_error(user_claims=user_claims)
    user = UUID(Authorize.get_jwt_subject())  # type: ignore
    update_payload = TerminationUpdate(
        **payload.dict(exclude_unset=True), modified_by=user
    )
    try:
        termination = await terminations.update_termination(
            termination_uid=termination_uid, payload=update_payload
        )
    except IntegrityError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="duplicate or invalid field information.",
        )

    if termination is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="termination not found."
        )

    return termination


@router.delete("/{termination_uid}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_termination(
    termination_uid: UUID, terminations: TerminationCRUDDep, Authorize: AuthJWTDep
):
    """Delete termination."""
    Authorize.jwt_required()
    user_claims = Authorize.get_raw_jwt()
    await staff_user_or_error(user_claims=user_claims)

    deleted = await terminations.delete_termination(termination_uid=termination_uid)

    if not deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="termination not found."
        )
