import logging

logger = logging.getLogger(__name__)


def notify_excuse_decision(excuse):
    """
    Called whenever an excuse is approved or rejected, so the affected student
    can be notified. No email provider is wired up yet — this currently just
    logs. To go live: pick a provider (SendGrid, AWS SES, Flask-Mail+SMTP,
    etc.), add its credentials to config.py, and replace the logger.info
    call below with the actual send. Every call site (single approve/reject
    and bulk_review_excuses) already calls this function, so nothing else
    needs to change when you wire in real sending.
    """
    student = excuse.attendance.student
    recipient_email = getattr(student, "email", None) or getattr(student.user, "email", None)

    logger.info(
        "Excuse #%s for student #%s %s (notify: %s)",
        excuse.id,
        excuse.attendance.student_id,
        excuse.status.value,
        recipient_email or "no email on file",
    )