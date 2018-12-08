from server.models.Base import Base
from server import conn, server, jwt, bcrypt
import psycopg2.extras


class Term(Base):
    ATTRIBUTES = {
        'season': '',
        'term_year': 0,
        'id': 0
    }
    COLUMNS = {
        'season',
        'term_year'
    }
    TABLE = 'terms'
