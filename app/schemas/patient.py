from pydantic import BaseModel, Field


class PatientCreate(BaseModel):
    name: str
    age: int = Field(gt=0)
    phone: str = Field(pattern=r"^\d{10,15}$")


class PatientResponse(BaseModel):
    id: int
    name: str
    age: int
    phone: str

    class Config:
        from_attributes = True