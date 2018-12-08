from server.models.Base import Base
from server import conn, server, jwt, bcrypt
import psycopg2.extras


class Course(Base):
    ATTRIBUTES = {
        'name': '',
        'id': 0
    }
    COLUMNS = {
        'name'
    }
    TABLE = 'courses'
    TIMESTAMPS = False
