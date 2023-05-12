"""Employee children information models module."""
from datetime import date, datetime
from typing import Callable, ClassVar, Optional, Union
from uuid import UUID

from sqlmodel import CheckConstraint, Field, SQLModel, UniqueConstraint

from app.models.employee_info.employee import Gender
from app.models.shared.base import Base


class ChildBase(SQLModel):
    """Child base model."""

    parent_uid: UUID = Field(nullable=False, foreign_key="employee.uid")
    first_name: str = Field(nullable=False, index=True, max_length=100, min_length=1)
    gender: Gender = Field(
        nullable=False,
        max_length=1,
        min_length=1,
        sa_column_args=(CheckConstraint("gender in ('f', 'm', 'o')"),),
    )
    birth_date: date = Field(nullable=False)


class ChildCreate(ChildBase):
    """Child create model."""

    created_by: UUID
    modified_by: UUID


class ChildUpdate(SQLModel):
    """Child update model."""

    parent_uid: Optional[UUID]
    first_name: Optional[str]
    gender: Optional[Gender]
    birth_date: Optional[date]
    modified_by: UUID


class ChildDB(Base, ChildBase, table=True):
    """Child model for database table."""

    __tablename__: ClassVar[Union[str, Callable[..., str]]] = "child"
    __table_args__ = (UniqueConstraint("parent_uid", "first_name"),)


class ChildRead(ChildCreate):
    """Child read one model."""

    uid: UUID
    parent_uid: UUID
    created_by: UUID
    modified_by: UUID
    date_created: datetime
    date_modified: datetime


class ChildReadMany(SQLModel):
    """Child read many model."""

    count: int
    result: list[ChildRead]
