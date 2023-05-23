"""Address database operations module."""
from typing import Optional
from uuid import UUID

from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession

from app.models.employee_info.address import (
    AddressCreate,
    AddressDB,
    AddressReadMany,
    AddressUpdate,
)


class AddressCRUD:
    """Database operations handler class."""

    def __init__(self, session: AsyncSession) -> None:
        """DB operations class initializer."""
        self.session = session

    async def create_address(self, payload: AddressCreate) -> AddressDB:
        """Create database address."""
        values = payload.dict()

        address = AddressDB(**values)
        self.session.add(address)
        await self.session.commit()
        await self.session.refresh(address)

        return address

    async def read_many(self) -> AddressReadMany:
        """Fetch all address records."""
        statement = select(AddressDB)
        result = await self.session.exec(statement)  # type: ignore
        all_result = result.all()
        return AddressReadMany(count=len(all_result), result=all_result)

    async def read_by_uid(self, address_uid: UUID) -> Optional[AddressDB]:
        """Read address by uid."""
        statement = select(AddressDB).where(AddressDB.uid == address_uid)
        result = await self.session.exec(statement)  # type: ignore
        address = result.one_or_none()

        return address

    async def update_address(
        self, address_uid: UUID, payload: AddressUpdate
    ) -> Optional[AddressDB]:
        """Update address."""
        address = await self.read_by_uid(address_uid)
        if address is None:
            return None

        values = payload.dict(exclude_unset=True)
        for k, v in values.items():
            setattr(address, k, v)

        self.session.add(address)
        await self.session.commit()
        await self.session.refresh(address)

        return address

    async def delete_address(self, address_uid: UUID) -> bool:
        """Delete address."""
        address = await self.read_by_uid(address_uid)
        if address is None:
            return False
        await self.session.delete(address)
        await self.session.commit()

        return True
