"""Section api endpoints module."""
from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.exc import IntegrityError

from app.api.v1.organization_units.dependencies import get_sub_sections_crud
from app.api.v1.organization_units.sub_section_crud import SubSectionCRUD
from app.models.organization_units.sub_section import (
    SubSectionCreate,
    SubSectionRead,
    SubSectionReadMany,
    SubSectionUpdate,
)
from app.utils.lower_case_attrs import lower_str_attrs

router = APIRouter(prefix="/sub-sections", tags=["sub_section"])

SubSectionCRUDDep = Annotated[SubSectionCRUD, Depends(get_sub_sections_crud)]


@router.post("", response_model=SubSectionRead, status_code=status.HTTP_201_CREATED)
async def create_sub_section(
    payload: SubSectionCreate,
    sub_sections: SubSectionCRUDDep,
):
    """Create sub section."""
    lower_str_attrs(payload)
    try:
        sub_section = await sub_sections.create(payload=payload)
    except IntegrityError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="duplicate sub section name.",
        )
    return sub_section


@router.get("", response_model=SubSectionReadMany)
async def read_many(sub_sections: SubSectionCRUDDep):
    """Read many sub sections."""
    sub_section_list = await sub_sections.read_many()

    return sub_section_list


@router.get("/{sub_section_uid}", response_model=SubSectionRead)
async def read_by_uid(sub_section_uid: UUID, sub_sections: SubSectionCRUDDep):
    """Read sub section by uid."""
    sub_section = await sub_sections.read_by_uid(sub_section_uid)
    if sub_section is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="sub section not found."
        )
    return sub_section


@router.patch("/{sub_section_uid}", response_model=SubSectionRead)
async def update_sub_section(
    sub_section_uid: UUID,
    payload: SubSectionUpdate,
    sub_sections: SubSectionCRUDDep,
):
    """Update sub section."""
    lower_str_attrs(payload)
    sub_section = await sub_sections.update_sub_section(sub_section_uid, payload)
    if sub_section is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="sub section not found."
        )
    return sub_section


@router.delete("/{sub_section_uid}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_sub_section(sub_section_uid: UUID, sub_sections: SubSectionCRUDDep):
    """Delete sub section."""
    deleted = await sub_sections.delete_sub_section(sub_section_uid)
    if not deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="sub section not found."
        )
