"""Child api endpoints module."""
from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi_jwt_auth import AuthJWT  # type: ignore
from sqlalchemy.exc import IntegrityError

from app.api.v1.employee_info.child_crud import ChildCRUD
from app.api.v1.employee_info.dependencies import get_child_crud
from app.api.v1.utils import staff_user_or_error
from app.models.employee_info.child import (
    ChildBase,
    ChildCreate,
    ChildRead,
    ChildReadMany,
    ChildUpdate,
    ChildUpdateBase,
)
from app.utils.lower_case_attrs import lower_str_attrs

router = APIRouter(prefix="/employee/children", tags=["child"])

ChildCRUDDep = Annotated[ChildCRUD, Depends(get_child_crud)]
AuthJWTDep = Annotated[AuthJWT, Depends()]


@router.post("", response_model=ChildRead, status_code=status.HTTP_201_CREATED)
async def create_child(
    payload: ChildBase, children: ChildCRUDDep, Authorize: AuthJWTDep
):
    """Create child endpoint."""
    Authorize.jwt_required()
    user_claims = Authorize.get_raw_jwt()
    await staff_user_or_error(user_claims=user_claims)
    user = UUID(Authorize.get_jwt_subject())  # type: ignore
    lower_str_attrs(payload)
    create_payload = ChildCreate(**payload.dict(), created_by=user, modified_by=user)
    try:
        child = await children.create_child(create_payload)
    except IntegrityError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="duplicate or invalid field information.",
        )
    return child


@router.get("/employee-id/{employee_uid}", response_model=ChildReadMany)
async def read_many_by_employee(
    employee_uid: UUID, children: ChildCRUDDep, Authorize: AuthJWTDep
):
    """Read many children of an employee."""
    Authorize.jwt_required()
    child_list = await children.read_many_by_employee(employee_uid)

    return child_list


@router.get("", response_model=ChildReadMany)
async def read_many(children: ChildCRUDDep, Authorize: AuthJWTDep):
    """Read many children."""
    Authorize.jwt_required()
    child_list = await children.read_many()

    return child_list


@router.get("/child-id/{child_uid}", response_model=ChildRead)
async def read_by_uid(child_uid: UUID, children: ChildCRUDDep, Authorize: AuthJWTDep):
    """Read child by uid."""
    Authorize.jwt_required()
    child = await children.read_by_uid(child_uid)
    if child is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="child not found."
        )
    return child


@router.patch("/{child_uid}", response_model=ChildRead)
async def update_child(
    child_uid: UUID,
    payload: ChildUpdateBase,
    children: ChildCRUDDep,
    Authorize: AuthJWTDep,
):
    """Update child."""
    Authorize.jwt_required()
    user_claims = Authorize.get_raw_jwt()
    await staff_user_or_error(user_claims=user_claims)
    user = UUID(Authorize.get_jwt_subject())  # type: ignore
    lower_str_attrs(payload)
    update_payload = ChildUpdate(**payload.dict(exclude_unset=True), modified_by=user)
    child = await children.update_child(child_uid, update_payload)
    if child is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="child not found."
        )
    return child


@router.delete("/{child_uid}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_child(child_uid: UUID, children: ChildCRUDDep, Authorize: AuthJWTDep):
    """Delete child."""
    Authorize.jwt_required()
    user_claims = Authorize.get_raw_jwt()
    await staff_user_or_error(user_claims=user_claims)
    deleted = await children.delete_child(child_uid)
    if not deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="child not found."
        )
