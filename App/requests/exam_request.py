from datetime import date, datetime, time
from typing import Optional
from pydantic import BaseModel, ConfigDict, field_validator


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

    @field_validator("title")
    @classmethod
    def title_not_blank(cls, v: str) -> str:
        v = v.strip()
        if not v:
            raise ValueError("title cannot be blank")
        return v

    @field_validator("exam_date")
    @classmethod
    def exam_date_not_in_past(cls, v: date) -> date:
        if v < date.today():
            raise ValueError("exam_date cannot be in the past")
        return v

    @field_validator("duration_minutes")
    @classmethod
    def duration_positive(cls, v: Optional[int]) -> Optional[int]:
        if v is not None and v <= 0:
            raise ValueError("duration_minutes must be a positive number")
        return v

    @field_validator("total_marks")
    @classmethod
    def total_marks_positive(cls, v: int) -> int:
        if v <= 0:
            raise ValueError("total_marks must be a positive number")
        return v


# Schema used for creating or updating an exam
class ExamCreateRequest(ExamBase):
    pass


# Schema used for serializing exam data in API responses (equivalent to dump_only fields)
class ExamResponse(ExamBase):
    id: int
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    model_config = ConfigDict(from_attributes=True)