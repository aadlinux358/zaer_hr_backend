"""Designation api endpoints module."""
from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi_jwt_auth import AuthJWT  # type: ignore
from sqlalchemy.exc import IntegrityError

from app.api.v1.organization_units.dependencies import get_designation_crud
from app.api.v1.organization_units.designation_crud import DesignationCRUD
from app.api.v1.utils import superuser_or_error
from app.models.organization_units.designation import (
    DesignationBase,
    DesignationCreate,
    DesignationRead,
    DesignationReadMany,
    DesignationUpdate,
)
from app.utils.lower_case_attrs import lower_str_attrs

router = APIRouter(prefix="/designations", tags=["designation"])

DesignationCRUDDep = Annotated[DesignationCRUD, Depends(get_designation_crud)]
AuthJWTDep = Annotated[AuthJWT, Depends()]


@router.post("", response_model=DesignationRead, status_code=status.HTTP_201_CREATED)
async def create_designation(
    payload: DesignationBase, designations: DesignationCRUDDep, Authorize: AuthJWTDep
):
    """Create designation endpoint."""
    Authorize.jwt_required()
    user_claims = Authorize.get_raw_jwt()
    await superuser_or_error(user_claims)
    subject = UUID(Authorize.get_jwt_subject())  # type: ignore
    lower_str_attrs(payload)
    create_payload = DesignationCreate(
        **payload.dict(), created_by=subject, modified_by=subject
    )
    try:
        designation = await designations.create(payload=create_payload)
    except IntegrityError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="duplicate designation title.",
        )
    return designation


@router.get("", response_model=DesignationReadMany)
async def read_many(designations: DesignationCRUDDep, Authorize: AuthJWTDep):
    """Read many designations."""
    Authorize.jwt_required()
    designation_list = await designations.read_many()

    return designation_list


@router.get("/{designation_uid}", response_model=DesignationRead)
async def read_by_uid(
    designation_uid: UUID, designations: DesignationCRUDDep, Authorize: AuthJWTDep
):
    """Read designation by id."""
    Authorize.jwt_required()
    designation = await designations.read_by_uid(designation_uid)
    if designation is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="designation not found."
        )
    return designation


@router.patch("/{designation_uid}", response_model=DesignationRead)
async def update_designation(
    designation_uid: UUID,
    payload: DesignationBase,
    designations: DesignationCRUDDep,
    Authorize: AuthJWTDep,
):
    """Update designation."""
    Authorize.jwt_required()
    user_claims = Authorize.get_raw_jwt()
    await superuser_or_error(user_claims)
    subject = UUID(Authorize.get_jwt_subject())  # type: ignore
    lower_str_attrs(payload)
    update_payload = DesignationUpdate(**payload.dict(), modified_by=subject)
    designation = await designations.update_designation(designation_uid, update_payload)
    if designation is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="designation not found."
        )
    return designation


@router.delete("/{designation_uid}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_designation(
    designation_uid: UUID, designations: DesignationCRUDDep, Authorize: AuthJWTDep
):
    """Delete designation."""
    Authorize.jwt_required()
    user_claims = Authorize.get_raw_jwt()
    await superuser_or_error(user_claims)
    deleted = await designations.delete_designation(designation_uid)
    if not deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="designation not found."
        )
