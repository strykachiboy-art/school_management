from datetime import datetime, timezone
from App.extensions import db
from App.enums.promotion import PromotionDecision


def _utcnow():
    return datetime.now(timezone.utc)


class PromotionHistory(db.Model):
    __tablename__ = "promotion_history"

    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey("students.id"), nullable=False)
    academic_session_id = db.Column(db.Integer, db.ForeignKey("academic_sessions.id"), nullable=False)
    from_classroom_id = db.Column(db.Integer, db.ForeignKey("classrooms.id"), nullable=True)
    to_classroom_id = db.Column(db.Integer, db.ForeignKey("classrooms.id"), nullable=True)
    decision = db.Column(db.Enum(PromotionDecision), nullable=False)
    average_score = db.Column(db.Float, nullable=True)
    attendance_percentage = db.Column(db.Float, nullable=True)
    remarks = db.Column(db.String(255), nullable=True)
    decided_by = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=True)
    created_at = db.Column(db.DateTime, default=_utcnow, nullable=False)

    student = db.relationship("Student", back_populates="promotion_history")
    academic_session = db.relationship("AcademicSession")
    from_classroom = db.relationship("Classroom", foreign_keys=[from_classroom_id])
    to_classroom = db.relationship("Classroom", foreign_keys=[to_classroom_id])
    decided_by_user = db.relationship("User", foreign_keys=[decided_by])