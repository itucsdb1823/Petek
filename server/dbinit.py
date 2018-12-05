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
from migrations.create_lecturers_table import create_lecturers_table
from migrations.create_comments_table import create_comments_table
from migrations.create_roles_table import create_roles_table
from migrations.create_user_roles_table import create_user_roles_table
from migrations.create_grade_distributions_table import create_grade_distributions_table
import seeders
from seeders.CommentsTableSeeder import comments_table_seeder


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
    "DROP TABLE IF EXISTS grade_distributions",
    "DROP TABLE IF EXISTS courses",
    "DROP TABLE IF EXISTS terms",
    "DROP TABLE IF EXISTS tokens",
    "DROP TABLE IF EXISTS lecturers",
    "DROP TABLE IF EXISTS users",
]

INIT_STATEMENTS = [
    create_users_table,
    create_tokens_table,
    create_terms_table,
    create_courses_table,
    create_notes_table,
    create_lecturers_table,
<<<<<<< HEAD
    create_comments_table
=======
    create_roles_table,
    create_user_roles_table,
    create_grade_distributions_table,
>>>>>>> 6cd2763d995f90509a5a67293ce70d6e33bdc1bd
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


def generate_random_data(seeders_list):
    fake = Faker('tr_TR')
    fake_hash = bcrypt.generate_password_hash('secret').decode('utf-8')
    cur = conn.cursor()

    for i in seeders_list:
        i = int(i)
        if i == 1:
            seeders.users_table_seeder(cur=cur, fake=fake, fake_hash=fake_hash)
        if i == 2:
            seeders.courses_table_seeder(cur=cur, fake=fake)
        if i == 3:
            seeders.terms_table_seeder(cur=cur)
        if i == 4:
            seeders.notes_table_seeder(cur=cur, fake=fake)
        if i == 5:
            seeders.lecturers_table_seeder(cur=cur, fake=fake)
        if i == 6:
<<<<<<< HEAD
            comments_table_seeder(cur=cur, fake=fake)
=======
            seeders.roles_table_seeder(cur=cur, fake=fake)
>>>>>>> 6cd2763d995f90509a5a67293ce70d6e33bdc1bd
    
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
            print("Please enter the number(s) of which seeders to run (Put space between choices): ")
            print("1) Users Table Seeder")
            print("2) Courses Table Seeder")
            print("3) Terms Table Seeder")
            print("4) Notes Table Seeder")
            print("5) Lecturers Table Seeder")
<<<<<<< HEAD
            print("6) Comments Table Seeder")
=======
            print("6) Roles Table Seeder")
>>>>>>> 6cd2763d995f90509a5a67293ce70d6e33bdc1bd
            choices = input().split(' ')
            generate_random_data(choices)
        if choice == 4:
            exit()
