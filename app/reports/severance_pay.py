"""Employee severance pay report module."""
from datetime import date
from decimal import Decimal
from enum import Enum

from dateutil.relativedelta import relativedelta
from pydantic import BaseModel
from reportlab.lib.styles import ParagraphStyle  # type: ignore
from reportlab.pdfgen import canvas  # type: ignore
from reportlab.platypus import Paragraph  # type: ignore

from app.models.employee_info.employee import EmployeeSeverancePay

MONTH_DAYS = 26


class DurationType(str, Enum):
    """Duration type enum."""

    YEARS = "years"
    MONTHS = "months"
    DAYS = "days"


class ServicePay(BaseModel):
    """Sevice pay model."""

    duration_type: DurationType
    duration: int
    amount: Decimal


class SeverancePayReport:
    """Severance pay reporting class."""

    def __init__(
        self, employee: EmployeeSeverancePay, include_end_date: bool = False
    ) -> None:
        """Service pay class initializer."""
        self.employee = employee
        self._relative_delta = relativedelta(
            employee.termination_date, employee.current_hire_date
        )
        self.years = self._relative_delta.years
        self.months = self._relative_delta.months
        self.days = (
            self._relative_delta.days + 1
            if include_end_date
            else self._relative_delta.days
        )  # include end date

    def calc_fist_five_years_pay(self) -> ServicePay:
        """Calculate severance pay for the first five or less years of service."""
        if self.years <= 5:
            result = (self.employee.current_salary / MONTH_DAYS) * 2 * 6 * self.years
            amount = round(result, 2)
            return ServicePay(
                duration_type=DurationType.YEARS, duration=self.years, amount=amount
            )
        if self.years > 5:
            result = (self.employee.current_salary / MONTH_DAYS) * 2 * 6 * 5
            amount = round(result, 2)
            return ServicePay(
                duration_type=DurationType.YEARS, duration=5, amount=amount
            )

        return ServicePay(
            duration_type=DurationType.YEARS, duration=0, amount=Decimal()
        )

    def calc_between_five_and_ten_years_pay(self) -> ServicePay:
        """Calculate severance pay for service years between five to ten."""
        years = 0
        if self.years > 5 and self.years <= 10:
            years = self.years - 5
        elif self.years > 10:
            years = 5

        result = (self.employee.current_salary / MONTH_DAYS) * 3 * 6 * years
        amount = round(result, 2)
        return ServicePay(
            duration_type=DurationType.YEARS, duration=years, amount=amount
        )

    def calc_more_than_ten_years_pay(self) -> ServicePay:
        """Calculate severance pay for more than ten years of service."""
        if self.years > 10:
            years = self.years - 10
            result = (self.employee.current_salary / MONTH_DAYS) * 4 * 6 * years
            amount = round(result, 2)
            return ServicePay(
                duration_type=DurationType.YEARS, duration=years, amount=amount
            )
        return ServicePay(
            duration_type=DurationType.YEARS, duration=0, amount=Decimal()
        )

    def calc_remaining_months(self) -> ServicePay:
        """Calculate severance pay for any remaining months."""
        multiplier = 0
        if (self.years <= 5) and (self.months < 1) and (self.days < 1):
            multiplier = 2
        elif (
            (self.years >= 5)
            and ((self.months > 0) or (self.days > 0))
            and (self.years < 10)
        ):
            multiplier = 3
        else:
            multiplier = 4

        if self.months:
            result = (
                (self.employee.current_salary / MONTH_DAYS)
                * multiplier
                * 6
                * Decimal(self.months / 12)
            )
            amount = round(result, 2)
            return ServicePay(
                duration_type=DurationType.MONTHS, duration=self.months, amount=amount
            )
        return ServicePay(
            duration_type=DurationType.MONTHS, duration=0, amount=Decimal()
        )

    def calc_remaining_days(self) -> ServicePay:
        """Calculate severance pay for any remaining days."""
        multiplier = 0
        if self.years <= 5:
            multiplier = 2
        elif (self.years > 5) and (self.years < 10):
            multiplier = 3
        else:
            multiplier = 4
        if self.days:
            result = (
                (self.employee.current_salary / MONTH_DAYS)
                * multiplier
                * 6
                * Decimal(self.days / 313)
            )
            amount = round(result, 2)
            return ServicePay(
                duration_type=DurationType.DAYS, duration=self.days, amount=amount
            )
        return ServicePay(duration_type=DurationType.DAYS, duration=0, amount=Decimal())

    def calc_total_service_pay(self) -> Decimal:
        """Calculate the total serverance service pay."""
        first_five_years = self.calc_fist_five_years_pay()
        between_five_and_ten = self.calc_between_five_and_ten_years_pay()
        more_than_ten = self.calc_more_than_ten_years_pay()
        remaining_months = self.calc_remaining_months()
        remaining_days = self.calc_remaining_days()
        result = (
            first_five_years.amount
            + between_five_and_ten.amount
            + more_than_ten.amount
            + remaining_months.amount
            + remaining_days.amount
        )
        return round(result, 2)

    def _draw_header(self, c: canvas.Canvas):
        """Draw severance pay report header."""
        c.setFontSize(9)
        c.drawString(30, 12, f"Date:- {date.today()}")
        c.setFontSize(10)
        c.drawImage("../app/assets/images/small_logo.jpg", 30, 30, 80, 40)
        c.setFontSize(15)
        c.drawString(140, 40, "ZaEr plc - Asmara")
        c.setFontSize(10)
        c.drawString(310, 40, "Tegadelti Avenue n.13")
        c.drawString(450, 40, "Tel: 00291-1-182383")
        c.setFontSize(8)
        c.drawString(135, 55, "Integrated Textiles & Garment Factory")
        c.setFontSize(10)
        c.drawString(320, 55, "P.O.Box 11933")
        c.drawString(448, 55, "Fax: 00291-1-181493")
        c.drawString(140, 70, "ZAMBAITI GROUP - ITALY")
        c.drawString(317, 70, "Asmara - Eritrea")
        c.drawString(445, 70, "zaer@zaerasmara.com")

    def _draw_employee_info(self, c: canvas.Canvas):
        """Draw employee severance pay report info."""
        first_name = self.employee.first_name
        last_name = self.employee.last_name
        grandfather_name = self.employee.grandfather_name
        fullname = f"{first_name} {last_name} {grandfather_name}"
        c.drawString(45, 120, f"Full Name: {fullname.upper()}")
        c.drawString(300, 120, f"Employee ID: {self.employee.badge_number}")
        c.drawString(45, 135, f"Employement Date: {self.employee.current_hire_date}")
        c.drawString(
            300, 135, f"Termination/Resignation Date: {self.employee.termination_date}"
        )
        c.drawString(45, 150, f"Department: {self.employee.department.upper()}")
        c.drawString(300, 150, f"Salary: Nfa {self.employee.current_salary}")
        c.drawString(
            45,
            180,
            f"Served for {self.years} years {self.months} months {self.days} days",
        )

    def _draw_compensation_info(self, c: canvas.Canvas):
        """Draw employee severance pay report compensation."""
        c.setFontSize(13)
        c.drawString(45, 230, "1. COMPENSATION")
        c.setFontSize(10)
        c.drawString(
            60,
            245,
            "For service of up to two years; a days pay for each month of service",
        )
        c.drawString(60, 260, "Salary / 26 x Days")
        c.drawString(
            60,
            275,
            "For service of more than two years; a month pay for each year of service",
        )
        c.drawString(60, 290, "Monthly Salary x Years Served")

    def _draw_service_pay(self, c: canvas.Canvas):
        """Draw employee severance pay report service pay."""
        c.setFontSize(13)
        c.drawString(45, 340, "2. SERVICE PAY")
        c.setFontSize(10)
        content = """ Two weeks' wages for each of the first five years of employment.
               Three weeks' wages for each year of employment from five to ten years
               of service and four weeks' wage above ten years of service."""
        ParagraphStyle("p_style")
        p = Paragraph(content)
        p.wrapOn(c, 350, 50)
        p.drawOn(c, 60, 335)
        ffy = self.calc_fist_five_years_pay()
        bfat = self.calc_between_five_and_ten_years_pay()
        mtt = self.calc_more_than_ten_years_pay()
        rm = self.calc_remaining_months()
        rd = self.calc_remaining_days()
        c.drawString(
            70,
            400,
            f"Salary / 26 x 2 x 6 x ({ffy.duration} Years): {ffy.amount}",
        )
        c.drawString(
            70,
            415,
            f"Salary / 26 x 3 x 6 x ({bfat.duration} Years): {bfat.amount}",
        )
        c.drawString(
            70,
            430,
            f"Salary / 26 x 4 x 6 x ({mtt.duration} Years): {mtt.amount}",
        )
        c.drawString(
            70,
            445,
            f"Salary / 26 x 2 x 6 x ({rm.duration} Months / 12): {rm.amount}",
        )
        c.drawString(
            70,
            460,
            f"Salary / 26 x 2 x 6 x ({rd.duration} Days / 313): {rd.amount}",
        )
        c.drawString(60, 475, f"SUB-TOTAL: {self.calc_total_service_pay()}")

    def _draw_notice_for_termination(self, c: canvas.Canvas):
        """Draw employee severance pay report notice for termination."""
        c.setFontSize(13)
        c.drawString(45, 525, "3. NOTICE FOR TERMINATION")
        c.setFontSize(10)
        content = """ Seven days, fourteen days, twenty one days' payment for service of
                    less than one year, two years, more than two years consecutively."""
        ParagraphStyle("p_style")
        p = Paragraph(content)
        p.wrapOn(c, 350, 50)
        p.drawOn(c, 60, 530)
        c.drawString(70, 590, "Salary / 26 x Days(7, 14, 21, 30)")

    def _draw_annual_leave(self, c: canvas.Canvas):
        """Draw employee annual leave severance report."""
        c.setFontSize(13)
        c.drawString(45, 630, "4. ANNUAL LEAVE")
        c.setFontSize(10)
        c.drawString(60, 645, "Annual leave due days' x salary per day")
        c.drawString(60, 660, "Salary / 26 x Days")
        c.drawString(60, 675, "TOTAL GROSS PAYABLE (1 + 2 + 3 + 4)")

    def create_report(self) -> str:
        """Create severance report pdf file."""
        filename = f"employee_{self.employee.badge_number}_severance_pay.pdf"
        c = canvas.Canvas(filename, bottomup=0)
        self._draw_header(c)
        self._draw_employee_info(c)
        self._draw_compensation_info(c)
        self._draw_service_pay(c)
        self._draw_notice_for_termination(c)
        self._draw_annual_leave(c)
        c.showPage()
        c.save()
        return filename
