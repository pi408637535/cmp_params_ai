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
    "servers": [
        {
            "url": "http://127.0.0.1:9980"
        }
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
        },
        "/cmp/query": {
            "post": {
                "tags": ["Cmp"],
                "summary": "Query data with specified parameters",
                "operationId": "queryCmpData",
                 "consumes": [
                    "application/json"
                ],
                "parameters": [
                    {
                        "name": "body",
                        "in": "body",
                        "required": True,
                        "schema": {
                            "type": "object",
                            "properties": {
                                "filterParamDetail": {
                                    "type": "array",
                                    "items": {
                                        "type": "object",
                                        "properties": {
                                            "conditionType": {
                                                "type": "string"
                                            },
                                            "condition": {
                                                "type": "array",
                                                "items": {
                                                    "type": "string"
                                                }
                                            },
                                            "includeString": {
                                                "type": "string"
                                            }
                                        }
                                    }
                                },
                                "featureId": {
                                    "type": "integer"
                                },
                                "ruleParams": {
                                    "type": "string"
                                },
                                "dataStartTime": {
                                    "type": "integer"
                                },
                                "dataEndTime": {
                                    "type": "integer"
                                }
                            }
                        },
                        "example": {  # 新增example字段展示案例数据
                            "filterParamDetail": [
                                {
                                    "conditionType": "Market",
                                    "condition": [
                                        "US"
                                    ],
                                    "includeString": "in"
                                }
                            ],
                            "featureId": 222,
                            "ruleParams": "{\"quantitythresold\":\"100\"}",
                            "dataStartTime": 1745510400000,
                            "dataEndTime": 1748361600000
                        }
                    },

                ],


                "responses": {
                    "200": {
                        "description": "Success, returns a floating-point result",
                        "schema": {
                            "type": "number"
                        }
                    },
                    "400": {
                        "description": "Invalid request parameters",
                        "schema": {
                            "type": "string"
                        }
                    },
                    "500": {
                        "description": "Internal server error",
                        "schema": {
                            "type": "string"
                        }
                    }
                }
            }
        }
    }
}