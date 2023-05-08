"""Unit models module."""
from datetime import datetime
from typing import TYPE_CHECKING, Callable, ClassVar, Optional, Union
from uuid import UUID

from sqlmodel import Field, Relationship, SQLModel

from app.models.shared.base import Base

if TYPE_CHECKING:
    from app.models import SectionDB


class UnitBase(SQLModel):
    """unit base class containing shared attrs."""

    name: str = Field(nullable=False, unique=True, max_length=100, index=True)
    section_uid: UUID


class UnitCreate(UnitBase):
    """unit create model."""

    created_by: UUID
    modified_by: UUID


class UnitUpdateBase(SQLModel):
    """Unit update optional fields model."""

    name: Optional[str]
    section_uid: Optional[UUID]


class UnitUpdate(UnitUpdateBase):
    """unit update model."""

    modified_by: UUID


class UnitDB(Base, UnitBase, table=True):
    """unit model for database table."""

    __tablename__: ClassVar[Union[str, Callable[..., str]]] = "unit"
    section_uid: UUID = Field(foreign_key="section.uid")
    section: "SectionDB" = Relationship(back_populates="units")


class UnitRead(UnitCreate):
    """unit read one model."""

    uid: UUID
    created_by: UUID
    modified_by: UUID
    date_created: datetime
    date_modified: datetime


class UnitReadMany(SQLModel):
    """unit read many model."""

    count: int
    result: list[UnitRead]
