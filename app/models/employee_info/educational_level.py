"""Employee educational level models module."""
from datetime import datetime
from typing import Callable, ClassVar, Optional, Union
from uuid import UUID

from sqlmodel import Field, SQLModel

from app.models.shared.base import Base


class EducationalLevelBase(SQLModel):
    """Educational level base model."""

    level: str = Field(nullable=False, unique=True, max_length=100, min_length=1)
    level_order: int = Field(nullable=False, unique=True, ge=0)


class EducationalLevelCreate(EducationalLevelBase):
    """Educational level create model."""

    created_by: UUID
    modified_by: UUID


class EducationalLevelUpdateBase(SQLModel):
    """Educational level update base model."""

    level: Optional[str]
    level_order: Optional[int]


class EducationalLevelUpdate(EducationalLevelUpdateBase):
    """Educational level update model."""

    modified_by: UUID


class EducationalLevelDB(Base, EducationalLevelBase, table=True):
    """Educational level model for database table."""

    __tablename__: ClassVar[Union[str, Callable[..., str]]] = "educational_level"


class EducationalLevelRead(EducationalLevelCreate):
    """Educational level read one model."""

    uid: UUID
    created_by: UUID
    modified_by: UUID
    date_created: datetime
    date_modified: datetime


class EducationalLevelReadMany(SQLModel):
    """Educational level read many model."""

    count: int
    result: list[EducationalLevelRead]
