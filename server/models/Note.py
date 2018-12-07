from server.models.Base import Base
import psycopg2.extras
import datetime
import time
from server import conn


class Note(Base):
    id = 0
    title = ''
    content = ''
    lecturer = 'Unknown'
    link = ''
    course_id = 0
    course_code = 0
    english = False
    term_id = 0
    slug = ''
    user_id = 0

    def __init__(
            self, _id=0, title='', content='',
            lecturer='', link='', course_id=0, course_code=0, english=False,
            term_id=0,
            user_id=0
    ):
        self.errors = []
        self.title = title
        self.content = content
        self.lecturer = lecturer
        self.link = link
        self.course_id = int(course_id)
        self.course_code = int(course_code)
        self.english = bool(english)
        self.term_id = int(term_id)
        self.id = int(_id)
        self.user_id = int(user_id)

    def delete(self):
        cur = conn.cursor()
        cur.execute("DELETE FROM notes WHERE id=%s AND user_id=%s", (self.id, self.user_id))
        conn.commit()
        cur.close()

    def update(self):
        title = self.title
        content = self.content
        lecturer = self.lecturer
        link = self.link
        english = self.english
        course_id = self.course_id
        course_code = self.course_code
        term_id = self.term_id

        if self.validate() is False:
            return False

        cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)

        cur.execute("SELECT * FROM notes WHERE id=%s AND "
                    "user_id = %s LIMIT 1", (self.id, self.user_id))
        note = cur.fetchone()

        if note is None:
            self.errors.append("This note doesn't exist in the database")
            return False

        cur.execute("UPDATE notes SET "
                    "title=%s, "
                    "content=%s, "
                    "lecturer=%s, "
                    "link=%s, "
                    "english=%s, "
                    "course_id=%s, course_code=%s, term_id=%s WHERE id=%s",
                    (title, content, lecturer, link, english, course_id,
                     course_code, term_id, note['id']))

        conn.commit()
        cur.close()
        return True

    def get(self, slug):
        cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
        cur.execute("SELECT * FROM notes WHERE slug=%s LIMIT 1", (slug,))

        note = cur.fetchone()
        cur.execute("SELECT id, name, slug, email FROM users WHERE id=%s LIMIT 1", (note['user_id'],))
        note['user'] = cur.fetchone()

        cur.execute("SELECT * FROM comments WHERE type_id=%s AND type='notes' ORDER BY created_at DESC", (note['id'],))
        comments = cur.fetchall()
        for comment in comments:
            cur.execute("SELECT id, name, slug FROM users WHERE id=%s LIMIT 1", (comment['user_id'],))
            comment['user'] = cur.fetchone()

        cur.close()
        note['comments'] = comments
        return note

    def validate(self):
        if self.term_id == "" or self.term_id is None:
            self.errors.append("Term field is required")
        else:
            cur = conn.cursor()
            cur.execute("SELECT * FROM terms WHERE id=%s LIMIT 1", (self.term_id,))
            term = cur.fetchone()
            cur.close()
            if term is None:
                self.errors.append("Term could not found!")

        if self.course_id == "" or self.course_id is None:
            self.errors.append("Course field is required")
        else:
            cur = conn.cursor()
            cur.execute("SELECT * FROM courses WHERE id=%s LIMIT 1", (self.course_id,))
            course = cur.fetchone()
            cur.close()
            if course is None:
                self.errors.append("Course could not found!")

        if self.user_id == "" or self.user_id is None:
            self.errors.append("Please login to proceed")
        else:
            cur = conn.cursor()
            cur.execute("SELECT * FROM users WHERE id=%s LIMIT 1", (self.user_id,))
            user = cur.fetchone()
            cur.close()
            if user is None:
                self.errors.append("User could not found!")

        if self.title == "" or self.title is None:
            self.errors.append("Title field is required")

        if self.link == "" or self.link is None:
            self.errors.append("Link field is required")

        if self.errors:
            return False

        return True

    def save(self):
        if self.validate() is False:
            return False

        self.slug = self.generate_slug(name=self.title, table_name='notes')
        ts = time.time()
        created_at = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')

        cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
        cur.execute(
            "INSERT INTO notes(title, content, lecturer, link, course_id, course_code, english, term_id, slug, created_at, user_id) VALUES(%s, %s, %s, %s, %s,%s, %s, %s, %s, %s, %s) returning id",
            (
                str(self.title), str(self.content), str(self.lecturer), str(self.link), int(self.course_id),
                int(self.course_code), bool(self.english),
                int(self.term_id), str(self.slug), str(created_at), int(self.user_id)
            )
        )

        conn.commit()
        cur.close()
        return True

    def all(self):
        cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
        cur.execute("SELECT * FROM notes ORDER BY created_at DESC")
        notes = cur.fetchall()
        for note in notes:
            cur.execute("SELECT name, slug, email FROM users WHERE id=%s LIMIT 1", (note['user_id'],))
            note['user'] = cur.fetchone()
        cur.close()
        return notes
