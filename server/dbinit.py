# import psycopg2 as dbapi2
import psycopg2
from config import config
from faker import Faker
from flask import Flask
from flask_bcrypt import Bcrypt
from migrations.create_notes_table import create_notes_table
from migrations.create_users_table import create_users_table
from migrations.create_tokens_table import create_tokens_table
from migrations.create_terms_table import create_terms_table
from migrations.create_courses_table import create_courses_table

server = Flask(__name__, template_folder='../dist', static_folder="../dist/static")
bcrypt = Bcrypt(server)
params = config(filename="database.ini")

# connect to the PostgreSQL server
print('Connecting to the PostgreSQL database...')
conn = psycopg2.connect(**params)

yes = {'yes', 'y', 'ye', '', 'Y', 'Yes'}
no = {'no', 'n', 'N', 'No'}

DROP_STATEMENTS = [
    "DROP TABLE IF EXISTS notes",
    "DROP TABLE IF EXISTS courses",
    "DROP TABLE IF EXISTS terms",
    "DROP TABLE IF EXISTS tokens",
    "DROP TABLE IF EXISTS users",

]

INIT_STATEMENTS = [
    create_users_table,
    create_tokens_table,
    create_terms_table,
    create_courses_table,
    create_notes_table
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


def generate_random_data(users_number = 5, notes_number = 5, courses_number = 5):
    fake = Faker('tr_TR')

    terms_number = 9
    fake_hash = bcrypt.generate_password_hash('secret').decode('utf-8')
    cur = conn.cursor()
    for i in range(0, users_number):
        cur.execute("""INSERT INTO users(name, email, password, confirmation_code, slug, created_at)
                    VALUES(%s, %s, %s, %s, %s, %s) returning id""",
                    (str(fake.name()), str(fake.email()), fake_hash, str(fake.user_name()),
                     str(fake.slug()), str(fake.date_time_this_month())))

    for i in range(0, courses_number):
        cur.execute("""INSERT INTO courses(name) VALUES(%s) returning id""",
                    (str(fake.lexify(text="???", letters="ABCDEFGHIJKLMNOPQRSTUVWXYZ")),))

    cur.execute("""INSERT INTO terms(season, term_year) VALUES(%s, %s) returning id""",
                (str('GÜZ'), str('16/17')))
    cur.execute("""INSERT INTO terms(season, term_year) VALUES(%s, %s) returning id""",
               (str('BAHAR'), str('16/17')))
    cur.execute("""INSERT INTO terms(season, term_year) VALUES(%s, %s) returning id""",
                (str('YAZ'), str('16/17')))
    cur.execute("""INSERT INTO terms(season, term_year) VALUES(%s, %s) returning id""",
                (str('GÜZ'), str('17/18')))
    cur.execute("""INSERT INTO terms(season, term_year) VALUES(%s, %s) returning id""",
                (str('BAHAR'), str('17/18')))
    cur.execute("""INSERT INTO terms(season, term_year) VALUES(%s, %s) returning id""",
                (str('YAZ'), str('17/18')))
    cur.execute("""INSERT INTO terms(season, term_year) VALUES(%s, %s) returning id""",
                (str('GÜZ'), str('18/19')))
    cur.execute("""INSERT INTO terms(season, term_year) VALUES(%s, %s) returning id""",
                (str('BAHAR'), str('15/16')))
    cur.execute("""INSERT INTO terms(season, term_year) VALUES(%s, %s) returning id""",
                (str('YAZ'), str('15/16')))

    # for i in range(0, notes_number):
    #     cur.execute("""INSERT INTO notes(title, link, slug, course_id, course_code, term_id, user_id, created_at)
    #                         VALUES(%s, %s, %s, %s, %s, %s, %s, %s) returning id""",
    #                 (str(fake.text()), str(fake.text()), str(fake.slug()),
    #                  int(fake.random_int(min=1, max=courses_number)), int(fake.random_int(min=100, max=600)),
    #                  int(fake.random_int(min=1, max=terms_number)), int(fake.random_int(min=1, max=users_number)),
    #                  str(fake.date_time_this_month())
    #                  ))

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
            print("Please enter the number of random users: ")
            users_number = int(input())
            print("Please enter the number of random notes: ")
            notes_number= int(input())
            print("Please enter the number of random courses: ")
            courses_number = int(input())
            generate_random_data(users_number, notes_number, courses_number)
        if choice == 4:
            exit()
