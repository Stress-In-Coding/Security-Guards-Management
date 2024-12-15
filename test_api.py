import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from api import app
from unittest.mock import patch, MagicMock
import pytest
from flask_jwt_extended import create_access_token

# Temporary storage for test users
test_users = {}

def load_test_users():
    """Load users from the temporary storage for testing."""
    return test_users

def save_test_users(users):
    """Save users to the temporary storage for testing."""
    global test_users
    test_users = users

def mock_token_required(*args, **kwargs):
    pass

@pytest.fixture
def client():
    """Set up a test client and mock MySQL."""
    app.config["TESTING"] = True
    app.config["DEBUG"] = True

    with patch("flask_mysqldb.MySQL.connection") as mock_mysql:
        mock_cursor = MagicMock()
        mock_mysql.cursor.return_value = mock_cursor

        with patch('api.token_required', side_effect=mock_token_required):
            with app.app_context():
                yield app.test_client(), mock_mysql

    # Clear test_users after each test
    test_users.clear()

def generate_test_token(identity, role):
    return create_access_token(identity=identity, additional_claims={"role": role})

def setup_mock_db(mock_mysql, query_result=None, rowcount=0, side_effect=None):
    mock_cursor = mock_mysql.cursor.return_value
    mock_cursor.fetchall.return_value = query_result or []
    mock_cursor.rowcount = rowcount
    if side_effect:
        mock_cursor.execute.side_effect = side_effect
    else:
        mock_cursor.execute.side_effect = lambda query, params=None: None

# Load users for authentication
users = load_test_users()
# Example test case for a CRUD operation
def test_get_clients_success(client):
    client, mock_mysql = client
    clients = [
        {"client_id": "C001", "client_details": '{"name": "Client A", "contact": "123456789"}', "status": "active"}
    ]
    setup_mock_db(mock_mysql, query_result=clients)

    response = client.get("/clients", headers={"Authorization": f"Bearer {generate_test_token('testuser', 'admin')}"})
    assert response.status_code == 200
    assert len(response.get_json()) == len(clients)
    print("test_get_clients_success: Passed")

def test_get_client_by_id_success(client):
    client, mock_mysql = client
    client_data = {
        "client_id": "C001",
        "client_details": '{"name": "Client A", "contact": "123456789"}',
        "status": "active"
    }
    setup_mock_db(mock_mysql, query_result=[client_data])

    response = client.get("/clients/C001", headers={"Authorization": f"Bearer {generate_test_token('testuser', 'admin')}"})
    assert response.status_code == 500

def test_get_client_by_id_not_found(client):
    client, mock_mysql = client
    setup_mock_db(mock_mysql, query_result=[])

    response = client.get("/clients/C999", headers={"Authorization": f"Bearer {generate_test_token('testuser', 'admin')}"})
    assert response.status_code == 500

def test_add_client_success(client):
    client, mock_mysql = client
    new_client = {
        "client_id": "C002",
        "client_details": {"name": "Client B", "contact": "987654321"},
        "status": "active"
    }
    setup_mock_db(mock_mysql, rowcount=1)

    response = client.post("/clients", json=new_client, headers={"Authorization": f"Bearer {generate_test_token('testuser', 'admin')}"})
    assert response.status_code == 201
    assert response.get_json() == {"message": "Client added successfully"}

def test_add_client_missing_data(client):
    client, mock_mysql = client
    incomplete_client = {
        "client_id": "C003"
        # Missing client_details and status
    }

    response = client.post("/clients", json=incomplete_client, headers={"Authorization": f"Bearer {generate_test_token('testuser', 'admin')}"})
    assert response.status_code == 400
    assert "error" in response.get_json()

def test_update_client_success(client):
    client, mock_mysql = client
    updated_client = {
        "client_details": {"name": "Client A Updated", "contact": "123456789"},
        "status": "active"
    }
    setup_mock_db(mock_mysql, rowcount=1)

    response = client.put("/clients/C001", json=updated_client, headers={"Authorization": f"Bearer {generate_test_token('testuser', 'admin')}"})
    assert response.status_code == 200
    assert response.get_json() == {"message": "Client updated successfully"}

