from libs.query_helper import queryHelper, engine
from psycopg2 import DatabaseError
from pprint import pprint

class TodoManager:
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
                todo_id=todo_id
            )
            )

        return data

    def createTodo(self, data):
        
        with engine.connect() as conn:
            trans = conn.begin()
            try:
                a = conn.execute(
                    '''
                        insert into todo (title , description , status_id, due) values (?, ?, ?, ?)
                    ''',
                    data['title'],
                    data['description'],
                    data['status_id'],
                    data['due']
                )
                b = trans.commit()
                return a, b
            except DatabaseError as error:
                pprint(error)
                trans.rollback()
                return None
