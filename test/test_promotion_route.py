from datetime import date
from App.extensions import db as _db
from App.models.classroom import Classroom
from App.models.attendance import Attendance
from App.enums.attendance import AttendanceStatus


def _mark_present(app, student, term, count, start_day=1):
    with app.app_context():
        for i in range(count):
            att = Attendance(
                student_id=student.id,
                term_id=term.id,
                date=date(2026, 9, start_day + i),
                status=AttendanceStatus.PRESENT,
            )
            _db.session.add(att)
        _db.session.commit()


# ====================================== evaluate route ===============================================

def test_evaluate_promotion_route_success(client, admin_headers, student, academic_session, exam, make_result, term, app):
    make_result(student_obj=student, exam_obj=exam, marks=80)
    _mark_present(app, student, term, 10)

    response = client.get(
        f"/promotions/students/{student.id}/sessions/{academic_session.id}/evaluate",
        headers=admin_headers,
    )
    assert response.status_code == 200
    data = response.get_json()
    assert data["recommendation"] == "promoted"
    assert data["average_score"] == 80.0


def test_evaluate_promotion_route_not_found(client, admin_headers, academic_session):
    response = client.get(
        f"/promotions/students/99999/sessions/{academic_session.id}/evaluate",
        headers=admin_headers,
    )
    assert response.status_code == 404


def test_evaluate_promotion_route_forbidden_for_student(client, student_headers, student, academic_session):
    response = client.get(
        f"/promotions/students/{student.id}/sessions/{academic_session.id}/evaluate",
        headers=student_headers,
    )
    assert response.status_code == 403


# ====================================== promote route ===============================================

def test_promote_student_route_success(client, admin_headers, student, academic_session, exam, make_result, term, app):
    from datetime import date
    from App.extensions import db as _db2
    from App.models.attendance import Attendance
    from App.enums.attendance import AttendanceStatus

    make_result(student_obj=student, exam_obj=exam, marks=85)
    with app.app_context():
        for i in range(10):
            _db2.session.add(Attendance(
                student_id=student.id, term_id=term.id,
                date=date(2026, 9, 1 + i), status=AttendanceStatus.PRESENT,
            ))
        _db2.session.commit()

        new_classroom = Classroom(name="Room Promote", capacity=30)
        _db2.session.add(new_classroom)
        _db2.session.commit()
        new_classroom_id = new_classroom.id

    response = client.post(
        f"/promotions/students/{student.id}/sessions/{academic_session.id}/promote",
        json={"to_classroom_id": new_classroom_id, "remarks": "Great year"},
        headers=admin_headers,
    )
    assert response.status_code == 201
    data = response.get_json()
    assert data["decision"] == "promoted"
    assert data["to_classroom_id"] == new_classroom_id
    assert data["remarks"] == "Great year"


def test_promote_student_route_invalid_classroom(client, admin_headers, student, academic_session):
    response = client.post(
        f"/promotions/students/{student.id}/sessions/{academic_session.id}/promote",
        json={"to_classroom_id": 99999},
        headers=admin_headers,
    )
    assert response.status_code == 400


def test_promote_student_route_allowed_for_teacher(client, teacher_headers, student, academic_session, classroom):
    response = client.post(
        f"/promotions/students/{student.id}/sessions/{academic_session.id}/promote",
        json={"to_classroom_id": classroom.id},
        headers=teacher_headers,
    )
    assert response.status_code == 201


def test_admin_cannot_promote_failing_student(client, admin_headers, student, academic_session, exam, make_result, classroom):
    # Low mark → fails the promotion threshold, no attendance recorded either.
    make_result(student_obj=student, exam_obj=exam, marks=10)

    response = client.post(
        f"/promotions/students/{student.id}/sessions/{academic_session.id}/promote",
        json={"to_classroom_id": classroom.id},
        headers=admin_headers,
    )
    assert response.status_code == 403


def test_teacher_can_override_and_promote_failing_student(client, teacher_headers, student, academic_session, exam, make_result, classroom):
    make_result(student_obj=student, exam_obj=exam, marks=10)

    response = client.post(
        f"/promotions/students/{student.id}/sessions/{academic_session.id}/promote",
        json={"to_classroom_id": classroom.id, "remarks": "Teacher override"},
        headers=teacher_headers,
    )
    assert response.status_code == 201
    data = response.get_json()
    assert data["decision"] == "promoted"
    assert data["remarks"] == "Teacher override"


# ====================================== repeat route ===============================================

def test_repeat_student_route_success(client, admin_headers, student, academic_session):
    response = client.post(
        f"/promotions/students/{student.id}/sessions/{academic_session.id}/repeat",
        json={"remarks": "Needs improvement"},
        headers=admin_headers,
    )
    assert response.status_code == 201
    data = response.get_json()
    assert data["decision"] == "repeated"


def test_repeat_student_route_not_found(client, admin_headers, academic_session):
    response = client.post(
        f"/promotions/students/99999/sessions/{academic_session.id}/repeat",
        json={},
        headers=admin_headers,
    )
    assert response.status_code == 404


# ====================================== graduate route ===============================================

def test_graduate_student_route_success(client, admin_headers, student, academic_session):
    response = client.post(
        f"/promotions/students/{student.id}/sessions/{academic_session.id}/graduate",
        json={"remarks": "Well done"},
        headers=admin_headers,
    )
    assert response.status_code == 201
    data = response.get_json()
    assert data["decision"] == "graduated"
    assert data["to_classroom_id"] is None


# ====================================== history routes ===============================================

def test_student_promotion_history_route_admin_can_view(client, admin_headers, student, academic_session):
    client.post(
        f"/promotions/students/{student.id}/sessions/{academic_session.id}/repeat",
        json={"remarks": "First"},
        headers=admin_headers,
    )

    response = client.get(f"/promotions/students/{student.id}/history", headers=admin_headers)
    assert response.status_code == 200
    data = response.get_json()
    assert len(data) == 1
    assert data[0]["remarks"] == "First"


def test_student_promotion_history_route_student_can_view_own(client, admin_headers, student_headers, student, academic_session):
    client.post(
        f"/promotions/students/{student.id}/sessions/{academic_session.id}/repeat",
        json={},
        headers=admin_headers,
    )

    response = client.get(f"/promotions/students/{student.id}/history", headers=student_headers)
    assert response.status_code == 200


def test_student_promotion_history_route_student_cannot_view_others(client, student_headers, student2, academic_session):
    response = client.get(f"/promotions/students/{student2.id}/history", headers=student_headers)
    assert response.status_code == 403


def test_session_promotions_route_admin_only(client, admin_headers, teacher_headers, student, student2, academic_session, classroom):
    client.post(
        f"/promotions/students/{student.id}/sessions/{academic_session.id}/promote",
        json={"to_classroom_id": classroom.id},
        headers=teacher_headers,
    )
    client.post(
        f"/promotions/students/{student2.id}/sessions/{academic_session.id}/repeat",
        json={},
        headers=admin_headers,
    )

    response = client.get(f"/promotions/sessions/{academic_session.id}", headers=admin_headers)
    assert response.status_code == 200
    assert len(response.get_json()) == 2


def test_session_promotions_route_forbidden_for_student(client, student_headers, academic_session):
    response = client.get(f"/promotions/sessions/{academic_session.id}", headers=student_headers)
    assert response.status_code == 403