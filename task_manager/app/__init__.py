from flask import Flask
from .extensions import db, migrate, jwt
from flasgger import Swagger
from .swagger import template, swagger_config

def create_app():
    app = Flask(__name__)

    # Configurations
    app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///tasks.db"
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['JWT_SECRET_KEY'] = "supersecretkey"

    # Init extensions
    db.init_app(app)
    migrate.init_app(app, db)
    jwt.init_app(app)
    Swagger(app, template=template, config=swagger_config)

    # Register Blueprints
    from .auth_routes import auth_bp
    from .task_routes import task_bp

    app.register_blueprint(auth_bp)
    app.register_blueprint(task_bp)

    # Root/Home Route
    @app.route("/")
    def home():
        return {
            "message": "Task Manager API is running!",
            "documentation": "/docs",
            "auth_register": "/auth/register",
            "auth_login": "/auth/login",
            "tasks": "/tasks"
        }

    return app
