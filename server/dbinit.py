import psycopg2 as dbapi2

conn = dbapi2.connect(host="localhost", database="petek", user="postgres", password="secret")

yes = {'yes', 'y', 'ye', ''}
no = {'no', 'n'}

DROP_STATEMENTS = [
    "DROP TABLE users"
]


INIT_STATEMENTS = [
    "CREATE TABLE IF NOT EXISTS users (NUM INTEGER)"
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
