def lecturers_table_seeder(cur, fake, num=10):
    for i in range(0, num):
        cur.execute("""INSERT INTO lecturers(name, email, slug, created_at, user_id)
                    VALUES(%s, %s, %s, %s, %s) returning id""",
                    (str(fake.name()), str(fake.email()), str(fake.slug()),
                     str(fake.date_time_this_month()), str(i+1)))
