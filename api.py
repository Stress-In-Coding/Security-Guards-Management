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
