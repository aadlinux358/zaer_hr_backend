"""Country api endpoints module."""
from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi_jwt_auth import AuthJWT  # type: ignore
from sqlalchemy.exc import IntegrityError

from app.api.v1.employee_info.country_crud import CountryCRUD
from app.api.v1.employee_info.dependencies import get_country_crud
from app.api.v1.utils.exception_responses import superuser_or_error
from app.models.employee_info.country import (
    CountryBase,
    CountryCreate,
    CountryRead,
    CountryReadMany,
    CountryUpdate,
    CountryUpdateBase,
)
from app.utils.lower_case_attrs import lower_str_attrs

router = APIRouter(prefix="/countries", tags=["country"])

CountryCRUDDep = Annotated[CountryCRUD, Depends(get_country_crud)]
AuthJWTDep = Annotated[AuthJWT, Depends()]


@router.post("", response_model=CountryRead, status_code=status.HTTP_201_CREATED)
async def create_country(
    payload: CountryBase, countries: CountryCRUDDep, Authorize: AuthJWTDep
):
    """Create country endpoint."""
    Authorize.jwt_required()
    user_claims = Authorize.get_raw_jwt()
    await superuser_or_error(user_claims=user_claims)
    subject = UUID(Authorize.get_jwt_subject())  # type: ignore
    lower_str_attrs(payload)
    create_payload = CountryCreate(
        **payload.dict(), created_by=subject, modified_by=subject
    )
    try:
        country = await countries.create(payload=create_payload)
    except IntegrityError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="duplicate country name.",
        )

    return country


@router.get("", response_model=CountryReadMany)
async def read_many(countries: CountryCRUDDep, Authorize: AuthJWTDep):
    """Read many countries."""
    Authorize.jwt_required()
    country_list = await countries.read_many()

    return country_list


@router.get("/{country_uid}", response_model=CountryRead)
async def read_by_uid(
    country_uid: UUID, countries: CountryCRUDDep, Authorize: AuthJWTDep
):
    """Read country by uid."""
    Authorize.jwt_required()
    country = await countries.read_by_uid(country_uid)
    if country is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="country not found."
        )
    return country


@router.patch("/{country_uid}", response_model=CountryRead)
async def updated_country(
    country_uid: UUID,
    payload: CountryUpdateBase,
    countries: CountryCRUDDep,
    Authorize: AuthJWTDep,
):
    """Update country."""
    Authorize.jwt_required()
    user_claims = Authorize.get_raw_jwt()
    await superuser_or_error(user_claims=user_claims)
    subject = UUID(Authorize.get_jwt_subject())  # type: ignore
    lower_str_attrs(payload)
    update_payload = CountryUpdate(
        **payload.dict(exclude_unset=True), modified_by=subject
    )
    country = await countries.update_country(country_uid, update_payload)
    if country is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="country not found."
        )
    return country


@router.delete("/{country_uid}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_country(
    country_uid: UUID, countries: CountryCRUDDep, Authorize: AuthJWTDep
):
    """Delete country."""
    Authorize.jwt_required()
    user_claims = Authorize.get_raw_jwt()
    await superuser_or_error(user_claims=user_claims)
    deleted = await countries.delete_country(country_uid)
    if not deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="country not found."
        )
