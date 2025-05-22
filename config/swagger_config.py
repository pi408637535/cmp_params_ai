# swagger_config.py
template = {
    "info": {
        "title": "Popular API",
        "description": "API for calculating city popularity",
        "version": "1.0.0"
    },
    "basePath": "/",
    "schemes": [
        "http",
        "https"
    ],
    "paths": {
        "/popular/get/{city}": {
            "get": {
                "tags": ["Popular"],
                "summary": "Calculate popularity score for a city",
                "operationId": "getPopularity",
                "parameters": [
                    {
                        "name": "city",
                        "in": "path",
                        "description": "The name of the city",
                        "required": True,
                        "type": "string"
                    }
                ],
                "responses": {
                    "200": {
                        "description": "Success, returns the popularity score",
                        "schema": {
                            "type": "number"
                        }
                    },
                    "400": {
                        "description": "Invalid city input",
                        "schema": {
                            "type": "string"
                        }
                    },
                    "500": {
                        "description": "Internal Server Error",
                        "schema": {
                            "type": "string"
                        }
                    }
                }
            }
        }
    }
}