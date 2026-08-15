from flask import abort
from sqlalchemy.exc import IntegrityError

from App.extensions import db
from App.models.academic_session import AcademicSession


# ============================ create academic session ============================

def create_academic_session(data):
    create_academic = AcademicSession(
        name = data.name,
        start_date = data.start_date,
        end_date = data.end_date
    )
    
    try:
        db.session.add(create_academic)
        db.session.commit()
    except IntegrityError:
        db.session.rollback()
        abort(400, description=" Could not create acdemic session — check for duplicate name. ")
    
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

def update_academic_session(data, academic_id):
    
    academic_session = db.session.get(AcademicSession, academic_id)
    
    if academic_session is None:
            return None
    
    academic_session.name = data.name or academic_session.name
    academic_session.start_date = data.start_date or academic_session.start_date
    academic_session.end_date = data.end_date or academic_session.end_date
    

    try:
        db.session.commit()
    except IntegrityError:
        db.session.rollback()
        abort(400, description="Could not update academic_session — check for duplicate name.")
    
    return academic_session
    

# ============================== Delete academic session =================================

def delete_session(academic_id):
    academic_session = db.session.get(AcademicSession, academic_id)
    
    if academic_session is None:
        return False

    db.session.delete(academic_session)
    db.session.commit()
    
    return True


# ============================== Activate academic session =================================

def activate_academic_session(academic_id):
    academic_session = db.session.get(AcademicSession, academic_id)

    if academic_session is None:
        return None

    db.session.query(AcademicSession).filter(
        AcademicSession.id != academic_id
    ).update({AcademicSession.is_active: False})

    academic_session.is_active = True
    db.session.commit()

    return academic_session