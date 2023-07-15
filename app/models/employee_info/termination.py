"""Employee hire and termination models module."""
from datetime import date, datetime
from typing import Callable, ClassVar, Optional, Union
from uuid import UUID

from sqlmodel import Field, SQLModel, UniqueConstraint

from app.models.shared.base import Base


class TerminationBase(SQLModel):
    """Termination base model."""

    employee_uid: UUID
    termination_date: date = Field(nullable=False)


class TerminationCreate(TerminationBase):
    """Termination create model."""

    hire_date: date = Field(nullable=False)
    created_by: UUID
    modified_by: UUID


class TerminationUpdateBase(SQLModel):
    """Termination update model."""

    employee_uid: Optional[UUID]
    hire_date: Optional[date]
    termination_date: Optional[date]


class TerminationUpdate(TerminationUpdateBase):
    """Termination update model."""

    modified_by: UUID


class TerminationDB(Base, TerminationBase, table=True):
    """Termination model for database table."""

    __tablename__: ClassVar[Union[str, Callable[..., str]]] = "termination"
    __table_args__ = (
        UniqueConstraint("employee_uid", "hire_date"),
        UniqueConstraint("employee_uid", "termination_date"),
    )
    employee_uid: UUID = Field(nullable=False, foreign_key="employee.uid")
    hire_date: date = Field(nullable=False)


class TerminationRead(TerminationCreate):
    """Termination read one model."""

    uid: UUID
    hire_date: date
    employee_uid: UUID
    date_created: datetime
    date_modified: datetime


class TerminationReadMany(SQLModel):
    """Termination read many model."""

    count: int
    result: list[TerminationRead]
