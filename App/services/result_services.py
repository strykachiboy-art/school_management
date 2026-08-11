from flask import abort, request
from App.models.result import Result
from App.models.student import Student
from App.models.exam import Exam
from App.models.result import Result
from sqlalchemy import or_
from sqlalchemy.exc import IntegrityError

from App.extensions import db


# ========================== Create Result ============================
def create_result(student_id, exam_id, marks_obtained):
    student = db.session.get(Student, student_id)
    
    if student is None:
        abort(404, description = "Student not found")
        
    exam = db.session.get(Exam, exam_id)
    
    if exam is None:
        abort(404, description = "Exam not found")
    
    result = Result(
        student_id=student_id,
        exam_id = exam_id,
        marks_obtained = marks_obtained
    )
    
    db.session.add(result)
    db.session.commit
    
    return result


#================================ Get Result ==================================
def get_result(result_id):
    return db.session.get(Result, result_id)



#=============================== Get all Result ===============================
def get_all_result():
    return db.session.execute(
        db.select(Result)
    ).scalars().all()
    
    
    
#============================== Update Result ====================================
def update_result(result_id, mark_obtained):
    result = db.session.get(Result, result_id)
    
    if result is None:
        abort(404, description = "Result does not exist")
    
    result.marks_obtained = mark_obtained
    
    db.session.commit()
    
    return result



# ============================= Delete result =====================================
def delete_result(result_id):
    result = db.session.get(Result, result_id)
    
    if result is None:
       abort(404, description = "Result does not exist")
       
    db.session.delete(result)
    db.session.commit()
    
    return result



#=========================== Search_result =====================================
def search_results(student_id = None, exam_id= None):
    statement = db.select(Result)
    
    if student_id is not None:
        statement = statement.where(
            Result.student_id == student_id
        )
    
    if exam_id is not None:
        statement = statement.where(
            Result.exam_id == exam_id
        )
    
    return db.session.execute(statement).scalars().all()



# =========================== Paginate_Result ===================================
def paginate_result(page = 1, per_page = 10):
    statement = db.select(Result)
    
    return db.paginate(statement,
                       page=page,
                       per_page=per_page,
                       error_out=False)
    
    