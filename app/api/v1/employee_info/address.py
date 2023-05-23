"""Address api endpoints module."""
from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi_jwt_auth import AuthJWT  # type: ignore
from sqlalchemy.exc import IntegrityError

from app.api.v1.employee_info.address_crud import AddressCRUD
from app.api.v1.employee_info.dependencies import get_address_crud
from app.api.v1.utils import staff_user_or_error
from app.models.employee_info.address import (
    AddressBase,
    AddressCreate,
    AddressRead,
    AddressReadMany,
    AddressUpdate,
    AddressUpdateBase,
)
from app.utils.lower_case_attrs import lower_str_attrs

router = APIRouter(prefix="/employee/addresses", tags=["address"])

AddressCRUDDep = Annotated[AddressCRUD, Depends(get_address_crud)]
AuthJWTDep = Annotated[AuthJWT, Depends()]


@router.post("", response_model=AddressRead, status_code=status.HTTP_201_CREATED)
async def create_address(
    payload: AddressBase, addresses: AddressCRUDDep, Authorize: AuthJWTDep
):
    """Create address endpoint."""
    Authorize.jwt_required()
    user_claims = Authorize.get_raw_jwt()
    await staff_user_or_error(user_claims=user_claims)
    user = UUID(Authorize.get_jwt_subject())  # type: ignore
    lower_str_attrs(payload)
    create_payload = AddressCreate(**payload.dict(), created_by=user, modified_by=user)
    try:
        address = await addresses.create_address(create_payload)
    except IntegrityError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="duplicate or invalid field information.",
        )
    return address


@router.get("", response_model=AddressReadMany)
async def read_many(addresses: AddressCRUDDep, Authorize: AuthJWTDep):
    """Read many addresses."""
    Authorize.jwt_required()
    address_list = await addresses.read_many()

    return address_list


@router.get("/{address_uid}", response_model=AddressRead)
async def read_by_uid(
    address_uid: UUID, addresses: AddressCRUDDep, Authorize: AuthJWTDep
):
    """Read address by uid."""
    Authorize.jwt_required()
    address = await addresses.read_by_uid(address_uid)
    if address is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="address not found."
        )
    return address


@router.patch("/{address_uid}", response_model=AddressRead)
async def update_address(
    address_uid: UUID,
    payload: AddressUpdateBase,
    addresses: AddressCRUDDep,
    Authorize: AuthJWTDep,
):
    """Update address."""
    Authorize.jwt_required()
    user_claims = Authorize.get_raw_jwt()
    await staff_user_or_error(user_claims=user_claims)
    user = UUID(Authorize.get_jwt_subject())  # type: ignore
    lower_str_attrs(payload)
    update_payload = AddressUpdate(**payload.dict(exclude_unset=True), modified_by=user)
    address = await addresses.update_address(address_uid, update_payload)
    if address is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="address not found."
        )
    return address


@router.delete("/{address_uid}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_address(
    address_uid: UUID, addresses: AddressCRUDDep, Authorize: AuthJWTDep
):
    """Delete address."""
    Authorize.jwt_required()
    user_claims = Authorize.get_raw_jwt()
    await staff_user_or_error(user_claims=user_claims)
    deleted = await addresses.delete_address(address_uid)
    if not deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="address not found."
        )
