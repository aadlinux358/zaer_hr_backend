"""Child api endpoints module."""
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.exc import IntegrityError

from app.api.v1.employee_info.child_crud import ChildCRUD
from app.api.v1.employee_info.dependencies import get_child_crud
from app.models.employee_info.child import (
    ChildCreate,
    ChildRead,
    ChildReadMany,
    ChildUpdate,
)
from app.utils.lower_case_attrs import lower_str_attrs

router = APIRouter(prefix="/children", tags=["child"])


@router.post("", response_model=ChildRead, status_code=status.HTTP_201_CREATED)
async def create_child(
    payload: ChildCreate, children: ChildCRUD = Depends(get_child_crud)
):
    """Create child endpoint."""
    lower_str_attrs(payload)
    try:
        child = await children.create_child(payload)
    except IntegrityError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="duplicate or invalid field information.",
        )
    return child


@router.get("", response_model=ChildReadMany)
async def read_many(children: ChildCRUD = Depends(get_child_crud)):
    """Read many children."""
    child_list = await children.read_many()

    return child_list


@router.get("/{child_uid}", response_model=ChildRead)
async def read_by_uid(child_uid: UUID, children: ChildCRUD = Depends(get_child_crud)):
    """Read child by uid."""
    child = await children.read_by_uid(child_uid)
    if child is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="child not found."
        )
    return child


@router.patch("/{child_uid}", response_model=ChildRead)
async def update_child(
    child_uid: UUID, payload: ChildUpdate, children: ChildCRUD = Depends(get_child_crud)
):
    """Update child."""
    lower_str_attrs(payload)
    child = await children.update_child(child_uid, payload)
    if child is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="child not found."
        )
    return child


@router.delete("/{child_uid}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_child(child_uid: UUID, children: ChildCRUD = Depends(get_child_crud)):
    """Delete child."""
    deleted = await children.delete_child(child_uid)
    if not deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="child not found."
        )
