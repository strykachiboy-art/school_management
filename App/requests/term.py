from datetime import date, datetime
from typing import Optional
from pydantic import BaseModel, ConfigDict, field_validator


# Base schema containing shared term fields
class TermBase(BaseModel):
    name: str
    end_date: date
    is_current: Optional[bool] = False
    academic_session_id: int

    @field_validator("name")
    @classmethod
    def name_not_blank(cls, v: str) -> str:
        v = v.strip()
        if not v:
            raise ValueError("name cannot be blank")
        return v


# Schema used for creating or updating a term
class TermCreateRequest(TermBase):
    pass


# Schema used for serializing term data in API responses (equivalent to dump_only fields)
class TermResponse(TermBase):
    id: int
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    model_config = ConfigDict(from_attributes=True)