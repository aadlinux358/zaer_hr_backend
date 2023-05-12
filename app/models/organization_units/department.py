"""Department models module."""
from datetime import datetime
from typing import TYPE_CHECKING, Callable, ClassVar, Optional, Union
from uuid import UUID

from sqlmodel import Field, Relationship, SQLModel, UniqueConstraint

from app.models.shared.base import Base

if TYPE_CHECKING:
    from app.models import DivisionDB, SectionDB


class DepartmentBase(SQLModel):
    """Department base class that contains shared attributes."""

    name: str = Field(nullable=False, max_length=100, min_length=1, index=True)
    division_uid: UUID


class DepartmentCreate(DepartmentBase):
    """Department model used for creating department."""

    created_by: UUID
    modified_by: UUID


class DepartmentUpdateBase(SQLModel):
    """Department model for updating optional department fields."""

    name: Optional[str]
    division_uid: Optional[UUID]


class DepartmentUpdate(DepartmentUpdateBase):
    """Department model for updating department."""

    modified_by: UUID


class DepartmentDB(Base, DepartmentBase, table=True):
    """Department model for database table."""

    __tablename__: ClassVar[Union[str, Callable[..., str]]] = "department"
    __table_args__ = (UniqueConstraint("division_uid", "name"),)
    division_uid: UUID = Field(foreign_key="division.uid")
    division: "DivisionDB" = Relationship(back_populates="departments")
    sections: list["SectionDB"] = Relationship(back_populates="department")


class DepartmentRead(DepartmentCreate):
    """Department model for reading department data."""

    uid: UUID
    created_by: UUID
    modified_by: UUID
    date_created: datetime
    date_modified: datetime


class DepartmentReadPrintFormat(SQLModel):
    """Department model for printing."""

    uid: UUID
    name: str
    division: str  # instead of uuid
    created_by: UUID
    modified_by: UUID
    date_created: datetime
    date_modified: datetime


class DepartmentReadMany(SQLModel):
    """Department model for reading many departments."""

    count: int
    result: list[DepartmentRead]


class DepartmentReadManyPrintFormat(SQLModel):
    """Department read many departments for printing."""

    count: int
    result: list[DepartmentReadPrintFormat]
