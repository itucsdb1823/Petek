from server.models import Base


class User(Base):
    username = ''
    password = ''

    def __init__(self, username, password):
        self.username = username
        self.password = password

