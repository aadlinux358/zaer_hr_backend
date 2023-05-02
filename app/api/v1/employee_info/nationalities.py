"""Nationality api endpoints module."""
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.exc import IntegrityError

from app.api.v1.employee_info.dependencies import get_nationality_crud
from app.api.v1.employee_info.nationalities_crud import NationalityCRUD
from app.models.employee_info.nationalities import (
    NationalityCreate,
    NationalityRead,
    NationalityReadMany,
    NationalityUpdate,
)
from app.utils.lower_case_attrs import lower_str_attrs

router = APIRouter(prefix="/nationalities", tags=["nationality"])


@router.post("", response_model=NationalityRead, status_code=status.HTTP_201_CREATED)
async def create_nationality(
    payload: NationalityCreate,
    nationalities: NationalityCRUD = Depends(get_nationality_crud),
):
    """Create nationality endpoint."""
    lower_str_attrs(payload)
    try:
        nationality = await nationalities.create(payload=payload)
    except IntegrityError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="duplicate nationality name.",
        )

    return nationality


@router.get("", response_model=NationalityReadMany)
async def read_many(nationalities: NationalityCRUD = Depends(get_nationality_crud)):
    """Read many nationalities."""
    nationality_list = await nationalities.read_many()

    return nationality_list


@router.get("/{nationality_uid}", response_model=NationalityRead)
async def read_by_uid(
    nationality_uid: UUID,
    nationalities: NationalityCRUD = Depends(get_nationality_crud),
):
    """Read nationality by uid."""
    nationality = await nationalities.read_by_uid(nationality_uid)
    if nationality is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="nationality not found."
        )
    return nationality


@router.patch("/{nationality_uid}", response_model=NationalityRead)
async def updated_nationality(
    nationality_uid: UUID,
    payload: NationalityUpdate,
    nationalities: NationalityCRUD = Depends(get_nationality_crud),
):
    """Update nationality."""
    lower_str_attrs(payload)
    nationality = await nationalities.update_nationality(nationality_uid, payload)
    if nationality is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="nationality not found."
        )
    return nationality


@router.delete("/{nationality_uid}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_nationality(
    nationality_uid: UUID,
    nationalities: NationalityCRUD = Depends(get_nationality_crud),
):
    """Delete nationality."""
    deleted = await nationalities.delete_nationality(nationality_uid)
    if not deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="nationality not found."
        )
