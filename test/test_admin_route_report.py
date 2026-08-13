from App.extensions import db
from App.models.student import Student
from App.models.teacher import Teacher
from App.models.subject import Subject
from App.models.classroom import Classroom


def test_get_admin_report_counts(client, admin_headers, teacher, student, subject, classroom):
    response = client.get("/admin/report", headers=admin_headers)
    assert response.status_code == 200

    data = response.get_json()
    assert data["total_students"] == 1
    assert data["total_teachers"] == 1
    assert data["total_subjects"] == 1
    assert data["total_classrooms"] == 1


def test_get_admin_report_empty(client, admin_headers):
    """No teacher/student/subject/classroom fixtures used -> all counts should be 0."""
    response = client.get("/admin/report", headers=admin_headers)
    assert response.status_code == 200

    data = response.get_json()
    assert data["total_students"] == 0
    assert data["total_teachers"] == 0
    assert data["total_subjects"] == 0
    assert data["total_classrooms"] == 0


def test_get_admin_report_requires_admin_role(client, teacher_headers):
    """A teacher token should not satisfy @role_required("admin")."""
    response = client.get("/admin/report", headers=teacher_headers)
    assert response.status_code == 403


def test_get_admin_report_requires_auth(client):
    response = client.get("/admin/report")
    assert response.status_code in (401, 403)