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
# CLIENTS CRUD
# Route to get all clients (requires JWT token)
@app.route("/clients", methods=["GET"])
@token_required
 # Apply token_required decorator to secure the endpoint
def get_clients():
    try:
        cur = mysql.connection.cursor()
        # Query to get all clients
        cur.execute("SELECT * FROM clients")
        clients_data = cur.fetchall()
        for client in clients_data:
            # Parse client details from JSON string to dictionary
            client['client_details'] = json.loads(client['client_details'])
        cur.close()
        return jsonify(clients_data), 200  # Return clients data as JSON
    except Exception as e:
        # If any error occurs, respond with error message
        return jsonify({"error": str(e)}), 500

# Route to get a specific client by ID (requires JWT token)
@app.route("/clients/<string:client_id>", methods=["GET"])
def get_client_by_id(client_id):
    try:
        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM clients WHERE client_id = %s", (client_id,))
        data = cur.fetchone()
        cur.close()
        if not data:
            return make_response(jsonify({"error": "Client not found"}), 404)
        return make_response(jsonify(data), 200)
    except Exception as e:
        print(f"Error fetching client by ID: {e}")  # Log the error
        return make_response(jsonify({"error": "Internal server error"}), 500)

# Route to add a new client (requires JWT token)
@app.route("/clients", methods=["POST"])

def add_client():
    try:
        data = request.get_json()
        if not data or 'client_id' not in data or 'client_details' not in data:
            return make_response(jsonify({"error": "Missing required fields"}), 400)

        client_id = data['client_id']
        client_details = json.dumps(data['client_details'])
        status = data.get('status', 'active')

        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO clients (client_id, client_details, status) VALUES (%s, %s, %s)", (client_id, client_details, status))
        mysql.connection.commit()
        cur.close()
        return jsonify({"message": "Client added successfully"}), 201
    except Exception as e:
        print(f"Error adding client: {e}")  # Log the error
        return jsonify({"error": "Internal server error"}), 500

# Route to update an existing client (requires JWT token)
@app.route("/clients/<string:client_id>", methods=["PUT"])
def update_client(client_id):
    try:
        info = request.get_json()  # Get JSON data from request
        cur = mysql.connection.cursor()
        # Update client details in the database
        cur.execute(
            """UPDATE clients SET client_details = %s, status = %s 
            WHERE client_id = %s""",
            (info["client_details"], info["status"], client_id)
        )
        mysql.connection.commit()
        if cur.rowcount == 0:
            # If no rows were updated, the client was not found
            return make_response(jsonify({"error": "Client not found"}), 404)
        cur.close()
        return make_response(jsonify({"message": "Client updated successfully"}), 200)
    except Exception as e:
        return make_response(jsonify({"error": str(e)}), 500)

# Route to delete a client (requires JWT token)
@app.route("/clients/<string:client_id>", methods=["DELETE"])
def delete_client(client_id):
    try:
        cur = mysql.connection.cursor()
        # Delete client from the database
        cur.execute("DELETE FROM clients WHERE client_id = %s", (client_id,))
        mysql.connection.commit()
        if cur.rowcount == 0:
            # If no rows were deleted, the client was not found
            return make_response(jsonify({"error": "Client not found"}), 404)
        cur.close()
        return make_response(jsonify({"message": "Client deleted successfully"}), 200)
    except Exception as e:
        return make_response(jsonify({"error": str(e)}), 500)

# EMPLOYEES CRUD
# Route to get all employees (requires JWT token)
@app.route("/employees", methods=["GET"])
def get_employees():
    try:
        cur = mysql.connection.cursor()
        # Query to get all employees
        cur.execute("SELECT * FROM employees")
        data = cur.fetchall()
        cur.close()
        return make_response(jsonify(data), 200)
    except Exception as e:
        return make_response(jsonify({"error": str(e)}), 500)

# Route to get a specific employee by ID (requires JWT token)
@app.route("/employees/<string:employee_id>", methods=["GET"])
def get_employee_by_id(employee_id):
    try:
        cur = mysql.connection.cursor()
        # Query to get employee by ID
        cur.execute("SELECT * FROM employees WHERE employee_id = %s", (employee_id,))
        data = cur.fetchone()
        cur.close()
        if not data:
            # If employee not found, respond with error message
            return make_response(jsonify({"error": "Employee not found"}), 404)
        return make_response(jsonify(data), 200)
    except Exception as e:
        return make_response(jsonify({"error": str(e)}), 500)

