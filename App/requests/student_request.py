from datetime import date, datetime
from typing import Optional
from pydantic import BaseModel, EmailStr, Field, ConfigDict


# Base schema containing shared fields
class StudentBase(BaseModel):
    full_name: str
    email: Optional[EmailStr] = None
    phone: Optional[str] = None
    admission_number: Optional[str] = None
    classroom_id: Optional[int] = None
    gender: Optional[str] = None
    date_of_birth: Optional[date] = None
    address: Optional[str] = None


# Schema used for creating a student (username/password are create-only)
class StudentCreateRequest(StudentBase):
    username: str
    password: str


# Schema used for serializing student data in API responses (equivalent to dump_only fields)
class StudentResponse(StudentBase):
    id: int
    user_id: int
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    model_config = ConfigDict(from_attributes=True)