from flask_restful import Resource
from flask import jsonify
import psycopg2
from server.config import config
from server import cur, conn
from server.models.User import User


class Auth(Resource):
    def get(self):
        user = User(username='yavuz', password='asdf')
        user.save()
        command = (
            """
            CREATE TABLE IF NOT EXISTS users (
                id PRIMARY KEY,
                name VARCHAR(255),
                email VARCHAR(255) UNIQUE
            )
            """)
        cur.execute(command)
        conn.commit()

        return jsonify({
            'sa': 'as'
        })

    def post(self):
        pass

    def put(self):
        pass

    def delete(self):
        pass
