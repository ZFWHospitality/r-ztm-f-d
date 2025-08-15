# r-ztm-f-d

# Title: Task Manager API

## Objective:
Build a RESTful API for a simple task manager application using either Flask or Django. The API should allow users to perform basic CRUD operations on tasks and should include user authentication.

## Requirements:

1. Task Model:

* Create a model for tasks with the following fields:
** id (auto-generated)
** title (string)
** description (text)
** completed (boolean)
** created_at (timestamp)
** updated_at (timestamp)

2. API Endpoints:

* Implement the following endpoints:
** GET /tasks: Retrieve a list of all tasks.
** GET /tasks/{id}: Retrieve details of a specific task.
** POST /tasks: Create a new task.
** PUT /tasks/{id}: Update details of a specific task.
** DELETE /tasks/{id}: Delete a specific task.

3. User Authentication:

* Implement user authentication using either JWT or session-based authentication.
* Users should be able to register and log in.
* Only authenticated users should be able to create, update, or delete tasks.

4. Documentation:

* Provide clear and concise API documentation, including examples of requests and responses.
* Use any documentation tool of your choice (e.g., Swagger, ReDoc).

5. Testing:

* Write unit tests to ensure the correctness of your API endpoints.
* Include instructions on how to run the tests.

## Bonus Points (Optional):

* Implement pagination for the list of tasks.
* Add filtering options for tasks (e.g., filter by completed status).
* Include user roles (e.g., admin, regular user) with different permissions.

## Submission:

* Share your codebase via a version control system (e.g., GitHub).
* Include a README.md file with instructions on how to set up and run the application.
* Provide any additional notes or explanations you think are necessary.
## Evaluation Criteria:

* Code organization and structure.
* Correct implementation of CRUD operations.
* User authentication and authorization.
* Quality and coverage of tests.
* Clarity and completeness of documentation.



## How to setup and run the code:

* I’ve created a script named run_project.py that fully automates the Django project setup and launch process.
With just a single command:

# python run_project.py

* the script will:

Install all required dependencies.

Apply database migrations.

Create a superuser (if one doesn’t already exist).

Start the development server.

In short, it handles everything for you — no manual steps needed.

## To access API Documentation:

*  just go on this url http://127.0.0.1:8000/swagger/ you will be able to access a api documentation 
 