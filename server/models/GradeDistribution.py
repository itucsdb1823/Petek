from server.models.Base import Base
from server import conn, server, jwt, bcrypt
import psycopg2.extras
import random
import datetime
import time


class GradeDistribution(Base):
    id = 0
    lecturer_id = 0
    user_id = 0
    image = ''
    course_id = 0
    course_code = 0
    english = False
    term_id = 0
    created_at = ''

    def __init__(self, lecturer_id=0, user_id=0, image='', course_id=0, course_code=0, english=False, term_id=0, _id=0):
        self.errors = []
        self.lecturer_id = lecturer_id
        self.user_id = user_id
        self.image = image
        self.course_code = course_code
        self.course_id = course_id
        self.english = english
        self.term_id = term_id
        self.id = _id

    def all(self):
        cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
        cur.execute("SELECT * FROM courses ORDER BY name ASC")
        courses = cur.fetchall()
        cur.close()
        return courses

    def save(self):
        if self.validate() is False:
            return False

        ts = time.time()
        self.created_at = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')

        cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
        cur.execute(
            "INSERT INTO grade_distributions"
            "(lecturer_id, user_id, image, course_id, course_code, english, term_id, created_at) "
            "VALUES(%s, %s, %s, %s, %s, %s, %s, %s) returning id",
            (
                int(self.lecturer_id), int(self.user_id), self.image, int(self.course_id),
                int(self.course_code), bool(self.english), int(self.term_id), str(self.created_at)
            ))

        self.id = cur.fetchone()['id']
        conn.commit()
        cur.close()
        return True

    def validate(self):
        cur = conn.cursor()
        cur.execute("SELECT * FROM terms WHERE id=%s LIMIT 1", (self.term_id,))
        term = cur.fetchone()
        cur.close()
        if term is None:
            self.errors.append("Term could not found!")

        cur = conn.cursor()
        cur.execute("SELECT * FROM lecturers WHERE id=%s LIMIT 1", (self.lecturer_id,))
        lecturer = cur.fetchone()
        cur.close()
        if lecturer is None:
            self.errors.append("Lecturer could not found!")

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

    def generateImageName(self):
        return ''.join(random.choice('abcde') for _ in range(50)) + '.jpg'

    def delete(self):
        cur = conn.cursor()
        cur.execute("DELETE FROM grade_distributions WHERE id=%s AND user_id=%s", (self.id, self.user_id))
        conn.commit()
        cur.close()
