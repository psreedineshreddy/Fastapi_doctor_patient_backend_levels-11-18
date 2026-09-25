from pydantic import BaseModel, EmailStr


class RegisterRequest(BaseModel):
    email: EmailStr
    password: str
    role: str = "doctor"


class LoginRequest(BaseModel):
    email: EmailStr
    password: str