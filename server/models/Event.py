from server.models.Base import Base
from server.models.User import User
import psycopg2.extras
import datetime
import time
from server import conn


class Event(Base):
    ATTRIBUTES = {}
    COLUMNS = {}
    TABLE = 'events'

    def __init__(self):
        super().__init__()
        self.ATTRIBUTES = {
            'title': '',
            'description': '',
            'user_id': 0,
            'started_at': '',
            'max_participant': 0,
            'id': 0
        }
        self.COLUMNS = {
            'title',
            'description',
            'user_id',
            'started_at',
            'max_participant'
        }


    def validate(self):
        user = User().where('id', self.ATTRIBUTES['user_id']).first()
        if user is None:
            self.setError("User not found in the database!")
        if self.getErrors():
            return False
        return True
