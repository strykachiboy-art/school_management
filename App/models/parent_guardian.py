from datetime import datetime, timezone
from App.extensions import db
from App.enums.parent_guardian import ParentGuardianEnum


def _utcnow():
    return datetime.now(timezone.utc)


class ParentGuardian(db.Model):
    __tablename__ = "parentguardians"
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False, unique=True)
    email = db.Column(db.String(255), nullable=True)
    phone = db.Column(db.String(20), nullable=True)
    address = db.Column(db.String(50), nullable=True)
    occupation = db.Column(db.String(30), nullable=False)
    created_at = db.Column(db.DateTime, default=_utcnow, nullable=False)
    updated_at = db.Column(db.DateTime, default=_utcnow, onupdate=_utcnow, nullable=False)
    
    user = db.relationship("User")


class ParentGuardianStudent(db.Model):
    __tablename__ = "parent_guardian_students"
    
    id = db.Column(db.Integer, primary_key=True)
    parent_guardian_id = db.Column(db.Integer, db.ForeignKey("parentguardians.id"), nullable=False)
    student_id = db.Column(db.Integer, db.ForeignKey("students.id"), nullable=False)
    relationship = db.Column(db.Enum(ParentGuardianEnum), nullable=False)
    created_at = db.Column(db.DateTime, default=_utcnow, nullable=False)
    updated_at = db.Column(db.DateTime, default=_utcnow, onupdate=_utcnow, nullable=False)
    