"""Employee address information models module."""
from datetime import datetime
from typing import Callable, ClassVar, Optional, Union
from uuid import UUID

from sqlmodel import Field, SQLModel

from app.models.shared.base import Base


class AddressBase(SQLModel):
    """Address base model."""

    employee_uid: UUID = Field(nullable=False, foreign_key="employee.uid", unique=True)
    city: str = Field(nullable=False, max_length=100, min_length=1)
    district: str = Field(nullable=False, max_length=100, min_length=1)
    street: str = Field(default="", nullable=False, max_length=100, min_length=0)
    house_number: int = Field(default=0, nullable=False, ge=0)


class AddressCreate(AddressBase):
    """Address create model."""

    created_by: UUID
    modified_by: UUID


class AddressUpdateBase(SQLModel):
    """Address update base model."""

    city: Optional[str]
    district: Optional[str]
    street: Optional[str]
    house_number: Optional[int]


class AddressUpdate(AddressUpdateBase):
    """Address update model."""

    modified_by: UUID


class AddressDB(Base, AddressBase, table=True):
    """Address model for database table."""

    __tablename__: ClassVar[Union[str, Callable[..., str]]] = "address"


class AddressRead(AddressCreate):
    """Address read one model."""

    uid: UUID
    created_by: UUID
    modified_by: UUID
    date_created: datetime
    date_modified: datetime


class AddressReadMany(SQLModel):
    """Address read many model."""

    count: int
    result: list[AddressRead]
