from App.extensions import db
from App.enums.audit import AuditAction
from datetime import datetime, timezone


def _utcnow():
    """Return the current UTC time."""
    return datetime.now(timezone.utc)

class AuditLog(db.Model):
    __tablename__ = "audit_logs"

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    actor_id = db.Column(
        db.Integer,
        db.ForeignKey("users.id"),
        nullable=False,
        index=True
    )

    action = db.Column(
        db.Enum(AuditAction),
        nullable=False
    )

    resource_type = db.Column(
        db.String(100),
        nullable=False
    )

    resource_id = db.Column(
        db.Integer,
        nullable=True
    )

    description = db.Column(
        db.Text,
        nullable=False
    )

    # Stores relevant before/after changes when applicable
    changes = db.Column(
        db.JSON,
        nullable=True
    )

    # Security metadata
    ip_address = db.Column(
        db.String(45),
        nullable=True
    )

    user_agent = db.Column(
        db.String(255),
        nullable=True
    )

    created_at = db.Column(
        db.DateTime(timezone=True),
        default=_utcnow,
        nullable=False,
        index=True
    )

    __table_args__ = (
        db.Index(
            "idx_audit_resource",
            "resource_type",
            "resource_id"
        ),
    )

    actor = db.relationship(
        "User",
        back_populates="audit_logs"
    )

    def __repr__(self):
        return (
            f"<AuditLog id={self.id} "
            f"action={self.action.value} "
            f"actor={self.actor_id}>"
        )

    def to_dict(self):
        return {
            "id": self.id,
            "actor_id": self.actor_id,
            "action": (
                self.action.value
                if hasattr(self.action, "value")
                else str(self.action)
            ),
            "resource_type": self.resource_type,
            "resource_id": self.resource_id,
            "description": self.description,
            "changes": self.changes,
            "ip_address": self.ip_address,
            "user_agent": self.user_agent,
            "created_at": (
                self.created_at.isoformat()
                if self.created_at
                else None
            ),
        }