from datetime import datetime, timezone
from App.extensions import db
from App.enums.notification import NotificationType


def _utcnow():
    return datetime.now(timezone.utc)


class Notification(db.Model):
    
    id = db.Column(db.Integer, primary_key = True)
    recepient_id = db.Column(db.Integer, db.ForeignKey("users.id"),
                             nullable = False)
    title = db.Column(db.String(60), nullable = False)
    message = db.Column(db.Text, nullable = False)
    notification_type = db.Column(db.Enum(NotificationType), nullable = False)
    is_read = db.Column(db.Boolean, nullable = True, default = False)
    read_at = db.Column(db.DateTime, nullable = True)
    created_at = db.Column(db.DateTime, default=_utcnow, nullable=False)
    updated_at = db.Column(db.DateTime, default=_utcnow, onupdate=_utcnow, nullable=False)