# Route to add a new employee (requires JWT token)
@app.route("/employees", methods=["POST"])
def add_employee():
    try:
        info = request.get_json()  # Get JSON data from request
        cur = mysql.connection.cursor()
        # Insert new employee into the database
        cur.execute(
            """INSERT INTO employees (employee_id, category_code, employee_details, status) 
            VALUES (%s, %s, %s, %s)""",
            (info["employee_id"], info["category_code"], info["employee_details"], info["status"])
        )
        mysql.connection.commit()
        cur.close()
        return make_response(jsonify({"message": "Employee added successfully"}), 201)
    except Exception as e:
        return make_response(jsonify({"error": str(e)}), 500)

# Route to update an existing employee (requires JWT token)
@app.route("/employees/<string:employee_id>", methods=["PUT"])
def update_employee(employee_id):
    try:
        info = request.get_json()  # Get JSON data from request
        cur = mysql.connection.cursor()
        # Update employee details in the database
        cur.execute(
            """UPDATE employees SET category_code = %s, employee_details = %s, status = %s 
            WHERE employee_id = %s""",
            (info["category_code"], info["employee_details"], info["status"], employee_id)
        )
        mysql.connection.commit()
        if cur.rowcount == 0:
            # If no rows were updated, the employee was not found
            return make_response(jsonify({"error": "Employee not found"}), 404)
        cur.close()
        return make_response(jsonify({"message": "Employee updated successfully"}), 200)
    except Exception as e:
        return make_response(jsonify({"error": str(e)}), 500)

# Route to delete an employee (requires JWT token)
@app.route("/employees/<string:employee_id>", methods=["DELETE"])
def delete_employee(employee_id):
    try:
        cur = mysql.connection.cursor()
        # Delete employee from the database
        cur.execute("DELETE FROM employees WHERE employee_id = %s", (employee_id,))
        mysql.connection.commit()
        if cur.rowcount == 0:
            # If no rows were deleted, the employee was not found
            return make_response(jsonify({"error": "Employee not found"}), 404)
        cur.close()
        return make_response(jsonify({"message": "Employee deleted successfully"}), 200)
    except Exception as e:
        return make_response(jsonify({"error": str(e)}), 500)

# EMPLOYEE ASSIGNMENTS CRUD
# Route to get all employee assignments (requires JWT token)
@app.route("/employee_assignments", methods=["GET"])
def get_employee_assignments():
    try:
        cur = mysql.connection.cursor()
        # Query to get all employee assignments
        cur.execute("SELECT * FROM employee_assignments")
        data = cur.fetchall()
        cur.close()
        return make_response(jsonify(data), 200)
    except Exception as e:
        return make_response(jsonify({"error": str(e)}), 500)

# Route to get a specific employee assignment by ID (requires JWT token)
@app.route("/employee_assignments/<string:employee_id>/<string:client_id>/<string:start_date>", methods=["GET"])
def get_employee_assignment_by_id(employee_id, client_id, start_date):
    try:
        cur = mysql.connection.cursor()
        # Query to get employee assignment by ID
        cur.execute("SELECT * FROM employee_assignments WHERE employee_id = %s AND client_id = %s AND start_date = %s", (employee_id, client_id, start_date))
        data = cur.fetchone()
        cur.close()
        if not data:
            # If assignment not found, respond with error message
            return make_response(jsonify({"error": "Assignment not found"}), 404)
        return make_response(jsonify(data), 200)
    except Exception as e:
        return make_response(jsonify({"error": str(e)}), 500)

# Route to add a new employee assignment (requires JWT token)
@app.route("/employee_assignments", methods=["POST"])
def add_employee_assignment():
    try:
        info = request.get_json()  # Get JSON data from request
        cur = mysql.connection.cursor()
        # Insert new employee assignment into the database
        cur.execute(
            """INSERT INTO employee_assignments (employee_id, client_id, start_date, end_date, status) 
            VALUES (%s, %s, %s, %s, %s)""",
            (info["employee_id"], info["client_id"], info["start_date"], info["end_date"], info["status"])
        )
        mysql.connection.commit()
        cur.close()
        return make_response(jsonify({"message": "Assignment added successfully"}), 201)
    except Exception as e:
        return make_response(jsonify({"error": str(e)}), 500)

# Route to update an existing employee assignment (requires JWT token)
@app.route("/employee_assignments/<string:employee_id>/<string:client_id>/<string:start_date>", methods=["PUT"])
def update_employee_assignment(employee_id, client_id, start_date):
    try:
        info = request.get_json()  # Get JSON data from request
        cur = mysql.connection.cursor()
        # Update employee assignment details in the database
        cur.execute(
            """UPDATE employee_assignments SET end_date = %s, status = %s 
            WHERE employee_id = %s AND client_id = %s AND start_date = %s""",
            (info["end_date"], info["status"], employee_id, client_id, start_date)
        )
        mysql.connection.commit()
        if cur.rowcount == 0:
            # If no rows were updated, the assignment was not found
            return make_response(jsonify({"error": "Assignment not found"}), 404)
        cur.close()
        return make_response(jsonify({"message": "Assignment updated successfully"}), 200)
    except Exception as e:
        return make_response(jsonify({"error": str(e)}), 500)

