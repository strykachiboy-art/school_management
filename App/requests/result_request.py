from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field, ConfigDict


# Base schema containing shared fields for results
class ResultBase(BaseModel):
    student_id: int
    exam_id: int
    marks_obtained: float


# Schema used for creating or updating a result record
class ResultCreateRequest(ResultBase):
    pass


# Schema used for serializing result data in API responses (equivalent to dump_only fields)
class ResultResponse(ResultBase):
    id: int
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    model_config = ConfigDict(from_attributes=True)