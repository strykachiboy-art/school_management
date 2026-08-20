from datetime import datetime, timezone
from App.extensions import db
from App.enums.parent_guardian import ParentGuardianEnum 


def _utcnow():
    return datetime.now(timezone.utc)


class ParentGuardian(db.Model):
    __tablename__ = "parentguardians"
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False, unique=True)
    occupation = db.Column(db.String(30), nullable=False)
    relationship = db.Column(db.Enum(ParentGuardianEnum), nullable=False)
    created_at = db.Column(db.DateTime, default=_utcnow, nullable=False)
    updated_at = db.Column(db.DateTime, default=_utcnow, onupdate=_utcnow, nullable=False)
    
    user = db.relationship("User")