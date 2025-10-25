import os
import logging
from functools import wraps
from flask import Flask, jsonify, session, request
from sqlalchemy import text
from dotenv import load_dotenv
from jwt_utils import generate_jwt, decode_jwt
from db_config import init_db, db
from models import User
from service.user_service import create_user, authenticate_user, get_user_by_id
from service.task_service import get_all_task, get_task_by_id, create_new_task, update_task, delete_task, filter_tasks

load_dotenv()
app = Flask(__name__)  

logger = logging.getLogger('global_logger')
logger.setLevel(logging.DEBUG)
file_handler = logging.FileHandler('app.log')
file_handler.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
file_handler.setFormatter(formatter)
logger.addHandler(file_handler) 
app.logger = logger

init_db(app)

def jwt_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        auth_header = request.headers.get('Authorization')
        if not auth_header or not auth_header.startswith("Bearer "):
            return jsonify({"error": "Missing or invalid Authorization header"}), 401

        token = auth_header.split(" ")[1]
        decoded = decode_jwt(token)
        if "error" in decoded:
            return jsonify(decoded), 401

        request.user_id = decoded["user_id"]
        return f(*args, **kwargs)
    return decorated


@app.route('/signup', methods=['POST'])
def signup():
    data = request.get_json()
    username = data.get("username").strip()
    password = data.get("password").strip()

    if not username or not password:
        return jsonify({"error": "Username and password required"}), 400

    response, status = create_user(username, password)
    return jsonify(response), status


@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get("username").strip()
    password = data.get("password").strip()

    user = authenticate_user(username, password)
    if not user:
        return jsonify({"error": "Invalid username or password"}), 401

    token = generate_jwt(user.id)
    return jsonify({
        "message": "Login successful",
        "token": token
    }), 200


@app.route('/profile', methods=['POST'])
def profile():
    auth_header = request.headers.get('Authorization')
    if not auth_header or not auth_header.startswith("Bearer "):
        return jsonify({"error": "Missing or invalid Authorization header"}), 401

    token = auth_header.split(" ")[1]
    decoded = decode_jwt(token)

    if "error" in decoded:
        return jsonify(decoded), 401

    user = get_user_by_id(decoded["user_id"])
    if not user:
        return jsonify({"error": "User not found"}), 404

    return jsonify({
        "message": "User profile fetched successfully",
        "user": {
            "id": user.id,
            "username": user.username,
            "created_at": user.created_at
        }
    }), 200

@app.route('/tasks', methods=['POST'])
@jwt_required
def get_tasks():
    data = request.get_json() or {}
    user_id = request.user_id

    page = int(data.get("page", 1))

    result = get_all_task(user_id, page)
    return jsonify(result), 200


@app.route('/tasks/<int:task_id>', methods=['POST'])
@jwt_required
def get_task(task_id):
    user_id = request.user_id
    task = get_task_by_id(task_id, user_id)
    if not task:
        return jsonify({"error": "Task not found or deleted"}), 404
    return jsonify(task.to_dict()), 200

@app.route('/tasks/create', methods=['POST'])
@jwt_required
def create_task():
    data = request.get_json()
    title = data.get("title").strip()
    description = data.get("description", "").strip()
    user_id = request.user_id

    if not title or not description:
        return jsonify({"error": "Title and description are required"}), 400

    task = create_new_task(title, description, user_id)
    return jsonify(task.to_dict()), 201

@app.route('/tasks/update/<int:task_id>', methods=['POST'])
@jwt_required   
def update_task_route(task_id):
    data = request.get_json() or {}
    title = data.get("title")
    description = data.get("description")
    completed = data.get("completed")
    user_id = request.user_id

    if title is None and description is None and completed is None:
        return jsonify({"error": "No data provided to update"}), 400

    task = update_task(task_id, title, description, completed, user_id)
    if not task:
        return jsonify({"error": "Task not found"}), 404

    return jsonify(task.to_dict()), 200

@app.route('/tasks/delete/<int:task_id>', methods=['POST'])
@jwt_required
def delete_task_route(task_id):
    user_id = request.user_id
    success = delete_task(task_id, user_id)
    if not success:
        return jsonify({"error": "Task not found"}), 404

    return jsonify({"message": "Task deleted successfully"}), 200

@app.route('/tasks/filter', methods=['POST'])
@jwt_required
def filter_tasks_route():
    data = request.get_json() or {}
    user_id = request.user_id

    completed = data.get("completed")
    created_before = data.get("created_before")
    created_after = data.get("created_after")

    result = filter_tasks(user_id, completed, created_before, created_after)

    if isinstance(result, dict) and "error" in result:
        return jsonify(result), 400

    return jsonify(result), 200

if __name__ == "__main__":
    with app.app_context():
        try:
            db.create_all()
            result = db.session.execute(text('SELECT DATABASE()')).fetchone()
            app.logger.info(f"Connected to database: {result[0]}")
        except Exception as e:
            app.logger.error(f"Error creating database tables: {e}")
    app.run(host='0.0.0.0', port=int(os.getenv('PORT')), debug=True)