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