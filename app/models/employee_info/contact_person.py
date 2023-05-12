"""Employee contact person information models module."""
from datetime import datetime
from typing import Callable, ClassVar, Optional, Union
from uuid import UUID

from sqlmodel import Field, SQLModel

from app.models.shared.base import Base


class ContactPersonBase(SQLModel):
    """Contact person base model."""

    employee_uid: UUID = Field(nullable=False, unique=True, foreign_key="employee.uid")
    first_name: str = Field(nullable=False, max_length=100, min_length=1)
    last_name: str = Field(nullable=False, max_length=100, min_length=1)
    phone_number: str = Field(nullable=False, unique=True, max_length=100, min_length=1)
    relationship_to_employee: str = Field(nullable=False, max_length=100, min_length=1)


class ContactPersonCreate(ContactPersonBase):
    """Contact person create model."""

    created_by: UUID
    modified_by: UUID


class ContactPersonUpdate(SQLModel):
    """Contact person update model."""

    first_name: Optional[str]
    last_name: Optional[str]
    phone_number: Optional[str]
    relationship_to_employee: Optional[str]
    modified_by: UUID


class ContactPersonDB(Base, ContactPersonBase, table=True):
    """Contact person model for database table."""

    __tablename__: ClassVar[Union[str, Callable[..., str]]] = "contact_person"


class ContactPersonRead(ContactPersonCreate):
    """Contact person read one model."""

    uid: UUID
    created_by: UUID
    modified_by: UUID
    date_created: datetime
    date_modified: datetime


class ContactPersonReadMany(SQLModel):
    """Contact person read many model."""

    count: int
    result: list[ContactPersonRead]
