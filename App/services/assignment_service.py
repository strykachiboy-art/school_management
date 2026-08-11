from App.extensions import db
from App.models.subject import Subject
from App.models.teacher import Teacher
from App.models.student import Student
from App.models.classroom import Classroom

MAX_TEACHERS_PER_ASSIGNMENT = 500
MAX_STUDENTS_PER_ASSIGNMENT = 500
MAX_CLASSROOMS_PER_ASSIGNMENT = 500


# ================================ Generic helpers ==================================
def _get_subject_or_raise(subject_id):
    subject = db.session.get(Subject, subject_id)
    if not subject:
        raise ValueError(f"Subject with ID {subject_id} does not exist.")
    return subject


def _fetch_and_validate(model, ids, max_allowed, label):
    ids = list(set(ids))  # dedupe

    if len(ids) > max_allowed:
        raise ValueError(
            f"Too many {label} IDs in one request ({len(ids)}). "
            f"Max is {max_allowed} — split into smaller batches."
        )

    # Modern SQLAlchemy 2.0 query style
    stmt = db.select(model).where(model.id.in_(ids))
    records = db.session.scalars(stmt).all()

    found_ids = {r.id for r in records}
    missing_ids = set(ids) - found_ids
    if missing_ids:
        raise ValueError(f"{label.capitalize()} IDs not found: {sorted(missing_ids)}")

    return records


def _assign_subject_to(model, subject_id, record_ids, max_allowed, label):
    subject = _get_subject_or_raise(subject_id)
    records = _fetch_and_validate(model, record_ids, max_allowed, label)

    for record in records:
        if subject in record.subjects:
            raise ValueError(f"{label.capitalize()} with ID {record.id} is already assigned to this subject.")
        record.subjects.append(subject)

    db.session.commit()


def _remove_subject_from(model, subject_id, record_ids, max_allowed, label):
    subject = _get_subject_or_raise(subject_id)
    records = _fetch_and_validate(model, record_ids, max_allowed, label)

    for record in records:
        if subject in record.subjects:
            record.subjects.remove(subject)

    db.session.commit()


def _get_subjects_for(model, record_id, label):
    record = db.session.get(model, record_id)
    if not record:
        raise ValueError(f"{label.capitalize()} with ID {record_id} does not exist.")
    return record.subjects


# ================================ Teacher assignment ==================================
def assign_subject_to_teachers(subject_id, teacher_ids):
    _assign_subject_to(Teacher, subject_id, teacher_ids, MAX_TEACHERS_PER_ASSIGNMENT, "teacher")

def remove_subject_from_teachers(subject_id, teacher_ids):
    _remove_subject_from(Teacher, subject_id, teacher_ids, MAX_TEACHERS_PER_ASSIGNMENT, "teacher")

def get_subjects_for_teacher(teacher_id):
    return _get_subjects_for(Teacher, teacher_id, "teacher")


# ================================ Student assignment ==================================
def assign_subject_to_students(subject_id, student_ids):
    _assign_subject_to(Student, subject_id, student_ids, MAX_STUDENTS_PER_ASSIGNMENT, "student")

def remove_subject_from_students(subject_id, student_ids):
    _remove_subject_from(Student, subject_id, student_ids, MAX_STUDENTS_PER_ASSIGNMENT, "student")

def get_subjects_for_student(student_id):
    return _get_subjects_for(Student, student_id, "student")


# ================================ Classroom assignment ==================================
def assign_subject_to_classrooms(subject_id, classroom_ids):
    _assign_subject_to(Classroom, subject_id, classroom_ids, MAX_CLASSROOMS_PER_ASSIGNMENT, "classroom")

def remove_subject_from_classrooms(subject_id, classroom_ids):
    _remove_subject_from(Classroom, subject_id, classroom_ids, MAX_CLASSROOMS_PER_ASSIGNMENT, "classroom")

def get_subjects_for_classroom(classroom_id):
    return _get_subjects_for(Classroom, classroom_id, "classroom")