from server.models.Base import Base
from server import cur, conn, server, jwt


class User(Base):
    name = ''
    password = ''

    def __init__(self, name, password):
        self.name = name
        self.password = password

    @staticmethod
    def get(name, password):
        cur.execute("SELECT * FROM users WHERE name=%s", (name,))
        user = cur.fetchone()
        if user and user['password'] == password:
            return user
        return None
