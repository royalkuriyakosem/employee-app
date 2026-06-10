"""
Employee entity — ORM mapped class for table `employees`.
"""

from typing import TYPE_CHECKING
import enum
from sqlalchemy import Integer, String, Enum, Index, text
from sqlalchemy.orm import Mapped, mapped_column, relationship
from models import Entity
from models.address import Address

if TYPE_CHECKING:
    from models.employee import Employee
else:
    Employee = "Employee"


class EmployeeRole(str, enum.Enum):
    UI = "UI"
    UX = "UX"
    DEVELOPER = "Developer"
    HR = "HR"


class EmployeeStatus(str, enum.Enum):
    ACTIVE = "Active"
    INACTIVE = "Inactive"
    PROBATION = "Probation"


class Employee(Entity):
    __abstract__ = False
    __tablename__ = "employees"
    __table_args__ = (
        Index(
            "uq_employee_email_active",
            "email",
            unique=True,
            postgresql_where=text("deleted_at IS NULL"),
        ),
    )

    name: Mapped[str] = mapped_column(String(100), nullable=False)
    email: Mapped[str] = mapped_column(String(255), nullable=False)
    age: Mapped[int] = mapped_column(Integer, nullable=True)
    password_hash: Mapped[str] = mapped_column(String(255), nullable=False)
    address: Mapped[list["Address"]] = relationship(  # type:ignore
        "Address",
        back_populates="employee",
    )
    role: Mapped[EmployeeRole] = mapped_column(
        Enum(
            EmployeeRole,
            name="employeerole",
            values_callable=lambda enum_cls: [e.value for e in enum_cls],
        )
    )
    status: Mapped[EmployeeStatus] = mapped_column(
        Enum(
            EmployeeStatus,
            name="employeestatus",
            values_callable=lambda enum_cls: [e.value for e in enum_cls],
        )
    )
    experience: Mapped[int] = mapped_column(Integer, nullable=True)
