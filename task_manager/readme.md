# Task Manager API (Flask)

This project is a simple **Task Manager REST API** built with **Flask**. It supports user registration, login (JWT), and CRUD operations on tasks.

---

## Features

* JWT Authentication
* CRUD for Tasks
* Protected create/update/delete
* SQLite database

---

## Setup Instructions

### 1. Clone Project

```
git clone <your-repo-url>
```

### 2. Create Virtual Environment

```
python -m venv venv
# Windows
venv\Scripts\activate
# macOS / Linux
source venv/bin/activate
```

### 3. Install Dependencies

```
pip install -r requirements.txt
```


### 4. Run the Application

```
python run.py
```

Server runs at: **[http://127.0.0.1:5000/](http://127.0.0.1:5000/)**

---

## API Endpoints

### Auth

* POST /register — Register user
* POST /login — Login & get JWT

### Tasks (require Authorization: Bearer <token>)

* GET /tasks — List tasks
* GET /tasks/<id> — Get task
* POST /tasks — Create task
* PUT /tasks/<id> — Update task
* DELETE /tasks/<id> — Delete task

---
