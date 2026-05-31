"""
Address entity — ORM mapped class for table `employees`.
"""

from typing import TYPE_CHECKING
from sqlalchemy import DateTime, Integer, String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from models import Entity
if TYPE_CHECKING:
    from models.employee import Employee
else:
    Employee = "Employee"

class Address(Entity):
    __abstract__= False
    __tablename__= "address"

    line1: Mapped[str] = mapped_column(String(100), nullable=False)
    city: Mapped[str] = mapped_column(String(100), nullable=False)
    postal_code: Mapped[str] = mapped_column(String(100), nullable=False)
    country: Mapped[str] = mapped_column(String(100), nullable=False)
    employee_id: Mapped[int] = mapped_column(
        "Integer",
        ForeignKey("employees.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    employee: Mapped["Employee"] = relationship(Employee, back_populates="address")
