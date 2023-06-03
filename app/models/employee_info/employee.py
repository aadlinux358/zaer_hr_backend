"""Employee information models module."""
from datetime import date, datetime
from decimal import Decimal
from enum import Enum
from typing import Callable, ClassVar, Optional, Union
from uuid import UUID

from pydantic import validator
from sqlmodel import CheckConstraint, Field, Identity, SQLModel

from app.models.shared.base import Base


class Gender(str, Enum):
    """Gender enum class."""

    MALE = ("m",)
    FEMALE = ("f",)
    OTHER = "o"


class MaritalStatus(str, Enum):
    """Marital status enum class."""

    SINGLE = ("single",)
    MARRIED = ("married",)
    DIVORCED = ("divorced",)
    WIDOWED = "widowed"


class ContractType(str, Enum):
    """Contract type enum class."""

    FULL_TIME = ("full time",)
    PART_TIME = "part time"


class NationalService(str, Enum):
    """National service enum class."""

    RELEASED = ("released",)
    EXEMPTED = ("exempted",)
    SERVING = ("serving",)
    NOTCOMPLETED = "not completed"


class EmployeeBase(SQLModel):
    """Employee base model with shared attributes."""

    first_name: str = Field(max_length=200, min_length=1, nullable=False)
    last_name: str = Field(max_length=200, min_length=1, nullable=False)
    grandfather_name: str = Field(max_length=200, min_length=1, nullable=False)
    gender: Gender = Field(
        nullable=False,
        max_length=1,
        min_length=1,
        sa_column_args=(CheckConstraint("gender in ('f', 'm', 'o')"),),
    )
    birth_date: date = Field(nullable=False)
    current_salary: Decimal = Field(nullable=False, ge=0.00, default_factory=Decimal)
    current_hire_date: date = Field(nullable=False)
    designation_uid: UUID = Field(nullable=False, foreign_key="designation.uid")
    section_uid: UUID
    is_active: bool = Field(default=True, nullable=False)
    is_terminated: bool = Field(default=False, nullable=False)
    nationality_uid: UUID = Field(nullable=False, foreign_key="nationality.uid")
    country_uid: UUID = Field(nullable=False, foreign_key="country.uid")
    origin_of_birth: str = Field(
        nullable=False,
        max_length=100,
        min_length=1,
    )
    birth_place: str = Field(
        nullable=False,
        max_length=100,
        min_length=1,
    )
    mother_first_name: str = Field(
        nullable=False,
        max_length=100,
        min_length=1,
    )
    mother_last_name: str = Field(
        nullable=False,
        max_length=100,
        min_length=1,
    )
    mother_grandfather_name: str = Field(
        nullable=False,
        max_length=100,
        min_length=1,
    )
    marital_status: MaritalStatus = Field(
        default=MaritalStatus.SINGLE.value,
        nullable=False,
        sa_column_args=(
            CheckConstraint(
                "marital_status in ('single', 'married', 'divorced', 'widowed')"
            ),
        ),
    )
    educational_level_uid: UUID = Field(
        nullable=False, foreign_key="educational_level.uid"
    )
    phone_number: str = Field(nullable=True, unique=True, max_length=100, min_length=1)
    national_id: str = Field(nullable=True, unique=True, max_length=100, min_length=1)
    contract_type: ContractType = Field(
        default=ContractType.FULL_TIME.value,
        nullable=False,
        sa_column_args=(
            CheckConstraint("contract_type in ('full time', 'part time')"),
        ),
    )
    national_service: NationalService = Field(
        default=NationalService.RELEASED.value,
        nullable=False,
        sa_column_args=(
            CheckConstraint("national_service in ('released', 'exempted', 'serving')"),
        ),
    )
    apprenticeship_from_date: date = Field(nullable=False)
    apprenticeship_to_date: date = Field(nullable=False)

    @validator("phone_number")
    def phone_number_must_contain_only_digits(cls, v):
        """Validate phone number string."""
        if not v.isdigit():
            raise ValueError("phone must contain only digits")
        return v


class EmployeeCreate(EmployeeBase):
    """Employee create model."""

    created_by: UUID
    modified_by: UUID


class EmployeeUpdateBase(SQLModel):
    """Employee update base model."""

    first_name: Optional[str]
    last_name: Optional[str]
    grandfather_name: Optional[str]
    gender: Optional[Gender]
    birth_date: Optional[date]
    current_salary: Optional[Decimal]
    current_hire_date: Optional[date]
    designation_uid: Optional[UUID]
    unit_uid: Optional[UUID]
    nationality_uid: Optional[UUID]
    birth_place: Optional[str]
    origin_of_birth: Optional[str]
    mother_first_name: Optional[str]
    mother_last_name: Optional[str]
    mother_grandfather_name: Optional[str]
    marital_status: Optional[MaritalStatus]
    educational_level_uid: Optional[UUID]
    phone_number: Optional[str]
    national_id: Optional[str]
    contract_type: Optional[ContractType]
    national_service: Optional[NationalService]
    apprenticeship_from_date: Optional[date]
    apprenticeship_to_date: Optional[date]

    @validator("phone_number")
    def phone_number_must_contain_only_digits(cls, v):
        """Validate phone number string."""
        if not v.isdigit():
            raise ValueError("phone must contain only digits")
        return v


class EmployeeUpdate(EmployeeUpdateBase):
    """Employee update model."""

    is_active: Optional[bool]
    is_terminated: Optional[bool]
    modified_by: UUID


class EmployeeDB(Base, EmployeeBase, table=True):
    """Employee model for database table."""

    __tablename__: ClassVar[Union[str, Callable[..., str]]] = "employee"
    badge_number: int = Field(
        nullable=False, unique=True, index=True, sa_column_args=(Identity(always=True),)
    )
    section_uid: UUID = Field(nullable=False, foreign_key="section.uid")


class EmployeeRead(EmployeeCreate):
    """Employee read one model."""

    uid: UUID
    badge_number: int
    created_by: UUID
    modified_by: UUID
    date_created: datetime
    date_modified: datetime


class EmployeeReadMany(SQLModel):
    """Employee read many model."""

    count: int
    result: list[EmployeeRead]
