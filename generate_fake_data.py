import random  # Standard library for generating random numbers
from faker import Faker  # Library to generate fake data for testing
import mysql.connector  # MySQL database connector for Python
import json  # Standard library for JSON encoding and decoding

# Initialize a Faker instance to generate fake data
faker = Faker()

# Establish a connection to the MySQL database
conn = mysql.connector.connect(
    host="localhost",  # The hostname of the database server
    user="root",  # The username to connect to the database
    password="root",  # The password for the database user
    database="security_guards_db"  # The name of the database to connect to
)

# Create a cursor object to execute SQL queries
cursor = conn.cursor()

def fetch_existing_ids(query):
    """
    Helper function to fetch existing IDs from the database.
    This function executes a given SQL query and returns a set of IDs.
    """
    cursor.execute(query)  # Execute the provided SQL query
    return {row[0] for row in cursor.fetchall()}  # Fetch all results and return as a set of IDs

def insert_data(query, data):
    """
    Helper function to insert data into the database.
    This function uses executemany to insert multiple rows at once.
    """
    cursor.executemany(query, data)  # Execute the query with the provided data
    conn.commit()  # Commit the transaction to save changes to the database

def populate_clients(n):
    """
    Populate the clients table with n entries.
    Each client has a unique ID, details in JSON format, and a status.
    """
    existing_client_ids = fetch_existing_ids("SELECT client_id FROM clients")  # Fetch existing client IDs
    clients = []  # List to store new client data

    for i in range(n):
        client_id = f"C{i+1:03}"  # Generate a client ID in the format C001, C002, etc.
        while client_id in existing_client_ids:
            i += 1
            client_id = f"C{i+1:03}"  # Ensure the client ID is unique
        
        client_details = json.dumps({
            "name": faker.company(),  # Generate a fake company name
            "contact": faker.phone_number()  # Generate a fake phone number
        })
        status = random.choice(["active", "inactive"])  # Randomly assign a status
        clients.append((client_id, client_details, status))  # Add the client data to the list
        existing_client_ids.add(client_id)  # Add the new client ID to the set of existing IDs

    insert_data(
        """INSERT INTO clients (client_id, client_details, status)
        VALUES (%s, %s, %s)""",
        clients  # Insert the list of clients into the database
    )

def populate_employees(n):
    """
    Populate the employees table with n entries.
    Each employee has a unique ID, category code, details in JSON format, and a status.
    """
    existing_employee_ids = fetch_existing_ids("SELECT employee_id FROM employees")  # Fetch existing employee IDs
    employees = []  # List to store new employee data

    for i in range(n):
        employee_id = f"E{i+1:03}"  # Generate an employee ID in the format E001, E002, etc.
        while employee_id in existing_employee_ids:
            i += 1
            employee_id = f"E{i+1:03}"  # Ensure the employee ID is unique
        
        employee_details = json.dumps({
            "first_name": faker.first_name(),  # Generate a fake first name
            "last_name": faker.last_name()  # Generate a fake last name
        })
        category_code = f"CAT{random.randint(1, 5):03}"  # Randomly assign a category code
        status = random.choice(["active", "inactive"])  # Randomly assign a status
        employees.append((employee_id, category_code, employee_details, status))  # Add the employee data to the list
        existing_employee_ids.add(employee_id)  # Add the new employee ID to the set of existing IDs

    insert_data(
        """INSERT INTO employees (employee_id, category_code, employee_details, status)
        VALUES (%s, %s, %s, %s)""",
        employees  # Insert the list of employees into the database
    )

def populate_assignments(n):
    """
    Populate the employee_assignments table with n entries.
    Each assignment links an employee to a client with a start and end date, and a status.
    """
    assignments = []  # List to store new assignment data

    for _ in range(n):
        while True:
            employee_id = f"E{random.randint(1, 25):03}"  # Randomly select an employee ID
            client_id = f"C{random.randint(1, 25):03}"  # Randomly select a client ID
            start_date = faker.date_this_year()  # Generate a start date within the current year
            end_date = faker.date_between(start_date=start_date)  # Generate an end date after the start date
            status = random.choice(["active", "completed", "cancelled"])  # Randomly assign a status
            
            # Check if the assignment already exists
            cursor.execute(
                """SELECT COUNT(*) FROM employee_assignments
                WHERE employee_id = %s AND client_id = %s AND start_date = %s""",
                (employee_id, client_id, start_date)
            )
            (count,) = cursor.fetchone()
            
            if count == 0:  # If the assignment does not exist, add it to the list
                assignments.append((employee_id, client_id, start_date, end_date, status))
                break

    insert_data(
        """INSERT INTO employee_assignments (employee_id, client_id, start_date, end_date, status)
        VALUES (%s, %s, %s, %s, %s)""",
        assignments  # Insert the list of assignments into the database
    )

def populate_training(n):
    """
    Populate the employee_training table with n entries.
    Each training session links an employee to a course with a start and end date, and a status.
    """
    training_sessions = []  # List to store new training session data

    for _ in range(n):
        employee_id = f"E{random.randint(1, 25):03}"  # Randomly select an employee ID
        course_id = f"COURSE{random.randint(1, 10):03}"  # Randomly select a course ID
        start_date = faker.date_this_year()  # Generate a start date within the current year
        end_date = faker.date_between(start_date=start_date)  # Generate an end date after the start date
        status = random.choice(["ongoing", "completed", "cancelled"])  # Randomly assign a status
        training_sessions.append((employee_id, course_id, start_date, end_date, status))  # Add the training session data to the list

    insert_data(
        """INSERT INTO employee_training (employee_id, course_id, start_date, end_date, status)
        VALUES (%s, %s, %s, %s, %s)""",
        training_sessions  # Insert the list of training sessions into the database
    )

