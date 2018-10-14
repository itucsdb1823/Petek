import os
import sys

import psycopg2 as dbapi2

conn = dbapi2.connect(host="localhost", database="petek", user="postgres", password="secret")


INIT_STATEMENTS = [
    """CREATE TABLE IF NOT EXISTS tokens (
        user_id INTEGER NOT NULL REFERENCES users(id),
        token VARCHAR(255) PRIMARY KEY UNIQUE,
        revoked BOOLEAN DEFAULT 0
    )""",
]


def initialize(url):
    with dbapi2.connect(url) as connection:
        cursor = connection.cursor()
        for statement in INIT_STATEMENTS:
            cursor.execute(statement)
        cursor.close()


if __name__ == "__main__":
    url = os.getenv("DATABASE_URL")
    if url is None:
        print("Usage: DATABASE_URL=url python dbinit.py", file=sys.stderr)
        sys.exit(1)
    initialize(url)
