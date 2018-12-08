from server.models.Base import Base
from server import conn, server, jwt, bcrypt
import psycopg2.extras
import random
import datetime
import time

from server.models.Course import Course
from server.models.Lecturer import Lecturer
from server.models.Term import Term
from server.models.User import User


class GradeDistribution(Base):
    ATTRIBUTES = {}
    COLUMNS = {}
    HIDDEN = {}
    TABLE = 'grade_distributions'

    def __init__(self):
        super().__init__()
        self.ATTRIBUTES = {
            'id': '',
            'lecturer_id': '',
            'user_id': '',
            'image': '',
            'course_id': '',
            'course_code': '',
            'english': False,
            'term_id': ''
        }
        self.COLUMNS = {
            'lecturer_id': '',
            'user_id': '',
            'image': '',
            'course_id': '',
            'course_code': '',
            'english': '',
            'term_id': '',
        }
        self.HIDDEN = {}

    def validate(self):
        term = Term().where('id', self.ATTRIBUTES['term_id']).first()
        if term.exists() is False:
            self.setError('Term could not found')
        else:
            self.plus('term', term.data())

        lecturer = Lecturer().where('id', self.ATTRIBUTES['lecturer_id']).first()
        if lecturer.exists() is False:
            self.setError('Lecturer could not found')
        else:
            self.plus('lecturer', lecturer.data())

        course = Course().where('id', self.ATTRIBUTES['course_id']).first()
        if course.exists() is False:
            self.setError('Course could not found')
        else:
            self.plus('course', course)

        user = User().where('id', self.ATTRIBUTES['user_id']).first()
        if user.exists() is False:
            self.setError('User could not found')
        else:
            self.plus('user', user)

        if not self.getErrors():
            return True
        return False

    def generateImageName(self):
        return ''.join(random.choice('abcde') for _ in range(50)) + '.jpg'
