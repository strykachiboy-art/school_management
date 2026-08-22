from datetime import datetime
from pydantic import BaseModel, Field, field_validator
from App.enums.audit import AuditAction


class AuditLogFilterRequest(BaseModel):
    """Query params for GET /audit-logs. No create request needed —
    log entries are written internally by log_action(), not via API."""

    actor_id: int | None = None
    action: AuditAction | None = None
    resource_type: str | None = Field(None, min_length=1, max_length=100)
    resource_id: int | None = None
    date_from: datetime | None = None
    date_to: datetime | None = None
    page: int = Field(1, ge=1)
    per_page: int = Field(20, ge=1, le=100)

    @field_validator("resource_type")
    @classmethod
    def not_blank(cls, v: str | None) -> str | None:
        if v is not None:
            v = v.strip()
            if not v:
                raise ValueError("resource_type cannot be blank")
        return v

    @field_validator("date_to")
    @classmethod
    def date_range_valid(cls, v: datetime | None, info) -> datetime | None:
        date_from = info.data.get("date_from")
        if v and date_from and v < date_from:
            raise ValueError("date_to cannot be before date_from")
        return v