from flask import abort
from sqlalchemy.exc import IntegrityError

from App.extensions import db
from App.models.term import Term


# ============================ Create Term ============================

def create_term(data):
    """
    Creates a new Term attached to an Academic Session.
    """
    create_term = Term(
        name=data.name,
        start_date=data.start_date,
        end_date=data.end_date,
        academic_session_id=data.academic_session_id
    )
    
    try:
        db.session.add(create_term)
        db.session.commit()
    except IntegrityError:
        db.session.rollback()
        abort(400, description="Could not create Term — check for duplicate name or missing required fields.")
    
    return create_term


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

def update_term(data, term_id):
    """
    Handles standard term metadata updates (name, start_date, end_date).
    Does NOT allow modifying academic_session_id.
    """
    term = db.session.get(Term, term_id)
    
    if term is None:
        return None
    
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
    
    return term


# ============================== Reassign Academic Session ===================================

def reassign_term_session(term_id, new_academic_session_id):
    """
    Explicit administrative operation to transfer a term to a different academic session.
    """
    term = db.session.get(Term, term_id)
    
    if term is None:
        return None

    term.academic_session_id = new_academic_session_id

    try:
        db.session.commit()
    except IntegrityError:
        db.session.rollback()
        abort(400, description="Could not reassign academic session — check for valid session ID or conflict.")

    return term


# ============================== Delete Term =================================

def delete_term(term_id):
    """
    Deletes a term record by ID.
    """
    term = db.session.get(Term, term_id)
    
    if term is None:
        return False

    db.session.delete(term)
    db.session.commit()
    
    return True


# ============================== Activate Term =================================

def activate_term(term_id):
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

    return set_term