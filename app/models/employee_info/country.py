"""Country models module."""
from datetime import datetime
from typing import Callable, ClassVar, Optional, Union
from uuid import UUID

from sqlmodel import Field, SQLModel

from app.models.shared.base import Base


class CountryBase(SQLModel):
    """Countries base model."""

    name: str = Field(nullable=False, unique=True)


class CountryCreate(CountryBase):
    """Country create model."""

    created_by: UUID
    modified_by: UUID


class CountryUpdateBase(SQLModel):
    """Country update base model."""

    name: Optional[str]


class CountryUpdate(CountryUpdateBase):
    """Country update model."""

    modified_by: UUID


class CountryDB(Base, CountryBase, table=True):
    """Country model for database table."""

    __tablename__: ClassVar[Union[str, Callable[..., str]]] = "country"


class CountryRead(CountryCreate):
    """Country read one model."""

    uid: UUID
    created_by: UUID
    modified_by: UUID
    date_created: datetime
    date_modified: datetime


class CountryReadMany(SQLModel):
    """Country read many model."""

    count: int
    result: list[CountryRead]
