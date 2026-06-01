"""
Employee entity — ORM mapped class for table `employees`.
"""

from typing import TYPE_CHECKING
import enum
from sqlalchemy import Integer, String, Enum
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


class Employee(Entity):
    __abstract__ = False
    __tablename__ = "employees"

    name: Mapped[str] = mapped_column(String(100), nullable=False)
    email: Mapped[str] = mapped_column(String(255), nullable=False, unique=True)
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
    # def to_api_dict(self) -> dict[str, Any]:
    #     """JSON-friendly representation (ISO 8601 for timestamps)."""
    #     return {
    #         "id": self.id,
    #         "name": self.name,
    #         "email": self.email,
    #         "age": self.age,
    #         "created_at": datetime_to_iso(self.created_at),
    #         "updated_at": datetime_to_iso(self.updated_at),
    #         "deleted_at": datetime_to_iso(self.deleted_at),
    #     }
