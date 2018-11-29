from server.models.Base import Base
import psycopg2.extras
from server import conn, server, jwt, bcrypt
from slugify import slugify
import datetime
import time


class Note(Base):
    id = 0
    errors = []
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

    def create(self, note):
        pass

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
            self.errors.append("This note doesn't belong to your user id")
            self.errors.append("Or this note doesn't exist in the database")
            return False

        if title:
            cur.execute("UPDATE notes SET title=%s WHERE id=%s", (title, note.id))
            slug = self.generate_slug(name=title)
            cur.execute("UPDATE notes SET slug=%s WHERE id=%s", slug, note.id)
        if content:
            cur.execute("UPDATE notes SET content=%s WHERE id=%s", content, note.id)
        if lecturer:
            cur.execute("UPDATE notes SET lecturer=%s WHERE id=%s", lecturer, note.id)
        if link:
            cur.execute("UPDATE notes SET link=%s WHERE id=%s", link, note.id)
        if english:
            cur.execute("UPDATE notes SET english=TRUE WHERE id=%s", note.id)
        else:
            cur.execute("UPDATE notes SET english=FALSE WHERE id=%s", note.id)
        if course_id:
            cur.execute("UPDATE notes SET course_id=%s WHERE id=%s", str(course_id), note.id)
        if course_code:
            cur.execute("UPDATE notes SET course_code=%s WHERE id=%s", str(course_code), note.id)
        if term_id:
            cur.execute("UPDATE notes SET term_id=%s WHERE id=%s", str(term_id), note.id)

        ts = time.time()
        created_at = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')
        cur.execute("UPDATE notes SET created_at=%s WHERE id=%s", (str(created_at), note.id))

        conn.commit()
        cur.close()
        return True

    def get(self, slug):
        cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
        cur.execute("SELECT * FROM notes WHERE slug=%s LIMIT 1", (slug,))
        note = cur.fetchone()
        cur.execute("SELECT name, slug, email FROM users WHERE id=%s LIMIT 1", (note['user_id'],))
        note['user'] = cur.fetchone()
        cur.close()
        return note

    def validate(self):
        cur = conn.cursor()
        cur.execute("SELECT * FROM terms WHERE id=%s LIMIT 1", (self.term_id,))
        term = cur.fetchone()
        cur.close()
        if term is None:
            self.errors.append("Term could not found!")

        cur = conn.cursor()
        cur.execute("SELECT * FROM courses WHERE id=%s LIMIT 1", (self.course_id,))
        course = cur.fetchone()
        cur.close()
        if course is None:
            self.errors.append("Course could not found!")

        cur = conn.cursor()
        cur.execute("SELECT * FROM users WHERE id=%s LIMIT 1", (self.user_id,))
        user = cur.fetchone()
        cur.close()
        if user is None:
            self.errors.append("User could not found!")

        if self.errors:
            return False

        return True

    def getErrors(self):
        return self.errors

    def save(self):
        if self.validate() is False:
            return False

        self.slug = self.generate_slug(name=self.title)
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

    def generate_slug(self, name):
        cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
        slug = slugify(name)
        slug_is_not_unique = True
        i = 2
        tslug = slug
        while slug_is_not_unique:
            cur.execute("SELECT * FROM notes WHERE slug=%s LIMIT 1", (slug,))
            found = cur.fetchone()
            if found is not None:
                slug = tslug + str(i)
                i += 1
            else:
                slug_is_not_unique = False
        return slug

    def all(self):
        cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
        cur.execute("SELECT * FROM notes ORDER BY created_at DESC")
        notes = cur.fetchall()
        for note in notes:
            cur.execute("SELECT name, slug, email FROM users WHERE id=%s LIMIT 1", (note['user_id'],))
            note['user'] = cur.fetchone()
        cur.close()
        return notes
