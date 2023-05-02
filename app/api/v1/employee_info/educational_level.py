"""Educational level api endpoints module."""
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.exc import IntegrityError

from app.api.v1.employee_info.dependencies import get_educational_level_crud
from app.api.v1.employee_info.educational_level_crud import EducationalLevelCRUD
from app.models.employee_info.educational_level import (
    EducationalLevelCreate,
    EducationalLevelRead,
    EducationalLevelReadMany,
    EducationalLevelUpdate,
)
from app.utils.lower_case_attrs import lower_str_attrs

router = APIRouter(prefix="/educational-levels", tags=["educational_level"])


@router.post(
    "", response_model=EducationalLevelRead, status_code=status.HTTP_201_CREATED
)
async def create_educational_level(
    payload: EducationalLevelCreate,
    educational_levels: EducationalLevelCRUD = Depends(get_educational_level_crud),
):
    """Create educational level endpoint."""
    lower_str_attrs(payload)
    try:
        educational_level = await educational_levels.create(payload=payload)
    except IntegrityError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="duplicate educational level.",
        )

    return educational_level


@router.get("", response_model=EducationalLevelReadMany)
async def read_many(
    educational_levels: EducationalLevelCRUD = Depends(get_educational_level_crud),
):
    """Read many educational levels."""
    educational_level_list = await educational_levels.read_many()

    return educational_level_list


@router.get("/{educational_level_uid}", response_model=EducationalLevelRead)
async def read_by_uid(
    educational_level_uid: UUID,
    educational_levels: EducationalLevelCRUD = Depends(get_educational_level_crud),
):
    """Read educational level by uid."""
    educational_level = await educational_levels.read_by_uid(educational_level_uid)
    if educational_level is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="educational level not found."
        )
    return educational_level


@router.patch("/{educational_level_uid}", response_model=EducationalLevelRead)
async def updated_educational_level(
    educational_level_uid: UUID,
    payload: EducationalLevelUpdate,
    educational_levels: EducationalLevelCRUD = Depends(get_educational_level_crud),
):
    """Update educational level."""
    lower_str_attrs(payload)
    educational_level = await educational_levels.update_educational_level(
        educational_level_uid, payload
    )
    if educational_level is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="educational level not found."
        )
    return educational_level


@router.delete("/{educational_level_uid}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_educational_level(
    educational_level_uid: UUID,
    educational_levels: EducationalLevelCRUD = Depends(get_educational_level_crud),
):
    """Delete educational level."""
    deleted = await educational_levels.delete_educational_level(educational_level_uid)
    if not deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="educational level not found."
        )
