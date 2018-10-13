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
            """
        )
        if command is not None:
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
