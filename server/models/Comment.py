from server.models.Base import Base
from server.models.User import User
from server.models.Lecturer import Lecturer
from server.models.Note import Note
import psycopg2.extras
import datetime
import time
from server import conn


class Comment(Base):
    ATTRIBUTES = {}
    COLUMNS = {}
    TABLE = 'comments'

    def __init__(self):
        super().__init__()
        self.ATTRIBUTES = {
            'comment': '',
            'user_id': 0,
            'type': '',
            'type_id': 0,
            'id': 0
        }
        self.COLUMNS = {
            'comment',
            'user_id',
            'type',
            'type_id'
        }

    def validate(self):
        user = User().where('id', self.ATTRIBUTES['user_id']).first()
        if user.exists() is False:
            self.setError("User not found in the database!")

        if self.ATTRIBUTES['type'] == 'lecturers':
            lecturer = Lecturer().where('id', self.ATTRIBUTES['type_id']).first()
            if lecturer.exists() is False:
                self.setError("Lecturer not found in the database!")
        elif self.ATTRIBUTES['type'] == 'notes':
            note = Note().where('id', self.ATTRIBUTES['type_id']).first()
            if note.exists() is False:
                self.setError("Note not found in the database!")
        else:
            self.setError("Comment type is not valid")

        if self.getErrors():
            return False
        return True
