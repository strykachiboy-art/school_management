from datetime import datetime
from typing import Optional
from pydantic import BaseModel, ConfigDict


# Base schema containing shared classroom fields
class ClassroomBase(BaseModel):
    name: str
    capacity: int
    location: Optional[str] = None
    teacher_id: Optional[int] = None


# Schema used for creating or updating a classroom
class ClassroomCreateRequest(ClassroomBase):
    pass


# Schema used for serializing classroom data in API responses (equivalent to dump_only fields)
class ClassroomResponse(ClassroomBase):
    id: int
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    model_config = ConfigDict(from_attributes=True)