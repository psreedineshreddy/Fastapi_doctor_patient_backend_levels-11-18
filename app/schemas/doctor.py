from pydantic import BaseModel, EmailStr


class DoctorCreate(BaseModel):
    name: str
    specialization: str
    email: EmailStr

class DoctorUpdate(BaseModel):
    name: str
    specialization: str
    email: EmailStr

class DoctorResponse(BaseModel):
    id: int
    name: str
    specialization: str
    email: EmailStr
    is_active: bool

class DoctorListResponse(BaseModel):
    total: int
    page: int
    limit: int
    data: list[DoctorResponse]
    
    class Config:
        from_attributes = True