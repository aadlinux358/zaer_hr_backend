"""Department models module."""
from datetime import datetime
from typing import TYPE_CHECKING, Callable, ClassVar, Optional, Union
from uuid import UUID

from sqlmodel import Field, Relationship, SQLModel

from app.models.shared.base import Base

if TYPE_CHECKING:
    from app.models import SectionDB


class DepartmentBase(SQLModel):
    """Department base class that contain shared attributes."""

    name: str = Field(nullable=False, unique=True, max_length=100, index=True)


class DepartmentCreate(DepartmentBase):
    """Department model used for creating departments."""

    created_by: UUID
    modified_by: UUID


class DepartmentUpdate(SQLModel):
    """Department model for updating department."""

    name: Optional[str]
    modified_by: UUID


class DepartmentDB(Base, DepartmentBase, table=True):
    """Department model for database table."""

    __tablename__: ClassVar[Union[str, Callable[..., str]]] = "department"
    sections: list["SectionDB"] = Relationship(back_populates="department")


class DepartmentRead(DepartmentBase):
    """Department model for reading department data."""

    uid: UUID
    date_created: datetime
    date_modified: datetime


class DepartmentReadMany(SQLModel):
    """Department model for reading many departments."""

    count: int
    result: list[DepartmentRead]
