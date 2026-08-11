import pytest


# ============================== GET single exam ==============================

def test_get_exam_success(client, admin_headers, exam):
    response = client.get(f"/exams/{exam.id}", headers=admin_headers)
    assert response.status_code == 200

    data = response.get_json()
    assert data["id"] == exam.id
    assert data["title"] == "Midterm Exam"
    assert data["total_marks"] == 100


def test_get_exam_not_found(client, admin_headers):
    response = client.get("/exams/99999", headers=admin_headers)
    assert response.status_code == 404
    assert response.get_json()["error"] == "Exam not found"


# ============================== GET all exams ==============================

def test_get_all_exams(client, admin_headers, exam):
    response = client.get("/exams/", headers=admin_headers)
    assert response.status_code == 200

    data = response.get_json()
    assert isinstance(data, list)
    assert any(e["id"] == exam.id for e in data)


def test_get_all_exams_empty(client, admin_headers):
    response = client.get("/exams/", headers=admin_headers)
    assert response.status_code == 200
    assert response.get_json() == []


# ============================== CREATE exam ==============================

def test_create_exam_success(client, admin_headers, subject, classroom):
    payload = {
        "title": "Final Exam",
        "description": "Comprehensive final",
        "subject_id": subject.id,
        "classroom_id": classroom.id,
        "exam_date": "2026-12-15",
        "start_time": "10:00:00",
        "duration_minutes": 120,
        "total_marks": 100,
    }
    response = client.post("/exams/create", json=payload, headers=admin_headers)
    assert response.status_code == 201

    data = response.get_json()
    assert data["title"] == "Final Exam"
    assert data["subject_id"] == subject.id
    assert data["classroom_id"] == classroom.id


def test_create_exam_missing_required_field(client, admin_headers, subject, classroom):
    """total_marks is required=True in ExamSchema; omitting it should 400."""
    payload = {
        "title": "Incomplete Exam",
        "subject_id": subject.id,
        "classroom_id": classroom.id,
        "exam_date": "2026-12-15",
        "start_time": "10:00:00",
    }
    response = client.post("/exams/create", json=payload, headers=admin_headers)
    assert response.status_code == 400

    data = response.get_json()
    assert data["error"] == "Validation failed"
    assert "total_marks" in data["messages"]


def test_create_exam_invalid_date_format(client, admin_headers, subject, classroom):
    payload = {
        "title": "Bad Date Exam",
        "subject_id": subject.id,
        "classroom_id": classroom.id,
        "exam_date": "not-a-date",
        "start_time": "10:00:00",
        "total_marks": 100,
    }
    response = client.post("/exams/create", json=payload, headers=admin_headers)
    assert response.status_code == 400
    assert response.get_json()["error"] == "Validation failed"


# ============================== DELETE exam ==============================

def test_delete_exam_success(client, admin_headers, exam):
    response = client.delete(f"/exams/{exam.id}", headers=admin_headers)
    assert response.status_code == 200
    assert response.get_json()["message"] == "Exam deleted successfully"

    # confirm it's actually gone
    follow_up = client.get(f"/exams/{exam.id}", headers=admin_headers)
    assert follow_up.status_code == 404


def test_delete_exam_not_found(client, admin_headers):
    response = client.delete("/exams/99999", headers=admin_headers)
    assert response.status_code == 404
    assert response.get_json()["error"] == "Exam not found"


# ============================== Auth guard ==============================

def test_get_exam_requires_auth(client, exam):
    """No Authorization header at all should not return exam data."""
    response = client.get(f"/exams/{exam.id}")
    assert response.status_code in (401, 403)