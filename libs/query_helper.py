from psycopg2 import DatabaseError
import sqlalchemy
import os
from datetime import datetime


engine = sqlalchemy.create_engine(os.getenv('SQL_URI'), convert_unicode=True)


def queryHelper(query):
    with engine.connect() as conn:
        result = conn.execute(query).fetchall()
        return [dict(row.items()) for row in result]


def _convertValue(value):
    if isinstance(value, bool):
        return "true" if value else "false"
    elif isinstance(value, str) or isinstance(value, datetime):
        return ("\'" + str(value) + "\'")
    else:
        return str(value)


def update(table, data, where):
    with engine.connect() as conn:
        result = False
        try:
            data_keys = data.keys()
            where_keys = where.keys()
            update_data = ', '.join(
                [str(key) + '=' + _convertValue(data[key]) for key in data_keys]
            )
            where_data = ' and '.join(
                [str(key) + '=' + _convertValue(where[key]) for key in where_keys]
            )
            conn.execute(
                '''
                    update {table} set {update_data} where {where_data}
                '''.format(
                    update_data=update_data,
                    where_data=where_data,
                    table=table
                )
            )

            result = True
        except DatabaseError as error:
            trans.rollback()
        finally:
            conn.close()
        return result


def delete(table, where):
    with engine.connect() as conn:
        result = False
        try:
            where_keys = where.keys()
            where_data = ' and '.join(
                [str(key) + '=' + _convertValue(where[key]) for key in where_keys]
            )
            conn.execute(
                '''
                    DELETE FROM {table} where {where_data}
                '''.format(
                    where_data=where_data,
                    table=table
                )
            )

            result = True
        except DatabaseError as error:
            trans.rollback()
        finally:
            conn.close()
        return result
