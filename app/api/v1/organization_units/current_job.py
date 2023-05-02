"""Current job api endpoints module."""
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.exc import IntegrityError

from app.api.v1.organization_units.current_job_crud import CurrentJobCRUD
from app.api.v1.organization_units.dependencies import get_current_job_crud
from app.models.organization_units.current_job import (
    CurrentJobCreate,
    CurrentJobRead,
    CurrentJobReadMany,
    CurrentJobUpdate,
)
from app.utils.lower_case_attrs import lower_str_attrs

router = APIRouter(prefix="/current-jobs", tags=["current_job"])


@router.post("", response_model=CurrentJobRead, status_code=status.HTTP_201_CREATED)
async def create_current_job(
    payload: CurrentJobCreate,
    current_jobs: CurrentJobCRUD = Depends(get_current_job_crud),
):
    """Create current job endpoint."""
    lower_str_attrs(payload)
    try:
        current_job = await current_jobs.create(payload=payload)
    except IntegrityError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="duplicate current job title.",
        )
    return current_job


@router.get("", response_model=CurrentJobReadMany)
async def read_many(current_jobs: CurrentJobCRUD = Depends(get_current_job_crud)):
    """Read many current jobs."""
    current_job_list = await current_jobs.read_many()

    return current_job_list


@router.get("/{current_job_uid}", response_model=CurrentJobRead)
async def read_by_uid(
    current_job_uid: UUID, current_jobs: CurrentJobCRUD = Depends(get_current_job_crud)
):
    """Read current job by id."""
    current_job = await current_jobs.read_by_uid(current_job_uid)
    if current_job is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="current job not found."
        )
    return current_job


@router.patch("/{current_job_uid}", response_model=CurrentJobRead)
async def update_current_job(
    current_job_uid: UUID,
    payload: CurrentJobUpdate,
    current_jobs: CurrentJobCRUD = Depends(get_current_job_crud),
):
    """Update current job."""
    lower_str_attrs(payload)
    current_job = await current_jobs.update_current_job(current_job_uid, payload)
    if current_job is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="current job not found."
        )
    return current_job


@router.delete("/{current_job_uid}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_current_job(
    current_job_uid: UUID, current_jobs: CurrentJobCRUD = Depends(get_current_job_crud)
):
    """Delete current job."""
    deleted = await current_jobs.delete_current_job(current_job_uid)
    if not deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="current job not found."
        )
