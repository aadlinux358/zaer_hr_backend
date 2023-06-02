"""Section models module."""
from datetime import datetime
from typing import TYPE_CHECKING, Callable, ClassVar, Optional, Union
from uuid import UUID

from sqlmodel import Field, Relationship, SQLModel, UniqueConstraint

from app.models.shared.base import Base

if TYPE_CHECKING:
    from app.models import UnitDB


class SectionBase(SQLModel):
    """section base class containing shared attrs."""

    name: str = Field(nullable=False, max_length=100, min_length=1, index=True)
    unit_uid: UUID


class SectionCreate(SectionBase):
    """section create model."""

    created_by: UUID
    modified_by: UUID


class SectionUpdateBase(SQLModel):
    """Section update model for optional fields."""

    name: Optional[str]
    unit_uid: Optional[UUID]


class SectionUpdate(SectionUpdateBase):
    """section update model."""

    modified_by: UUID


class SectionDB(Base, SectionBase, table=True):
    """section model for database table."""

    __tablename__: ClassVar[Union[str, Callable[..., str]]] = "section"
    __table_args__ = (UniqueConstraint("unit_uid", "name"),)
    unit_uid: UUID = Field(foreign_key="unit.uid")
    unit: "UnitDB" = Relationship(back_populates="sections")


class SectionRead(SectionCreate):
    """section read one model."""

    uid: UUID
    created_by: UUID
    modified_by: UUID
    date_created: datetime
    date_modified: datetime


class SectionReadMany(SQLModel):
    """section read many model."""

    count: int
    result: list[SectionRead]
