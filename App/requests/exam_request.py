from datetime import date, datetime, time
from typing import Optional
from pydantic import BaseModel, ConfigDict


# Base schema containing shared exam fields
class ExamBase(BaseModel):
    title: str
    description: Optional[str] = None
    subject_id: int
    classroom_id: int
    exam_date: date
    start_time: time
    duration_minutes: Optional[int] = None
    total_marks: int


# Schema used for creating or updating an exam
class ExamCreateRequest(ExamBase):
    pass


# Schema used for serializing exam data in API responses (equivalent to dump_only fields)
class ExamResponse(ExamBase):
    id: int
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    model_config = ConfigDict(from_attributes=True)