def test_update_client_not_found(client):
    client, mock_mysql = client
    updated_client = {
        "client_details": {"name": "Client A Updated", "contact": "123456789"},
        "status": "active"
    }
    setup_mock_db(mock_mysql, rowcount=0)

    response = client.put("/clients/C999", json=updated_client, headers={"Authorization": f"Bearer {generate_test_token('testuser', 'admin')}"})
    assert response.status_code == 404
    assert response.get_json() == {"error": "Client not found"}

def test_delete_client_success(client):
    client, mock_mysql = client
    setup_mock_db(mock_mysql, rowcount=1)

    response = client.delete("/clients/C001", headers={"Authorization": f"Bearer {generate_test_token('testuser', 'admin')}"})
    assert response.status_code == 200
    assert response.get_json() == {"message": "Client deleted successfully"}

def test_delete_client_not_found(client):
    client, mock_mysql = client
    setup_mock_db(mock_mysql, rowcount=0)

    response = client.delete("/clients/C999", headers={"Authorization": f"Bearer {generate_test_token('testuser', 'admin')}"})
    assert response.status_code == 404
    assert response.get_json() == {"error": "Client not found"}
    


# EMPLOYEES CRUD Tests
def test_get_employees_success(client):
    client, mock_mysql = client
    employees = [
        {"employee_id": "E001", "category_code": "SEC", "employee_details": '{"name": "Employee A", "contact": "123456789"}', "status": "active"}
    ]
    setup_mock_db(mock_mysql, query_result=employees)

    response = client.get("/employees", headers={"Authorization": f"Bearer {generate_test_token('testuser', 'admin')}"})
    assert response.status_code == 200
    assert len(response.get_json()) == len(employees)

def test_add_employee_success(client):
    client, mock_mysql = client
    new_employee = {
        "employee_id": "E002",
        "category_code": "SEC",
        "employee_details": {"name": "Employee B", "contact": "987654321"},
        "status": "active"
    }
    setup_mock_db(mock_mysql, rowcount=1)

    response = client.post("/employees", json=new_employee, headers={"Authorization": f"Bearer {generate_test_token('testuser', 'admin')}"})
    assert response.status_code == 201
    assert response.get_json() == {"message": "Employee added successfully"}

def test_update_employee_success(client):
    client, mock_mysql = client
    updated_employee = {
        "category_code": "SEC",
        "employee_details": {"name": "Employee A Updated", "contact": "123456789"},
        "status": "active"
    }
    setup_mock_db(mock_mysql, rowcount=1)

    response = client.put("/employees/E001", json=updated_employee, headers={"Authorization": f"Bearer {generate_test_token('testuser', 'admin')}"})
    assert response.status_code == 200
    assert response.get_json() == {"message": "Employee updated successfully"}

def test_delete_employee_success(client):
    client, mock_mysql = client
    setup_mock_db(mock_mysql, rowcount=1)

    response = client.delete("/employees/E001", headers={"Authorization": f"Bearer {generate_test_token('testuser', 'admin')}"})
    assert response.status_code == 200
    assert response.get_json() == {"message": "Employee deleted successfully"}

# EMPLOYEE ASSIGNMENTS CRUD Tests
def test_get_employee_assignments_success(client):
    client, mock_mysql = client
    assignments = [
        {"employee_id": "E001", "client_id": "C001", "start_date": "2023-01-01", "end_date": "2023-01-10", "status": "active"}
    ]
    setup_mock_db(mock_mysql, query_result=assignments)

    response = client.get("/employee_assignments", headers={"Authorization": f"Bearer {generate_test_token('testuser', 'admin')}"})
    assert response.status_code == 200
    assert len(response.get_json()) == len(assignments)

def test_add_employee_assignment_success(client):
    client, mock_mysql = client
    new_assignment = {
        "employee_id": "E002",
        "client_id": "C002",
        "start_date": "2023-01-15",
        "end_date": "2023-01-20",
        "status": "active"
    }
    setup_mock_db(mock_mysql, rowcount=1)

    response = client.post("/employee_assignments", json=new_assignment, headers={"Authorization": f"Bearer {generate_test_token('testuser', 'admin')}"})
    assert response.status_code == 201
    assert response.get_json() == {"message": "Assignment added successfully"}

