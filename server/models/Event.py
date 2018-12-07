from server.models.Base import Base
import psycopg2.extras
import datetime
import time
from server import conn


class Event(Base):
    id = 0
    title = ''
    description = ''
    user_id = 0
    started_at = ''
    max_participant = 0

    def __init__(self, _id=0, _title='', _description='',
                 _user_id=0, _started_at='Unknown', _max_participant=0):
        self.id = _id
        self.title = _title
        self.description = _description
        self.user_id = _user_id
        self.started_at = _started_at
        self.max_participant = _max_participant
        self.errors = []

    def validate(self):
        cur = conn.cursor()
        cur.execute("SELECT * FROM users WHERE id=%s LIMIT 1", (self.user_id,))
        user = cur.fetchone()
        if user is None:
            self.errors.append("User not found in the database!")

        if self.title == "" or self.title is None:
            self.errors.append("Title cannot be empty")

        if self.description == "" or self.description is None:
            self.errors.append("Description cannot be empty")

        cur.close()
        if self.errors:
            return False
        return True

    def delete(self):
        cur = conn.cursor()
        cur.execute("DELETE FROM events WHERE id=%s AND user_id=%s", (self.id, self.user_id))
        conn.commit()
        cur.close()

    def get(self, id):
        cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
        cur.execute("SELECT * FROM events WHERE id=%s LIMIT 1", (id,))
        comment = cur.fetchone()
        cur.execute("SELECT name, slug, email FROM users WHERE id=%s LIMIT 1", (comment['user_id'],))
        comment['user'] = cur.fetchone()
        cur.close()
        return comment

    def update(self):
        if self.validate() is False:
            return False
        title = self.title
        description = self.description
        started_at = self.started_at
        max_participant = self.max_participant

        cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
        cur.execute("SELECT * FROM events WHERE id=%s AND "
                    "user_id=%s LIMIT 1", (self.id, self.user_id))
        event = cur.fetchone()
        if event is None:
            self.errors.append("This event doesn't exist in the database")
            return False

        cur.execute("""UPDATE events SET title=%s, description=%s,
            started_at=%s, max_participant = %s WHERE id = %s""",
                    (title, description, started_at, max_participant, event['id']))

        conn.commit()
        cur.close()
        return True

    def save(self):
        if self.validate() is False:
            return False

        ts = time.time()
        created_at = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')

        cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
        cur.execute("""INSERT INTO events(title, description, user_id, 
            started_at, max_participant, created_at)
            VALUES(%s, %s, %s, %s, %s, %s) RETURNING id""",
            (str(self.title), str(self.description), int(self.user_id),
             str(self.started_at), int(self.max_participant), str(created_at)))
        conn.commit()
        cur.close()
        return True

    def all(self):
        cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
        cur.execute("SELECT * FROM events ORDER BY created_at DESC")
        events = cur.fetchall()
        for event in events:
            cur.execute("SELECT name, slug, email FROM users WHERE id=%s LIMIT 1", (event['user_id'],))
            event['user'] = cur.fetchone()
        cur.close()
        return events
