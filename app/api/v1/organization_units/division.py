"""Division api endpoints module."""
from typing import Annotated
from uuid import UUID

import pandas as pd
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import FileResponse
from fastapi_jwt_auth import AuthJWT  # type: ignore
from sqlalchemy.exc import IntegrityError

from app.api.v1.organization_units.dependencies import get_divisions_crud
from app.api.v1.organization_units.division_crud import DivisionCRUD
from app.api.v1.utils import superuser_or_error
from app.models.organization_units.division import (
    DivisionBase,
    DivisionCreate,
    DivisionRead,
    DivisionReadMany,
    DivisionUpdate,
)
from app.utils.lower_case_attrs import lower_str_attrs

router = APIRouter(prefix="/divisions", tags=["division"])

DivisionCRUDDep = Annotated[DivisionCRUD, Depends(get_divisions_crud)]
AuthJWTDep = Annotated[AuthJWT, Depends()]


@router.post("", response_model=DivisionRead, status_code=status.HTTP_201_CREATED)
async def create_division(
    payload: DivisionBase, divisions: DivisionCRUDDep, Authorize: AuthJWTDep
):
    """Create division endpoint."""
    Authorize.jwt_required()
    user_claims = Authorize.get_raw_jwt()
    await superuser_or_error(user_claims)
    subject = UUID(Authorize.get_jwt_subject())  # type: ignore

    lower_str_attrs(payload)
    create_payload = DivisionCreate(
        **payload.dict(), created_by=subject, modified_by=subject
    )
    try:
        division = await divisions.create(payload=create_payload)
    except IntegrityError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="duplicate division name."
        )

    return division


@router.get("", response_model=DivisionReadMany)
async def read_many(divisions: DivisionCRUDDep, Authorize: AuthJWTDep):
    """Read many divisions."""
    Authorize.jwt_required()
    division_list = await divisions.read_many()

    return division_list


@router.get("/{division_uid}", response_model=DivisionRead)
async def read_by_uid(
    division_uid: UUID, divisions: DivisionCRUDDep, Authorize: AuthJWTDep
):
    """Read division by uid."""
    Authorize.jwt_required()
    division = await divisions.read_by_uid(division_uid)
    if division is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="division not found."
        )
    return division


@router.patch("/{division_uid}", response_model=DivisionRead)
async def updated_division(
    division_uid: UUID,
    payload: DivisionBase,
    divisions: DivisionCRUDDep,
    Authorize: AuthJWTDep,
):
    """Update division."""
    Authorize.jwt_required()
    user_claims = Authorize.get_raw_jwt()
    await superuser_or_error(user_claims)
    subject = UUID(Authorize.get_jwt_subject())  # type: ignore

    lower_str_attrs(payload)
    update_payload = DivisionUpdate(**payload.dict(), modified_by=subject)
    division = await divisions.update_division(division_uid, update_payload)
    if division is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="division not found."
        )
    return division


@router.delete("/{division_uid}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_division(
    division_uid: UUID, divisions: DivisionCRUDDep, Authorize: AuthJWTDep
):
    """Delete division."""
    Authorize.jwt_required()
    user_claims = Authorize.get_raw_jwt()
    await superuser_or_error(user_claims)
    deleted = await divisions.delete_division(division_uid)
    if not deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="division not found."
        )


@router.get("/download/csv", response_class=FileResponse)
async def download_csv(
    divisions: DivisionCRUDDep, Authorize: AuthJWTDep
) -> FileResponse:
    """Download divisions as csv."""
    Authorize.jwt_required()
    divisions_list = await divisions.read_many()
    df = pd.DataFrame([d.dict() for d in divisions_list.result])
    df.to_csv("hr_tmp/divisions.csv", index=False)
    return FileResponse("hr_tmp/divisions.csv")


@router.get("/download/xlsx", response_class=FileResponse)
async def download_excel(
    divisions: DivisionCRUDDep, Authorize: AuthJWTDep
) -> FileResponse:
    """Download divisions as excel."""
    Authorize.jwt_required()
    divisions_list = await divisions.read_many()
    df = pd.DataFrame([d.dict() for d in divisions_list.result])
    df.to_excel("hr_tmp/divisions.xlsx", index=False)
    return FileResponse("hr_tmp/divisions.xlsx")
