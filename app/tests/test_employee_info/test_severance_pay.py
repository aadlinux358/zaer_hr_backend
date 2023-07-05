"""Employee severance pay tests module."""
from datetime import date
from decimal import Decimal
from typing import Final

import pytest

from app.models.employee_info.employee import EmployeeSeverancePay
from app.reports import severance_pay

EMPLOYEE: Final = EmployeeSeverancePay(
    badge_number=3580,
    first_name="yonas",
    last_name="werede",
    grandfather_name="tesfaslasie",
    department="workshop",
    current_hire_date=date(2018, 3, 7),
    termination_date=date(2022, 9, 7),
    current_salary=Decimal("2609"),
)


@pytest.mark.asyncio
async def test_calc_first_five_years_pay_for_less_than_five_years():
    sr = severance_pay.SeverancePayReport(employee=EMPLOYEE)
    result = sr.calc_fist_five_years_pay()

    assert result.duration_type == severance_pay.DurationType.YEARS
    assert result.duration == 4
    assert result.amount == Decimal("4816.62")


@pytest.mark.asyncio
async def test_calc_first_five_years_pay_for_more_than_five_years():
    employee = EMPLOYEE
    employee.current_hire_date = date(2015, 3, 7)
    employee.termination_date = date(2023, 3, 7)

    sr = severance_pay.SeverancePayReport(employee=employee)
    result = sr.calc_fist_five_years_pay()

    assert result.duration_type == severance_pay.DurationType.YEARS
    assert result.duration == 5
    assert result.amount == Decimal("6020.77")


@pytest.mark.asyncio
async def test_calc_between_five_and_ten_years_pay():
    employee = EMPLOYEE
    employee.current_hire_date = date(2015, 3, 7)
    employee.termination_date = date(2023, 3, 7)

    sr = severance_pay.SeverancePayReport(employee=employee)
    result = sr.calc_between_five_and_ten_years_pay()

    assert result.duration_type == severance_pay.DurationType.YEARS
    assert result.duration == 3
    assert result.amount == Decimal("5418.69")


@pytest.mark.asyncio
async def test_calc_between_five_and_ten_years_pay_for_less_than_five_years():
    employee = EMPLOYEE
    employee.current_hire_date = date(2019, 3, 7)
    employee.termination_date = date(2023, 3, 7)

    sr = severance_pay.SeverancePayReport(employee=employee)
    result = sr.calc_between_five_and_ten_years_pay()

    assert result.duration_type == severance_pay.DurationType.YEARS
    assert result.duration == 0
    assert result.amount == Decimal()


@pytest.mark.asyncio
async def test_calc_more_than_ten_years_pay():
    employee = EMPLOYEE
    employee.current_hire_date = date(2005, 3, 7)
    employee.termination_date = date(2023, 3, 7)

    sr = severance_pay.SeverancePayReport(employee=employee)
    result = sr.calc_more_than_ten_years_pay()

    assert result.duration_type == severance_pay.DurationType.YEARS
    assert result.duration == 8
    assert result.amount == Decimal("19266.46")


@pytest.mark.asyncio
async def test_calc_more_than_ten_years_pay_for_less_than_10_years():
    employee = EMPLOYEE
    employee.current_hire_date = date(2019, 3, 7)
    employee.termination_date = date(2023, 3, 7)

    sr = severance_pay.SeverancePayReport(employee=employee)
    result = sr.calc_more_than_ten_years_pay()

    assert result.duration_type == severance_pay.DurationType.YEARS
    assert result.duration == 0
    assert result.amount == Decimal()


@pytest.mark.asyncio
async def test_calc_remaining_months():
    employee = EMPLOYEE
    employee.current_hire_date = date(2018, 3, 7)
    employee.termination_date = date(2023, 9, 7)

    sr = severance_pay.SeverancePayReport(employee=employee)
    result = sr.calc_remaining_months()

    assert result.duration_type == severance_pay.DurationType.MONTHS
    assert result.duration == 6
    assert result.amount == Decimal("903.12")


@pytest.mark.asyncio
async def test_calc_remaining_days_excluding_end_date():
    employee = EMPLOYEE
    employee.current_hire_date = date(2018, 3, 7)
    employee.termination_date = date(2023, 9, 25)

    sr = severance_pay.SeverancePayReport(employee=employee, include_end_date=False)
    result = sr.calc_remaining_days()

    assert result.duration_type == severance_pay.DurationType.DAYS
    assert result.duration == 18
    assert result.amount == Decimal("69.25")


@pytest.mark.asyncio
async def test_calc_remaining_days_including_end_date():
    employee = EMPLOYEE
    employee.current_hire_date = date(2018, 3, 7)
    employee.termination_date = date(2023, 9, 25)

    sr = severance_pay.SeverancePayReport(employee=employee, include_end_date=True)
    result = sr.calc_remaining_days()

    assert result.duration_type == severance_pay.DurationType.DAYS
    assert result.duration == 19
    assert result.amount == Decimal("73.10")


@pytest.mark.asyncio
async def test_calc_total_service_pay():
    employee = EMPLOYEE
    employee.current_salary = Decimal("2131")
    employee.current_hire_date = date(2007, 11, 1)
    employee.termination_date = date(2023, 5, 13)

    sr = severance_pay.SeverancePayReport(employee=employee)
    result = sr.calc_total_service_pay()

    assert result == Decimal("23188.57")
