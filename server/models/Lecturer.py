import datetime
import time
from server import conn, server, jwt, bcrypt
from slugify import slugify
import psycopg2.extras
from flask_jwt_simple import create_jwt, jwt_required, get_jwt_identity


class Lecturer:
    name = ''
    email = ''
    user_id = ''
    id = ''
    slug = ''
    errors = []

    def __init__(self, name='', email='', user_id=0):
        self.name = name
        self.email = email
        self.user_id = user_id

    def generate_slug(self, name):
        cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
        slug = slugify(name)
        slug_is_not_unique = True
        i = 2
        tslug = slug
        while slug_is_not_unique:
            cur.execute("SELECT * FROM lecturers WHERE slug=%s LIMIT 1", (slug,))
            found = cur.fetchone()
            if found is not None:
                slug = tslug + str(i)
                i += 1
            else:
                slug_is_not_unique = False
        return slug

    def get(self, slug):
        cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
        cur.execute("SELECT * FROM lecturers WHERE slug = %s LIMIT 1", (str(slug),))
        lecturer = cur.fetchone()
        cur.close()
        return lecturer

    def create(self):
        ts = time.time()
        created_at = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')
        self.slug = self.generate_slug(name=self.name)

        # check uniqueness of the lecturer, create slug from name and check its uniqueness

        cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
        cur.execute("SELECT * FROM lecturers WHERE email=%s LIMIT 1", (self.email,))
        lecturer = cur.fetchone()
        if lecturer is not None:
            self.errors.append("There is already a lecturer with this email")
            return False

        cur.execute(
            "INSERT INTO lecturers(name, email, user_id, slug, created_at) VALUES(%s, %s, %s, %s, %s) returning id",
            (self.name, self.email, int(self.user_id), self.slug, str(created_at)))

        self.id = cur.fetchone()['id']

        conn.commit()
        cur.close()
        return True

    def delete(self, lecturer_id, user_id):

        cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
        lecturer = cur.execute("""SELECT FROM lecturers 
                    WHERE id = %s AND user_id = %s""", (lecturer_id, user_id))
        if lecturer is None:
            self.errors.append("No lecturer with that id and user id is found.")
            return False

        cur.execute("""DELETE FROM lecturers WHERE id = %s AND user_id = %s""",
                    (lecturer_id, user_id))

        conn.commit()
        cur.close()
        return True


    def update(self):
        oldLecturer = self.get(slug=self.slug)
        print(oldLecturer.slug)
        print(oldLecturer.name)
        if self.name != oldLecturer.name:
            self.slug = self.generate_slug(name=self.name)
        cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)

        lecturer = cur.execute("""SELECT FROM lecturers 
            WHERE id = %s AND user_id = %s""", (self.id, self.user_id))
        if lecturer is None:
            self.errors.append("You can't update, that lecturer is not registered in your user_id")
            return False

        cur.execute("""UPDATE lecturers SET name = %s, slug = %s, 
            email = %s WHERE id = %s AND user_id = %s""", (self.name,
            self.slug, self.email, self.id, self.user_id))
        conn.commit()
        cur.close()
        return True

    def GetErrors(self):
        return self.errors


