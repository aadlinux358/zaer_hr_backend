"""Section api endpoints module."""
from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi_jwt_auth import AuthJWT  # type: ignore
from sqlalchemy.exc import IntegrityError

from app.api.v1.organization_units.dependencies import get_sections_crud
from app.api.v1.organization_units.section_crud import SectionCRUD
from app.api.v1.utils import superuser_or_error
from app.models.organization_units.section import (
    SectionBase,
    SectionCreate,
    SectionRead,
    SectionReadMany,
    SectionUpdate,
    SectionUpdateBase,
)
from app.utils.lower_case_attrs import lower_str_attrs

router = APIRouter(prefix="/sections", tags=["section"])

SectionCRUDDep = Annotated[SectionCRUD, Depends(get_sections_crud)]
AuthJWTDep = Annotated[AuthJWT, Depends()]


@router.post("", response_model=SectionRead, status_code=status.HTTP_201_CREATED)
async def create_section(
    payload: SectionBase, sections: SectionCRUDDep, Authorize: AuthJWTDep
):
    """Create section."""
    Authorize.jwt_required()
    user_claims = Authorize.get_raw_jwt()
    await superuser_or_error(user_claims)
    subject = UUID(Authorize.get_jwt_subject())  # type: ignore

    lower_str_attrs(payload)
    create_payload = SectionCreate(
        **payload.dict(), modified_by=subject, created_by=subject
    )
    try:
        section = await sections.create(payload=create_payload)
    except IntegrityError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="duplicate section name.",
        )
    return section


@router.get("", response_model=SectionReadMany)
async def read_many(sections: SectionCRUDDep, Authorize: AuthJWTDep):
    """Read many sections."""
    Authorize.jwt_required()
    section_list = await sections.read_many()

    return section_list


@router.get("/{section_uid}", response_model=SectionRead)
async def read_by_uid(
    section_uid: UUID, sections: SectionCRUDDep, Authorize: AuthJWTDep
):
    """Read section by uid."""
    Authorize.jwt_required()
    section = await sections.read_by_uid(section_uid)
    if section is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="section not found."
        )
    return section


@router.patch("/{section_uid}", response_model=SectionRead)
async def update_section(
    section_uid: UUID,
    payload: SectionUpdateBase,
    sections: SectionCRUDDep,
    Authorize: AuthJWTDep,
):
    """Update section."""
    Authorize.jwt_required()
    user_claims = Authorize.get_raw_jwt()
    await superuser_or_error(user_claims)
    subject = UUID(Authorize.get_jwt_subject())  # type: ignore

    lower_str_attrs(payload)
    update_payload = SectionUpdate(
        **payload.dict(exclude_unset=True), modified_by=subject
    )
    section = await sections.update_section(section_uid, update_payload)
    if section is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="section not found."
        )
    return section


@router.delete("/{section_uid}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_section(
    section_uid: UUID, sections: SectionCRUDDep, Authorize: AuthJWTDep
):
    """Delete section."""
    Authorize.jwt_required()
    user_claims = Authorize.get_raw_jwt()
    await superuser_or_error(user_claims)
    deleted = await sections.delete_section(section_uid)
    if not deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="section not found."
        )
