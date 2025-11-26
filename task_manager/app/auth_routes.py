from flask import Blueprint, request, jsonify
from .models import User
from .extensions import db
from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import create_access_token
from flasgger import swag_from

auth_bp = Blueprint("auth", __name__, url_prefix="/auth")


@auth_bp.post("/register")
@swag_from({
    "tags": ["Authentication"],
    "summary": "Register a new user",
    "description": "Creates a new user account with username and password.",
    "parameters": [
        {
            "in": "body",
            "name": "body",
            "required": True,
            "schema": {
                "properties": {
                    "username": {"type": "string", "example": "harsh123"},
                    "password": {"type": "string", "example": "harsh"}
                },
                "required": ["username", "password"]
            }
        }
    ],
    "responses": {
        201: {"description": "User created successfully"},
        400: {"description": "User already exists or invalid request"}
    }
})
def register():
    data = request.get_json()

    if not data or "username" not in data or "password" not in data:
        return jsonify({"error": "username and password are required"}), 400

    existing_user = User.query.filter_by(username=data["username"]).first()
    if existing_user:
        return jsonify({"error": "Username already exists"}), 400

    user = User(
        username=data["username"],
        password=generate_password_hash(data["password"])
    )

    db.session.add(user)
    db.session.commit()

    return jsonify({"message": "User registered successfully"}), 201



@auth_bp.post("/login")
@swag_from({
    "tags": ["Authentication"],
    "summary": "Login user",
    "description": "Returns JWT access token after validating credentials.",
    "parameters": [
        {
            "name": "body",
            "in": "body",
            "required": True,
            "schema": {
                "type": "object",
                "properties": {
                    "username": {"type": "string", "example": "harsh123"},
                    "password": {"type": "string", "example": "harsh"}
                },
                "required": ["username", "password"]
            }
        }
    ],
    "responses": {
        200: {
            "description": "Login successful, JWT token returned",
            "examples": {
                "application/json": {
                    "access_token": "eyJ0eXAiOiJKV1QiLCJh..."
                }
            }
        },
        400: {"description": "Missing username or password"},
        401: {"description": "Invalid username or password"}
    }
})
def login():
    """
    Login user and return JWT token
    """
    data = request.get_json()

    # Validate request body
    if not data or "username" not in data or "password" not in data:
        return jsonify({"error": "username and password are required"}), 400

    # Find user
    user = User.query.filter_by(username=data["username"]).first()
    if not user:
        return jsonify({"error": "Invalid username or password"}), 401

    # Check password
    if not check_password_hash(user.password, data["password"]):
        return jsonify({"error": "Invalid username or password"}), 401

    # Create JWT token
    token = create_access_token(identity=user.id)

    return jsonify({"access_token": token}), 200