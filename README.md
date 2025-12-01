🚀 Task Manager API – Zippee Assignment Submission

A fully functional Task Manager REST API built using Django REST Framework, with:

CRUD operations for tasks
JWT-based authentication
User authorization (owner-only update/delete)
Pagination, filtering, searching
API documentation (Swagger + ReDoc)
Automated tests (14 tests, all passing)


📦 Tech Stack

Python 3.10+
Django 4.x
Django REST Framework
SimpleJWT (JWT Authentication)
drf-yasg (Swagger & ReDoc API docs)
django-filter (Filtering)
pytest + pytest-django (Testing)

📁 Code Organization & Structure

project_root/
│── core/                    # Main project settings & URLs
│   ├── settings.py          # Installed apps, DRF setup, JWT, Swagger config
│   ├── urls.py              # Routes for APIs and docs
│
│── tasks/                   # Main Task Manager application
│   ├── models.py            # Task model (title, desc, completed, timestamps, owner)
│   ├── serializers.py       # Serializers for Task and User
│   ├── views.py             # CRUD API + custom update/delete messages
│   ├── permissions.py       # Owner-or-admin rule
│   ├── tests.py             # Complete automated test suite
│   ├── admin.py             # Admin panel support
│
│── manage.py                # Django management script
│── requirements.txt         # Python dependencies
│── README.md                # Project documentation



✨ Features Implemented

1️⃣ CRUD Operations (Fully Implemented)

Method	Endpoint	Description
GET	/api/tasks/	List user’s tasks (paginated + filtered)
GET	/api/tasks/{id}/	Retrieve task details
POST	/api/tasks/	Create a new task
PUT	/api/tasks/{id}/	Full update (returns success message)
PATCH	/api/tasks/{id}/	Partial update (returns success message)
DELETE	/api/tasks/{id}/	Delete task (returns success message)


Custom Response Messages:

Update →

{
  "message": "Task updated successfully!",
  "task": { ... }
}


Delete →

{
  "message": "Task 'Buy groceries' has been deleted successfully."
}



🔐 User Authentication & Authorization

✔ JWT Authentication
Implemented using SimpleJWT:
POST /api/token/ → login
POST /api/token/refresh/ → refresh token

✔ Authorization Rules
Only authenticated users can create tasks
Users can only view their own tasks
Users can only update or delete their own tasks
Admin (is_staff=True) can view/edit/delete all tasks

✔ Permissions Implemented
IsOwnerOrAdmin ensures:
if request.method in SAFE_METHODS: allow
else: allow only owner or admin


🔎 Filtering, Searching & Pagination
✔ Pagination
Enabled globally:
Default: 10 items per page
Use:
/api/tasks/?page=2

✔ Filtering
/api/tasks/?completed=True

✔ Search
/api/tasks/?search=grocery

✔ Ordering
/api/tasks/?ordering=created_at


📚 API Documentation (Swagger + ReDoc)
Automatically generated using drf-yasg.
Swagger UI
👉 http://127.0.0.1:8000/docs/swagger/
ReDoc
👉 http://127.0.0.1:8000/docs/redoc/

Both support:
JWT authorization button
Example request/response bodies
Descriptions of all CRUD routes
Custom update/delete examples

🧪 Automated Testing
A comprehensive test suite (14 tests) verifies:
✔ Authentication
Token generation
Access control
Owner vs non-owner access
✔ CRUD Functionality
Create
Retrieve
Update (PUT/PATCH)
Delete
✔ Authorization
Non-owner update/delete returns 403 or 404
Admin can access all tasks
✔ Filtering & Pagination
completed=True filter
Pagination envelope exists
✔ Custom Responses
Update returns "Task updated successfully!"
Delete returns "Task '<title>' has been deleted successfully."


▶️ How to Run Tests

python manage.py test tasks

Using pytest (if installed):
pytest -q

Expected output:
Found 14 tests.
..............
OK


⚙️ Setup & Installation
git clone
cd vaibhav_task_manager

python3 -m venv .venv
source .venv/bin/activate

pip install -r requirements.txt

python manage.py migrate
python manage.py runserver



🧪 Quick Usage Flow
1️⃣ Register User
POST /api/users/

{
  "username": "vaibhav",
  "password": "test123"
}

2️⃣ Login & Get Tokens
POST /api/token/
{
  "username": "vaibhav",
  "password": "test123"
}

Copy "access" token and use:
Authorization: Bearer <access>


3️⃣ Create Task
POST /api/tasks/
{
  "title": "Buy Milk",
  "description": "2 packets",
  "completed": false
}


🏁 Final Notes
This submission satisfies:

✔ Code organization and structure
✔ Complete CRUD implementation
✔ Authentication + Authorization
✔ Comprehensive test coverage
✔ Clear and complete documentation