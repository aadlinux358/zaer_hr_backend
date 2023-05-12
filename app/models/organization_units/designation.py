"""Designation models module."""
from datetime import datetime
from typing import Callable, ClassVar, Optional, Union
from uuid import UUID

from sqlmodel import Field, SQLModel

from app.models.shared.base import Base


class DesignationBase(SQLModel):
    """Designation base model."""

    title: str = Field(
        nullable=False, unique=True, max_length=100, min_length=1, index=True
    )


class DesignationCreate(DesignationBase):
    """Designation create model."""

    created_by: UUID
    modified_by: UUID


class DesignationUpdate(SQLModel):
    """Designation update model."""

    title: Optional[str]
    modified_by: UUID


class DesignationDB(Base, DesignationBase, table=True):
    """Designation model for database table."""

    __tablename__: ClassVar[Union[str, Callable[..., str]]] = "designation"


class DesignationRead(DesignationCreate):
    """Designation model for reading one."""

    uid: UUID
    created_by: UUID
    modified_by: UUID
    date_created: datetime
    date_modified: datetime


class DesignationReadMany(SQLModel):
    """Designation model for reading many."""

    count: int
    result: list[DesignationRead]
