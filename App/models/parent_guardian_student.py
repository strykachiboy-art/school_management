from datetime import datetime, timezone
from App.extensions import db
from App.enums.parent_guardian import ParentGuardianEnum 


def _utcnow():
    return datetime.now(timezone.utc)


class ParentGuardianStudent(db.Model):
    __tablename__ = "parent_guardian_students"
    
    id = db.Column(db.Integer, primary_key=True)
    parent_guardian_id = db.Column(db.Integer, db.ForeignKey("parentguardians.id"), nullable=False, unique=True)
    student_id = db.Column(db.Integer, db.ForeignKey("students.id"), nullable=False, unique=True)
    relationship = db.Column(db.Enum(ParentGuardianEnum), nullable=False)
    created_at = db.Column(db.DateTime, default=_utcnow, nullable=False)
    updated_at = db.Column(db.DateTime, default=_utcnow, onupdate=_utcnow, nullable=False)