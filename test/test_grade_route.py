import pytest
from flask import url_for


def test_get_student_grade_returns_computed_grade(client, admin_headers, student, result):
    with client.application.test_request_context():
        url = url_for("admin.get_student_grade", student_id=student.id)

    response = client.get(url, headers=admin_headers)

    assert response.status_code == 200
    data = response.get_json()

    assert data["total"] == result.marks_obtained
    assert data["average"] == result.marks_obtained
    assert data["grade"] in {"A", "B", "C", "D", "E", "F"}
    assert data["remark"] != "unknown"


def test_get_student_grade_no_results_returns_fail(client, admin_headers, student):
    
    with client.application.test_request_context():
        url = url_for("admin.get_student_grade", student_id=student.id)

    response = client.get(url, headers=admin_headers)

    assert response.status_code == 200
    data = response.get_json()

    assert data["total"] == 0
    assert data["average"] == 0
    assert data["grade"] == "F"
    assert data["remark"] == "Fail"


def test_get_student_grade_requires_auth(client, student):
    with client.application.test_request_context():
        url = url_for("admin.get_student_grade", student_id=student.id)

    response = client.get(url, headers={"Accept": "application/json"})

    assert response.status_code in (401, 403)