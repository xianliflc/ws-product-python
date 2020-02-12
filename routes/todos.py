from flask_restful import Resource
import libs.http_status as status
import libs.json_response as response
from libs.validator import Validator, require_json
from managers.todo_manager import TodoManager
from pprint import pprint

manager = TodoManager()


class TodosResource(Resource):
    def get(self):
        data = manager.getTodos()

        return response.response(data, status.HTTP_OK.get('code'))

    @require_json
    @Validator("todo_validator.TodoCreationSchema")
    def post(self, data=None, errors=None):
        if errors:
            return response.error(errors, status.HTTP_BAD_REQUEST.get('code'))

        try:
            result = manager.createTodo(data)

            if result:
                return response.response(result, status.HTTP_CREATED.get('code'))
            else:
                return response.error(
                    status.HTTP_BAD_REQUEST.get('message'),
                    status.HTTP_BAD_REQUEST.get('code')
                )
        except ValueError as error:
            return response.error(
                str(error),
                status.HTTP_BAD_REQUEST.get('code')
            )


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

    @require_json
    @Validator("todo_validator.TodoUpdateSchema")
    def patch(self, todo_id, data=None, errors=None):
        if errors or not data:
            return response.error(errors, status.HTTP_BAD_REQUEST.get('code'))
        todo = manager.getTodoById(todo_id)

        if not todo:
            return response.error({
                'message': status.HTTP_NOT_FOUND.get('message')
            }, status.HTTP_NOT_FOUND.get('code'))

        try:
            result = manager.updateTodoById(todo_id, data)

            if result:
                return response.response(None, status.HTTP_NOTHING.get('code'))
            else:
                return response.error(
                    status.HTTP_BAD_REQUEST.get('message'),
                    status.HTTP_BAD_REQUEST.get('code')
                )
        except ValueError as error:
            return response.error(
                str(error),
                status.HTTP_BAD_REQUEST.get('code')
            )

    def delete(self, todo_id):
        manager = TodoManager()
        data = manager.getTodoById(todo_id)

        if data:
            result = manager.deleteTodoById(todo_id)
            if result:
                return response.response(None, status.HTTP_NOTHING.get('code'))
            else:
                return response.error(
                    status.HTTP_INTERNAL_ERROR.get('message'),
                    status.HTTP_INTERNAL_ERROR.get('code')
                )                
        else:
            return response.error({
                'message': status.HTTP_NOT_FOUND.get('message')
            }, status.HTTP_NOT_FOUND.get('code'))
