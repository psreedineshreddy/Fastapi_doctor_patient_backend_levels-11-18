from pydantic import BaseModel, Field, field_validator


class PatientCreate(BaseModel):
    name: str
    age: int = Field(gt=0)
    phone: str
    doctor_id: int

    @field_validator("phone")
    @classmethod
    def validate_phone(cls, value):
        if not value.isdigit() or len(value) != 10:
            raise ValueError("Phone number must contain exactly 10 digits")
        return value


class PatientResponse(BaseModel):
    id: int
    name: str
    age: int
    phone: str
    doctor_id: int


class PatientListResponse(BaseModel):
    total: int
    page: int
    limit: int
    data: list[PatientResponse]

    class Config:
        from_attributes = True