from flask import Flask, request, jsonify
from flask_restful import Api, Resource
from flasgger import Swagger
from models import tutorial_fields
from flasgger.utils import swag_from
from com.cmp.config.swagger import swagger_template, swagger_config
import random,math

from services import (
    create_tutorial, get_all_tutorials, get_tutorial_by_id,
    update_tutorial, delete_tutorial, delete_all_tutorials,
    find_published_tutorials
)

app = Flask(__name__)
api = Api(app)
swagger = Swagger(app, template=swagger_template, config=swagger_config)

class TutorialList(Resource):
    @swag_from({
        'tags': ['tutorials', 'get', 'filter'],
        'responses': {
            200: {
                'description': 'Retrieve all Tutorials',
                'schema': {
                    'type': 'array',
                    'items': {
                        'type': 'object',
                        'properties': tutorial_fields
                    }
                }
            },
            204: {
                'description': 'There are no Tutorials'
            },
            500: {
                'description': 'Internal Server Error'
            }
        }
    })
    def get(self):
        title = request.args.get('title')
        tutorials = get_all_tutorials(title)
        if not tutorials:
            return '', 204
        return tutorials, 200

    @swag_from({
        'tags': ['tutorials', 'post'],
        'responses': {
            201: {
                'description': 'Create a new Tutorial',
                'schema': {
                    'type': 'object',
                    'properties': tutorial_fields
                }
            },
            500: {
                'description': 'Internal Server Error'
            }
        }
    })
    def post(self):
        tutorial = request.get_json()
        try:
            new_tutorial = create_tutorial(tutorial)
            return new_tutorial, 201
        except Exception:
            return '', 500

class Tutorial(Resource):
    @swag_from({
        'tags': ['tutorials', 'get'],
        'responses': {
            200: {
                'description': 'Retrieve a Tutorial by Id',
                'schema': {
                    'type': 'object',
                    'properties': tutorial_fields
                }
            },
            404: {
                'description': 'Tutorial not found'
            },
            500: {
                'description': 'Internal Server Error'
            }
        }
    })
    def get(self, id):
        tutorial = get_tutorial_by_id(id)
        if tutorial:
            return tutorial, 200
        return '', 404

    @swag_from({
        'tags': ['tutorials', 'put'],
        'responses': {
            200: {
                'description': 'Update a Tutorial by Id',
                'schema': {
                    'type': 'object',
                    'properties': tutorial_fields
                }
            },
            404: {
                'description': 'Tutorial not found'
            },
            500: {
                'description': 'Internal Server Error'
            }
        }
    })
    def put(self, id):
        tutorial = request.get_json()
        updated_tutorial = update_tutorial(id, tutorial)
        if updated_tutorial:
            return updated_tutorial, 200
        return '', 404

    @swag_from({
        'tags': ['tutorials', 'delete'],
        'responses': {
            204: {
                'description': 'Delete a Tutorial by Id'
            },
            500: {
                'description': 'Internal Server Error'
            }
        }
    })
    def delete(self, id):
        try:
            delete_tutorial(id)
            return '', 204
        except Exception:
            return '', 500

class DeleteAllTutorials(Resource):
    @swag_from({
        'tags': ['tutorials', 'delete'],
        'responses': {
            204: {
                'description': 'Delete all Tutorials'
            },
            500: {
                'description': 'Internal Server Error'
            }
        }
    })
    def delete(self):
        try:
            delete_all_tutorials()
            return '', 204
        except Exception:
            return '', 500

class PublishedTutorials(Resource):
    @swag_from({
        'tags': ['tutorials', 'get', 'filter'],
        'responses': {
            200: {
                'description': 'Retrieve all published Tutorials',
                'schema': {
                    'type': 'array',
                    'items': {
                        'type': 'object',
                        'properties': tutorial_fields
                    }
                }
            },
            204: {
                'description': 'There are no published Tutorials'
            },
            500: {
                'description': 'Internal Server Error'
            }
        }
    })
    def get(self):
        published_tutorials = find_published_tutorials()
        if not published_tutorials:
            return '', 204
        return published_tutorials, 200


class Popular(Resource):
    @swag_from({
        'tags': ['popular', 'get'],
        'responses': {
            200: {
                'description': 'Retrieve a Tutorial by Id',
                'schema': {
                    'type': 'object',
                    'properties': tutorial_fields
                }
            },
            404: {
                'description': 'Ppular not found'
            },
            500: {
                'description': 'Internal Server Error'
            }
        }
    })
    def get(self, city):
        print(city)
        if True:
            return math.exp(len(city)), 200
        return '', 404

api.add_resource(TutorialList, '/api/tutorials')
api.add_resource(Tutorial, '/api/tutorials/<int:id>')
api.add_resource(DeleteAllTutorials, '/api/tutorials/delete-all')
api.add_resource(PublishedTutorials, '/api/tutorials/published')
api.add_resource(Popular, '/api/popular/<string:city>')


if __name__ == '__main__':
    app.run(debug=True, port=9980)