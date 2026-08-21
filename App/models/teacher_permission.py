from datetime import datetime, timezone
from App.extensions import db
from App.enums.permission import Permission


def _utcnow():
    return datetime.now(timezone.utc)


class TeacherPermission(db.Model):
    __tablename__ = "teacher_permissions"

    __table_args__ = (
        db.UniqueConstraint("teacher_id", "permission", name="uq_teacher_permission"),
    )

    id = db.Column(db.Integer, primary_key=True)
    teacher_id = db.Column(db.Integer, db.ForeignKey("teachers.id", ondelete="CASCADE"), nullable=False)
    permission = db.Column(db.Enum(Permission), nullable=False)
    created_at = db.Column(db.DateTime, default=_utcnow, nullable=False)
    updated_at = db.Column(db.DateTime, default=_utcnow, onupdate=_utcnow, nullable=False)

    teacher = db.relationship("Teacher", back_populates="permissions")