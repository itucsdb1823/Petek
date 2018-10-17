# import psycopg2 as dbapi2
import psycopg2
from config import config
from faker import Faker
from flask import Flask
from flask_bcrypt import Bcrypt

server = Flask(__name__, template_folder='../dist', static_folder="../dist/static")
bcrypt = Bcrypt(server)
params = config(filename="database.ini")

# connect to the PostgreSQL server
print('Connecting to the PostgreSQL database...')
conn = psycopg2.connect(**params)

yes = {'yes', 'y', 'ye', '', 'Y', 'Yes'}
no = {'no', 'n', 'N', 'No'}

DROP_STATEMENTS = [
    "DROP TABLE IF EXISTS users",
    "DROP TABLE IF EXISTS tokens"
]

INIT_STATEMENTS = [
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
    """,
    """CREATE TABLE IF NOT EXISTS tokens (
        user_id INTEGER NOT NULL REFERENCES users(id),
        token VARCHAR(255) PRIMARY KEY UNIQUE,
        revoked BOOLEAN DEFAULT FALSE,
        created_at timestamp NOT NULL
    )""",
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


def generate_random_data(number_of_elements):
    fake = Faker('tr_TR')

    fake_hash = bcrypt.generate_password_hash('secret').decode('utf-8')
    cur = conn.cursor()
    for i in range(0, number_of_elements):
        cur.execute("""INSERT INTO users(name, email, password, confirmation_code, slug, created_at)
                    VALUES(%s, %s, %s, %s, %s, %s) returning id""",
                    (str(fake.name()), str(fake.email()), fake_hash, str(fake.user_name()),
                     str(fake.slug()), str(fake.date_time_this_month())))
    conn.commit()
    cur.close()


if __name__ == "__main__":
    while True:
        print("Please select your choice:")
        print("1) Update tables")
        print("2) Drop tables")
        print("3) Fill database with random data")
        print("4) Exit")
        choice = int(input())
        if choice == 1:
            update_all()
        if choice == 2:
            drop_all()
        if choice == 3:
            print("Please enter the number of random elements: ")
            number_of_elements = int(input())
            generate_random_data(number_of_elements)
        if choice == 4:
            exit()
