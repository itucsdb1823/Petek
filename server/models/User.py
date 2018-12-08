import json
import sys

from server.models.Base import Base
from server import conn, bcrypt
import datetime
import time
from flask_jwt_simple import create_jwt, jwt_required, get_jwt_identity
import psycopg2.extras
from validate_email import validate_email
from slugify import slugify


class User(Base):
    ATTRIBUTES = {}
    COLUMNS = {}
    HIDDEN = {}
    TABLE = 'users'

    def __init__(self):
        super().__init__()
        self.ATTRIBUTES = {
            'name': '',
            'email': '',
            'slug': '',
            'id': ''
        }
        self.COLUMNS = {
            'name': '',
            'email': '',
            'password': ''
        }
        self.HIDDEN = {
            'password': ''
        }


    def email_is_valid(self, email):
        is_valid = validate_email(email)
        if is_valid is False:
            print("This is not a valid email")
            return False
        return True

    def hasRole(self, roles):
        cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
        if isinstance(roles, list):
            cur.execute("SELECT id FROM roles WHERE name IN roles")
            role_ids = cur.fetchall()
            for role_id in role_ids:
                cur.execute("SELECT * FROM user_roles WHERE user_id=%s AND role_id=%s", (self.id, role_id))
                exist = cur.fetchone()
                if exist:
                    return True
        else:
            cur.execute("SELECT id FROM roles WHERE name=%s", (roles,))
            role_id = cur.fetchone()['id']
            cur.execute("SELECT * FROM user_roles WHERE user_id=%s AND role_id=%s", (self.id, role_id))
            exist = cur.fetchone()
            if exist:
                return True
        return False

    def validate(self):
        user = User().where('email', self.ATTRIBUTES['email']).first().exists()
        if user:
            self.setError('There is already an email with this address')

        if not self.getErrors():
            return True
        return False

    def generateToken(self):
        return {'jwt': create_jwt(identity={
            'id': self.ATTRIBUTES['id']
        })}
