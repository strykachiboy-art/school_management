from datetime import datetime, timezone
from App.extensions import db
from App.enums.attendance import AttendanceStatus


def _utcnow():
    """Return the current UTC time."""
    return datetime.now(timezone.utc)


class Attendance(db.Model):
    __tablename__ = "attendances"

    # Define unique constraint for student, term, and date combination
    __table_args__ = (
        db.UniqueConstraint(
            "student_id", "term_id", "date", name="uq_student_term_date_attendance"
        ),
    )

    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey("students.id"), nullable=False)
    term_id = db.Column(db.Integer, db.ForeignKey("terms.id"), nullable=False)
    date = db.Column(db.Date, nullable=False)
    status = db.Column(db.Enum(AttendanceStatus), nullable=False)
    created_at = db.Column(db.DateTime, default=_utcnow, nullable=False)
    updated_at = db.Column(
        db.DateTime, default=_utcnow, onupdate=_utcnow, nullable=False
    )

    student = db.relationship("Student", back_populates="attendance_records")
    term = db.relationship("Term", back_populates="attendance_records")
