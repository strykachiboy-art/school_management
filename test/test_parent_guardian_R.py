# from unittest.mock import patch
# from App.enums.role import Role

# # ==========================================
# # Parent Guardian Route Tests
# # ==========================================

# @patch("App.routes.admin.parent_guardian.create_parent_guardian")
# def test_create_guardian_success(mock_create, client, admin_headers):
#     """Test successful creation of a parent/guardian (POST /parent-guardians)."""
#     mock_guardian = type('MockGuardian', (), {
#         "id": 1,
#         "user_id": 10,
#         "occupation": "Engineer",
#         "email": "test@example.com",
#         "phone": "123456789",
#         "address": "123 Street"
#     })()
#     mock_create.return_value = mock_guardian

#     payload = {
#         "user_id": 10,
#         "occupation": "Engineer",
#         "email": "test@example.com",
#         "phone": "123456789",
#         "address": "123 Street"
#     }

#     # Pass admin_headers here
#     response = client.post("/parent-guardians", json=payload, headers=admin_headers)
    
#     assert response.status_code == 201
#     data = response.get_json()
#     assert data["message"] == "Parent/Guardian created successfully"
#     assert data["id"] == 1
#     assert data["occupation"] == "Engineer"


# @patch("App.routes.admin.parent_guardian.get_all_parent_guardians")
# def test_list_guardians_success(mock_get_all, client, admin_headers):
#     """Test retrieving all parent/guardians (GET /parent-guardians)."""
#     mock_guardian = type('MockGuardian', (), {
#         "id": 1,
#         "user_id": 10,
#         "occupation": "Engineer",
#         "email": "test@example.com",
#         "phone": "123456789",
#         "address": "123 Street"
#     })()
#     mock_get_all.return_value = [mock_guardian]

#     response = client.get("/parent-guardians", headers=admin_headers)
    
#     assert response.status_code == 200
#     data = response.get_json()
#     assert isinstance(data, list)
#     assert len(data) == 1
#     assert data[0]["id"] == 1


# @patch("App.routes.admin.parent_guardian.get_parent_guardian")
# def test_get_guardian_by_id_found(mock_get, client, admin_headers):
#     """Test getting a single parent/guardian by ID when found (GET /parent-guardians/<id>)."""
#     mock_guardian = type('MockGuardian', (), {
#         "id": 1,
#         "user_id": 10,
#         "occupation": "Engineer",
#         "email": "test@example.com",
#         "phone": "123456789",
#         "address": "123 Street"
#     })()
#     mock_get.return_value = mock_guardian

#     response = client.get("/parent-guardians/1", headers=admin_headers)
    
#     assert response.status_code == 200
#     data = response.get_json()
#     assert data["id"] == 1


# @patch("App.routes.admin.parent_guardian.get_parent_guardian")
# def test_get_guardian_by_id_not_found(mock_get, client, admin_headers):
#     """Test getting a single parent/guardian by ID when missing (404)."""
#     mock_get.return_value = None

#     response = client.get("/parent-guardians/999", headers=admin_headers)
    
#     assert response.status_code == 404
#     assert response.get_json()["error"] == "Parent/Guardian not found"


# @patch("App.routes.admin.parent_guardian.update_parent_guardian")
# def test_update_guardian_success(mock_update, client, admin_headers):
#     """Test updating a parent/guardian (PUT/PATCH /parent-guardians/<id>)."""
#     mock_update.return_value = True

#     payload = {"occupation": "Senior Engineer"}
#     response = client.patch("/parent-guardians/1", json=payload, headers=admin_headers)
    
#     assert response.status_code == 200
#     assert response.get_json()["message"] == "Parent/Guardian updated successfully"


# @patch("App.routes.admin.parent_guardian.delete_parent_guardian")
# def test_delete_guardian_success(mock_delete, client, admin_headers):
#     """Test deleting a parent/guardian (DELETE /parent-guardians/<id>)."""
#     mock_delete.return_value = True

#     response = client.delete("/parent-guardians/1", headers=admin_headers)
    
#     assert response.status_code == 200
#     assert response.get_json()["message"] == "Parent/Guardian deleted successfully"


# # ==========================================
# # Student Assignment Route Tests
# # ==========================================

# @patch("App.routes.admin.parent_guardian.assign_student_to_guardian")
# def test_assign_student_success(mock_assign, client, admin_headers):
#     """Test assigning a student to a guardian (POST /parent-guardians/students)."""
#     mock_assignment = type('MockAssignment', (), {
#         "id": 1,
#         "parent_guardian_id": 1,
#         "student_id": 5,
#         "relationship": type('MockEnum', (), {"value": "FATHER"})()
#     })()
#     mock_assign.return_value = mock_assignment

#     payload = {
#         "parent_guardian_id": 1,
#         "student_id": 5,
#         "relationship": "FATHER"
#     }

#     response = client.post("/parent-guardians/students", json=payload, headers=admin_headers)
    
#     assert response.status_code == 201
#     data = response.get_json()
#     assert data["message"] == "Student assigned to guardian successfully"
#     assert data["relationship"] == "FATHER"


# @patch("App.routes.admin.parent_guardian.remove_student_from_guardian")
# def test_remove_student_assignment_success(mock_remove, client, admin_headers):
#     """Test removing a student link (DELETE /parent-guardians/students/assignments/<id>)."""
#     mock_remove.return_value = True

#     response = client.delete("/parent-guardians/students/assignments/1", headers=admin_headers)
    
#     assert response.status_code == 200
#     assert response.get_json()["message"] == "Student unlinked from guardian successfully"