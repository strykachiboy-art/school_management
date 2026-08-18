from App.extensions import db
from App.models.association import classroom_subjects

from datetime import datetime, timezone


def _utcnow():
    """Return the current UTC time."""
    return datetime.now(timezone.utc)


class Classroom(db.Model):
    __tablename__ = "classrooms"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False, unique=True)
    capacity = db.Column(db.Integer, nullable=False)
    location = db.Column(db.String(100), nullable=True)
    teacher_id = db.Column(db.Integer, db.ForeignKey("teachers.id"), nullable=True)
    created_at = db.Column(db.DateTime, default=_utcnow)
    updated_at = db.Column(db.DateTime, default=_utcnow, onupdate=_utcnow)
    is_final_level = db.Column(db.Boolean, nullable = False, default = False)
    
    subjects = db.relationship("Subject", back_populates = "classrooms", secondary = classroom_subjects)
    teacher = db.relationship("Teacher", back_populates="classrooms", uselist=False)
    students = db.relationship("Student", back_populates="classroom")
    exams = db.relationship("Exam", back_populates="classroom")