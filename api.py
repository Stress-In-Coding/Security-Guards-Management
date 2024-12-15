# Importing necessary libraries from Flask and other modules
from flask import Flask, make_response, jsonify, request, render_template  # Flask and its components
from flask_mysqldb import MySQL  # Flask extension for MySQL database integration
from flask_jwt_extended import JWTManager, jwt_required, get_jwt_identity, create_access_token  # Flask extension for JWT handling
from datetime import datetime, timedelta, timezone  # Datetime utilities for handling time-related operations
from functools import wraps  # Utilities for creating decorators
from unittest.mock import patch  # For mocking parts of your code in tests
import pytest  # Testing framework
import json  # JSON encoding and decoding
from werkzeug.security import generate_password_hash, check_password_hash  # For password hashing

# Initialize the Flask application
app = Flask(__name__)

# Configuring the MySQL database connection
app.config["MYSQL_HOST"] = "localhost"  # MySQL server host
app.config["MYSQL_USER"] = "root"  # MySQL username
app.config["MYSQL_PASSWORD"] = "root"  # MySQL password
app.config["MYSQL_DB"] = "security_guards_db"  # MySQL database name
app.config["MYSQL_CURSORCLASS"] = "DictCursor"  # Use dictionary cursor for better readability
app.config["SECRET_KEY"] = "your_secret_key"  # Secret key for JWT encoding

# Initialize JWTManager with the Flask app
jwt = JWTManager(app)

# Initialize MySQL with Flask app
mysql = MySQL(app)

# Custom error handler for 404 Not Found error
@app.errorhandler(404)
def not_found(error):
    # Respond with a JSON error message and 404 status code
    return make_response(jsonify({"error": "Not found"}), 404)

# Custom error handler for 400 Bad Request error
@app.errorhandler(400)
def bad_request(error):
    # Respond with a JSON error message and 400 status code
    return make_response(jsonify({"error": "Bad request"}), 400)

# JWT Authentication Decorator
# This ensures that the request has a valid JWT token
def token_required(f):
    @wraps(f)
    @jwt_required()  # Use flask_jwt_extended's jwt_required decorator
    def decorated(*args, **kwargs):
        # Get the identity of the current user
        current_user = get_jwt_identity()
        request.user = current_user  # Attach user data to the request
        return f(*args, **kwargs)
    return decorated

# Role-based Access Control Decorator
# This ensures that the user has the required role to access the endpoint
def role_required(role):
    def decorator(f):
        @wraps(f)
        def decorated(*args, **kwargs):
            # Check if user has the required role
            if not hasattr(request, "user") or request.user.get("role") != role:
                return make_response(jsonify({"error": "Access forbidden"}), 403)
            return f(*args, **kwargs)
        return decorated
    return decorator

# Route to handle user login and JWT generation
@app.route("/login", methods=["POST"])
def login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    if not username or not password:
        return jsonify({"error": "Username and password required"}), 400

    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM users WHERE username = %s", (username,))
    user = cur.fetchone()
    cur.close()

    if user and check_password_hash(user['password_hash'], password):
        # Use the username as the identity
        token = create_access_token(identity=username)
        return jsonify({"token": token}), 200

    return jsonify({"error": "Invalid credentials"}), 401
