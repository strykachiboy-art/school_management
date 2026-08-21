from App.extensions import db
from App.models.student import Student
from App.models.result import Result
from App.models.exam import Exam
from App.services.grade_service import calculate_student_grade


def get_student_own_grade(student_id, term_id=None):
    student = db.session.get(Student, student_id)

    if student is None:
        raise ValueError("Student not found")

    query = Result.query.filter_by(student_id=student_id)

    if term_id is not None:
        query = query.join(Result.exam).filter(Exam.term_id == term_id)

    results = query.all()

    if not results:
        raise ValueError("No results found for this student")

    grade = calculate_student_grade(results)

    return {
        "average": grade["average"],
        "grade": grade["grade"],
        "remark": grade["remark"]
    }