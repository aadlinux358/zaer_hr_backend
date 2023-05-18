"""Educational level api endpoints module."""
from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi_jwt_auth import AuthJWT  # type: ignore
from sqlalchemy.exc import IntegrityError

from app.api.v1.employee_info.dependencies import get_educational_level_crud
from app.api.v1.employee_info.educational_level_crud import EducationalLevelCRUD
from app.api.v1.utils.exception_responses import superuser_or_error
from app.models.employee_info.educational_level import (
    EducationalLevelBase,
    EducationalLevelCreate,
    EducationalLevelRead,
    EducationalLevelReadMany,
    EducationalLevelUpdate,
    EducationalLevelUpdateBase,
)
from app.utils.lower_case_attrs import lower_str_attrs

router = APIRouter(prefix="/educational-levels", tags=["educational_level"])

EducationalLevelCRUDDep = Annotated[
    EducationalLevelCRUD, Depends(get_educational_level_crud)
]
AuthJWTDep = Annotated[AuthJWT, Depends()]


@router.post(
    "", response_model=EducationalLevelRead, status_code=status.HTTP_201_CREATED
)
async def create_educational_level(
    payload: EducationalLevelBase,
    educational_levels: EducationalLevelCRUDDep,
    Authorize: AuthJWTDep,
):
    """Create educational level endpoint."""
    Authorize.jwt_required()
    user_claims = Authorize.get_raw_jwt()
    await superuser_or_error(user_claims=user_claims)
    subject = UUID(Authorize.get_jwt_subject())  # type: ignore
    lower_str_attrs(payload)
    create_payload = EducationalLevelCreate(
        **payload.dict(), created_by=subject, modified_by=subject
    )
    try:
        educational_level = await educational_levels.create(payload=create_payload)
    except IntegrityError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="duplicate educational level.",
        )

    return educational_level


@router.get("", response_model=EducationalLevelReadMany)
async def read_many(educational_levels: EducationalLevelCRUDDep, Authorize: AuthJWTDep):
    """Read many educational levels."""
    Authorize.jwt_required()
    educational_level_list = await educational_levels.read_many()

    return educational_level_list


@router.get("/{educational_level_uid}", response_model=EducationalLevelRead)
async def read_by_uid(
    educational_level_uid: UUID,
    educational_levels: EducationalLevelCRUDDep,
    Authorize: AuthJWTDep,
):
    """Read educational level by uid."""
    Authorize.jwt_required()
    educational_level = await educational_levels.read_by_uid(educational_level_uid)
    if educational_level is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="educational level not found."
        )
    return educational_level


@router.patch("/{educational_level_uid}", response_model=EducationalLevelRead)
async def updated_educational_level(
    educational_level_uid: UUID,
    payload: EducationalLevelUpdateBase,
    educational_levels: EducationalLevelCRUDDep,
    Authorize: AuthJWTDep,
):
    """Update educational level."""
    Authorize.jwt_required()
    user_claims = Authorize.get_raw_jwt()
    await superuser_or_error(user_claims=user_claims)
    subject = UUID(Authorize.get_jwt_subject())  # type: ignore
    lower_str_attrs(payload)
    update_payload = EducationalLevelUpdate(
        **payload.dict(exclude_unset=True), modified_by=subject
    )
    try:
        educational_level = await educational_levels.update_educational_level(
        educational_level_uid, update_payload
        )
    except IntegrityError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="duplicate educational level.",
        )
    if educational_level is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="educational level not found."
        )
    return educational_level


@router.delete("/{educational_level_uid}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_educational_level(
    educational_level_uid: UUID,
    educational_levels: EducationalLevelCRUDDep,
    Authorize: AuthJWTDep,
):
    """Delete educational level."""
    Authorize.jwt_required()
    user_claims = Authorize.get_raw_jwt()
    await superuser_or_error(user_claims=user_claims)
    deleted = await educational_levels.delete_educational_level(educational_level_uid)
    if not deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="educational level not found."
        )
