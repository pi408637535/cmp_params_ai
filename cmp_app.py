"""
The simple example using OpenAPI 3.0 callbacks
"""
import time

from flask_restful import Api, Resource
from flasgger import Swagger
import math
from flasgger import LazyJSONEncoder
from config.swagger_config import template  # 假设你已经将 template 移到 swagger_config.py 文件中
from flask import Flask, request,jsonify
import requests
import json
import pandas as pd

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


class CmpController(Resource):
    def post(self):
        # 获取请求的 JSON 数据
        print(request.headers.get('Content-Type'))
        data = request.get_json()

        # 打印接收到的参数
        print("接收到的参数：")
        # print(f"filterParamDetail: {data.get('filterParamDetail')}")
        # print(f"featureId: {data.get('featureId')}")
        # print(f"ruleParams: {data.get('ruleParams')}")
        # print(f"dataStartTime: {data.get('dataStartTime')}")
        # print(f"dataEndTime: {data.get('dataEndTime')}")

        url = 'https://bos-qa.qa.tigerbrokers.net/api/cmp/v2/back-test?_s=1747732124778&timezone=local&lang=zh_CN&bos_license=TBNZ'
        headers = {
            'accept': 'application/json, text/plain, */*',
            'accept-language': 'zh-CN,zh;q=0.9',
            'authorization': 'Basic ST-2916f02b0f9848e991c0d081eff23a53',
            'content-type': 'application/json',
            'origin': 'https://bos-dev.itiger.com',
            'priority': 'u=1, i',
            'referer': 'https://bos-dev.itiger.com/',
            'sec-ch-ua': '"Google Chrome";v="135", "Not-A.Brand";v="8", "Chromium";v="135"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"macOS"',
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'cross-site',
            'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Safari/537.36',
            'Cookie': 'JSESSIONID=8F279191A61F5FFD92493461DBF30C25; ngxid=CkQhs2gtPdCqk1d6WR4LAg=='
        }

        data = {
            "filterParamDetail": data.get('filterParamDetail'),
            "featureId": data.get('featureId'),
            "ruleParams": data.get('ruleParams'),
            "dataStartTime": data.get('dataStartTime'),
            "dataEndTime": data.get('dataEndTime')
        }

        try:
            response = requests.post(url, headers=headers, data=json.dumps(data))
            response.raise_for_status()  # 检查请求是否成功
            print("请求成功")
            print("状态码:", response.status_code)

            # 解析响应数据
            result = response.json()
            if int(result.get('code')) != 200:
                return 0

            print("API状态码:", result.get('code'))  # 输出: 200
            print("返回数据:", result.get('data'))  # 输出: 1299
            print("消息:", result.get('message'))  # 输出: 成功
            print("服务器时间:", result.get('serverTime'))
            #Todo 一个获取任务状态的节点，前期先sleep
            time.sleep(15)

            return self._post_es(200, result.get('data'))

        except requests.exceptions.RequestException as e:
            print(f"请求失败: {e}")

    def _post_es(self, size, back_id):
        # Elasticsearch请求配置
        url = 'http://10.68.37.201:9200/rule_backtest_case/_search'
        headers = {
            'Content-Type': 'application/json',
            'Authorization': 'Basic ZWxhc3RpYzpscUVwQjdjM2ZUdzNZbXNCeG9SYw=='
        }
        payload = {
            "size": size,
            "query": {
                "match": {
                    "backTestId": back_id
                }
            }
        }

        try:
            # 发送请求
            response = requests.post(url, headers=headers, json=payload)
            response.raise_for_status()  # 检查请求是否成功
            data = response.json()

            # 从响应中提取所有_source数据
            if 'hits' in data and 'hits' in data['hits']:
                source_data = [hit['_source'] for hit in data['hits']['hits']]

                # 创建DataFrame
                df = pd.DataFrame(source_data)

                print("数据基本信息：")
                df.info()

                # 显示数据集行数和列数
                rows, columns = df.shape
                if rows > 5:
                    return 0.8
                elif 1 < rows <= 5:
                    return 0.4
                else:
                    return 0
                # if rows < 10:
                #     # 不足10行数据显示全量数据信息
                #     print("数据全部内容信息：")
                #     print(df.to_csv(sep='\t', na_rep='nan'))
                # else:
                #     # 超过10行数据显示数据前几行信息
                #     print("数据前几行内容信息：")
                #     print(df.head().to_csv(sep='\t', na_rep='nan'))
            else:
                return 0

        except requests.exceptions.HTTPError as http_err:
            print(f"HTTP错误: {http_err}")
            print(f"响应内容: {response.text}")  # 打印详细错误信息
        except requests.exceptions.RequestException as req_err:
            print(f"请求异常: {req_err}")
        except json.JSONDecodeError as json_err:
            print(f"JSON解析错误: {response.text[:200]}...")  # 打印响应前200个字符
        except Exception as err:
            print(f"其他错误: {err}")

api.add_resource(Popular, '/popular/get/<string:city>')
# 注册资源
api.add_resource(CmpController, '/cmp/query')

if __name__ == "__main__":
    app.run(debug=True, port=9980)