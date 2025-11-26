template = {
    "swagger": "2.0",
    "info": {
        "title": "Task Manager API",
        "description": "API documentation for Task Manager",
        "version": "1.0.0"
    },
    "basePath": "/",
    "schemes": ["http", "https"],
    "securityDefinitions": {
        "Bearer": {
            "type": "apiKey",
            "name": "Authorization",
            "in": "header",
            "description": "JWT Authorization header using the Bearer scheme. Example: 'Bearer <token>'"
        }
    },
    "security": [{"Bearer": []}]  # <-- this enables the Authorize button globally
}


swagger_config = {
    "headers": [],
    "specs": [
        {
            "endpoint": 'apispec',
            "route": '/apispec.json'
        }
    ],
    "static_url_path": "/flasgger_static",
    "swagger_ui": True,
    "specs_route": "/docs/"
}
