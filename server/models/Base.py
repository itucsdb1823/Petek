from slugify import slugify
from server import conn
import psycopg2.extras


class Base:
    errors = []

    def save(self):
        print('yey')

    def getErrors(self):
        return self.errors

    def generate_slug(self, name, table_name):
        cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
        slug = slugify(name)
        slug_is_not_unique = True
        i = 2
        tslug = slug
        while slug_is_not_unique:
            cur.execute("SELECT * FROM "+table_name+" WHERE slug=%s LIMIT 1", (slug,))
            found = cur.fetchone()
            if found is not None:
                slug = tslug + str(i)
                i += 1
            else:
                slug_is_not_unique = False
        return slug
