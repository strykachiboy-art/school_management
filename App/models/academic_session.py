from App.extensions import db
from datetime import datetime, timezone


def _utcnow():
    """Return the current UTC time."""
    return datetime.now(timezone.utc)


class AcademicSession(db.Model):
    __tablename__ = "academic_sessions"
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False, unique=True)
    start_date = db.Column(db.DateTime, nullable=False, default=_utcnow)
    end_date = db.Column(db.DateTime, nullable=False)
    is_active = db.Column(db.Boolean, nullable=False, default=False)
    created_at = db.Column(db.DateTime, nullable=False, default=_utcnow)
    updated_at = db.Column(
        db.DateTime, 
        nullable=False, 
        default=_utcnow, 
        onupdate=_utcnow
    )