def populate_employee_category():
    """
    Populate the employee_category table with predefined categories.
    This function checks for existing categories and only inserts new ones.
    """
    existing_categories = fetch_existing_ids("SELECT category_code FROM employee_category")  # Fetch existing category codes
    categories = [
        ('CAT001', 'Security Guard'),
        ('CAT002', 'Supervisor'),
        ('CAT003', 'Manager'),
        ('CAT004', 'Receptionist'),
        ('CAT005', 'Technician')
    ]

    # Filter out categories that already exist in the database
    new_categories = [category for category in categories if category[0] not in existing_categories]

    if new_categories:  # If there are new categories, insert them into the database
        insert_data(
            """INSERT INTO employee_category (category_code, category_description)
            VALUES (%s, %s)""",
            new_categories
        )

def populate_qualifications(n):
    """
    Populate the qualifications table with n entries.
    Each qualification has a unique ID, details in JSON format, and a status.
    """
    existing_qualification_ids = fetch_existing_ids("SELECT qualification_id FROM qualifications")  # Fetch existing qualification IDs
    qualifications = []  # List to store new qualification data

    for i in range(n):
        qualification_id = f"QUAL{i+1:03}"  # Generate a qualification ID in the format QUAL001, QUAL002, etc.
        while qualification_id in existing_qualification_ids:
            i += 1
            qualification_id = f"QUAL{i+1:03}"  # Ensure the qualification ID is unique
        
        qualification_details = json.dumps({
            "name": faker.word(),  # Generate a fake qualification name
            "description": faker.sentence()  # Generate a fake qualification description
        })
        status = random.choice(["active", "inactive"])  # Randomly assign a status
        qualifications.append((qualification_id, qualification_details, status))  # Add the qualification data to the list
        existing_qualification_ids.add(qualification_id)  # Add the new qualification ID to the set of existing IDs

    insert_data(
        """INSERT INTO qualifications (qualification_id, qualification_details, status)
        VALUES (%s, %s, %s)""",
        qualifications  # Insert the list of qualifications into the database
    )

def populate_training_courses(n):
    """
    Populate the training_courses table with n entries.
    Each course has a unique ID, details in JSON format, and a status.
    """
    existing_course_ids = fetch_existing_ids("SELECT course_id FROM training_courses")  # Fetch existing course IDs
    courses = []  # List to store new course data

    for i in range(n):
        course_id = f"COURSE{i+1:03}"  # Generate a course ID in the format COURSE001, COURSE002, etc.
        while course_id in existing_course_ids:
            i += 1
            course_id = f"COURSE{i+1:03}"  # Ensure the course ID is unique
        
        course_details = json.dumps({
            "title": faker.catch_phrase(),  # Generate a fake course title
            "description": faker.text()  # Generate a fake course description
        })
        status = random.choice(["active", "inactive"])  # Randomly assign a status
        courses.append((course_id, course_details, status))  # Add the course data to the list
        existing_course_ids.add(course_id)  # Add the new course ID to the set of existing IDs

    insert_data(
        """INSERT INTO training_courses (course_id, course_details, status)
        VALUES (%s, %s, %s)""",
        courses  # Insert the list of courses into the database
    )

def populate_users(n):
    """
    Populate the users table with n entries.
    Each user has a unique ID, username, password hash, role, and status.
    """
    existing_usernames = fetch_existing_ids("SELECT username FROM users")  # Fetch existing usernames
    users = []  # List to store new user data

    for _ in range(n):
        user_id = faker.uuid4()  # Generate a unique user ID
        username = faker.user_name()  # Generate a fake username
        while username in existing_usernames:
            username = faker.user_name()  # Ensure the username is unique
        
        password_hash = faker.password()  # Generate a fake password hash
        role = random.choice(["admin", "manager", "user"])  # Randomly assign a role
        status = random.choice(["active", "inactive"])  # Randomly assign a status
        users.append((user_id, username, password_hash, role, status))  # Add the user data to the list
        existing_usernames.add(username)  # Add the new username to the set of existing usernames

    insert_data(
        """INSERT INTO users (user_id, username, password_hash, role, status)
        VALUES (%s, %s, %s, %s, %s)""",
        users  # Insert the list of users into the database
    )

# Populate the tables with sample data
populate_clients(25)  # Populate the clients table with 25 entries
populate_employees(25)  # Populate the employees table with 25 entries
populate_assignments(25)  # Populate the employee_assignments table with 25 entries
populate_training(25)  # Populate the employee_training table with 25 entries
populate_employee_category()  # Populate the employee_category table with predefined categories
populate_qualifications(25)  # Populate the qualifications table with 25 entries
populate_training_courses(25)  # Populate the training_courses table with 25 entries
populate_users(25)  # Populate the users table with 25 entries

# Close the cursor and connection to the database
cursor.close()  # Close the cursor to free up resources
conn.close()  # Close the database connection