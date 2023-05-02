"""Contact person api endpoints module."""
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.exc import IntegrityError

from app.api.v1.employee_info.contact_person_crud import ContactPersonCRUD
from app.api.v1.employee_info.dependencies import get_contact_person_crud
from app.models.employee_info.contact_person import (
    ContactPersonCreate,
    ContactPersonRead,
    ContactPersonReadMany,
    ContactPersonUpdate,
)
from app.utils.lower_case_attrs import lower_str_attrs

router = APIRouter(prefix="/contact-person", tags=["contact_person"])


@router.post("", response_model=ContactPersonRead, status_code=status.HTTP_201_CREATED)
async def create_contact_person(
    payload: ContactPersonCreate,
    contact_persons: ContactPersonCRUD = Depends(get_contact_person_crud),
):
    """Create contact person endpoint."""
    lower_str_attrs(payload)
    try:
        contact_person = await contact_persons.create_contact_person(payload)
    except IntegrityError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="duplicate or invalid field information.",
        )
    return contact_person


@router.get("", response_model=ContactPersonReadMany)
async def read_many(
    contact_persons: ContactPersonCRUD = Depends(get_contact_person_crud),
):
    """Read many contact persons."""
    contact_person_list = await contact_persons.read_many()

    return contact_person_list


@router.get("/{contact_person_uid}", response_model=ContactPersonRead)
async def read_by_uid(
    contact_person_uid: UUID,
    contact_persons: ContactPersonCRUD = Depends(get_contact_person_crud),
):
    """Read contact person by uid."""
    contact_person = await contact_persons.read_by_uid(contact_person_uid)
    if contact_person is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="contact person not found."
        )
    return contact_person


@router.patch("/{contact_person_uid}", response_model=ContactPersonRead)
async def update_contact_person(
    contact_person_uid: UUID,
    payload: ContactPersonUpdate,
    contact_persons: ContactPersonCRUD = Depends(get_contact_person_crud),
):
    """Update contact person."""
    lower_str_attrs(payload)
    contact_person = await contact_persons.update_contact_person(
        contact_person_uid, payload
    )
    if contact_person is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="contact person not found."
        )
    return contact_person


@router.delete("/{contact_person_uid}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_contact_person(
    contact_person_uid: UUID,
    contact_persons: ContactPersonCRUD = Depends(get_contact_person_crud),
):
    """Delete contact person."""
    deleted = await contact_persons.delete_contact_person(contact_person_uid)
    if not deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="contact person not found."
        )