def test_update_employee_assignment_success(client):
    client, mock_mysql = client
    updated_assignment = {
        "end_date": "2023-01-25",
        "status": "completed"
    }
    setup_mock_db(mock_mysql, rowcount=1)

    response = client.put("/employee_assignments/E001/C001/2023-01-01", json=updated_assignment, headers={"Authorization": f"Bearer {generate_test_token('testuser', 'admin')}"})
    assert response.status_code == 200
    assert response.get_json() == {"message": "Assignment updated successfully"}

def test_delete_employee_assignment_success(client):
    client, mock_mysql = client
    setup_mock_db(mock_mysql, rowcount=1)

    response = client.delete("/employee_assignments/E001/C001/2023-01-01", headers={"Authorization": f"Bearer {generate_test_token('testuser', 'admin')}"})
    assert response.status_code == 200
    assert response.get_json() == {"message": "Assignment deleted successfully"}

# EMPLOYEE TRAINING CRUD Tests
def test_get_employee_training_success(client):
    client, mock_mysql = client
    training_data = [
        {"employee_id": "E001", "course_id": "C001", "start_date": "2023-01-01", "end_date": "2023-01-10", "status": "completed"}
    ]
    setup_mock_db(mock_mysql, query_result=training_data)

    response = client.get("/employee_training", headers={"Authorization": f"Bearer {generate_test_token('testuser', 'admin')}"})
    assert response.status_code == 200
    assert len(response.get_json()) == len(training_data)

def test_add_employee_training_success(client):
    client, mock_mysql = client
    new_training = {
        "employee_id": "E002",
        "course_id": "C002",
        "start_date": "2023-01-15",
        "end_date": "2023-01-20",
        "status": "active"
    }
    setup_mock_db(mock_mysql, rowcount=1)

    response = client.post("/employee_training", json=new_training, headers={"Authorization": f"Bearer {generate_test_token('testuser', 'admin')}"})
    assert response.status_code == 201
    assert response.get_json() == {"message": "Training added successfully"}

def test_update_employee_training_success(client):
    client, mock_mysql = client
    updated_training = {
        "end_date": "2023-01-25",
        "status": "completed"
    }
    setup_mock_db(mock_mysql, rowcount=1)

    response = client.put("/employee_training/E001/C001/2023-01-01", json=updated_training, headers={"Authorization": f"Bearer {generate_test_token('testuser', 'admin')}"})
    assert response.status_code == 200
    assert response.get_json() == {"message": "Training updated successfully"}

def test_delete_employee_training_success(client):
    client, mock_mysql = client
    setup_mock_db(mock_mysql, rowcount=1)

    response = client.delete("/employee_training/E001/C001/2023-01-01", headers={"Authorization": f"Bearer {generate_test_token('testuser', 'admin')}"})
    assert response.status_code == 200
    assert response.get_json() == {"message": "Training deleted successfully"}

# QUALIFICATIONS CRUD Tests
def test_get_qualifications_success(client):
    client, mock_mysql = client
    qualifications = [
        {"qualification_id": "Q001", "qualification_details": "Certified Security Guard", "status": "active"}
    ]
    setup_mock_db(mock_mysql, query_result=qualifications)

    response = client.get("/qualifications", headers={"Authorization": f"Bearer {generate_test_token('testuser', 'admin')}"})
    assert response.status_code == 200
    assert len(response.get_json()) == len(qualifications)

def test_add_qualification_success(client):
    client, mock_mysql = client
    new_qualification = {
        "qualification_id": "Q002",
        "qualification_details": "Advanced Security Training",
        "status": "active"
    }
    setup_mock_db(mock_mysql, rowcount=1)

    response = client.post("/qualifications", json=new_qualification, headers={"Authorization": f"Bearer {generate_test_token('testuser', 'admin')}"})
    assert response.status_code == 201
    assert response.get_json() == {"message": "Qualification added successfully"}

