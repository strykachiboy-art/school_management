from flask import abort
from sqlalchemy.exc import IntegrityError

from App.extensions import db
from App.models.academic_session import AcademicSession
from App.services.audit_log_service import create_audit_log
from App.enums.audit import AuditAction


# ============================ create academic session ============================

def create_academic_session(data, actor_id):
    create_academic = AcademicSession(
        name=data.name,
        start_date=data.start_date,
        end_date=data.end_date
    )
    
    try:
        db.session.add(create_academic)
        db.session.commit()
    except IntegrityError:
        db.session.rollback()
        abort(400, description="Could not create academic session — check for duplicate name.")
    
    create_audit_log(
        actor_id=actor_id,
        action=AuditAction.CREATE,
        resource_type="AcademicSession",
        resource_id=create_academic.id,
        description=f"Created academic session {create_academic.name}",
    )
    
    return create_academic


# =============================== Get all Academic session =============================

def get_all_academic_session(search="", page=1, per_page=10):
    stmt = db.select(AcademicSession)
    if search:
        stmt = stmt.where(AcademicSession.name.ilike(f"%{search}%"))

    stmt = stmt.order_by(AcademicSession.id.desc())
    
    return db.paginate(stmt, page=page, per_page=per_page, error_out=False)


# ============================== Get academic session ===================================

def get_academic_session(Academic_id):
    return db.session.get(AcademicSession, Academic_id)


# ============================== Update academic session =================================

def update_academic_session(data, academic_id, actor_id):
    academic_session = db.session.get(AcademicSession, academic_id)
    
    if academic_session is None:
        return None
    
    changes = {}
    if data.name and data.name != academic_session.name:
        changes["name"] = {"before": academic_session.name, "after": data.name}
    if data.start_date and data.start_date != academic_session.start_date:
        changes["start_date"] = {"before": str(academic_session.start_date), "after": str(data.start_date)}
    if data.end_date and data.end_date != academic_session.end_date:
        changes["end_date"] = {"before": str(academic_session.end_date), "after": str(data.end_date)}

    academic_session.name = data.name or academic_session.name
    academic_session.start_date = data.start_date or academic_session.start_date
    academic_session.end_date = data.end_date or academic_session.end_date

    try:
        db.session.commit()
    except IntegrityError:
        db.session.rollback()
        abort(400, description="Could not update academic_session — check for duplicate name.")
    
    if changes:
        create_audit_log(
            actor_id=actor_id,
            action=AuditAction.UPDATE,
            resource_type="AcademicSession",
            resource_id=academic_session.id,
            description=f"Updated academic session {academic_session.name}",
            changes=changes,
        )
    
    return academic_session
    

# ============================== Delete academic session =================================

def delete_session(academic_id, actor_id):
    academic_session = db.session.get(AcademicSession, academic_id)
    
    if academic_session is None:
        return False

    session_name = academic_session.name
    db.session.delete(academic_session)
    db.session.commit()
    
    create_audit_log(
        actor_id=actor_id,
        action=AuditAction.DELETE,
        resource_type="AcademicSession",
        resource_id=academic_id,
        description=f"Deleted academic session {session_name}",
    )
    
    return True


# ============================== Activate academic session =================================

def activate_academic_session(academic_id, actor_id):
    academic_session = db.session.get(AcademicSession, academic_id)

    if academic_session is None:
        return None

    db.session.query(AcademicSession).filter(
        AcademicSession.id != academic_id
    ).update({AcademicSession.is_active: False})

    academic_session.is_active = True
    db.session.commit()

    create_audit_log(
        actor_id=actor_id,
        action=AuditAction.UPDATE,
        resource_type="AcademicSession",
        resource_id=academic_session.id,
        description=f"Activated academic session {academic_session.name}",
    )

    return academic_session