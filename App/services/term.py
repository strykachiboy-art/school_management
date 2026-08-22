from flask import abort
from sqlalchemy.exc import IntegrityError

from App.extensions import db
from App.models.term import Term
from App.services.audit_log_service import create_audit_log
from App.enums.audit import AuditAction


# ============================ Create Term ============================

def create_term(data, actor_id=None):
    """
    Creates a new Term attached to an Academic Session.
    """
    create_term_obj = Term(
        name=data.name,
        start_date=data.start_date,
        end_date=data.end_date,
        academic_session_id=data.academic_session_id
    )
    
    try:
        db.session.add(create_term_obj)
        db.session.commit()
    except IntegrityError:
        db.session.rollback()
        abort(400, description="Could not create Term — check for duplicate name or missing required fields.")
    
    if actor_id:
        create_audit_log(
            actor_id=actor_id,
            action=AuditAction.CREATE,
            resource_type="Term",
            resource_id=create_term_obj.id,
            description=f"Created term '{create_term_obj.name}' for session ID {create_term_obj.academic_session_id}",
        )

    return create_term_obj


# =============================== Get All Terms =============================

def get_all_term(search="", page=1, per_page=3):
    """
    Retrieves paginated terms filtered optional search term.
    """
    stmt = db.select(Term)
    
    if search:
        stmt = stmt.where(Term.name.ilike(f"%{search}%"))

    stmt = stmt.order_by(Term.id.desc())
    
    return db.paginate(stmt, page=page, per_page=per_page, error_out=False)


# ============================== Get Term By ID ===================================

def get_term_by_id(term_id):
    """
    Fetches a single term by ID.
    """
    return db.session.get(Term, term_id)


# ============================== Update Term Details ===================================

def update_term(data, term_id, actor_id=None):
    """
    Handles standard term metadata updates (name, start_date, end_date).
    Does NOT allow modifying academic_session_id.
    """
    term = db.session.get(Term, term_id)
    
    if term is None:
        return None
    
    changes = {}
    if hasattr(data, 'name') and data.name is not None and data.name != term.name:
        changes["name"] = {"before": term.name, "after": data.name}
    if hasattr(data, 'start_date') and data.start_date is not None and data.start_date != term.start_date:
        changes["start_date"] = {"before": str(term.start_date), "after": str(data.start_date)}
    if hasattr(data, 'end_date') and data.end_date is not None and data.end_date != term.end_date:
        changes["end_date"] = {"before": str(term.end_date), "after": str(data.end_date)}

    if hasattr(data, 'name') and data.name is not None:
        term.name = data.name
    if hasattr(data, 'start_date') and data.start_date is not None:
        term.start_date = data.start_date
    if hasattr(data, 'end_date') and data.end_date is not None:
        term.end_date = data.end_date

    try:
        db.session.commit()
    except IntegrityError:
        db.session.rollback()
        abort(400, description="Could not update Term — check for duplicate name.")
    
    if changes and actor_id:
        create_audit_log(
            actor_id=actor_id,
            action=AuditAction.UPDATE,
            resource_type="Term",
            resource_id=term.id,
            description=f"Updated term ID {term.id} ('{term.name}')",
            changes=changes,
        )

    return term


# ============================== Reassign Academic Session ===================================

def reassign_term_session(term_id, new_academic_session_id, actor_id=None):
    """
    Explicit administrative operation to transfer a term to a different academic session.
    """
    term = db.session.get(Term, term_id)
    
    if term is None:
        return None

    old_session_id = term.academic_session_id
    term.academic_session_id = new_academic_session_id

    try:
        db.session.commit()
    except IntegrityError:
        db.session.rollback()
        abort(400, description="Could not reassign academic session — check for valid session ID or conflict.")

    if actor_id:
        create_audit_log(
            actor_id=actor_id,
            action=AuditAction.UPDATE,
            resource_type="Term",
            resource_id=term.id,
            description=f"Reassigned term ID {term.id} from session {old_session_id} to session {new_academic_session_id}",
            changes={"academic_session_id": {"before": old_session_id, "after": new_academic_session_id}}
        )

    return term


# ============================== Delete Term =================================

def delete_term(term_id, actor_id=None):
    """
    Deletes a term record by ID.
    """
    term = db.session.get(Term, term_id)
    
    if term is None:
        return False

    term_name = term.name
    db.session.delete(term)
    db.session.commit()
    
    if actor_id:
        create_audit_log(
            actor_id=actor_id,
            action=AuditAction.DELETE,
            resource_type="Term",
            resource_id=term_id,
            description=f"Deleted term ID {term_id} ('{term_name}')",
        )

    return True


# ============================== Activate Term =================================

def activate_term(term_id, actor_id=None):
    """
    Sets a specific term as current and deactivates other terms within the same academic session.
    """
    set_term = db.session.get(Term, term_id)

    if set_term is None:
        return None

    db.session.query(Term).filter(
        Term.academic_session_id == set_term.academic_session_id,
        Term.id != term_id
    ).update({
        Term.is_current: False
    })

    set_term.is_current = True
    db.session.commit()

    if actor_id:
        create_audit_log(
            actor_id=actor_id,
            action=AuditAction.UPDATE,
            resource_type="Term",
            resource_id=set_term.id,
            description=f"Activated term ID {set_term.id} ('{set_term.name}') in session ID {set_term.academic_session_id}",
        )

    return set_term