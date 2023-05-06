"""Current job models module."""
from datetime import datetime
from typing import Callable, ClassVar, Optional, Union
from uuid import UUID

from sqlmodel import Field, SQLModel

from app.models.shared.base import Base


class CurrentJobBase(SQLModel):
    """Current job base model."""

    title: str = Field(nullable=False, unique=True, max_length=100, index=True)


class CurrentJobCreate(CurrentJobBase):
    """Current job create model."""

    created_by: UUID
    modified_by: UUID


class CurrentJobUpdate(SQLModel):
    """Current job update model."""

    title: Optional[str]
    modified_by: UUID


class CurrentJobDB(Base, CurrentJobBase, table=True):
    """Current job model for database table."""

    __tablename__: ClassVar[Union[str, Callable[..., str]]] = "current_job"


class CurrentJobRead(CurrentJobCreate):
    """Current job model for reading one."""

    uid: UUID
    created_by: UUID
    modified_by: UUID
    date_created: datetime
    date_modified: datetime


class CurrentJobReadMany(SQLModel):
    """Current job model for reading many."""

    count: int
    result: list[CurrentJobRead]
