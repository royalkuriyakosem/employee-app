"""
Department Entitiy - ORM mapped class for table 'department'
"""

from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String
from models.entity import Entity


class Department(Entity):
    __abstract__ = False
    __tablename__ = "department"

    name: Mapped[int] = mapped_column(String(100), nullable=False)

    # def to_api_dict(self) -> dict[str, Any]:
    #     """JSON-friendly representation (ISO 8601 for timestamps)."""
    #     return {
    #         "id": self.id,
    #         "name": self.name,
    #         "created_at": datetime_to_iso(self.created_at),
    #         "updated_at": datetime_to_iso(self.updated_at),
    #         "deleted_at": datetime_to_iso(self.deleted_at),
    #     }
