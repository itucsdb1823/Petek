from server.models.Base import Base
from server import conn, server, jwt, bcrypt
import psycopg2.extras


class Term(Base):
    ATTRIBUTES = {}
    COLUMNS = {}
    TABLE = 'terms'
    TIMESTAMPS = False
    def __init__(self):
        super().__init__()
        self.ATTRIBUTES = {
            'season': '',
            'term_year': 0,
            'id': 0
        }
        self.COLUMNS = {
            'season',
            'term_year'
        }
        self.TIMESTAMPS = False

