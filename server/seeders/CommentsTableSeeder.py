import random


def comments_table_seeder(cur, fake, num=10):
    types = ['lecturers', 'notes']
    cur.execute("SELECT id FROM users")
    users = [x for xs in cur.fetchall() for x in xs]
    cur.execute("SELECT id FROM lecturers")
    lecturers = [x for xs in cur.fetchall() for x in xs]
    cur.execute("SELECT id FROM notes")
    notes = [x for xs in cur.fetchall() for x in xs]

    for i in range(0, num):
        type = random.choice(types)
        if type == 'lecturers':
            type_id = int(random.choice(lecturers))
        else:
            type_id = int(random.choice(notes))

        cur.execute("""INSERT INTO comments(comment, user_id, type, type_id)
            VALUES(%s, %s, %s, %s) returning id""",
            (str(fake.text()), int(random.choice(users)),
             type, type_id))



