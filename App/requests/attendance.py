from datetime import date, datetime
from typing import Optional
from pydantic import BaseModel, ConfigDict, field_validator
from App.enums.attendance import AttendanceStatus


# Base schema containing shared attendance fields
class AttendanceBase(BaseModel):
    student_id: int
    term_id: int
    date: date
    status: AttendanceStatus


# Schema used for creating a new attendance record
class AttendanceCreateRequest(AttendanceBase):
    pass


# Schema used for updating an existing attendance record (all fields optional)
class AttendanceUpdateRequest(BaseModel):
    student_id: Optional[int] = None
    term_id: Optional[int] = None
    date: Optional[date] = None
    status: Optional[AttendanceStatus] = None


# Schema used for serializing attendance data in API responses
class AttendanceResponse(AttendanceBase):
    id: int
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    model_config = ConfigDict(from_attributes=True)