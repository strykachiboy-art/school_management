from flask import abort

from App.extensions import db
from App.models.student import Student
from App.models.classroom import Classroom
from App.models.academic_session import AcademicSession
from App.models.exam import Exam
from App.models.result import Result
from App.models.attendance import Attendance
from App.models.term import Term
from App.models.promotion_history import PromotionHistory
from App.enums.promotion import PromotionDecision
from App.enums.attendance import AttendanceStatus

# Minimum thresholds for a "promote" recommendation.
# Adjust these to match the school's actual policy.
PASS_AVERAGE_THRESHOLD = 50.0
MIN_ATTENDANCE_THRESHOLD = 75.0


def _calculate_average_score(student_id, academic_session_id):
    stmt = (
        db.select(Result.marks_obtained)
        .join(Exam, Result.exam_id == Exam.id)
        .where(Result.student_id == student_id, Exam.session_id == academic_session_id)
    )
    marks = db.session.scalars(stmt).all()

    if not marks:
        return 0.0

    return round(sum(marks) / len(marks), 2)


def _calculate_attendance_percentage(student_id, academic_session_id):
    stmt = (
        db.select(Attendance.status)
        .join(Term, Attendance.term_id == Term.id)
        .where(Attendance.student_id == student_id, Term.academic_session_id == academic_session_id)
    )
    statuses = db.session.scalars(stmt).all()

    if not statuses:
        return 0.0

    excused_count = sum(1 for s in statuses if s == AttendanceStatus.EXCUSED)
    effective_total = len(statuses) - excused_count

    if effective_total <= 0:
        return 0.0

    present_equivalent = sum(
        1 for s in statuses if s in (AttendanceStatus.PRESENT, AttendanceStatus.LATE)
    )

    return round((present_equivalent / effective_total) * 100, 2)


def evaluate_student_promotion(student_id, academic_session_id):
    student = db.session.get(Student, student_id)
    if student is None:
        return None

    session = db.session.get(AcademicSession, academic_session_id)
    if session is None:
        return None

    average_score = _calculate_average_score(student_id, academic_session_id)
    attendance_percentage = _calculate_attendance_percentage(student_id, academic_session_id)

    passed = (
        average_score >= PASS_AVERAGE_THRESHOLD
        and attendance_percentage >= MIN_ATTENDANCE_THRESHOLD
    )

    if not passed:
        recommendation = PromotionDecision.REPEATED
    else:
        current_classroom = (
            db.session.get(Classroom, student.classroom_id) if student.classroom_id else None
        )
        if current_classroom is not None and current_classroom.is_final_level:
            recommendation = PromotionDecision.GRADUATED
        else:
            recommendation = PromotionDecision.PROMOTED

    return {
        "student_id": student_id,
        "academic_session_id": academic_session_id,
        "average_score": average_score,
        "attendance_percentage": attendance_percentage,
        "recommendation": recommendation,
    }


def promote_student(student_id, academic_session_id, to_classroom_id, remarks=None, decided_by=None, decided_by_role=None):
    student = db.session.get(Student, student_id)
    if student is None:
        return None

    to_classroom = db.session.get(Classroom, to_classroom_id)
    if to_classroom is None:
        abort(400, description="Target classroom not found")

    evaluation = evaluate_student_promotion(student_id, academic_session_id)

    # A student who didn't meet the promotion criteria can only be promoted
    # anyway if a teacher makes that call — admins can't override this alone.
    if evaluation and evaluation["recommendation"] == PromotionDecision.REPEATED:
        if decided_by_role != "teacher":
            abort(
                403,
                description=(
                    "This student did not meet the promotion criteria — "
                    "only a teacher can decide to promote them anyway."
                ),
            )

    from_classroom_id = student.classroom_id

    student.classroom_id = to_classroom_id

    history = PromotionHistory(
        student_id=student_id,
        academic_session_id=academic_session_id,
        from_classroom_id=from_classroom_id,
        to_classroom_id=to_classroom_id,
        decision=PromotionDecision.PROMOTED,
        average_score=evaluation["average_score"] if evaluation else None,
        attendance_percentage=evaluation["attendance_percentage"] if evaluation else None,
        remarks=remarks,
        decided_by=decided_by,
    )

    db.session.add(history)
    db.session.commit()

    return history


def repeat_student(student_id, academic_session_id, remarks=None, decided_by=None):
    student = db.session.get(Student, student_id)
    if student is None:
        return None

    evaluation = evaluate_student_promotion(student_id, academic_session_id)

    history = PromotionHistory(
        student_id=student_id,
        academic_session_id=academic_session_id,
        from_classroom_id=student.classroom_id,
        to_classroom_id=student.classroom_id,
        decision=PromotionDecision.REPEATED,
        average_score=evaluation["average_score"] if evaluation else None,
        attendance_percentage=evaluation["attendance_percentage"] if evaluation else None,
        remarks=remarks,
        decided_by=decided_by,
    )

    db.session.add(history)
    db.session.commit()

    return history


def graduate_student(student_id, academic_session_id, remarks=None, decided_by=None):
    student = db.session.get(Student, student_id)
    if student is None:
        return None

    evaluation = evaluate_student_promotion(student_id, academic_session_id)
    from_classroom_id = student.classroom_id

    student.classroom_id = None

    history = PromotionHistory(
        student_id=student_id,
        academic_session_id=academic_session_id,
        from_classroom_id=from_classroom_id,
        to_classroom_id=None,
        decision=PromotionDecision.GRADUATED,
        average_score=evaluation["average_score"] if evaluation else None,
        attendance_percentage=evaluation["attendance_percentage"] if evaluation else None,
        remarks=remarks,
        decided_by=decided_by,
    )

    db.session.add(history)
    db.session.commit()

    return history


def get_student_promotion_history(student_id):
    student = db.session.get(Student, student_id)
    if student is None:
        return None

    stmt = (
        db.select(PromotionHistory)
        .where(PromotionHistory.student_id == student_id)
        .order_by(PromotionHistory.created_at.asc())
    )
    return db.session.scalars(stmt).all()


def get_session_promotions(academic_session_id):
    session = db.session.get(AcademicSession, academic_session_id)
    if session is None:
        return None

    stmt = (
        db.select(PromotionHistory)
        .where(PromotionHistory.academic_session_id == academic_session_id)
        .order_by(PromotionHistory.created_at.asc())
    )
    return db.session.scalars(stmt).all()