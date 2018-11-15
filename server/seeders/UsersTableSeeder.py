def users_table_seeder(cur, fake, fake_hash, num=10):
    for i in range(0, num):
        cur.execute("""INSERT INTO users(name, email, password, confirmation_code, slug, created_at)
                    VALUES(%s, %s, %s, %s, %s, %s) returning id""",
                    (str(fake.name()), str(fake.email()), fake_hash, str(fake.user_name()),
                     str(fake.slug()), str(fake.date_time_this_month())))
