import random

def events_table_seeder(cur, fake, num=10):
    cur.execute("SELECT id FROM users")
    users = [x for xs in cur.fetchall() for x in xs]

    for i in range(0, num):
        cur.execute("""INSERT INTO events(title, description, user_id, 
            created_at, started_at, max_participant)
            VALUES(%s, %s, %s, %s, %s, %s) returning id""",
            (str(fake.text()), str(fake.text()), int(random.choice(users)),
             fake.date_time_this_month(), fake.future_datetime(),
             random.randint(0, 100))
        )
