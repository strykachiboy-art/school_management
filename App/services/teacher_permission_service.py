from flask import abort
from sqlalchemy.exc import IntegrityError

from App.extensions import db
from App.models.teacher import Teacher
from App.models.teacher_permission import TeacherPermission
from App.enums.permission import Permission


def _get_teacher_or_404(teacher_id: int) -> Teacher:
    teacher = db.session.get(Teacher, teacher_id)
    if teacher is None:
        abort(404, description=f"Teacher with ID {teacher_id} not found.")
    return teacher


def assign_teacher_permission(teacher_id: int, permission: Permission) -> TeacherPermission:
    """Admin assigns a single permission to a teacher. Prevents duplicates."""
    _get_teacher_or_404(teacher_id)

    existing = db.session.scalar(
        db.select(TeacherPermission).where(
            TeacherPermission.teacher_id == teacher_id,
            TeacherPermission.permission == permission,
        )
    )
    if existing:
        abort(400, description=f"Teacher already has the '{permission.value}' permission.")

    record = TeacherPermission(teacher_id=teacher_id, permission=permission)

    try:
        db.session.add(record)
        db.session.commit()
    except IntegrityError:
        db.session.rollback()
        abort(400, description=f"Teacher already has the '{permission.value}' permission.")

    return record


def get_teacher_permissions(teacher_id: int) -> list[TeacherPermission]:
    """All permissions currently assigned to one teacher."""
    _get_teacher_or_404(teacher_id)

    return db.session.scalars(
        db.select(TeacherPermission).where(TeacherPermission.teacher_id == teacher_id)
    ).all()


def get_all_teacher_permissions() -> list[TeacherPermission]:
    """Admin view — every permission assignment, across all teachers."""
    return db.session.scalars(db.select(TeacherPermission)).all()


def update_teacher_permissions(teacher_id: int, permissions: list[Permission]) -> list[TeacherPermission]:
    # """
    # Replaces a teacher's full permission set with the given list.
    # Only adds what's missing and removes what's no longer wanted —
    # unchanged permissions keep their original row untouched.
    # """
    _get_teacher_or_404(teacher_id)

    desired = set(permissions)

    existing_records = db.session.scalars(
        db.select(TeacherPermission).where(TeacherPermission.teacher_id == teacher_id)
    ).all()
    existing_permissions = {r.permission for r in existing_records}

    # Remove permissions no longer wanted.
    for record in existing_records:
        if record.permission not in desired:
            db.session.delete(record)

    # Add permissions that are newly wanted.
    to_add = desired - existing_permissions
    new_records = [TeacherPermission(teacher_id=teacher_id, permission=p) for p in to_add]
    db.session.add_all(new_records)

    db.session.commit()

    return db.session.scalars(
        db.select(TeacherPermission).where(TeacherPermission.teacher_id == teacher_id)
    ).all()


def remove_teacher_permission(teacher_id: int, permission: Permission) -> None:
    """Admin revokes a specific permission from a teacher."""
    record = db.session.scalar(
        db.select(TeacherPermission).where(
            TeacherPermission.teacher_id == teacher_id,
            TeacherPermission.permission == permission,
        )
    )
    if record is None:
        abort(404, description=f"Teacher does not have the '{permission.value}' permission.")

    db.session.delete(record)
    db.session.commit()