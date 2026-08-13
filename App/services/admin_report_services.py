from sqlalchemy import select, func

from App.extensions import db
from App.models.student import Student
from App.models.teacher import Teacher
from App.models.subject import Subject
from App.models.classroom import Classroom


def get_admin_report():
    total_students = db.session.scalar(select(func.count()).select_from(Student))
    total_teachers = db.session.scalar(select(func.count()).select_from(Teacher))
    total_subjects = db.session.scalar(select(func.count()).select_from(Subject))
    total_classrooms = db.session.scalar(select(func.count()).select_from(Classroom))

    return {
        "total_students": total_students,
        "total_teachers": total_teachers,
        "total_subjects": total_subjects,
        "total_classrooms": total_classrooms,
    }