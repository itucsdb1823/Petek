import random


def notes_table_seeder(cur, fake, num=10):
    cur.execute("SELECT id FROM terms")
    terms = [x for xs in cur.fetchall() for x in xs]
    cur.execute("SELECT id FROM courses")
    courses = [x for xs in cur.fetchall() for x in xs]
    cur.execute("SELECT id FROM users")
    users = [x for xs in cur.fetchall() for x in xs]

    for i in range(0, num):
        cur.execute("""INSERT INTO notes(title, link, slug, course_id, course_code, term_id, user_id, created_at, english)
                            VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s) returning id""",
                    (str(fake.text()), str(fake.text()), str(fake.slug()),
                     int(random.choice(courses)), int(fake.random_int(min=100, max=600)),
                     int(random.choice(terms)), int(random.choice(users)),
                     str(fake.date_time_this_month()),
                     bool(random.getrandbits(1))
                     ))
