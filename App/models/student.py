from datetime import datetime, timezone
from App.models.association import student_subjects

from App.extensions import db

def _utcnow():
    """Return the current UTC time."""
    return datetime.now(timezone.utc)

class Student(db.Model):
    __tablename__ = "students"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False, unique=True)
    full_name = db.Column(db.String(120), nullable=False)
    email = db.Column(db.String(255), nullable=True)
    phone = db.Column(db.String(20), nullable=True)
    admission_number = db.Column(db.String(50), nullable=True, unique=True)
    classroom_id = db.Column(db.Integer, db.ForeignKey("classrooms.id"), nullable=True)
    gender = db.Column(db.String(20), nullable=True)
    date_of_birth = db.Column(db.Date, nullable=True)
    address = db.Column(db.String(255), nullable=True)
    created_at = db.Column(db.DateTime, nullable=False, default=_utcnow)
    updated_at = db.Column(db.DateTime, nullable=False, default=_utcnow, onupdate=_utcnow)
    
    subjects = db.relationship("Subject", back_populates = "students", secondary = student_subjects)
    user = db.relationship("User", backref=db.backref("student_profile", uselist = False))
    classroom = db.relationship("Classroom", back_populates="students")
    results = db.relationship("Result", back_populates="student")