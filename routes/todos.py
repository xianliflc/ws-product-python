from flask_restful import Resource
from flask import request, jsonify
# from libs.rate_limiter import rate_limiter
from libs.query_helper import queryHelper
import libs.http_status as status
import libs.json_response as response
from libs.validator import Validator, require_json
from managers.todo_manager import TodoManager
from pprint import pprint


class TodosResource(Resource):
    def get(self):
        manager = TodoManager()
        data = manager.getTodos()

        return response.response(data, status.HTTP_OK.get('code'))

    @require_json
    @Validator("todo_validator.TodoCreationSchema")
    def post(self, data=None, errors=None):
        if errors:
            return response.error(errors, status.HTTP_BAD_REQUEST.get('code'))
        # pprint(data)
        manager = TodoManager()
        result = manager.createTodo(data)
        # pprint(result)
        return response.response(errors, status.HTTP_CREATED.get('code'))

        # if result[1]:
        #     return response.response(result[0], status.HTTP_CREATED.get('code'))
        # else:
        #     return response.error(result[0], status.HTTP_BAD_REQUEST.get('code'))


class TodoResource(Resource):
    def get(self, todo_id):
        manager = TodoManager()
        data = manager.getTodoById(todo_id)

        if data:
            return response.response(data, status.HTTP_OK.get('code'))
        else:
            return response.error({
                'message': status.HTTP_NOT_FOUND.get('message')
            }, status.HTTP_NOT_FOUND.get('code'))
