"""
Associations entity - An Entity to map employee and Deparment
"""

from models import Entity
from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from models.employee import Employee
from models.department import Department


class Associations(Entity):
    __abstract__ = False
    __tablename__ = "associations"

    employee_id: Mapped[int] = mapped_column(
        "employee_id", ForeignKey("employees.id"), nullable=False
    )
    department_id: Mapped[int] = mapped_column(
        "department_id", ForeignKey("department.id"), nullable=False
    )

    employee: Mapped["Employee"] = relationship(Employee)
    department: Mapped["Department"] = relationship(Department)
