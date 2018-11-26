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

    def get(slug):
        cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
        cur.execute("SELECT * FROM lecturers WHERE slug=%s LIMIT 1", (slug,))
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
            print("There is already a lecturer with this email")
            return "There is already a lecturer with this email"

        cur.execute(
            "INSERT INTO lecturers(name, email, user_id, slug, created_at) VALUES(%s, %s, %s, %s, %s) returning id",
            (self.name, self.email, int(self.user_id), self.slug, str(created_at)))

        self.id = cur.fetchone()['id']

        conn.commit()
        cur.close()
        return True

    def delete(self, slug, user_id):

        cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
        cur.execute("""DELETE FROM lecturers 
                        WHERE lecturers.slug = %s 
                        AND lecturers.user_id = %s""",
                    (slug, user_id))
        conn.commit()
        cur.close()
        return True
