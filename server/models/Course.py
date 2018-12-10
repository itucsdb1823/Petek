from server.models.Base import Base
from server import conn, server, jwt, bcrypt
import psycopg2.extras


class Course(Base):
    ATTRIBUTES = {}
    COLUMNS = {}
    TABLE = 'courses'
    TIMESTAMPS = False

    def __init__(self):
        super().__init__()
        self.ATTRIBUTES = {
            'name': '',
            'id': 0
        }
        self.COLUMNS = {
            'name'
        }
        self.TIMESTAMPS = False

    def validate(self):
        course = Course().where('name', self.ATTRIBUTES['name']).first()
        if course.exists():
            self.setError('Course already exists')

        if self.getErrors():
            return False
        return True