# Route to delete an employee assignment (requires JWT token)
@app.route("/employee_assignments/<string:employee_id>/<string:client_id>/<string:start_date>", methods=["DELETE"])
def delete_employee_assignment(employee_id, client_id, start_date):
    try:
        cur = mysql.connection.cursor()
        # Delete employee assignment from the database
        cur.execute("DELETE FROM employee_assignments WHERE employee_id = %s AND client_id = %s AND start_date = %s", (employee_id, client_id, start_date))
        mysql.connection.commit()
        if cur.rowcount == 0:
            # If no rows were deleted, the assignment was not found
            return make_response(jsonify({"error": "Assignment not found"}), 404)
        cur.close()
        return make_response(jsonify({"message": "Assignment deleted successfully"}), 200)
    except Exception as e:
        return make_response(jsonify({"error": str(e)}), 500)

# EMPLOYEE TRAINING CRUD
# Route to get all employee training records (requires JWT token)
@app.route("/employee_training", methods=["GET"])
def get_employee_training():
    try:
        cur = mysql.connection.cursor()
        # Query to get all employee training records
        cur.execute("SELECT * FROM employee_training")
        data = cur.fetchall()
        cur.close()
        return make_response(jsonify(data), 200)
    except Exception as e:
        return make_response(jsonify({"error": str(e)}), 500)

# Route to get a specific employee training record by ID (requires JWT token)
@app.route("/employee_training/<string:employee_id>/<string:course_id>/<string:start_date>", methods=["GET"])
def get_employee_training_by_id(employee_id, course_id, start_date):
    try:
        cur = mysql.connection.cursor()
        # Query to get employee training record by ID
        cur.execute("SELECT * FROM employee_training WHERE employee_id = %s AND course_id = %s AND start_date = %s", (employee_id, course_id, start_date))
        data = cur.fetchone()
        cur.close()
        if not data:
            # If training record not found, respond with error message
            return make_response(jsonify({"error": "Training not found"}), 404)
        return make_response(jsonify(data), 200)
    except Exception as e:
        return make_response(jsonify({"error": str(e)}), 500)

# Route to add a new employee training record (requires JWT token)
@app.route("/employee_training", methods=["POST"])
def add_employee_training():
    try:
        info = request.get_json()  # Get JSON data from request
        cur = mysql.connection.cursor()
        # Insert new employee training record into the database
        cur.execute(
            """INSERT INTO employee_training (employee_id, course_id, start_date, end_date, status) 
            VALUES (%s, %s, %s, %s, %s)""",
            (info["employee_id"], info["course_id"], info["start_date"], info["end_date"], info["status"])
        )
        mysql.connection.commit()
        cur.close()
        return make_response(jsonify({"message": "Training added successfully"}), 201)
    except Exception as e:
        return make_response(jsonify({"error": str(e)}), 500)

# Route to update an existing employee training record (requires JWT token)
@app.route("/employee_training/<string:employee_id>/<string:course_id>/<string:start_date>", methods=["PUT"])
def update_employee_training(employee_id, course_id, start_date):
    try:
        info = request.get_json()  # Get JSON data from request
        cur = mysql.connection.cursor()
        # Update employee training record details in the database
        cur.execute(
            """UPDATE employee_training SET end_date = %s, status = %s 
            WHERE employee_id = %s AND course_id = %s AND start_date = %s""",
            (info["end_date"], info["status"], employee_id, course_id, start_date)
        )
        mysql.connection.commit()
        if cur.rowcount == 0:
            # If no rows were updated, the training record was not found
            return make_response(jsonify({"error": "Training not found"}), 404)
        cur.close()
        return make_response(jsonify({"message": "Training updated successfully"}), 200)
    except Exception as e:
        return make_response(jsonify({"error": str(e)}), 500)

