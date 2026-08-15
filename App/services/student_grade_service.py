from App.extensions import db
from App.models.student import Student
from App.models.result import Result
from App.services.grade_service import calculate_student_grade


def get_student_own_grade(student_id):
    student = db.session.get(Student, student_id)

    if student is None:
        raise ValueError("Student not found")

    results = Result.query.filter_by(student_id=student_id).all()

    if not results:
        raise ValueError("No results found for this student")

    grade = calculate_student_grade(results)

    return {
        "average": grade["average"],
        "grade": grade["grade"],
        "remark": grade["remark"]
    }