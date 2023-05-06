"""Sub Section models module."""
from datetime import datetime
from typing import TYPE_CHECKING, Callable, ClassVar, Optional, Union
from uuid import UUID

from sqlmodel import Field, Relationship, SQLModel

from app.models.shared.base import Base

if TYPE_CHECKING:
    from app.models import SectionDB


class SubSectionBase(SQLModel):
    """Sub section base class containing shared attrs."""

    name: str = Field(nullable=False, unique=True, max_length=100, index=True)


class SubSectionCreate(SubSectionBase):
    """Sub section create model."""

    section_uid: UUID
    created_by: UUID
    modified_by: UUID


class SubSectionUpdate(SQLModel):
    """Sub section update model."""

    name: Optional[str]
    section_uid: Optional[UUID]
    modified_by: UUID


class SubSectionDB(Base, SubSectionBase, table=True):
    """Subsection model for database table."""

    __tablename__: ClassVar[Union[str, Callable[..., str]]] = "sub_section"
    section_uid: UUID = Field(foreign_key="section.uid")
    section: "SectionDB" = Relationship(back_populates="sub_sections")


class SubSectionRead(SubSectionCreate):
    """Sub section read one model."""

    uid: UUID
    created_by: UUID
    modified_by: UUID
    date_created: datetime
    date_modified: datetime


class SubSectionReadMany(SQLModel):
    """Sub section read many model."""

    count: int
    result: list[SubSectionRead]
