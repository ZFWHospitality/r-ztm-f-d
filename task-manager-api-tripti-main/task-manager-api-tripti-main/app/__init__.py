from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager
from flasgger import Swagger
from config import Config

db = SQLAlchemy()
migrate = Migrate()
jwt = JWTManager()

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    db.init_app(app)
    migrate.init_app(app, db)
    jwt.init_app(app)
    Swagger(app)

    with app.app_context():
        from .routes import tasks_bp
        from .auth import auth_bp
        app.register_blueprint(auth_bp)
        app.register_blueprint(tasks_bp)
        db.create_all()

    return app
