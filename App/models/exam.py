from App.extensions import db
from datetime import datetime, timezone


def _utcnow():
    return datetime.now(timezone.utc)

class Exam(db.Model):
    __tablename__ = "exams"
    id = db.Column(db.Integer, primary_key = True)
    title = db.Column(db.String(100), nullable = False)
    description = db.Column(db.Text, nullable = True)
    subject_id = db.Column(db.Integer, db.ForeignKey("subjects.id"), nullable = False)
    classroom_id = db.Column(db.Integer, db.ForeignKey("classrooms.id"), nullable = False)
    session_id = db.Column(db.Integer, db.ForeignKey("academic_sessions.id"), nullable=False)
    exam_date = db.Column(db.DateTime, nullable = False)
    start_time = db.Column(db.Time, nullable = False)
    duration_minutes = db.Column(db.Integer, nullable = False)
    total_marks = db.Column(db.Integer, nullable = False)
    created_at = db.Column(db.DateTime, default=_utcnow, nullable=False)
    updated_at = db.Column(db.DateTime, default=_utcnow, onupdate=_utcnow, nullable=False)

    results = db.relationship("Result", back_populates = "exam")
    subject = db.relationship("Subject", back_populates="exams")
    classroom = db.relationship("Classroom", back_populates="exams")
    session = db.relationship("AcademicSession", back_populates="exams")