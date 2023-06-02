"""Unit models module."""
from datetime import datetime
from typing import TYPE_CHECKING, Callable, ClassVar, Optional, Union
from uuid import UUID

from sqlmodel import Field, Relationship, SQLModel, UniqueConstraint

from app.models.shared.base import Base

if TYPE_CHECKING:
    from app.models import DepartmentDB, SectionDB


class UnitBase(SQLModel):
    """unit base class containing shared attrs."""

    name: str = Field(nullable=False, max_length=100, index=True)
    department_uid: UUID


class UnitCreate(UnitBase):
    """unit create model."""

    created_by: UUID
    modified_by: UUID


class UnitUpdateBase(SQLModel):
    """Unit update optional fields model."""

    name: Optional[str]
    department_uid: Optional[UUID]


class UnitUpdate(UnitUpdateBase):
    """unit update model."""

    modified_by: UUID


class UnitDB(Base, UnitBase, table=True):
    """unit model for database table."""

    __tablename__: ClassVar[Union[str, Callable[..., str]]] = "unit"
    __table_args__ = (UniqueConstraint("department_uid", "name"),)
    department_uid: UUID = Field(foreign_key="department.uid")
    department: "DepartmentDB" = Relationship(back_populates="units")
    sections: list["SectionDB"] = Relationship(back_populates="unit")


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
