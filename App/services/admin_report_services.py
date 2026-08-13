from App.models.student import Student
from App.models.teacher import Teacher
from App.models.subject import Subject
from App.models.classroom import Classroom

from flask import Flask

from flask import abort
from sqlalchemy.exc import IntegrityError

from App.extensions import db

def get_admin_report():
    # Get the total number of students
    total_students = db.session.execute(db.select(db.func.count()).select_from("student")).scalar()

    # Get the total number of teachers
    total_teachers = db.session.execute(db.select(db.func.count()).select_from("teacher")).scalar()

    # Get the total number of subjects
    total_subjects = db.session.execute(db.select(db.func.count()).select_from("subject")).scalar()

    # Get the total number of classrooms
    total_classrooms = db.session.execute(db.select(db.func.count()).select_from("classroom")).scalar()

    return {
        "total_students": total_students,
        "total_teachers": total_teachers,
        "total_subjects": total_subjects,
        "total_classrooms": total_classrooms
    }