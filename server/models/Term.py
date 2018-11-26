from server.models.Base import Base
from server import conn, server, jwt, bcrypt
import psycopg2.extras


class Term(Base):
    def all(self):
        cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
        cur.execute("SELECT * FROM terms ORDER BY term_year ASC")
        terms = cur.fetchall()
        cur.close()
        return terms
