import datetime
import time
from server import conn, server, jwt, bcrypt
from server.models.Base import Base
from server.models.User import User
from slugify import slugify
import psycopg2.extras
from flask_jwt_simple import create_jwt, jwt_required, get_jwt_identity


class Lecturer(Base):
    ATTRIBUTES = {
        'name' : '',
        'email' : '',
        'user_id' : 0,
        'slug' : '',
        'grade_distributions' : [],
        'id': 0
    }
    COLUMNS = {
        'name' : '',
        'email' : '',
        'user_id' : 0,
        'slug' : '',
        'grade_distributions' : []
    }
    TABLE = 'lecturers'

    def validate(self):
        user = User().where('id', self.ATTRIBUTES['user_id']).first()
        if user is None:
            self.setError("User not found in the database!")
        lecturer = Lecturer().where('email', self.ATTRIBUTES['email']).first()
        if lecturer is not None:
            self.setError("There is already a lecturer added with this email.")

        if self.getErrors():
            return False
        return True
