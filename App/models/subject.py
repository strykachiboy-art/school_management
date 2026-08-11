from datetime import datetime, timezone
from App.models.association import student_subjects, classroom_subjects, teacher_subjects

from App.extensions import db


def _utcnow():
    """Return the current UTC time."""
    return datetime.now(timezone.utc)


class Subject(db.Model):
    __tablename__ = "subjects"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False, unique=True)
    code = db.Column(db.String(20), nullable=False, unique=True)
    description = db.Column(db.Text, nullable=True)
    created_at = db.Column(db.DateTime, nullable=False, default=_utcnow)
    updated_at = db.Column(db.DateTime, nullable=False, default=_utcnow, onupdate=_utcnow)
    
    students = db.relationship("Student", secondary = student_subjects, back_populates = "subjects")
    teachers = db.relationship("Teacher", secondary = teacher_subjects, back_populates = "subjects")
    classrooms = db.relationship("Classroom", secondary = classroom_subjects, back_populates = "subjects")