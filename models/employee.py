"""
Employee entity — ORM mapped class for table `employees`.
"""

from datetime import datetime
from typing import Any, Optional, TYPE_CHECKING

from sqlalchemy import DateTime, Integer, String, func
from sqlalchemy.orm import Mapped, mapped_column, relationship
from models import Entity
from models.entity import datetime_to_iso
from models.address import Address

if TYPE_CHECKING:
    from models.employee import Employee
else:
    Employee = "Employee"


class Employee(Entity):
    __abstract__ = False
    __tablename__ = "employees"

    name: Mapped[str] = mapped_column(String(100), nullable=False)
    email: Mapped[str] = mapped_column(String(255), nullable=False, unique=True)
    age: Mapped[int] = mapped_column(Integer, nullable=True)
    # password_hash: Mapped[str] = mapped_column(String(255), nullable=False)
    addresses: Mapped[list["Address"]] = relationship( #type:ignore
        "Address",
        back_populates="employee",
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
    
