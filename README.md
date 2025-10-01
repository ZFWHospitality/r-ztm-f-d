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

## How to run it:

* The project has been made on an anaconda distribution of python.
* A copy of the environment has been attached in the Repo itself just install it.
* To create the environment from the file execute "conda env create -f environment.yml" command.
* Execute the command "conda activate djangoprac" to execute the env.
* Then go to the project and run it with command "python manage.py createsuperuser". This will help set up a super user which will be needed to access the API.
* Finally run the server it self with "python manage.py runserver".
* Go to "http://127.0.0.1:8000/admin/" and login this will start a session and create the required session and cookies to access the API for the current session.
* Now the project is deployed and can be used for testing. 
