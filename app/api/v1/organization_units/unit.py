"""Unit api endpoints module."""
from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi_jwt_auth import AuthJWT  # type: ignore
from sqlalchemy.exc import IntegrityError

from app.api.v1.organization_units.dependencies import get_units_crud
from app.api.v1.organization_units.unit_crud import UnitCRUD
from app.api.v1.utils import superuser_or_error
from app.models.organization_units.unit import (
    UnitBase,
    UnitCreate,
    UnitRead,
    UnitReadMany,
    UnitUpdate,
    UnitUpdateBase,
)
from app.utils.lower_case_attrs import lower_str_attrs

router = APIRouter(prefix="/units", tags=["unit"])

UnitCRUDDep = Annotated[UnitCRUD, Depends(get_units_crud)]
AuthJWTDep = Annotated[AuthJWT, Depends()]


@router.post("", response_model=UnitRead, status_code=status.HTTP_201_CREATED)
async def create_unit(payload: UnitBase, units: UnitCRUDDep, Authorize: AuthJWTDep):
    """Create unit."""
    Authorize.jwt_required()
    user_claims = Authorize.get_raw_jwt()
    await superuser_or_error(user_claims)
    subject = UUID(Authorize.get_jwt_subject())  # type: ignore
    lower_str_attrs(payload)
    create_payload = UnitCreate(
        **payload.dict(),
        created_by=subject,
        modified_by=subject,
    )
    try:
        unit = await units.create(payload=create_payload)
    except IntegrityError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="duplicate unit name.",
        )
    return unit


@router.get("", response_model=UnitReadMany)
async def read_many(units: UnitCRUDDep, Authorize: AuthJWTDep):
    """Read many units."""
    Authorize.jwt_required()
    unit_list = await units.read_many()

    return unit_list


@router.get("/{unit_uid}", response_model=UnitRead)
async def read_by_uid(unit_uid: UUID, units: UnitCRUDDep, Authorize: AuthJWTDep):
    """Read unit by uid."""
    Authorize.jwt_required()
    unit = await units.read_by_uid(unit_uid)
    if unit is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="unit not found."
        )
    return unit


@router.patch("/{unit_uid}", response_model=UnitRead)
async def update_unit(
    unit_uid: UUID, payload: UnitUpdateBase, units: UnitCRUDDep, Authorize: AuthJWTDep
):
    """Update unit."""
    Authorize.jwt_required()
    user_claims = Authorize.get_raw_jwt()
    await superuser_or_error(user_claims)
    subject = UUID(Authorize.get_jwt_subject())  # type: ignore

    lower_str_attrs(payload)
    update_payload = UnitUpdate(**payload.dict(exclude_unset=True), modified_by=subject)
    unit = await units.update_unit(unit_uid, update_payload)
    if unit is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="unit not found."
        )
    return unit


@router.delete("/{unit_uid}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_unit(unit_uid: UUID, units: UnitCRUDDep, Authorize: AuthJWTDep):
    """Delete unit."""
    Authorize.jwt_required()
    user_claims = Authorize.get_raw_jwt()
    await superuser_or_error(user_claims)
    deleted = await units.delete_unit(unit_uid)
    if not deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="unit not found."
        )
