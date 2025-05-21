# config/swagger.py
import os

swagger_template = {
    "swagger": "2.0",
    "info": {
        "title": os.getenv("SWAGGER_TITLE", "Tutorial API"),
        "description": "API for managing tutorials",
        "version": "1.0"
    },
    "basePath": "/",
    "schemes": ["http", "https"],

    "definitions": {
        "Tutorial": {
            "type": "object",
            "properties": {
                "id": {"type": "integer"},
                "title": {"type": "string"},
                "description": {"type": "string"},
                "published": {"type": "boolean"}
            }
        }
    }
}

swagger_config = {
    "headers": [],
    "specs": [
        {
            "endpoint": "apispec_1",
            "route": "/apispec_1.json",
            "rule_filter": lambda rule: True,
            "model_filter": lambda tag: True,
        }
    ],
    "static_url_path": "/flasgger_static",
    "swagger_ui": os.getenv("ENABLE_SWAGGER", "true").lower() == "true",
    "specs_route": "/apidocs/",
}