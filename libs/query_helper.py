from flask import jsonify
import sqlalchemy
import os


engine = sqlalchemy.create_engine(os.getenv('SQL_URI'), convert_unicode=True)


def queryHelper(query):
    with engine.connect() as conn:
        result = conn.execute(query).fetchall()
        return [dict(row.items()) for row in result]

# def insert(query):
#     with engine.connect() as conn:
#         result = conn.execute(query).fetchall()
#         return [dict(row.items()) for row in result]