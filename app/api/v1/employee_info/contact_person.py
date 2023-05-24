"""Contact person api endpoints module."""
from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi_jwt_auth import AuthJWT  # type: ignore
from sqlalchemy.exc import IntegrityError

from app.api.v1.employee_info.contact_person_crud import ContactPersonCRUD
from app.api.v1.employee_info.dependencies import get_contact_person_crud
from app.api.v1.utils import staff_user_or_error
from app.models.employee_info.contact_person import (
    ContactPersonBase,
    ContactPersonCreate,
    ContactPersonRead,
    ContactPersonReadMany,
    ContactPersonUpdate,
    ContactPersonUpdateBase,
)
from app.utils.lower_case_attrs import lower_str_attrs

router = APIRouter(prefix="/employee/contact-persons", tags=["contact_person"])

ContactPersonCRUDDep = Annotated[ContactPersonCRUD, Depends(get_contact_person_crud)]
AuthJWTDep = Annotated[AuthJWT, Depends()]


@router.post("", response_model=ContactPersonRead, status_code=status.HTTP_201_CREATED)
async def create_contact_person(
    payload: ContactPersonBase,
    contact_persons: ContactPersonCRUDDep,
    Authorize: AuthJWTDep,
):
    """Create contact person endpoint."""
    Authorize.jwt_required()
    user_claims = Authorize.get_raw_jwt()
    await staff_user_or_error(user_claims=user_claims)
    user = UUID(Authorize.get_jwt_subject())  # type: ignore
    lower_str_attrs(payload)
    create_payload = ContactPersonCreate(
        **payload.dict(), created_by=user, modified_by=user
    )
    try:
        contact_person = await contact_persons.create_contact_person(create_payload)
    except IntegrityError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="duplicate or invalid field information.",
        )
    return contact_person


@router.get("", response_model=ContactPersonReadMany)
async def read_many(contact_persons: ContactPersonCRUDDep, Authorize: AuthJWTDep):
    """Read many contact persons."""
    Authorize.jwt_required()
    contact_person_list = await contact_persons.read_many()

    return contact_person_list


@router.get("/employee-id/{employee_uid}", response_model=ContactPersonReadMany)
async def read_many_by_employee(
    employee_uid: UUID, contact_persons: ContactPersonCRUDDep, Authorize: AuthJWTDep
):
    """Read many contact persons of an employee."""
    Authorize.jwt_required()
    contact_person_list = await contact_persons.read_many_by_employee(employee_uid)

    return contact_person_list


@router.get("/contact-id/{contact_person_uid}", response_model=ContactPersonRead)
async def read_by_uid(
    contact_person_uid: UUID,
    contact_persons: ContactPersonCRUDDep,
    Authorize: AuthJWTDep,
):
    """Read contact person by uid."""
    Authorize.jwt_required()
    contact_person = await contact_persons.read_by_uid(contact_person_uid)
    if contact_person is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="contact person not found."
        )
    return contact_person


@router.patch("/{contact_person_uid}", response_model=ContactPersonRead)
async def update_contact_person(
    contact_person_uid: UUID,
    payload: ContactPersonUpdateBase,
    contact_persons: ContactPersonCRUDDep,
    Authorize: AuthJWTDep,
):
    """Update contact person."""
    Authorize.jwt_required()
    user_claims = Authorize.get_raw_jwt()
    await staff_user_or_error(user_claims=user_claims)
    user = UUID(Authorize.get_jwt_subject())  # type: ignore
    lower_str_attrs(payload)
    update_payload = ContactPersonUpdate(
        **payload.dict(exclude_unset=True), modified_by=user
    )
    contact_person = await contact_persons.update_contact_person(
        contact_person_uid, update_payload
    )
    if contact_person is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="contact person not found."
        )
    return contact_person


@router.delete("/{contact_person_uid}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_contact_person(
    contact_person_uid: UUID,
    contact_persons: ContactPersonCRUDDep,
    Authorize: AuthJWTDep,
):
    """Delete contact person."""
    Authorize.jwt_required()
    user_claims = Authorize.get_raw_jwt()
    await staff_user_or_error(user_claims=user_claims)
    deleted = await contact_persons.delete_contact_person(contact_person_uid)
    if not deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="contact person not found."
        )
