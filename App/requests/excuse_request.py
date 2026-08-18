from datetime import datetime
from typing import Optional
from pydantic import BaseModel, ConfigDict
from App.enums.excuse import ExcuseStatus


class ExcuseCreateRequest(BaseModel):
    attendance_id: int
    reason: str


class ExcuseUpdateRequest(BaseModel):
    reason: str


class ExcuseResponse(BaseModel):
    id: int
    attendance_id: int
    reason: str
    status: ExcuseStatus
    reviewed_by: Optional[int] = None
    reviewed_at: Optional[datetime] = None
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)