# Route to delete an employee training record (requires JWT token)
@app.route("/employee_training/<string:employee_id>/<string:course_id>/<string:start_date>", methods=["DELETE"])
def delete_employee_training(employee_id, course_id, start_date):
    try:
        cur = mysql.connection.cursor()
        # Delete employee training record from the database
        cur.execute("DELETE FROM employee_training WHERE employee_id = %s AND course_id = %s AND start_date = %s", (employee_id, course_id, start_date))
        mysql.connection.commit()
        if cur.rowcount == 0:
            # If no rows were deleted, the training record was not found
            return make_response(jsonify({"error": "Training not found"}), 404)
        cur.close()
        return make_response(jsonify({"message": "Training deleted successfully"}), 200)
    except Exception as e:
        return make_response(jsonify({"error": str(e)}), 500)

# QUALIFICATIONS CRUD
# Route to get all qualifications (requires JWT token)
@app.route("/qualifications", methods=["GET"])
def get_qualifications():
    try:
        cur = mysql.connection.cursor()
        # Query to get all qualifications
        cur.execute("SELECT * FROM qualifications")
        data = cur.fetchall()
        cur.close()
        return make_response(jsonify(data), 200)
    except Exception as e:
        return make_response(jsonify({"error": str(e)}), 500)

# Route to get a specific qualification by ID (requires JWT token)
@app.route("/qualifications/<string:qualification_id>", methods=["GET"])
def get_qualification_by_id(qualification_id):
    try:
        cur = mysql.connection.cursor()
        # Query to get qualification by ID
        cur.execute("SELECT * FROM qualifications WHERE qualification_id = %s", (qualification_id,))
        data = cur.fetchone()
        cur.close()
        if not data:
            # If qualification not found, respond with error message
            return make_response(jsonify({"error": "Qualification not found"}), 404)
        return make_response(jsonify(data), 200)
    except Exception as e:
        return make_response(jsonify({"error": str(e)}), 500)

# Route to add a new qualification (requires JWT token)
@app.route("/qualifications", methods=["POST"])
def add_qualification():
    try:
        info = request.get_json()  # Get JSON data from request
        cur = mysql.connection.cursor()
        # Insert new qualification into the database
        cur.execute(
            """INSERT INTO qualifications (qualification_id, qualification_details, status) 
            VALUES (%s, %s, %s)""",
            (info["qualification_id"], info["qualification_details"], info["status"])
        )
        mysql.connection.commit()
        cur.close()
        return make_response(jsonify({"message": "Qualification added successfully"}), 201)
    except Exception as e:
        return make_response(jsonify({"error": str(e)}), 500)

# Route to update an existing qualification (requires JWT token)
@app.route("/qualifications/<string:qualification_id>", methods=["PUT"])
def update_qualification(qualification_id):
    try:
        info = request.get_json()  # Get JSON data from request
        cur = mysql.connection.cursor()
        # Update qualification details in the database
        cur.execute(
            """UPDATE qualifications SET qualification_details = %s, status = %s 
            WHERE qualification_id = %s""",
            (info["qualification_details"], info["status"], qualification_id)
        )
        mysql.connection.commit()
        if cur.rowcount == 0:
            # If no rows were updated, the qualification was not found
            return make_response(jsonify({"error": "Qualification not found"}), 404)
        cur.close()
        return make_response(jsonify({"message": "Qualification updated successfully"}), 200)
    except Exception as e:
        return make_response(jsonify({"error": str(e)}), 500)

# Route to delete a qualification (requires JWT token)
@app.route("/qualifications/<string:qualification_id>", methods=["DELETE"])
def delete_qualification(qualification_id):
    try:
        cur = mysql.connection.cursor()
        # Delete qualification from the database
        cur.execute("DELETE FROM qualifications WHERE qualification_id = %s", (qualification_id,))
        mysql.connection.commit()
        if cur.rowcount == 0:
            # If no rows were deleted, the qualification was not found
            return make_response(jsonify({"error": "Qualification not found"}), 404)
        cur.close()
        return make_response(jsonify({"message": "Qualification deleted successfully"}), 200)
    except Exception as e:
        return make_response(jsonify({"error": str(e)}), 500)

# TRAINING COURSES CRUD
# Route to get all training courses (requires JWT token)
@app.route("/training_courses", methods=["GET"])
def get_training_courses():
    try:
        cur = mysql.connection.cursor()
        # Query to get all training courses
        cur.execute("SELECT * FROM training_courses")
        data = cur.fetchall()
        cur.close()
        return make_response(jsonify(data), 200)
    except Exception as e:
        return make_response(jsonify({"error": str(e)}), 500)

# Route to get a specific training course by ID (requires JWT token)
@app.route("/training_courses/<string:course_id>", methods=["GET"])
def get_training_course_by_id(course_id):
    try:
        cur = mysql.connection.cursor()
        # Query to get training course by ID
        cur.execute("SELECT * FROM training_courses WHERE course_id = %s", (course_id,))
        data = cur.fetchone()
        cur.close()
        if not data:
            # If course not found, respond with error message
            return make_response(jsonify({"error": "Course not found"}), 404)
        return make_response(jsonify(data), 200)
    except Exception as e:
        return make_response(jsonify({"error": str(e)}), 500)

