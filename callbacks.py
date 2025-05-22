"""
The simple example using OpenAPI 3.0 callbacks
"""
from flask_restful import Api, Resource
from flask import Flask, jsonify
from flasgger import Swagger, swag_from
import math
from flasgger import Swagger,LazyString, LazyJSONEncoder

app = Flask(__name__)
app.config['SWAGGER'] = {
    'title': 'OA3 Callbacks',
    'openapi': '3.0.2'
}

app.json_encoder = LazyJSONEncoder
api = Api(app)

@app.route('/run_callback/',  methods=['POST'])
def run_callback():
    """Example endpoint that specifies OA3 callbacks
    This is using docstring for specifications
    ---
    tags:
      - callbacks
    requestBody:
      description: Test
      required: true
      content:
        application/json:
          schema:
            properties:
              callback_url:
                type: string
                format: uri
                description: Callback URL for request
    callbacks:
        onSomeEvent:
          '{$request.body.callback_url}':
            post:
              requestBody:
                description: status payload
                content:
                  application/json:
                    schema:
                      properties:
                        status:
                          type: string
    """

    return jsonify({'result': 'ok'})

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

swagger = Swagger(app, template=template)

class Popular(Resource):
    @swag_from({
        # 'tags': ['Popular', 'get'],
        'responses': {
            200: {
                'description': 'Calculate popularity score for a city'
            },
            404: {
                'description': 'Popular not found'
            },
            500: {
                'description': 'Internal Server Error'
            }
        }
    })
    def get(self, city):
        try:
            print(city)
            if not city or not isinstance(city, str):
                return 'error', 400
            # 示例逻辑：基于城市名称长度计算分数
            score = math.exp(len(city))
            return score, 200
        except Exception as e:
            return 'error', 500

api.add_resource(Popular, '/popular/get/<string:city>')

if __name__ == "__main__":
    app.run(debug=True)