from flask import Blueprint, request, jsonify
from .models import Task
from .extensions import db
from flask_jwt_extended import jwt_required
from flasgger import swag_from

task_bp = Blueprint("tasks", __name__, url_prefix="/tasks")


# ---------------- GET ALL TASKS ----------------
@task_bp.get("")
@jwt_required()
@swag_from({
    "tags": ["Tasks"],
    "summary": "Get all tasks",
    "description": "Returns list of tasks. Optional query params: page, completed",
    "parameters": [
        {"name": "page", "in": "query", "type": "integer", "required": False},
        {"name": "completed", "in": "query", "type": "boolean", "required": False}
    ],
    "responses": {
        200: {"description": "List of tasks"}
    }
})
def get_tasks():
    page = request.args.get("page", 1, type=int)
    completed = request.args.get("completed", type=str)
    query = Task.query

    if completed is not None:
        if completed.lower() == "true":
            query = query.filter_by(completed=True)
        elif completed.lower() == "false":
            query = query.filter_by(completed=False)

    tasks = query.paginate(page=page, per_page=10, error_out=False).items
    result = [
        {
            "id": t.id,
            "title": t.title,
            "description": t.description,
            "completed": t.completed,
            "created_at": t.created_at,
            "updated_at": t.updated_at
        } for t in tasks
    ]
    return jsonify(result), 200


# ---------------- GET SINGLE TASK ----------------
@task_bp.get("/<int:task_id>")
@jwt_required()
@swag_from({
    "tags": ["Tasks"],
    "summary": "Get a single task",
    "parameters": [
        {"name": "task_id", "in": "path", "type": "integer", "required": True}
    ],
    "responses": {
        200: {"description": "Task details"},
        404: {"description": "Task not found"}
    }
})
def get_task(task_id):
    task = Task.query.get_or_404(task_id)
    return jsonify({
        "id": task.id,
        "title": task.title,
        "description": task.description,
        "completed": task.completed,
        "created_at": task.created_at,
        "updated_at": task.updated_at
    }), 200


# ---------------- CREATE TASK ----------------
@task_bp.post("")
@jwt_required()
@swag_from({
    "tags": ["Tasks"],
    "summary": "Create a new task",
    "parameters": [
        {
            "name": "body",
            "in": "body",
            "required": True,
            "schema": {
                "type": "object",
                "properties": {
                    "title": {"type": "string", "example": "My Task"},
                    "description": {"type": "string", "example": "Task description"}
                },
                "required": ["title"]
            }
        }
    ],
    "responses": {
        201: {"description": "Task created"},
        400: {"description": "Invalid input"}
    }
})
def create_task():
    data = request.get_json()
    if not data or "title" not in data:
        return jsonify({"error": "Title is required"}), 400

    task = Task(title=data["title"], description=data.get("description"))
    db.session.add(task)
    db.session.commit()
    return jsonify({"message": "Task created", "id": task.id}), 201


# ---------------- UPDATE TASK ----------------
@task_bp.put("/<int:task_id>")
@jwt_required()
@swag_from({
    "tags": ["Tasks"],
    "summary": "Update a task",
    "parameters": [
        {"name": "task_id", "in": "path", "type": "integer", "required": True},
        {
            "name": "body",
            "in": "body",
            "required": True,
            "schema": {
                "type": "object",
                "properties": {
                    "title": {"type": "string"},
                    "description": {"type": "string"},
                    "completed": {"type": "boolean"}
                }
            }
        }
    ],
    "responses": {
        200: {"description": "Task updated"},
        404: {"description": "Task not found"}
    }
})
def update_task(task_id):
    task = Task.query.get_or_404(task_id)
    data = request.get_json()

    if "title" in data:
        task.title = data["title"]
    if "description" in data:
        task.description = data["description"]
    if "completed" in data:
        task.completed = data["completed"]

    db.session.commit()
    return jsonify({"message": "Task updated"}), 200


# ---------------- DELETE TASK ----------------
@task_bp.delete("/<int:task_id>")
@jwt_required()
@swag_from({
    "tags": ["Tasks"],
    "summary": "Delete a task",
    "parameters": [
        {"name": "task_id", "in": "path", "type": "integer", "required": True}
    ],
    "responses": {
        200: {"description": "Task deleted"},
        404: {"description": "Task not found"}
    }
})
def delete_task(task_id):
    task = Task.query.get_or_404(task_id)
    db.session.delete(task)
    db.session.commit()
    return jsonify({"message": "Task deleted"}), 200
