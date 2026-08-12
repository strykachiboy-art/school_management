# test/test_teacher.py

def test_create_teacher_success(client, admin_headers):
    payload = {
        "username": "new_teacher",
        "full_name": "Jane Doe",
        "email": "jane.doe@example.com",
        "phone": "1234567890",
        "subject": "Chemistry",
        "password": "securepass123",  # required in practice despite Optional() — see bug note above
    }
    response = client.post("/teachers/create", data=payload, headers=admin_headers)
    assert response.status_code == 201
    data = response.get_json()
    assert data["full_name"] == "Jane Doe"


def test_create_teacher_duplicate_username(client, admin_headers, teacher):
    """teacher fixture already created a user with username 'teacher_1'."""
    payload = {
        "username": "teacher_1",
        "full_name": "Duplicate",
        "email": "unique_email@example.com",
        "password": "securepass123",
    }
    response = client.post("/teachers/create", data=payload, headers=admin_headers)
    # IntegrityError -> abort(400, description=...) -> caught by central handler
    assert response.status_code == 400


def test_get_teacher_success(client, admin_headers, teacher):
    response = client.get(f"/teachers/{teacher.id}", headers=admin_headers)
    assert response.status_code == 200
    assert response.get_json()["id"] == teacher.id


def test_get_teacher_not_found(client, admin_headers):
    response = client.get("/teachers/99999", headers=admin_headers)
    assert response.status_code == 404


def test_get_all_teachers(client, admin_headers, teacher):
    response = client.get("/teachers", headers=admin_headers)
    assert response.status_code == 200
    data = response.get_json()
    assert any(t["id"] == teacher.id for t in data)


def test_delete_teacher_success(client, admin_headers, teacher):
    response = client.delete(f"/teachers/{teacher.id}", headers=admin_headers)
    assert response.status_code == 200
    assert response.get_json()["message"] == "Teacher deleted successfully"


def test_delete_teacher_not_found(client, admin_headers):
    response = client.delete("/teachers/99999", headers=admin_headers)
    assert response.status_code == 404