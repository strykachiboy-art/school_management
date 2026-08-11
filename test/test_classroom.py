from App.models.classroom import Classroom


def test_create_classroom_success(client, admin_headers):
    payload = {"name": "Room 101", "capacity": "25", "location": "Building A"}
    response = client.post("/classrooms/create", data=payload, headers=admin_headers)
    assert response.status_code == 201
    data = response.get_json()
    assert data["name"] == "Room 101"
    assert data["capacity"] == 25


def test_create_classroom_missing_required_field(client, admin_headers, app):
    """name is DataRequired; form.validate() fails and falls through to
    render_template with a 200 HTML response — NOT a JSON 400. This
    documents current behavior; see note above about fixing this."""
    from App.extensions import db

    with app.app_context():
        before_count = db.session.query(Classroom).count()

    payload = {"capacity": "25"}  # missing name
    response = client.post("/classrooms/create", data=payload, headers=admin_headers)
    assert response.status_code == 200
    assert "application/json" not in response.content_type

    with app.app_context():
        after_count = db.session.query(Classroom).count()
    assert after_count == before_count  # nothing was created


def test_get_classroom_detail_success(client, admin_headers, classroom):
    response = client.get(f"/classrooms/{classroom.id}", headers=admin_headers)
    assert response.status_code == 200
    assert response.get_json()["id"] == classroom.id


def test_get_classroom_detail_not_found(client, admin_headers):
    response = client.get("/classrooms/99999", headers=admin_headers)
    assert response.status_code == 404


def test_get_all_classrooms_list(client, admin_headers, classroom):
    response = client.get("/classrooms?list=true", headers=admin_headers)
    assert response.status_code == 200
    data = response.get_json()
    assert any(c["id"] == classroom.id for c in data)


def test_delete_classroom_success(client, admin_headers, classroom):
    response = client.delete(f"/classrooms/{classroom.id}", headers=admin_headers)
    assert response.status_code == 200
    assert response.get_json()["message"] == "Classroom deleted successfully"

    follow_up = client.get(f"/classrooms/{classroom.id}", headers=admin_headers)
    assert follow_up.status_code == 404


def test_delete_classroom_not_found(client, admin_headers):
    response = client.delete("/classrooms/99999", headers=admin_headers)
    assert response.status_code == 404