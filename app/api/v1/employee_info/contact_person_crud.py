"""Contact person database operations module."""
from typing import Optional
from uuid import UUID

from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession

from app.models.employee_info.contact_person import (
    ContactPersonCreate,
    ContactPersonDB,
    ContactPersonReadMany,
    ContactPersonUpdate,
)


class ContactPersonCRUD:
    """Database operations handler class."""

    def __init__(self, session: AsyncSession) -> None:
        """DB operations class initializer."""
        self.session = session

    async def create_contact_person(
        self, payload: ContactPersonCreate
    ) -> ContactPersonDB:
        """Create database contact person."""
        values = payload.dict()

        contact_person = ContactPersonDB(**values)
        self.session.add(contact_person)
        await self.session.commit()
        await self.session.refresh(contact_person)

        return contact_person

    async def read_many(self, employee_uid: UUID) -> ContactPersonReadMany:
        """Fetch all contact person records."""
        statement = select(ContactPersonDB).where(
            ContactPersonDB.employee_uid == employee_uid
        )
        result = await self.session.exec(statement)  # type: ignore
        all_result = result.all()
        return ContactPersonReadMany(count=len(all_result), result=all_result)

    async def read_by_uid(self, contact_person_uid: UUID) -> Optional[ContactPersonDB]:
        """Read contact person by uid."""
        statement = select(ContactPersonDB).where(
            ContactPersonDB.uid == contact_person_uid
        )
        result = await self.session.exec(statement)  # type: ignore
        contact_person = result.one_or_none()

        return contact_person

    async def update_contact_person(
        self, contact_person_uid: UUID, payload: ContactPersonUpdate
    ) -> Optional[ContactPersonDB]:
        """Update contact person."""
        contact_person = await self.read_by_uid(contact_person_uid)
        if contact_person is None:
            return None

        values = payload.dict(exclude_unset=True)
        for k, v in values.items():
            setattr(contact_person, k, v)

        self.session.add(contact_person)
        await self.session.commit()
        await self.session.refresh(contact_person)

        return contact_person

    async def delete_contact_person(self, contact_person_uid: UUID) -> bool:
        """Delete contact person."""
        contact_person = await self.read_by_uid(contact_person_uid)
        if contact_person is None:
            return False
        await self.session.delete(contact_person)
        await self.session.commit()

        return True
