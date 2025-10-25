# Task Manager API - RESTful Backend with JWT Authentication

A stateless RESTful API for task management built with Flask, featuring JWT-based authentication, MySQL database, and comprehensive CRUD operations.
---

## 📋 Table of Contents

- [Overview](#overview)
- [Architecture & Design](#architecture--design)
- [Features](#features)
- [Technology Stack](#technology-stack)
- [Project Structure](#project-structure)
- [API Documentation](#api-documentation)
- [Installation & Setup](#installation--setup)
- [Database Schema](#database-schema)
- [Running Unit Tests](#-running-unit-tests)

---

## 🎯 Overview

This is a **stateless Task Manager API** that demonstrates modern backend development practices. The application provides secure user authentication using JWT tokens and full CRUD operations for task management. Built with a clean, modular architecture following separation of concerns principles.

> 💡 **New to this project?** Check out `PROJECT_EXPLANATION.txt` for a simple, beginner-friendly explanation of everything in this project.

**Key Highlights:**
- ✅ Stateless architecture with JWT authentication
- ✅ Secure password hashing with bcrypt
- ✅ Soft delete implementation for data integrity
- ✅ Pagination and advanced filtering
- ✅ Service layer pattern for business logic separation
- ✅ Comprehensive error handling and logging
- ✅ CORS enabled for frontend integration

---

## 🏗️ Architecture & Design

### Architecture Pattern: **Stateless RESTful API**

The application follows a **3-tier architecture**:

```
┌─────────────────────────────────────────────────────────┐
│                    Presentation Layer                   |
│                    (Flask Routes/app.py)                │
│  - Request handling                                     │
│  - JWT authentication decorator                         │
│  - Response formatting                                  │
└────────────────────┬────────────────────────────────────┘
                     │
┌────────────────────▼──────────────────────────────────────┐
│                   Service Layer                           │
│          (service/user_service.py,                        │
│           service/task_service.py)                        │
│  - Business logic                                         │
│  - Data validation                                        │
│  - Database operations                                    │
└────────────────────┬──────────────────────────────────────┘
                     │
┌────────────────────▼──────────────────────────────────────┐
│                  Data Access Layer                        │
│              (models.py, db_config.py)                    │
│  - SQLAlchemy ORM                                         │
│  - Database models                                        │
│  - MySQL connection                                       │
└───────────────────────────────────────────────────────────┘
```

### Why Stateless Architecture?

- **Scalability**: No server-side session storage required
- **Horizontal Scaling**: Multiple server instances can handle requests independently
- **JWT Tokens**: Self-contained authentication tokens eliminate server-side session management
- **Microservices Ready**: Easy to deploy as independent services

---

## ✨ Features

### Authentication & Authorization
- **User Registration**: Secure signup with password hashing
- **User Login**: JWT token generation upon successful authentication
- **JWT-based Authorization**: Bearer token authentication for protected routes
- **Profile Endpoint**: Retrieve authenticated user information

### Task Management (CRUD Operations)
- ✅ **Create**: Add new tasks with title and description
- 📖 **Read**: Retrieve all tasks (paginated) or individual task details
- ✏️ **Update**: Modify task title, description, or completion status
- 🗑️ **Delete**: Soft delete implementation (data preserved with deleted_at timestamp)

### Advanced Features
- **Pagination**: Efficiently handle large task lists (5 tasks per page)
- **Filtering**: Filter tasks by completion status and date ranges
- **Soft Delete**: Tasks are marked as deleted rather than permanently removed
- **User Isolation**: Users can only access their own tasks
- **Comprehensive Logging**: All operations logged to `app.log`

---

## 🛠️ Technology Stack

| Component | Technology | Purpose |
|-----------|-----------|---------|
| **Framework** | Flask 3.1.2 | Python web framework |
| **Database** | MySQL | Relational database |
| **ORM** | SQLAlchemy 3.1.1 | Database abstraction layer |
| **Authentication** | PyJWT 2.10.1 | JWT token generation/validation |
| **Password Security** | bcrypt 5.0.0 | Password hashing |
| **Database Driver** | PyMySQL 1.1.2 | MySQL connector |
| **Migration** | Flask-Migrate 4.1.0 | Database schema management |
| **CORS** | Flask-CORS 3.0.10 | Cross-origin resource sharing |
| **Environment** | python-dotenv 1.1.1 | Configuration management |
| **Testing** | pytest 8.3.4 | Unit testing framework |
| **Coverage** | pytest-cov 6.0.0 | Test coverage reporting |

---

## 📁 Project Structure

```
r-ztm-f-d/
├── app.py                      # Main Flask application & route handlers
├── models.py                   # SQLAlchemy database models (User, Task)
├── db_config.py               # Database configuration & initialization
├── jwt_utils.py               # JWT token generation & validation utilities
├── test_app.py                # Comprehensive unit test suite
├── pytest.ini                 # Pytest configuration
├── requirements.txt            # Python dependencies
├── .env.example               # Environment variables template
├── PROJECT_EXPLANATION.txt    # Simple explanation of the entire project
├── app.log                    # Application logs
│
└── service/                    # Business logic layer
    ├── user_service.py        # User authentication & management logic
    └── task_service.py        # Task CRUD operations & filtering logic
```

### Code Organization Principles

1. **Separation of Concerns**: Routes handle HTTP, services handle business logic
2. **Single Responsibility**: Each module has a clear, focused purpose
3. **DRY Principle**: Reusable JWT decorator and service functions
4. **Security First**: Authentication required for all task operations

---

## 📚 API Documentation

### Base URL
```
http://localhost:5000
```

### Authentication
All protected endpoints require a JWT token in the Authorization header:
```
Authorization: Bearer <your_jwt_token>
```

---

### 1. User Registration
**Endpoint:** `POST /signup`

**Request Body:**
```json
{
  "username": "john_doe",
  "password": "secure_password123"
}
```

**Response (Success - 201):**
```json
{
  "message": "User registered successfully"
}
```

**Response (Error - 400):**
```json
{
  "error": "User already exists"
}
```

---

### 2. User Login
**Endpoint:** `POST /login`

**Request Body:**
```json
{
  "username": "john_doe",
  "password": "secure_password123"
}
```

**Response (Success - 200):**
```json
{
  "message": "Login successful",
  "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
}
```

**Response (Error - 401):**
```json
{
  "error": "Invalid username or password"
}
```

---

### 3. Get User Profile
**Endpoint:** `POST /profile`

**Headers:**
```
Authorization: Bearer <token>
```

**Response (Success - 200):**
```json
{
  "message": "User profile fetched successfully",
  "user": {
    "id": 1,
    "username": "john_doe",
    "created_at": "2024-01-15T10:30:00"
  }
}
```

---

### 4. Get All Tasks (Paginated)
**Endpoint:** `POST /tasks`

**Headers:**
```
Authorization: Bearer <token>
```

**Request Body:**
```json
{
  "page": 1
}
```

**Response (Success - 200):**
```json
{
  "tasks": [
    {
      "id": 1,
      "title": "Complete project documentation",
      "description": "Write comprehensive API documentation",
      "completed": false,
      "created_at": "2024-01-15T10:30:00",
      "updated_at": "2024-01-15T10:30:00"
    },
    {
      "id": 2,
      "title": "Review code changes",
      "description": "Review pull request #123",
      "completed": true,
      "created_at": "2024-01-14T09:15:00",
      "updated_at": "2024-01-14T15:45:00"
    }
  ],
  "page": 1,
  "per_page": 5,
  "total_pages": 3,
  "total_tasks": 12,
  "has_next": true,
  "has_prev": false
}
```

---

### 5. Get Single Task
**Endpoint:** `POST /tasks/<task_id>`

**Headers:**
```
Authorization: Bearer <token>
```

**Response (Success - 200):**
```json
{
  "id": 1,
  "title": "Complete project documentation",
  "description": "Write comprehensive API documentation",
  "completed": false,
  "created_at": "2024-01-15T10:30:00",
  "updated_at": "2024-01-15T10:30:00"
}
```

**Response (Error - 404):**
```json
{
  "error": "Task not found or deleted"
}
```

---

### 6. Create Task
**Endpoint:** `POST /tasks/create`

**Headers:**
```
Authorization: Bearer <token>
```

**Request Body:**
```json
{
  "title": "New Task",
  "description": "Task description here"
}
```

**Response (Success - 201):**
```json
{
  "id": 3,
  "title": "New Task",
  "description": "Task description here",
  "completed": false,
  "created_at": "2024-01-15T12:00:00",
  "updated_at": "2024-01-15T12:00:00"
}
```

---

### 7. Update Task
**Endpoint:** `POST /tasks/update/<task_id>`

**Headers:**
```
Authorization: Bearer <token>
```

**Request Body:**
```json
{
  "title": "Updated Title",
  "description": "Updated description",
  "completed": true
}
```

**Response (Success - 200):**
```json
{
  "id": 1,
  "title": "Updated Title",
  "description": "Updated description",
  "completed": true,
  "created_at": "2024-01-15T10:30:00",
  "updated_at": "2024-01-15T14:20:00"
}
```

---

### 8. Delete Task
**Endpoint:** `POST /tasks/delete/<task_id>`

**Headers:**
```
Authorization: Bearer <token>
```

**Response (Success - 200):**
```json
{
  "message": "Task deleted successfully"
}
```

---

### 9. Filter Tasks
**Endpoint:** `POST /tasks/filter`

**Headers:**
```
Authorization: Bearer <token>
```

**Request Body:**
```json
{
  "completed": true,
  "created_before": "2024-01-31",
  "created_after": "2024-01-01"
}
```

**Response (Success - 200):**
```json
[
  {
    "id": 1,
    "title": "Completed Task",
    "description": "Task description",
    "completed": true,
    "created_at": "2024-01-15T10:30:00",
    "updated_at": "2024-01-15T14:20:00"
  }
]
```

---

## Installation & Setup

### Prerequisites
- Python 3.8+
- MySQL 5.7+
- pip (Python package manager)

### Step 1: Clone the Repository
```bash
git clone <repository-url>
cd r-ztm-f-d
```

### Step 2: Create Virtual Environment
```bash
python3 -m venv venv
source venv/bin/activate
```

### Step 3: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 4: Configure Environment Variables
Create a `.env` file in the root directory:

```env
# Database Configuration
DB_USER=your_mysql_username
DB_PASSWORD=your_mysql_password
DB_HOST=localhost
DB_NAME=task_manager_db

# JWT Configuration
JWT_SECRET_KEY=your_super_secret_key_here_minimum_32_characters

# Server Configuration
PORT=5000
```

### Step 5: Create MySQL Database
```sql
CREATE DATABASE task_manager_db;
```

### Step 6: Run the Application
```bash
python app.py
```

The API will be available at `http://localhost:5000`

---

## 🔒 Security Implementation

### 1. Password Security
- **Hashing Algorithm**: bcrypt with automatic salt generation
- **Salt**: Unique salt per password prevents rainbow table attacks
- **Verification**: Secure password checking during login

```python
# Password hashing
salt = bcrypt.gensalt()
hashed_password = bcrypt.hashpw(password.encode("utf-8"), salt)

# Password verification
bcrypt.checkpw(password.encode("utf-8"), user.password_hash)
```

### 2. JWT Authentication
- **Algorithm**: HS256 (HMAC with SHA-256)
- **Token Expiration**: 24 hours (configurable)
- **Bearer Token**: Standard Authorization header format
- **Token Validation**: Automatic expiration and signature verification

### 3. Authorization Decorator
Custom `@jwt_required` decorator ensures:
- Authorization header presence
- Valid Bearer token format
- Token expiration check
- Invalid token rejection
- User ID extraction from token payload

### 4. User Isolation
- All task operations filtered by `user_id` from JWT token
- Users can only access/modify their own tasks
- Database-level foreign key constraints

### 5. Soft Delete
- Tasks marked as deleted with `deleted_at` timestamp
- Data preserved for audit trails
- Deleted tasks excluded from queries

---

## 🗄️ Database Schema

### Users Table
```sql
CREATE TABLE users (
    id INT PRIMARY KEY AUTO_INCREMENT,
    username VARCHAR(100) UNIQUE NOT NULL,
    password_hash BLOB(128) NOT NULL,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);
```

### Tasks Table
```sql
CREATE TABLE tasks (
    id INT PRIMARY KEY AUTO_INCREMENT,
    title VARCHAR(200) NOT NULL,
    description TEXT,
    completed BOOLEAN DEFAULT FALSE,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    deleted_at DATETIME NULL,
    user_id INT NOT NULL,
    FOREIGN KEY (user_id) REFERENCES users(id)
);
```

### Relationships
- **One-to-Many**: One user can have many tasks
- **Foreign Key**: `tasks.user_id` references `users.id`
---

## 💡 Key Design Decisions

### 1. Why JWT over Session-based Authentication?
- **Stateless**: No server-side session storage needed
- **Scalability**: Easy horizontal scaling without session replication
- **Microservices**: Token can be validated across services

### 2. Why Service Layer?
- **Separation of Concerns**: Business logic separated from HTTP handling
- **Testability**: Services can be unit tested independently
- **Reusability**: Same services can be used by different endpoints
- **Maintainability**: Easier to modify business logic without touching routes

### 3. Why Soft Delete?
- **Data Integrity**: Preserve historical data for auditing
- **Recovery**: Ability to restore accidentally deleted tasks
- **Analytics**: Track deletion patterns
- **Compliance**: Meet data retention requirements

### 4. Why Pagination?
- **Performance**: Reduce database load and response size
- **User Experience**: Faster page loads
- **Scalability**: Handle large datasets efficiently
- **Network Efficiency**: Less data transfer

---

## 📊 API Response Patterns

### Success Responses
- **200 OK**: Successful GET, PUT operations
- **201 Created**: Successful POST (create) operations
- JSON responses with relevant data

### Error Responses
- **400 Bad Request**: Invalid input data
- **401 Unauthorized**: Missing or invalid JWT token
- **404 Not Found**: Resource doesn't exist
- **500 Internal Server Error**: Server-side errors

All errors follow consistent format:
```json
{
  "error": "Error message here"
}
```

---

## 🧪 Testing the API

### Using cURL

**1. Register a new user:**
```bash
curl -X POST http://localhost:5000/signup \
  -H "Content-Type: application/json" \
  -d '{"username":"testuser","password":"testpass123"}'
```

**2. Login:**
```bash
curl -X POST http://localhost:5000/login \
  -H "Content-Type: application/json" \
  -d '{"username":"testuser","password":"testpass123"}'
```

**3. Create a task (replace TOKEN with actual token):**
```bash
curl -X POST http://localhost:5000/tasks/create \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer TOKEN" \
  -d '{"title":"My Task","description":"Task description"}'
```

**4. Get all tasks:**
```bash
curl -X POST http://localhost:5000/tasks \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer TOKEN" \
  -d '{"page":1}'
```

---

## 🧪 Running Unit Tests

The application includes a comprehensive test suite using **pytest** that covers all API endpoints, authentication, authorization, and error handling.

### Test Coverage

The test suite includes:
- ✅ User authentication (signup, login, profile)
- ✅ JWT token validation
- ✅ Task CRUD operations
- ✅ Pagination functionality
- ✅ Task filtering (by completion status and date)
- ✅ User data isolation
- ✅ Error handling and edge cases
- ✅ Authorization checks

### Prerequisites

Install testing dependencies:
```bash
pip install -r requirements.txt
```

### Running Tests

**Run all tests:**
```bash
pytest test_app.py -v
```

**Run tests with detailed output:**
```bash
pytest test_app.py -v -s
```

**Run specific test class:**
```bash
pytest test_app.py::TestUserAuthentication -v
pytest test_app.py::TestTaskCRUD -v
pytest test_app.py::TestTaskFiltering -v
pytest test_app.py::TestUserIsolation -v
```

**Run with coverage report:**
```bash
pytest test_app.py --cov=. --cov-report=html
```

This generates an HTML coverage report in `htmlcov/index.html`

**Run with coverage summary:**
```bash
pytest test_app.py --cov=. --cov-report=term
```

### Test Structure

The test suite is organized into test classes:

1. **TestUserAuthentication**: Tests for signup, login, and profile endpoints
2. **TestTaskCRUD**: Tests for create, read, update, and delete operations
3. **TestTaskFiltering**: Tests for filtering and pagination
4. **TestUserIsolation**: Tests to ensure users can only access their own data

### Test Examples

**Test successful user registration:**
```python
def test_signup_success(self, client):
    response = client.post('/signup', json={
        'username': 'newuser',
        'password': 'password123'
    })
    assert response.status_code == 201
```

**Test task creation:**
```python
def test_create_task_success(self, client, auth_token):
    headers = {'Authorization': f'Bearer {auth_token}'}
    response = client.post('/tasks/create', json={
        'title': 'Test Task',
        'description': 'This is a test task'
    }, headers=headers)
    assert response.status_code == 201
```

### Expected Test Results

When all tests pass, you should see output like:
```
test_app.py::TestUserAuthentication::test_signup_success PASSED
test_app.py::TestUserAuthentication::test_login_success PASSED
test_app.py::TestTaskCRUD::test_create_task_success PASSED
...
========================= X passed in Y.YYs =========================
```

### Test Database

Tests use an in-memory SQLite database (configured in `test_app.py`) to ensure:
- Tests run quickly
- No interference with production database
- Clean state for each test
- Isolation between test runs

---

## 📝 Logging

All API operations are logged to `app.log` with:
- Timestamp
- Log level (DEBUG, INFO, ERROR)
- Operation details
- Error messages
---
This project is developed as a demonstration of RESTful API design and JWT authentication best practices.
---

