from datetime import datetime, timezone
from App.models.association import teacher_subjects

from App.extensions import db

def _utcnow():
    """Return the current UTC time."""
    return datetime.now(timezone.utc)


class Teacher(db.Model):
    __tablename__ = "teachers"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False, unique=True)
    full_name = db.Column(db.String(120), nullable=False)
    email = db.Column(db.String(255), nullable=True)
    phone = db.Column(db.String(20), nullable=True)
    gender = db.Column(db.String(20), nullable=True)
    date_of_birth = db.Column(db.Date, nullable=True)
    created_at = db.Column(db.DateTime, default=_utcnow)
    updated_at = db.Column(db.DateTime, default=_utcnow, onupdate=_utcnow)
    
    user = db.relationship("User", back_populates="teacher_profile")
    classrooms = db.relationship("Classroom", back_populates="teacher")
    subjects = db.relationship("Subject", back_populates="teachers", secondary=teacher_subjects)