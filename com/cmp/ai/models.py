from flask_restful import fields

# 定义 Tutorial 模型
tutorial_fields = {
    'id': fields.Integer,
    'title': fields.String,
    'description': fields.String,
    'published': fields.Boolean
}