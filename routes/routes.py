from flask_restful import Api
from routes.todos import TodosResource, TodoResource
from routes.todo_status import TodoStatusResource


def init_routes(api_app):
    api_rest = Api(api_app)

    api_rest.add_resource(TodoResource, '/todo/<int:todo_id>')
    api_rest.add_resource(TodosResource, '/todo')
    api_rest.add_resource(TodoStatusResource, '/status')
