"""Employee hire and termination models module."""
from datetime import date, datetime
from typing import Callable, ClassVar, Optional, Union
from uuid import UUID

from sqlmodel import Field, SQLModel, UniqueConstraint

from app.models.shared.base import Base


class TerminationBase(SQLModel):
    """Termination base model."""

    employee_uid: UUID
    hire_date: date = Field(nullable=False)
    termination_date: date = Field(nullable=False)


class TerminationCreate(TerminationBase):
    """Termination create model."""

    created_by: UUID
    modified_by: UUID


class TerminationUpdate(SQLModel):
    """Termination update model."""

    employee_uid: Optional[UUID]
    hire_date: Optional[UUID]
    termination_date: Optional[UUID]
    modified_by: UUID


class TerminationDB(Base, TerminationBase, table=True):
    """Termination model for database table."""

    __tablename__: ClassVar[Union[str, Callable[..., str]]] = "termination"
    __table_args__ = (
        UniqueConstraint("employee_uid", "hire_date"),
        UniqueConstraint("employee_uid", "termination_date"),
    )
    employee_uid: UUID = Field(nullable=False, foreign_key="employee.uid")


class TerminationRead(TerminationCreate):
    """Termination read one model."""

    uid: UUID
    employee_uid: UUID
    date_created: datetime
    date_modified: datetime


class TerminationReadMany(SQLModel):
    """Termination read many model."""

    count: int
    result: list[TerminationRead]
