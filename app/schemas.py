from pydantic import BaseModel, EmailStr
from typing import Optional

class EmployeeCreate(BaseModel):
    name: str
    email: EmailStr
    phone: str
    password: str
    access_type: Optional[str] = "user"  # Default to "user"
    token_type: Optional[str] = "bearer"  # Default to "bearer"

class ShowEmployee(BaseModel):
    id: int
    name: str
    email: EmailStr
    phone: str
    access_type: str
    token_type: str

    class Config:
        from_attributes = True

class EmployeeLogin(BaseModel):
    email: EmailStr
    password: str

class UpdateEmployee(BaseModel):
    name: Optional[str] = None
    phone: Optional[str] = None
    password: Optional[str] = None
    access_type: Optional[str] = None
    token_type: Optional[str] = None
