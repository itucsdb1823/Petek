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
