from server.models.Base import Base
from server.models.Term import Term
from server.models.Course import Course
from server.models.User import User
import psycopg2.extras
import datetime
import time
from server import conn


class Note(Base):
    ATTRIBUTES = {}
    COLUMNS = {}
    TABLE = 'notes'
    def __init__(self):
        super().__init__()
        self.ATTRIBUTES = {
            'id' : 0,
            'title' : '',
            'content' : '',
            'lecturer' : 'Unknown',
            'link' : '',
            'course_id' : '',
            'course_code' : 0,
            'english' : False,
            'term_id' : 0,
            'slug' : '',
            'user_id' : 0
        }
        self.COLUMNS = {
            'title' : '',
            'content' : '',
            'lecturer' : 'Unknown',
            'link' : '',
            'course_id' : '',
            'course_code' :0,
            'english' : False,
            'term_id' : 0,
            'slug' : '',
            'user_id' : 0
        }

    def validate(self):
        # term id exist
        term = Term().where('id', self.ATTRIBUTES['term_id']).first()
        if term.exists() is False:
            self.setError("Term not found")

        course = Course().where('id', self.ATTRIBUTES['course_id']).first()
        if course.exists() is False:
            self.setError("Course not found")

        user = User().where('id', self.ATTRIBUTES['user_id']).first()
        if user.exists() is False:
            self.setError("You are not the owner of this note")

        if self.getErrors():
            return False
        return True

