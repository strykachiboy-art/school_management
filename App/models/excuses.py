from datetime import datetime, timezone
from App.extensions import db
from App.enums.excuse import ExcuseStatus


def _utcnow():
    return datetime.now(timezone.utc)


class Excuse(db.Model):
    __tablename__ = "excuses"

    id = db.Column(db.Integer, primary_key=True)
    attendance_id = db.Column(
        db.Integer,
        db.ForeignKey("attendances.id"),
        nullable=False,
        unique=True,
    )
    reason = db.Column(db.String(500), nullable=False)
    status = db.Column(
        db.Enum(ExcuseStatus),
        nullable=False,
        default=ExcuseStatus.PENDING,
    )
    reviewed_by = db.Column(
        db.Integer,
        db.ForeignKey("users.id"),
        nullable=True,
    )
    reviewed_at = db.Column(db.DateTime, nullable=True)
    created_at = db.Column(db.DateTime, default=_utcnow, nullable=False)
    updated_at = db.Column(
        db.DateTime,
        default=_utcnow,
        onupdate=_utcnow,
        nullable=False,
    )

    # Relationships
    attendance = db.relationship("Attendance", back_populates="excuse")
    reviewer = db.relationship("User", foreign_keys=[reviewed_by])