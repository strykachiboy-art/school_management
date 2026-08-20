from App.extensions import db
from App.models.parent_guardian import ParentGuardian, ParentGuardianStudent

# ==========================================
# Parent Guardian Services
# ==========================================

def create_parent_guardian(data: dict):
    new_guardian = ParentGuardian(
        user_id=data.get("user_id"),
        occupation=data.get("occupation"),
        email=data.get("email"),
        phone=data.get("phone"),
        address=data.get("address")
    )
    db.session.add(new_guardian)
    db.session.commit()
    return new_guardian


def get_parent_guardian(guardian_id: int):
    return db.session.get(ParentGuardian, guardian_id)


def get_all_parent_guardians():
    return ParentGuardian.query.all()


def update_parent_guardian(guardian_id: int, data: dict):
    guardian = get_parent_guardian(guardian_id)
    if not guardian:
        return None
    
    for key, value in data.items():
        if value is not None:
            setattr(guardian, key, value)
            
    db.session.commit()
    return guardian


def delete_parent_guardian(guardian_id: int):
    guardian = get_parent_guardian(guardian_id)
    if not guardian:
        return False
    db.session.delete(guardian)
    db.session.commit()
    return True


# ==========================================
# Parent Guardian Student Services
# ==========================================

def assign_student_to_guardian(data: dict):
    assignment = ParentGuardianStudent(
        parent_guardian_id=data.get("parent_guardian_id"),
        student_id=data.get("student_id"),
        relationship=data.get("relationship")
    )
    db.session.add(assignment)
    db.session.commit()
    return assignment


def get_guardian_students(guardian_id: int):
    return ParentGuardianStudent.query.filter_by(parent_guardian_id=guardian_id).all()


def get_student_guardians(student_id: int):
    return ParentGuardianStudent.query.filter_by(student_id=student_id).all()


def update_guardian_student_relationship(record_id: int, data: dict):
    assignment = db.session.get(ParentGuardianStudent, record_id)
    if not assignment:
        return None
        
    for key, value in data.items():
        if value is not None:
            setattr(assignment, key, value)
            
    db.session.commit()
    return assignment


def remove_student_from_guardian(record_id: int):
    assignment = db.session.get(ParentGuardianStudent, record_id)
    if not assignment:
        return False
    db.session.delete(assignment)
    db.session.commit()
    return True