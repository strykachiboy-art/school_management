from datetime import datetime, timezone
from typing import Optional, Sequence

from sqlalchemy.exc import IntegrityError

from App.extensions import db
from App.models.notification import Notification
from App.enums.notification import NotificationType
from App.models.user import User
from App.services.audit_log_service import create_audit_log
from App.enums.audit import AuditAction


class InvalidRecipientError(Exception):
    """Raised when recipient_id doesn't correspond to a real user."""

def create_notification(
    recipient_id: int,
    title: str,
    message: str,
    notification_type: NotificationType,
    actor_id: Optional[int] = None,
) -> Notification:
    # Explicitly verify the user exists
    user = db.session.get(User, recipient_id)
    if not user:
        raise InvalidRecipientError(f"recipient_id {recipient_id} does not exist")

    notification = Notification(
        recipient_id=recipient_id,
        title=title,
        message=message,
        notification_type=notification_type,
        is_read=False,
    )
    db.session.add(notification)
    try:
        db.session.commit()
    except IntegrityError:
        db.session.rollback()
        raise InvalidRecipientError(f"recipient_id {recipient_id} does not exist")

    effective_actor_id = actor_id if actor_id is not None else recipient_id
    if effective_actor_id:
        create_audit_log(
            actor_id=effective_actor_id,
            action=AuditAction.CREATE,
            resource_type="Notification",
            resource_id=notification.id,
            description=f"Created notification for user ID {recipient_id}: {title}",
        )

    return notification


def get_notification(notification_id: int, recipient_id: int) -> Optional[Notification]:
    return Notification.query.filter_by(
        id=notification_id, recipient_id=recipient_id
    ).first()


def get_my_notifications(recipient_id: int, page: int = 1, per_page: int = 20):
    return (
        Notification.query
        .filter_by(recipient_id=recipient_id)
        .order_by(Notification.created_at.desc())
        .paginate(page=page, per_page=per_page, error_out=False)
    )


def get_unread_notifications(recipient_id: int, page: int = 1, per_page: int = 20):
    return (
        Notification.query
        .filter_by(recipient_id=recipient_id, is_read=False)
        .order_by(Notification.created_at.desc())
        .paginate(page=page, per_page=per_page, error_out=False)
    )


def mark_notification_as_read(notification_id: int, recipient_id: int, actor_id: Optional[int] = None) -> Optional[Notification]:
    notification = get_notification(notification_id, recipient_id)
    if notification is None:
        return None
    if not notification.is_read:
        notification.is_read = True
        notification.read_at = datetime.now(timezone.utc)
        db.session.commit()

        effective_actor_id = actor_id if actor_id is not None else recipient_id
        if effective_actor_id:
            create_audit_log(
                actor_id=effective_actor_id,
                action=AuditAction.UPDATE,
                resource_type="Notification",
                resource_id=notification.id,
                description=f"Marked notification ID {notification.id} as read",
                changes={"is_read": {"before": False, "after": True}}
            )

    return notification


def mark_all_notifications_as_read(recipient_id: int, actor_id: Optional[int] = None) -> int:
    now = datetime.now(timezone.utc)
    updated = (
        Notification.query
        .filter_by(recipient_id=recipient_id, is_read=False)
        .update({"is_read": True, "read_at": now}, synchronize_session=False)
    )
    db.session.commit()

    effective_actor_id = actor_id if actor_id is not None else recipient_id
    if updated > 0 and effective_actor_id:
        create_audit_log(
            actor_id=effective_actor_id,
            action=AuditAction.BULK_ACTION,
            resource_type="Notification",
            resource_id=None,
            description=f"Marked all unread notifications ({updated}) as read for user ID {recipient_id}",
        )

    return updated


def delete_notification(notification_id: int, recipient_id: int, actor_id: Optional[int] = None) -> bool:
    notification = get_notification(notification_id, recipient_id)
    if notification is None:
        return False
    db.session.delete(notification)
    db.session.commit()

    effective_actor_id = actor_id if actor_id is not None else recipient_id
    if effective_actor_id:
        create_audit_log(
            actor_id=effective_actor_id,
            action=AuditAction.DELETE,
            resource_type="Notification",
            resource_id=notification_id,
            description=f"Deleted notification ID {notification_id}",
        )

    return True


# --- reusable entry points other services should call directly ---

def notify_user(
    recipient_id: int, title: str, message: str, notification_type: NotificationType, actor_id: Optional[int] = None
) -> Notification:
    return create_notification(recipient_id, title, message, notification_type, actor_id=actor_id)


def notify_users(
    recipient_ids: Sequence[int],
    title: str,
    message: str,
    notification_type: NotificationType,
    actor_id: Optional[int] = None,
) -> list[Notification]:
    if not recipient_ids:
        return []

    notifications = [
        Notification(
            recipient_id=rid,
            title=title,
            message=message,
            notification_type=notification_type,
            is_read=False,
        )
        for rid in recipient_ids
    ]
    # return_defaults=True populates the primary key IDs back onto the instances
    db.session.bulk_save_objects(notifications, return_defaults=True)
    try:
        db.session.commit()
    except IntegrityError:
        db.session.rollback()
        raise InvalidRecipientError("one or more recipient_ids do not exist")

    if actor_id:
        create_audit_log(
            actor_id=actor_id,
            action=AuditAction.BULK_ACTION,
            resource_type="Notification",
            resource_id=None,
            description=f"Bulk sent notifications to {len(recipient_ids)} recipient(s): {title}",
            changes={"recipient_ids": list(recipient_ids)}
        )

    return notifications