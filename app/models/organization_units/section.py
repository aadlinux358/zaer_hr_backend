"""Section models module."""
from datetime import datetime
from typing import TYPE_CHECKING, Callable, ClassVar, Optional, Union
from uuid import UUID

from sqlmodel import Field, Relationship, SQLModel

from app.models.shared.base import Base

if TYPE_CHECKING:
    from app.models import DepartmentDB, UnitDB


class SectionBase(SQLModel):
    """section base class containing shared attrs."""

    name: str = Field(nullable=False, unique=True, max_length=100, index=True)
    department_uid: UUID


class SectionCreate(SectionBase):
    """section create model."""

    created_by: UUID
    modified_by: UUID


class SectionUpdateBase(SQLModel):
    """Section update model for optional fields."""

    name: Optional[str]
    department_uid: Optional[UUID]


class SectionUpdate(SectionUpdateBase):
    """section update model."""

    modified_by: UUID


class SectionDB(Base, SectionBase, table=True):
    """section model for database table."""

    __tablename__: ClassVar[Union[str, Callable[..., str]]] = "section"
    department_uid: UUID = Field(foreign_key="department.uid")
    department: "DepartmentDB" = Relationship(back_populates="sections")
    units: list["UnitDB"] = Relationship(back_populates="section")


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
