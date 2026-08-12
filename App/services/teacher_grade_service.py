# from flask import abort
from App.extensions import db
from App.models.student import Student
from App.models.result import Result
from App.services.grade_service import calculate_student_grade

def get_student_grade_for_teachers(student_id, teacher_id):
    student = db.session.get(Student, student_id)
    
    if student is None:
        raise ValueError("student not found")
    
    if student.classroom is None:
        raise ValueError("Student is not assigned to classroom")
    
    if student.classroom.teacher_id != teacher_id:
        raise ValueError("you are not allowed to view this student grade")
    
    results = Result.query.filter_by(student_id=student_id).all()
    
    return calculate_student_grade(results)