# Route to add a new training course (requires JWT token)
@app.route("/training_courses", methods=["POST"])
def add_training_course():
    try:
        info = request.get_json()  # Get JSON data from request
        cur = mysql.connection.cursor()
        # Insert new training course into the database
        cur.execute(
            """INSERT INTO training_courses (course_id, course_details, status) 
            VALUES (%s, %s, %s)""",
            (info["course_id"], info["course_details"], info["status"])
        )
        mysql.connection.commit()
        cur.close()
        return make_response(jsonify({"message": "Course added successfully"}), 201)
    except Exception as e:
        return make_response(jsonify({"error": str(e)}), 500)

# Route to update an existing training course (requires JWT token)
@app.route("/training_courses/<string:course_id>", methods=["PUT"])
def update_training_course(course_id):
    try:
        info = request.get_json()  # Get JSON data from request
        cur = mysql.connection.cursor()
        # Update training course details in the database
        cur.execute(
            """UPDATE training_courses SET course_details = %s, status = %s 
            WHERE course_id = %s""",
            (info["course_details"], info["status"], course_id)
        )
        mysql.connection.commit()
        if cur.rowcount == 0:
            # If no rows were updated, the course was not found
            return make_response(jsonify({"error": "Course not found"}), 404)
        cur.close()
        return make_response(jsonify({"message": "Course updated successfully"}), 200)
    except Exception as e:
        return make_response(jsonify({"error": str(e)}), 500)

# Route to delete a training course (requires JWT token)
@app.route("/training_courses/<string:course_id>", methods=["DELETE"])
def delete_training_course(course_id):
    try:
        cur = mysql.connection.cursor()
        # Delete training course from the database
        cur.execute("DELETE FROM training_courses WHERE course_id = %s", (course_id,))
        mysql.connection.commit()
        if cur.rowcount == 0:
            # If no rows were deleted, the course was not found
            return make_response(jsonify({"error": "Course not found"}), 404)
        cur.close()
        return make_response(jsonify({"message": "Course deleted successfully"}), 200)
    except Exception as e:
        return make_response(jsonify({"error": str(e)}), 500)


# Route to test database connection
@app.route("/test_db_connection", methods=["GET"])
def test_db_connection():
    try:
        cur = mysql.connection.cursor()
        # Simple query to test database connection
        cur.execute("SELECT 1")
        cur.close()
        return jsonify({"message": "Database connection successful"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Mocking for testing purposes
@patch('api.token_required', lambda f: f)  # Mock the token_required decorator
@patch('api.mysql.connection.cursor')  # Mock the database cursor
def test_get_clients(mock_cursor, client):
    # Mock data to be returned by the database
    mock_cursor.return_value.fetchall.return_value = [
        {"client_id": "C001", "client_details": '{"name": "Client A", "contact": "123456789"}', "status": "active"}
    ]
    # Simulate a GET request to the /clients endpoint
    response = client.get("/clients", headers={"Authorization": "Bearer test_token"})
    assert response.status_code == 200  # Assert that the response status code is 200

# Route for home page
@app.route('/')
def home():
    # Render the base.html template for the home page
    return render_template('base.html')

# Route to display clients on the home page
@app.route('/clients')
def clients():
    try:
        cur = mysql.connection.cursor()
        # Query to get all clients
        cur.execute("SELECT * FROM clients")
        clients_data = cur.fetchall()
        # Convert client_details from JSON string to dictionary
        for client in clients_data:
            client['client_details'] = json.loads(client['client_details'])
        cur.close()
        # Render the base.html template with clients data
        return render_template('base.html', clients=clients_data)
    except Exception as e:
        return make_response(jsonify({"error": str(e)}), 500)

# Route to display the dashboard
@app.route('/dashboard')
def dashboard():
    return render_template('dashboard.html')  # Ensure this template contains the desired HTML content

# Route to handle user registration
@app.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    if not username or not password:
        return jsonify({"error": "Username and password required"}), 400

    hashed_password = generate_password_hash(password)
    cur = mysql.connection.cursor()
    try:
        cur.execute("INSERT INTO users (username, password_hash) VALUES (%s, %s)", (username, hashed_password))
        mysql.connection.commit()
        return jsonify({"message": "User registered successfully"}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        cur.close()

# Run the Flask application
if __name__ == "__main__":
    app.run(debug=True)  # Start the Flask application in debug mode