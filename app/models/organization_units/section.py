"""Section models module."""
from datetime import datetime
from typing import TYPE_CHECKING, Callable, ClassVar, Optional, Union
from uuid import UUID

from sqlmodel import Field, Relationship, SQLModel

from app.models.shared.base import Base

if TYPE_CHECKING:
    from app.models import DepartmentDB, SubSectionDB


class SectionBase(SQLModel):
    """Section base class that contains shared attributes."""

    name: str = Field(nullable=False, unique=True, max_length=100, index=True)


class SectionCreate(SectionBase):
    """Section model used for creating sections."""

    department_uid: UUID
    created_by: UUID
    modified_by: UUID


class SectionUpdate(SQLModel):
    """Section model for updating section."""

    name: Optional[str]
    department_uid: Optional[UUID]
    modified_by: UUID


class SectionDB(Base, SectionBase, table=True):
    """Section model for database table."""

    __tablename__: ClassVar[Union[str, Callable[..., str]]] = "section"
    department_uid: UUID = Field(foreign_key="department.uid")
    department: "DepartmentDB" = Relationship(back_populates="sections")
    sub_sections: list["SubSectionDB"] = Relationship(back_populates="section")


class SectionRead(SectionCreate):
    """Section model for reading section data."""

    uid: UUID
    created_by: UUID
    modified_by: UUID
    date_created: datetime
    date_modified: datetime


class SectionReadMany(SQLModel):
    """Section model for reading many sections."""

    count: int
    result: list[SectionRead]
