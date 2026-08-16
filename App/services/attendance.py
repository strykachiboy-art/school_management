from flask import abort
from sqlalchemy.exc import IntegrityError

from App.extensions import db
from App.models.attendance import Attendance
from App.models.student import Student


# ============================ Create attendance ============================

def create_term(data):
    """
    Creates a new Term attached to an Academic Session.
    """
    create_attendance = Attendance(
        student_id=data.student_id,
        term_id=data.term_id,
        date=data.date,
        status=data.status
    )
    
    try:
        db.session.add(create_attendance)
        db.session.commit()
    except IntegrityError:
        db.session.rollback()
        abort(400, description="Could not create attendance — check for duplicate name or missing required fields.")
    
    return create_attendance


# ============================ Mark attendance ============================

def mark_classroom_attendance(classroom_id, term_id, date, attendance_data):
    
    try:
        students = Student.query.filter_by(
            classroom_id = classroom_id
        ).all()
        
        student_ids = {students.id for student in students}
        
        for record in attendance_data:
            student_ids = record["student_id"]
            status = record["status"]
            
        attendance = Attendance.query.filter_by(
            student_id = student_ids,
            date = date
        ).first()
        
        if attendance:
            attendance.term_id = term_id
            attendance.status = status
            
        else:
            attendance = Attendance(
                student_id = student_ids,
                term_id = term_id,
                date = date,
                status = status
            )
            
            db.session.add(attendance)
            
            db.session.commit()
            
            return True
        
    except Exception:
        db.session.rollback()
        raise
    
    