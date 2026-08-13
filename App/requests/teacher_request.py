from datetime import date, datetime
from typing import Optional
from pydantic import BaseModel, EmailStr, Field, ConfigDict


class TeacherBase(BaseModel):
    full_name: str
    email: Optional[EmailStr] = None
    phone: Optional[str] = None
    subject: Optional[str] = None
    gender: Optional[str] = None
    date_of_birth: Optional[date] = None


class TeacherCreateRequest(TeacherBase):
    username: str
    password: str


class TeacherResponse(TeacherBase):
    id: int
    user_id: int
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    model_config = ConfigDict(from_attributes=True)