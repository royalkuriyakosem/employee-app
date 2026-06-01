from pydantic import BaseModel


class AssociationCreate(BaseModel):
    employee_id: int
    department_id: int
