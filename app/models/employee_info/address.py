"""Employee address information models module."""
from datetime import datetime
from typing import Callable, ClassVar, Optional, Union
from uuid import UUID

from sqlmodel import Field, SQLModel

from app.models.shared.base import Base


class AddressBase(SQLModel):
    """Address base model."""

    employee_uid: UUID = Field(nullable=False, foreign_key="employee.uid", unique=True)
    city: str = Field(nullable=False)
    district: str = Field(nullable=False)


class AddressCreate(AddressBase):
    """Address create model."""

    created_by: UUID
    modified_by: UUID


class AddressUpdate(SQLModel):
    """Address update model."""

    city: Optional[str]
    district: Optional[str]
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
