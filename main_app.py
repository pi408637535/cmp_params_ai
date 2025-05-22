from flask import Flask, request
from flask_restful import Api, Resource
from flasgger import Swagger, swag_from
import math

app = Flask(__name__)
api = Api(app)

# Configuring Swagger
app.config['SWAGGER'] = {
    'title': 'My API',
    'uiversion': 3
}
swagger = Swagger(app)

class Welcome(Resource):
    @swag_from({
        'responses': {
            200: {
                'description': 'A status code 200 means successful and returns a message.',
                'content': {
                    'application/json': {
                        'examples': {
                            'example1': {
                                'summary': 'Successful response',
                                'value': {'message': 'Welcome GeeksforGeeks!!'}
                            }
                        }
                    }
                }
            }
        }
    })
    def get(self):
        """
        This is an example endpoint which returns a simple message.
        """
        return {'message': 'Welcome GeeksforGeeks!!'}

class Items(Resource):
    @swag_from({
        'responses': {
            200: {
                'description': 'A status code 200 means successful and returns a list of items.',
                # 'content': {
                #     'application/json': {
                #         'examples': {
                #             'example1': {
                #                 'summary': 'Successful response',
                #                 'value': {'items': ['Item 1', 'Item 2', 'Item 3']}
                #             }
                #         }
                #     }
                # }
            }
        }
    })
    def get(self):
        """
        This endpoint returns a list of items.
        """
        items = ['Item 1', 'Item 2', 'Item 3']
        return {'items': items}

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

api.add_resource(Welcome, '/')
api.add_resource(Items, '/items')
api.add_resource(Popular, '/popular/get/<string:city>')

if __name__ == '__main__':
    app.run(debug=True, port=9980)