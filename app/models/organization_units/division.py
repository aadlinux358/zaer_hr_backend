"""Division models module."""
from datetime import datetime
from typing import TYPE_CHECKING, Callable, ClassVar, Optional, Union
from uuid import UUID

from sqlmodel import Field, Relationship, SQLModel

from app.models.shared.base import Base

if TYPE_CHECKING:
    from app.models import DepartmentDB


class DivisionBase(SQLModel):
    """Division base class that contain shared attributes."""

    name: str = Field(
        nullable=False, unique=True, max_length=100, min_length=1, index=True
    )


class DivisionCreate(DivisionBase):
    """Division model used for creating divisions."""

    created_by: UUID
    modified_by: UUID


class DivisionUpdate(SQLModel):
    """Division model for updating division."""

    name: Optional[str]
    modified_by: UUID


class DivisionDB(Base, DivisionBase, table=True):
    """Division model for database table."""

    __tablename__: ClassVar[Union[str, Callable[..., str]]] = "division"
    departments: list["DepartmentDB"] = Relationship(back_populates="division")


class DivisionRead(DivisionBase):
    """Division model for reading division data."""

    uid: UUID
    created_by: UUID
    modified_by: UUID
    date_created: datetime
    date_modified: datetime


class DivisionReadMany(SQLModel):
    """Division model for reading many divisions."""

    count: int
    result: list[DivisionRead]
