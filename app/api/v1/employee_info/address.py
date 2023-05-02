"""Address api endpoints module."""
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.exc import IntegrityError

from app.api.v1.employee_info.address_crud import AddressCRUD
from app.api.v1.employee_info.dependencies import get_address_crud
from app.models.employee_info.address import (
    AddressCreate,
    AddressRead,
    AddressReadMany,
    AddressUpdate,
)
from app.utils.lower_case_attrs import lower_str_attrs

router = APIRouter(prefix="/addresses", tags=["address"])


@router.post("", response_model=AddressRead, status_code=status.HTTP_201_CREATED)
async def create_address(
    payload: AddressCreate, addresses: AddressCRUD = Depends(get_address_crud)
):
    """Create address endpoint."""
    lower_str_attrs(payload)
    try:
        address = await addresses.create_address(payload)
    except IntegrityError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="duplicate or invalid field information.",
        )
    return address


@router.get("", response_model=AddressReadMany)
async def read_many(addresses: AddressCRUD = Depends(get_address_crud)):
    """Read many addresses."""
    address_list = await addresses.read_many()

    return address_list


@router.get("/{address_uid}", response_model=AddressRead)
async def read_by_uid(
    address_uid: UUID, addresses: AddressCRUD = Depends(get_address_crud)
):
    """Read address by uid."""
    address = await addresses.read_by_uid(address_uid)
    if address is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="address not found."
        )
    return address


@router.patch("/{address_uid}", response_model=AddressRead)
async def update_address(
    address_uid: UUID,
    payload: AddressUpdate,
    addresses: AddressCRUD = Depends(get_address_crud),
):
    """Update address."""
    lower_str_attrs(payload)
    address = await addresses.update_address(address_uid, payload)
    if address is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="address not found."
        )
    return address


@router.delete("/{address_uid}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_address(
    address_uid: UUID, addresses: AddressCRUD = Depends(get_address_crud)
):
    """Delete address."""
    deleted = await addresses.delete_address(address_uid)
    if not deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="address not found."
        )
