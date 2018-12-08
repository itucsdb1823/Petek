import datetime
import sys
import time

from slugify import slugify
from server import conn
import psycopg2.extras


class Base:
    ERRORS = []
    ATTRIBUTES = {}
    HIDDEN = {}
    COLUMNS = {}
    UPDATES = {}
    RESPONSE = []
    CONDITIONS = []
    TABLE = ''
    LIMIT = ''
    TIMESTAMPS = True

    def __init__(self):
        self.ERRORS = []

    def getErrors(self):
        return self.ERRORS

    def generateSlug(self, name):
        cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
        slug = slugify(name)
        slug_is_not_unique = True
        i = 2
        tslug = slug
        while slug_is_not_unique:
            cur.execute("SELECT * FROM "+self.TABLE+" WHERE slug=%s LIMIT 1", (slug,))
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
        cur.execute("SELECT * FROM " + self.TABLE + " WHERE "+self.generateWhereCondition()+self.LIMIT,
                    self.generateWhereValues())
        if one:
            row = cur.fetchone()
            if row is not None:
                for column, value in row.items():
                    if column in self.ATTRIBUTES:
                        self.ATTRIBUTES[column] = value
                    elif column in self.HIDDEN:
                        self.HIDDEN[column] = value
                self.RESPONSE = self.ATTRIBUTES
            return self

        rows = cur.fetchall()
        if rows is None:
            return self
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
        self.RESPONSE[column] = value
        return self

    def first(self):
        self.limit(1)
        return self.get(one=True)

    def data(self):
        return self.RESPONSE

    def create(self, *args):
        self.COLUMNS = args[0]
        self.setData(self.COLUMNS, False)
        return self

    def save(self):
        cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
        cur.execute(
                "INSERT INTO "+self.TABLE+self.generateInsertIntoColumns() +
                "VALUES"+self.generateInsertIntoValueStrings()+" returning *",
                self.generateInsertIntoValues())

        returnedValue = cur.fetchone()
        self.setData(returnedValue)

        conn.commit()
        return self

    def generateInsertIntoColumns(self):
        s = '('
        i = 1
        for column, value in self.COLUMNS.items():
            if i == 1:
                s += column
                if self.TIMESTAMPS:
                    s += ', created_at'
            else:
                s += ', '+column
            i += 1
        s += ' ) '
        return s

    def generateInsertIntoValueStrings(self):
        s = '('
        i = 1
        for _ in self.COLUMNS.items():
            if i == 1:
                s += '%s' % '%s'
                if self.TIMESTAMPS:
                    s += ', ' + '%s' % '%s'
            else:
                s += ', %s' % '%s'
            i += 1
        s += ' ) '
        return s

    def generateInsertIntoValues(self):
        values = ()
        i = 1
        for column, value in self.COLUMNS.items():
            if i == 1:
                values = values + (value,)
                if self.TIMESTAMPS:
                    values = values + (self.generateCreatedAt(),)
            else:
                values = values + (value,)
            i += 1

        return values

    def generateCreatedAt(self):
        ts = time.time()
        return datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')

    def setData(self, d, writeToResponse=True):
        for column, value in d.items():
            if column in self.ATTRIBUTES:
                self.ATTRIBUTES[column] = value
        if writeToResponse:
            self.RESPONSE = self.ATTRIBUTES
        else:
            self.RESPONSE = {}

    def exists(self):
        if self.RESPONSE == [] or self.RESPONSE == {} or self.RESPONSE is None:
            return False
        return True

    def delete(self):
        cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
        cur.execute("DELETE FROM "+self.TABLE+" WHERE "+self.generateWhereCondition(),
                    self.generateWhereValues())
        conn.commit()

        self.RESPONSE = {}

    def setError(self, error):
        self.ERRORS.append(error)

    def update(self, *args):
        for key, value in args[0].items():
            self.UPDATES[key] = value

        print("UPDATE " + self.TABLE + " SET " +
                    self.generateUpdateColumns() + " WHERE " +
                    self.generateWhereCondition()+" returning *", file=sys.stderr)
        print(self.generateUpdateValues(), file=sys.stderr)

        cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
        cur.execute("UPDATE " + self.TABLE + " SET " +
                    self.generateUpdateColumns() + " WHERE " +
                    self.generateWhereCondition()+" returning *",
                    self.generateUpdateValues())
        returnedValue = cur.fetchone()
        self.setData(returnedValue)
        conn.commit()

    def generateUpdateColumns(self):
        s = ''
        i = 1
        for column, value in self.UPDATES.items():
            if i == 1:
                s += column + '=' + '%s' % '%s'
            else:
                s += ', '+column + '=' + '%s' % '%s'
            i += 1
        return s

    def generateUpdateValues(self):
        values = ()
        for column, value in self.UPDATES.items():
            values = values + (value,)
        for condition in self.CONDITIONS:
            values = values + (condition[2],)
        return values
