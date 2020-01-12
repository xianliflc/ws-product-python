from flask import jsonify
import sqlalchemy
import os


engine = sqlalchemy.create_engine(os.getenv('SQL_URI'))

def queryHelper(query):
    with engine.connect() as conn:
        result = conn.execute(query).fetchall()
        return [dict(row.items()) for row in result]