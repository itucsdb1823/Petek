from server.models.Base import Base
from server import conn, bcrypt
import datetime
import string
import random
import time
from flask_jwt_simple import create_jwt, jwt_required, get_jwt_identity
import psycopg2.extras
from validate_email import validate_email
from slugify import slugify


def id_generator(size=6, chars=string.ascii_uppercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))


class User(Base):
    name = ''
    password = ''
    email = ''
    token = ''
    slug = ''
    id = ''

    def __init__(self, name, password, email):
        self.name = name
        self.password = password
        self.email = email

    def email_is_valid(self, email):
        is_valid = validate_email(email)
        if is_valid is False:
            print("This is not a valid email")
            return False
        return True

    def email_is_unique(self, email):
        cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
        cur.execute("SELECT * FROM users WHERE email=%s LIMIT 1", (email,))
        user = cur.fetchone()
        if user is not None:
            return False
        return True

    def generate_slug(self, name):
        cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
        slug = slugify(name)
        slug_is_not_unique = True
        i = 2
        tslug = slug
        while slug_is_not_unique:
            cur.execute("SELECT * FROM users WHERE slug=%s LIMIT 1", (slug,))
            found = cur.fetchone()
            if found is not None:
                slug = tslug + str(i)
                i += 1
            else:
                slug_is_not_unique = False
        return slug

    def is_valid(self):
        if self.email_is_valid(email=self.email) and \
                self.email_is_unique(email=self.email):
            return True
        return False

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
        self.slug = self.generate_slug(name=self.name)

        # check uniqueness of the user, create slug from name and check its uniqueness

        cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
        cur.execute("SELECT * FROM users WHERE email=%s LIMIT 1", (self.email,))
        user = cur.fetchone()
        if user is not None:
            print("There is already a user with this email")
            return "There is already a user with this email"

        cur.execute("SELECT * FROM users WHERE name=%s LIMIT 1", (self.name,))
        user = cur.fetchone()
        if user is not None:
            print("There is already a user with this username")
            return "There is already a user with this username"

        # End checking

        cur.execute(
            "INSERT INTO users(name, email, password, slug, created_at) VALUES(%s, %s, %s, %s, %s) returning id",
            (self.name, self.email, hashed_password, self.slug, str(created_at)))

        self.id = cur.fetchone()['id']

        token = {'jwt': create_jwt(identity={
            'id': self.id

        })}

        cur.execute("INSERT INTO tokens(user_id, token, created_at) VALUES(%s, %s, %s)",
                    (str(self.id), str(token['jwt']), str(created_at)))

        conn.commit()
        cur.close()
        return token['jwt']

    def delete(self, id):

        cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
        cur.execute("DELETE FROM users WHERE users.id == id")
        conn.commit()
        cur.close()
