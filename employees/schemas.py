from pydantic import BaseModel, Field, ConfigDict, field_validator, model_validator
from datetime import datetime
from models.employee import EmployeeRole


class AddressCreate(BaseModel):
    line1: str
    city: str
    postal_code: str
    country: str

    @field_validator("postal_code")
    @classmethod
    def validate(cls, value: str):
        if not value.isdigit():
            raise ValueError("Postal code only contain digits (0-9)")
        return value

    @model_validator(mode="after")
    def postal_code_length_for_country(self):
        country = self.country.strip().upper()

        n = len(self.postal_code)

        if country in ("US", "UK") and n != 5:
            raise ValueError("Postal Code length should be 5")

        if country in ("IND") and n != 6:
            raise ValueError("Indain PostCodes are of length 6")

        return self


class EmployeeCreate(BaseModel):
    model_config = ConfigDict(extra="forbid", str_strip_whitespace=True)

    name: str
    email: str
    password: str = Field(min_length=6)
    age: int | None = Field(ge=0, le=150)
    address: AddressCreate | None = None
    role: EmployeeRole = EmployeeRole.DEVELOPER


class EmployeeResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    name: str
    email: str
    age: int | None


class GetEmployeeById(EmployeeResponse):
    created_at: datetime
    updated_at: datetime


# class GetAllAddress(AddressCreate):
#     employee: str


class UpdateEmployee(BaseModel):
    name: str
    email: str


class AddressResponse(AddressCreate):
    id: int
    # employee_name: str
