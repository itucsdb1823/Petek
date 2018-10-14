# import psycopg2 as dbapi2
import psycopg2
from config import config

params = config(filename="database.ini")

# connect to the PostgreSQL server
print('Connecting to the PostgreSQL database...')
conn = psycopg2.connect(**params)

yes = {'yes', 'y', 'ye', '', 'Y', 'Yes'}
no = {'no', 'n', 'N', 'No'}

DROP_STATEMENTS = [
    "DROP TABLE users"
]

INIT_STATEMENTS = [
<<<<<<< HEAD
    """CREATE TABLE IF NOT EXISTS tokens (
        user_id INTEGER NOT NULL REFERENCES users(id),
        token VARCHAR(255) PRIMARY KEY UNIQUE,
        revoked BOOLEAN DEFAULT 0
    )""",
=======
    """CREATE TABLE IF NOT EXISTS users (
            id serial PRIMARY KEY,
            name varchar(255) NOT NULL,
            email varchar(255) UNIQUE NOT NULL,
            password varchar(255) NOT NULL,
            confirmation_code varchar(255) NULL,
            confirmed boolean NOT NULL DEFAULT FALSE,
            banned boolean NOT NULL DEFAULT FALSE,
            slug varchar(255) UNIQUE,
            created_at timestamp NOT NULL,
            profile_picture varchar(255)
        )
    """

>>>>>>> 2e7f5a96e9caaa9bdc96c5365c3d597c2ce57ab6
]


def initialize(commands):
    cursor = conn.cursor()
    for statement in commands:
        cursor.execute(statement)
        conn.commit()
    cursor.close()


def drop_all():
    print("Do you really want to drop all tables?(Y\\N)")
    choice = input().lower()
    if choice in yes:
        print("Dropping all tables...")
        initialize(DROP_STATEMENTS)


def update_all():
    print("Updating all tables...")
    initialize(INIT_STATEMENTS)


if __name__ == "__main__":
    while True:
        print("Please select your choice:")
        print("1) Update tables")
        print("2) Drop tables")
        print("3) Exit")
        choice = int(input())
        if choice == 1:
            update_all()
        if choice == 2:
            drop_all()
        if choice == 3:
            exit()
