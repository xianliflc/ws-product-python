from libs.query_helper import queryHelper, engine, update, delete
from psycopg2 import DatabaseError
from pprint import pprint


class TodoManager:
    def getTodoStatusList(self):
        data = queryHelper('''
            SELECT
                ts.id,
                ts.display_name,
                ts.name
            FROM todo_status AS ts 
            ORDER BY ts.id ASC
            ''')

        return data

    def getTodoStatusById(self, status_id):
        data = queryHelper('''
            SELECT
                ts.id,
                ts.display_name,
                ts.name
            FROM todo_status AS ts
            WHERE ts.id = {status_id} 
            ORDER BY ts.id ASC
            '''.format(status_id=status_id)
        )

        return data

    def getTodos(self):
        data = queryHelper('''
            SELECT
                t.id,
                t.title,
                t.description,
                t.due,
                ts.display_name,
                ts.name,
                CASE WHEN t.due < datetime('now') THEN 1 ELSE 0 END AS is_expired
            FROM todo AS t 
                INNER JOIN todo_status AS ts
                    ON t.status_id = ts.id 
            ORDER BY t.id ASC
            ''')

        return data

    def getTodoById(self, todo_id):
        data = queryHelper('''
            SELECT
                t.id,
                t.title,
                t.description,
                t.due,
                ts.display_name,
                ts.name,
                CASE WHEN t.due < datetime('now') THEN 1 ELSE 0 END AS is_expired
            FROM todo AS t 
                INNER JOIN todo_status AS ts
                    ON t.status_id = ts.id 
            WHERE
                t.id = {todo_id}
            '''.format(
                todo_id=todo_id)
            )

        return data

    def deleteTodoById(self, todo_id):
        return delete('todo', {'id': todo_id})

    def createTodo(self, data):
        status = self.getTodoStatusById(data['status_id'])
        if not status:
            raise ValueError('Bad status id')
        with engine.connect() as conn:
            trans = conn.begin()
            try:
                result = conn.execute(
                    '''
                        insert into todo (title , description , status_id, due) values (?, ?, ?, ?)
                    ''',
                    data['title'],
                    data['description'],
                    data['status_id'],
                    data['due']
                )
                trans.commit()
            except DatabaseError as error:
                result = False
                trans.rollback()
            finally:
                conn.close()
                return {'id': result.lastrowid} if result else False

    def updateTodoById(self, todo_id, data):
        if 'status_id' in data:
            status = self.getTodoStatusById(data['status_id'])
            if not status:
                raise ValueError('Bad status id')
        return update('todo', data, {'id': todo_id})
