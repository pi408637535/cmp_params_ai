"""
The simple example using OpenAPI 3.0 callbacks
"""
from flask_restful import Api, Resource
from flask import Flask, jsonify
from flasgger import Swagger
import math
from flasgger import LazyJSONEncoder
from config.swagger_config import template  # 假设你已经将 template 移到 swagger_config.py 文件中

app = Flask(__name__)
app.config['SWAGGER'] = {
    'title': 'OA3 Callbacks',
    'openapi': '3.0.2'
}

app.json_encoder = LazyJSONEncoder
api = Api(app)

swagger = Swagger(app, template=template)

class Popular(Resource):
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
    app.run(debug=True, port=9980)