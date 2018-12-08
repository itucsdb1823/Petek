from server.models.Base import Base
from server.models.User import User
from server.models.Lecturer import Lecturer
from server.models.Note import Note
import psycopg2.extras
import datetime
import time
from server import conn


class Comment(Base):
    ATTRIBUTES = {
        'comment': '',
        'user_id': 0,
        'type': '',
        'type_id': 0,
        'id': 0
    }
    COLUMNS = {
        'comment',
        'user_id',
        'type',
        'type_id'
    }
    TABLE = 'comments'

    def validate(self):
        user = User().where('id', self.ATTRIBUTES['user_id']).first()
        if user is None:
            self.setError("User not found in the database!")

        if self.type == 'lecturers':
            lecturer = Lecturer().where('id', self.ATTRIBUTES['type_id']).first()
            if lecturer is None:
                self.setError("Lecturer not found in the database!")
        elif self.type == 'notes':
            note = Note().where('id', self.ATTRIBUTES['type_id']).first()
            if note is None:
                self.setError("Note not found in the database!")
        else:
            self.setError("Comment type is not valid")

        if self.getErrors():
            return False
        return True
