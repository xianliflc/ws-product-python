from flask_restful import Resource
import libs.http_status as status
import libs.json_response as response
from managers.todo_manager import TodoManager

manager = TodoManager()


class TodoStatusResource(Resource):
    def get(self):
        data = manager.getTodoStatusList()

        return response.response(data, status.HTTP_OK.get('code'))