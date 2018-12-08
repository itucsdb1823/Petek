import sys

from slugify import slugify
from server import conn
import psycopg2.extras


class Base:
    ERRORS = []
    ATTRIBUTES = {}
    RESPONSE = []
    CONDITIONS = []
    TABLE = ''
    LIMIT = ''

    def save(self):
        print('yey')

    def getErrors(self):
        return self.ERRORS

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

    def generateWhereCondition(self):
        where_condition = '1=1'
        for condition in self.CONDITIONS:
            where_condition += ' AND ' + condition[0]+' '+condition[1]+' '+"%s" % "%s"
        return where_condition

    def generateWhereValues(self):
        where_values = ()
        for condition in self.CONDITIONS:
            where_values = where_values + (condition[2],)
        return where_values

    def get(self, one=False):
        cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
        print("SELECT * FROM " + self.TABLE + " WHERE "+self.generateWhereCondition()+self.LIMIT, file=sys.stderr)
        cur.execute("SELECT * FROM " + self.TABLE + " WHERE "+self.generateWhereCondition()+self.LIMIT,
                    self.generateWhereValues())
        if one:
            row = cur.fetchone()
            for column, value in row.items():
                if column in self.ATTRIBUTES:
                    self.ATTRIBUTES[column] = value
            self.RESPONSE = self.ATTRIBUTES
            return self

        rows = cur.fetchall()
        self.RESPONSE = []
        for row in rows:
            data = {}
            for column, value in row.items():
                if column in self.ATTRIBUTES:
                    data[column] = value
            self.RESPONSE.append(data)
        return self

    def where(self, *args):
        if len(args) == 2:  # where('id', 5)
            self.CONDITIONS.append([args[0], '=', args[1]])
        elif len(args) == 3:  # where('id','=', 5)
            self.CONDITIONS.append([args[0], args[1], args[2]])
        elif len(args) == 1 and isinstance(args[0], list):  # where([['id','=',5],['slug', '=', 'asdf]])
            for condition in args[0]:
                self.CONDITIONS.append([condition[0], condition[1], condition[2]])
        return self

    def limit(self, count):
        self.LIMIT = ' LIMIT ' + str(count)
        return self

    def plus(self, column, value):
        self.ATTRIBUTES[column] = value
        return self

    def first(self):
        self.limit(1)
        return self.get(one=True)

    def data(self):
        return self.RESPONSE
