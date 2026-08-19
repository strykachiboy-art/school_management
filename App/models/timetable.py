from datetime import datetime, timezone

from App.extensions import db
from App.enums.day_of_week import DayOfWeek

def _utcnow():
    return datetime.now(timezone.utc)

class Timetable(db.Model):
    __tablename__ = "timetables"
    
    id = db.Column(db.Integer, primary_key = True)
    term_id = db.Column(db.Integer, db.ForeignKey("terms.id"), nullable = False)
    classroom_id = db.Column(db.Integer, db.ForeignKey("classrooms.id"), nullable = False)
    subject_id = db.Column(db.Integer, db.ForeignKey("subjects.id"), nullable = False)
    teacher_id = db.Column(db.Integer, db.ForeignKey("teachers.id"), nullable = False)
    day_of_week = db.Column(db.Enum(DayOfWeek), nullable = False)
    start_time = db.Column(db.Time, nullable = False)
    end_time = db.Column(db.Time, nullable = False)
    created_at = db.Column(db.DateTime, default=_utcnow, nullable = False)
    updated_at = db.Column(db.DateTime, default=_utcnow, onupdate=_utcnow, nullable = False)
    
    term = db.relationship("Term")
    classroom = db.relationship("Classroom")
    subject = db.relationship("Subject")
    teacher = db.relationship("Teacher")
    