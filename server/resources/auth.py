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
                id serial PRIMARY KEY,
                name varchar(255) NOT NULL,
                email varchar(255) UNIQUE NOT NULL
                password varchar(255) NOT NULL
                confirmation_code varchar(255) NULL
                confirmed boolean NOT NULL DEFAULT 0
                banned boolean NOT NULL DEFAULT 0
                slug varchar(255) UNIQUE
                created_at timestamp NOT NULL
                profile_picture bytea
            )
            """

        )
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
