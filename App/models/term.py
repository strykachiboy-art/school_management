from App.extensions import db
from datetime import datetime, timezone

def _utcnow():
    """Return the current UTC time."""
    return datetime.now(timezone.utc)

class Term(db.Model):
    
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(30), nullable = False)
    end_date = db.Column(db.Date, nullable = False)
    is_current = db.Column(db.Boolean, default = False, nullable = False)
    academic_session_id = db.Column(db.Integer, db.ForeignKey("academic_session.id"))
    created_at = db.Column(db.DateTime, default = _utcnow, nullable = False)
    updated_at = db.Column(db.DateTime, default = _utcnow, onupdate = _utcnow, nullable = False)
    
    academic_session = db.relationship("AcademicSession", back_populates = "term")