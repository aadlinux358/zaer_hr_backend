"""Nationalities models module."""
from datetime import datetime
from typing import Callable, ClassVar, Optional, Union
from uuid import UUID

from sqlmodel import Field, SQLModel

from app.models.shared.base import Base


class NationalityBase(SQLModel):
    """Nationalities base model."""

    name: str = Field(nullable=False, unique=True)


class NationalityCreate(NationalityBase):
    """Nationality create model."""

    created_by: UUID
    modified_by: UUID


class NationalityUpdate(SQLModel):
    """Nationality update model."""

    name: Optional[str]
    modified_by: UUID


class NationalityDB(Base, NationalityBase, table=True):
    """Nationality model for database table."""

    __tablename__: ClassVar[Union[str, Callable[..., str]]] = "nationality"


class NationalityRead(NationalityCreate):
    """Nationality read one model."""

    uid: UUID
    created_by: UUID
    modified_by: UUID
    date_created: datetime
    date_modified: datetime


class NationalityReadMany(SQLModel):
    """Nationality read many model."""

    count: int
    result: list[NationalityRead]
