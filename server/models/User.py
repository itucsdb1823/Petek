from server.models.Base import Base
from server import conn, server, jwt, bcrypt
import datetime
import string
import random
import time
from flask_jwt_simple import create_jwt, jwt_required, get_jwt_identity
import psycopg2.extras


def id_generator(size=6, chars=string.ascii_uppercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))


class User(Base):
    name = ''
    password = ''
    email = ''
    token = ''

    def __init__(self, name, password, email):
        self.name = name
        self.password = password
        self.email = email

    @staticmethod
    def get(email, password):
        cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
        cur.execute("SELECT * FROM users WHERE email=%s LIMIT 1", (email,))
        user = cur.fetchone()
        cur.close()
        if user and bcrypt.check_password_hash(user['password'], password):
            return user
        return None

    def create(self):
        hashed_password = bcrypt.generate_password_hash(self.password).decode('utf-8')
        ts = time.time()
        created_at = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')

        # check uniqueness of the user, create slug from name and check its uniqueness

        cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
        cur.execute("INSERT INTO users(name, email, password, slug, created_at) VALUES(%s, %s, %s, %s, %s) returning id",
                    (self.name, self.email, hashed_password, id_generator(20), str(created_at)))

        user_id = cur.fetchone()['id']

        token = {'jwt': create_jwt(identity={
            'id': user_id

        })}

        cur.execute("INSERT INTO tokens(user_id, token, created_at) VALUES(%s, %s, %s)", (str(user_id), str(token['jwt']), str(created_at)))

        conn.commit()
        cur.close()
        return token