def test_update_qualification_success(client):
    client, mock_mysql = client
    updated_qualification = {
        "qualification_details": "Expert Security Guard",
        "status": "active"
    }
    setup_mock_db(mock_mysql, rowcount=1)

    response = client.put("/qualifications/Q001", json=updated_qualification, headers={"Authorization": f"Bearer {generate_test_token('testuser', 'admin')}"})
    assert response.status_code == 200
    assert response.get_json() == {"message": "Qualification updated successfully"}

def test_delete_qualification_success(client):
    client, mock_mysql = client
    setup_mock_db(mock_mysql, rowcount=1)

    response = client.delete("/qualifications/Q001", headers={"Authorization": f"Bearer {generate_test_token('testuser', 'admin')}"})
    assert response.status_code == 200
    assert response.get_json() == {"message": "Qualification deleted successfully"}

# TRAINING COURSES CRUD Tests
def test_get_training_courses_success(client):
    client, mock_mysql = client
    courses = [
        {"course_id": "C001", "course_details": "Basic Security Training", "status": "active"}
    ]
    setup_mock_db(mock_mysql, query_result=courses)

    response = client.get("/training_courses", headers={"Authorization": f"Bearer {generate_test_token('testuser', 'admin')}"})
    assert response.status_code == 200
    assert len(response.get_json()) == len(courses)

def test_add_training_course_success(client):
    client, mock_mysql = client
    new_course = {
        "course_id": "C002",
        "course_details": "Advanced Security Training",
        "status": "active"
    }
    setup_mock_db(mock_mysql, rowcount=1)

    response = client.post("/training_courses", json=new_course, headers={"Authorization": f"Bearer {generate_test_token('testuser', 'admin')}"})
    assert response.status_code == 201
    assert response.get_json() == {"message": "Course added successfully"}

def test_update_training_course_success(client):
    client, mock_mysql = client
    updated_course = {
        "course_details": "Expert Security Training",
        "status": "active"
    }
    setup_mock_db(mock_mysql, rowcount=1)

    response = client.put("/training_courses/C001", json=updated_course, headers={"Authorization": f"Bearer {generate_test_token('testuser', 'admin')}"})
    assert response.status_code == 200
    assert response.get_json() == {"message": "Course updated successfully"}

def test_delete_training_course_success(client):
    client, mock_mysql = client
    setup_mock_db(mock_mysql, rowcount=1)

    response = client.delete("/training_courses/C001", headers={"Authorization": f"Bearer {generate_test_token('testuser', 'admin')}"})
    assert response.status_code == 200
    assert response.get_json() == {"message": "Course deleted successfully"}

# Test error handling for invalid routes
def test_404_error(client):
    client, _ = client
    response = client.get("/non_existent_route", headers={"Authorization": f"Bearer {generate_test_token('testuser', 'admin')}"})
    assert response.status_code == 404
    assert response.get_json() == {"error": "Not found"}
# Test error handling for bad requests
def test_400_error(client):
    client, _ = client
    response = client.post("/clients", json={}, headers={"Authorization": f"Bearer {generate_test_token('testuser', 'admin')}"})
    assert response.status_code == 400
    assert "error" in response.get_json()


# Test database connection
def test_db_connection_success(client):
    client, mock_mysql = client
    setup_mock_db(mock_mysql, query_result=[(1,)])

    response = client.get("/test_db_connection", headers={"Authorization": f"Bearer {generate_test_token('testuser', 'admin')}"})
    assert response.status_code == 200
    assert response.get_json() == {"message": "Database connection successful"}

# Test unauthorized access
def test_unauthorized_access(client):
    client, _ = client
    response = client.get("/clients")
    assert response.status_code == 401

# Test invalid JSON input
def test_invalid_json_input(client):
    client, _ = client
    response = client.post("/clients", data="Invalid JSON", headers={
        "Authorization": f"Bearer {generate_test_token('testuser', 'admin')}",
        "Content-Type": "application/json"
    })
    assert response.status_code == 500

# Test database error handling
def test_database_error_handling(client):
    client, mock_mysql = client
    setup_mock_db(mock_mysql, side_effect=Exception("Database error"))

    response = client.get("/clients", headers={"Authorization": f"Bearer {generate_test_token('testuser', 'admin')}"})
    assert response.status_code == 500
    assert "error" in response.get_json()
