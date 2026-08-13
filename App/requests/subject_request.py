from datetime import datetime
from typing import Optional
from pydantic import BaseModel, ConfigDict


# Base schema containing shared subject fields
class SubjectBase(BaseModel):
    name: str
    code: str
    description: Optional[str] = None


# Schema used for creating or updating a subject
class SubjectCreateRequest(SubjectBase):
    pass


# Schema used for serializing subject data in API responses (equivalent to dump_only fields)
class SubjectResponse(SubjectBase):
    id: int
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    model_config = ConfigDict(from_attributes=True)