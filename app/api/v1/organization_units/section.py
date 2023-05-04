"""Section api endpoints module."""
from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.exc import IntegrityError

from app.api.v1.organization_units.dependencies import get_sections_crud
from app.api.v1.organization_units.section_crud import SectionCRUD
from app.models.organization_units.section import (
    SectionCreate,
    SectionRead,
    SectionReadMany,
    SectionUpdate,
)
from app.utils.lower_case_attrs import lower_str_attrs

router = APIRouter(prefix="/sections", tags=["section"])

SectionCRUDDep = Annotated[SectionCRUD, Depends(get_sections_crud)]


@router.post("", response_model=SectionRead, status_code=status.HTTP_201_CREATED)
async def create_section(payload: SectionCreate, sections: SectionCRUDDep):
    """Create section."""
    lower_str_attrs(payload)
    try:
        section = await sections.create(payload=payload)
    except IntegrityError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="duplicate section name."
        )

    return section


@router.get("", response_model=SectionReadMany)
async def read_many(sections: SectionCRUDDep):
    """Read many sections."""
    section_list = await sections.read_many()

    return section_list


@router.get("/{section_uid}", response_model=SectionRead)
async def read_by_uid(section_uid: UUID, sections: SectionCRUDDep):
    """Read section by uid."""
    section = await sections.read_by_uid(section_uid)
    if section is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="section not found."
        )
    return section


@router.patch("/{section_uid}", response_model=SectionRead)
async def update_section(
    section_uid: UUID,
    payload: SectionUpdate,
    sections: SectionCRUDDep,
):
    """Update section."""
    lower_str_attrs(payload)
    section = await sections.update_section(section_uid, payload)
    if section is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="section not found."
        )

    return section


@router.delete("/{section_uid}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_section(section_uid: UUID, sections: SectionCRUDDep):
    """Delete section."""
    deleted = await sections.delete_section(section_uid)
    if not deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="section not found."
        )
