from datetime import datetime, timezone, timedelta
from App.extensions import db
from App.enums.audit import AuditAction
from App.services.audit_log_service import (
    create_audit_log,
    get_audit_log,
    get_filtered_audit_logs,
)


def test_create_audit_log_success(base_user):
    log = create_audit_log(
        actor_id=base_user.id,
        action=AuditAction.CREATE,
        resource_type="Subject",
        resource_id=1,
        description="Created a new test subject",
        ip_address="127.0.0.1",
        user_agent="pytest-agent",
    )
    
    assert log.id is not None
    assert log.actor_id == base_user.id
    assert log.action == AuditAction.CREATE
    assert log.resource_type == "Subject"
    assert log.resource_id == 1


def test_get_audit_log_found(base_user):
    log = create_audit_log(
        actor_id=base_user.id,
        action=AuditAction.UPDATE,
        resource_type="Student",
        resource_id=5,
        description="Updated student details",
    )
    
    fetched = get_audit_log(log.id)
    assert fetched is not None
    assert fetched.id == log.id


def test_get_filtered_audit_logs(base_user):
    create_audit_log(
        actor_id=base_user.id,
        action=AuditAction.CREATE,
        resource_type="Classroom",
        resource_id=10,
        description="Created classroom",
    )
    create_audit_log(
        actor_id=base_user.id,
        action=AuditAction.DELETE,
        resource_type="Classroom",
        resource_id=10,
        description="Deleted classroom",
    )

    result = get_filtered_audit_logs(action=AuditAction.DELETE, page=1, per_page=10)
    assert result.total == 1
    assert result.items[0].action == AuditAction.DELETE

    result_res = get_filtered_audit_logs(resource_type="Classroom", page=1, per_page=10)
    assert result_res.total >= 2