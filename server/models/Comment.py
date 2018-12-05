from server.models.Base import Base
import psycopg2.extras
import datetime
import time
from server import conn


class Comment(Base):
    id = 0
    comment = ''
    user_id = 0
    type = 'Unknown'
    type_id = 0

    def __init__(self, _id=0, _comment='', _user_id=0, _type='Unknown', _type_id=0):
        self.id = _id
        self.comment = _comment
        self.user_id = _user_id
        self.type = _type
        self.type_id = _type_id
        self.errors = []

    def validate(self):
        cur = conn.cursor()
        cur.execute("SELECT * FROM users WHERE id=%s LIMIT 1", (self.user_id,))
        user = cur.fetchone()
        if user is None:
            self.errors.append("User not found in the database!")

        if self.comment == "" or self.comment is None:
            self.errors.append("Comment cannot be empty")

        if self.type == 'lecturers':
            cur.execute("SELECT * FROM lecturers WHERE id=%s LIMIT 1",
                        (self.type_id,))
            lecturer = cur.fetchone()
            if lecturer is None:
                self.errors.append("Lecturer not found in the database!")
        elif self.type == 'notes':
            cur.execute("SELECT * FROM notes WHERE id=%s LIMIT 1",
                        (self.type_id,))
            note = cur.fetchone()
            if note is None:
                self.errors.append("Note not found in the database!")
        else:
            self.errors.append("Comment type is not valid")

        cur.close()
        if self.errors:
            return False
        return True

    def delete(self):
        cur = conn.cursor()
        cur.execute("DELETE FROM comments WHERE id=%s AND user_id=%s", (self.id, self.user_id))
        conn.commit()
        cur.close()

    def get(self, id):
        cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
        # Get the comment
        cur.execute("SELECT * FROM comments WHERE id=%s LIMIT 1", (id,))
        comment = cur.fetchone()
        # Get the user info of the comment
        cur.execute("SELECT name, slug, email FROM users WHERE id=%s LIMIT 1", (comment['user_id'],))
        comment['user'] = cur.fetchone()
        cur.close()
        return comment

    def Update(self):
        if self.validate() is False:
            return False
        commentText = self.comment

        cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
        cur.execute("SELECT * FROM comments WHERE id=%s AND "
                    "user_id=%s LIMIT 1", (self.id, self.user_id))
        comment = cur.fetchone()
        if comment is None:
            self.errors.append("This comment doesn't exist in the database")
            return False

        cur.execute("""UPDATE comments SET comment=%s WHERE
                    id = %s""", (commentText, comment['id']))
        conn.commit()
        cur.close()
        return True

    def save(self):
        if self.validate() is False:
            return False

        ts = time.time()
        created_at = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')

        cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
        cur.execute("""INSERT INTO comments(comment, user_id, type, type_id)
            VALUES(%s, %s, %s, %s) RETURNING id""",
            (str(self.comment), int(self.user_id), self.type, int(self.type_id)))
        conn.commit()
        cur.close()
        return True

    def all(self):
        cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
        cur.execute("SELECT * FROM comments ORDER BY created_at DESC")
        comments = cur.fetchall()
        for comment in comments:
            cur.execute("SELECT name, slug, email FROM users WHERE id=%s LIMIT 1", (comment['user_id'],))
            comment['user'] = cur.fetchone()
        cur.close()
        return comments




