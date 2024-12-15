# Security Guards Management System

## Description
This project is a comprehensive management system for security guards, clients, and their assignments. It includes a RESTful API for managing clients, employees, employee assignments, training, and more. The system is built using Flask, with MySQL as the database, and includes JWT for authentication. It also provides tools for generating fake data for testing purposes.

## Installation
To install the necessary dependencies, run the following command: cmd
pip install -r requirements.txt

## Configuration
Ensure you have the following environment variables set up:

- `MYSQL_HOST`: The hostname of the MySQL server (e.g., `localhost`).
- `MYSQL_USER`: The username for the MySQL database (e.g., `root`).
- `MYSQL_PASSWORD`: The password for the MySQL user.
- `MYSQL_DB`: The name of the MySQL database (e.g., `security_guards_db`).
- `SECRET_KEY`: A secret key for JWT encoding.

## Database Setup
To set up the database, you can use the provided SQL dump file: cmd
mysql -u root -p security_guards_db < security_guards_backup.sql

## API Endpoints

| Endpoint                          | Method | Description                                      |
|-----------------------------------|--------|--------------------------------------------------|
| /clients                          | GET    | List all clients                                 |
| /clients                          | POST   | Add a new client                                 |
| /clients/<client_id>              | GET    | Get a specific client by ID                      |
| /clients/<client_id>              | PUT    | Update an existing client                        |
| /clients/<client_id>              | DELETE | Delete a client                                  |
| /employees                        | GET    | List all employees                               |
| /employees                        | POST   | Add a new employee                               |
| /employees/<employee_id>          | GET    | Get a specific employee by ID                    |
| /employees/<employee_id>          | PUT    | Update an existing employee                      |
| /employees/<employee_id>          | DELETE | Delete an employee                               |
| /employee_assignments             | GET    | List all employee assignments                    |
| /employee_assignments             | POST   | Add a new employee assignment                    |
| /employee_assignments/<ids>       | GET    | Get a specific employee assignment by ID         |
| /employee_assignments/<ids>       | PUT    | Update an existing employee assignment           |
| /employee_assignments/<ids>       | DELETE | Delete an employee assignment                    |
| /employee_training                | GET    | List all employee training records               |
| /employee_training                | POST   | Add a new employee training record               |
| /employee_training/<ids>          | GET    | Get a specific employee training record by ID    |
| /employee_training/<ids>          | PUT    | Update an existing employee training record      |
| /employee_training/<ids>          | DELETE | Delete an employee training record               |
| /qualifications                   | GET    | List all qualifications                          |
| /qualifications                   | POST   | Add a new qualification                          |
| /qualifications/<qualification_id>| PUT    | Update an existing qualification                 |
| /qualifications/<qualification_id>| DELETE | Delete a qualification                           |
| /training_courses                 | GET    | List all training courses                        |
| /training_courses                 | POST   | Add a new training course                        |
| /training_courses/<course_id>     | PUT    | Update an existing training course               |
| /training_courses/<course_id>     | DELETE | Delete a training course                         |
| /users                            | GET    | List all users                                   |
| /users                            | POST   | Add a new user                                   |
| /users/<user_id>                  | PUT    | Update an existing user                          |
| /users/<user_id>                  | DELETE | Delete a user                                    |

## Testing
To run the tests, use the following command: cmd
pytest test_api.py

This will execute the test cases defined in `test_api.py`, which include tests for CRUD operations and error handling.

## Data Generation
To generate fake data for testing, run the `generate_fake_data.py` script. This script populates the database with sample data for clients, employees, assignments, training, and more.

## Git Commit Guidelines

Use conventional commits for clear and structured commit messages:

- `feat`: Add new features (e.g., `feat: add user authentication`)
- `fix`: Fix bugs or issues (e.g., `fix: resolve database connection issue`)
- `docs`: Update or add documentation (e.g., `docs: update API documentation`)
- `test`: Add or update tests (e.g., `test: add user registration tests`)
