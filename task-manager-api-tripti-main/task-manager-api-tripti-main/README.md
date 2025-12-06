# Task Manager API (Flask)

Full-featured RESTful Task Manager API with JWT authentication, Swagger docs, tests and Dockerfile.

## Features
- User register & login (JWT)
- CRUD for tasks (owner/admin authorization)
- Pagination & filtering
- Swagger UI (OpenAPI) at `/apidocs`
- Unit tests (pytest)
- Ready to push to GitHub and run in Docker

## Quickstart (local)
```bash
python -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate
pip install -r requirements.txt
export FLASK_APP=manage.py
python manage.py
# Visit http://127.0.0.1:5000/apidocs for Swagger UI
```

## Run tests
```bash
pytest -q
```

## Push to GitHub
```bash
git init
git add .
git commit -m "Initial commit"
git branch -M main
git remote add origin https://github.com/<username>/<repo>.git
git push -u origin main
```

