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
