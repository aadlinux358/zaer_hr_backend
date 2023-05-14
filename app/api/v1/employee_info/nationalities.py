"""Nationality api endpoints module."""
from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi_jwt_auth import AuthJWT  # type: ignore
from sqlalchemy.exc import IntegrityError

from app.api.v1.employee_info.dependencies import get_nationality_crud
from app.api.v1.employee_info.nationalities_crud import NationalityCRUD
from app.api.v1.utils.exception_responses import superuser_or_error
from app.models.employee_info.nationalities import (
    NationalityBase,
    NationalityCreate,
    NationalityRead,
    NationalityReadMany,
    NationalityUpdate,
    NationalityUpdateBase,
)
from app.utils.lower_case_attrs import lower_str_attrs

router = APIRouter(prefix="/nationalities", tags=["nationality"])

NationalityCRUDDep = Annotated[NationalityCRUD, Depends(get_nationality_crud)]
AuthJWTDep = Annotated[AuthJWT, Depends()]


@router.post("", response_model=NationalityRead, status_code=status.HTTP_201_CREATED)
async def create_nationality(
    payload: NationalityBase, nationalities: NationalityCRUDDep, Authorize: AuthJWTDep
):
    """Create nationality endpoint."""
    Authorize.jwt_required()
    user_claims = Authorize.get_raw_jwt()
    await superuser_or_error(user_claims=user_claims)
    subject = UUID(Authorize.get_jwt_subject())  # type: ignore
    lower_str_attrs(payload)
    create_payload = NationalityCreate(
        **payload.dict(), created_by=subject, modified_by=subject
    )
    try:
        nationality = await nationalities.create(payload=create_payload)
    except IntegrityError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="duplicate nationality name.",
        )

    return nationality


@router.get("", response_model=NationalityReadMany)
async def read_many(nationalities: NationalityCRUDDep, Authorize: AuthJWTDep):
    """Read many nationalities."""
    Authorize.jwt_required()
    nationality_list = await nationalities.read_many()

    return nationality_list


@router.get("/{nationality_uid}", response_model=NationalityRead)
async def read_by_uid(
    nationality_uid: UUID, nationalities: NationalityCRUDDep, Authorize: AuthJWTDep
):
    """Read nationality by uid."""
    Authorize.jwt_required()
    nationality = await nationalities.read_by_uid(nationality_uid)
    if nationality is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="nationality not found."
        )
    return nationality


@router.patch("/{nationality_uid}", response_model=NationalityRead)
async def updated_nationality(
    nationality_uid: UUID,
    payload: NationalityUpdateBase,
    nationalities: NationalityCRUDDep,
    Authorize: AuthJWTDep,
):
    """Update nationality."""
    Authorize.jwt_required()
    user_claims = Authorize.get_raw_jwt()
    await superuser_or_error(user_claims=user_claims)
    subject = UUID(Authorize.get_jwt_subject())  # type: ignore
    lower_str_attrs(payload)
    update_payload = NationalityUpdate(
        **payload.dict(exclude_unset=True), modified_by=subject
    )
    nationality = await nationalities.update_nationality(
        nationality_uid, update_payload
    )
    if nationality is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="nationality not found."
        )
    return nationality


@router.delete("/{nationality_uid}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_nationality(
    nationality_uid: UUID, nationalities: NationalityCRUDDep, Authorize: AuthJWTDep
):
    """Delete nationality."""
    Authorize.jwt_required()
    user_claims = Authorize.get_raw_jwt()
    await superuser_or_error(user_claims=user_claims)
    deleted = await nationalities.delete_nationality(nationality_uid)
    if not deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="nationality not found."
        )
